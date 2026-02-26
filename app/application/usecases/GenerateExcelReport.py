import json
import re
import time  # Tambah ini buat ukur durasi internal
from datetime import datetime
from typing import Callable, Any

from app.application.dto.generated_file import GeneratedFile
from app.application.exceptions.report_exceptions import MissingReportParameter, ReportGenerationFailed
from app.application.protocols.local_file_manager_port import LocalFileManagerPort
from app.application.protocols.memory_cache_port import MemoryCachePort
from app.application.protocols.report_generator_port import ReportGeneratorPort
from app.application.protocols.tenant_repository_port import TenantRepositoryPort
from app.application.protocols.token_decoder_port import TokenDecoderPort
from app.application.services.resolver.legacy_report_config_resolver import LegacyReportConfigResolverService
from app.application.services.sql.params_sanitizer import sanitize_params
from app.application.services.sql.sql_param_binder import bind_named_params
from app.core.logger import log  # Import logger andalan kita


class GenerateExcelReportUseCase:
    def __init__(
            self,
            *,
            token_decoder: TokenDecoderPort,
            db_config_resolver: TenantRepositoryPort,
            db_provider_factory: Callable[[Any], Any],
            report_generator: ReportGeneratorPort,
            local_file_mgr: LocalFileManagerPort,
            memory_cache_mgr: MemoryCachePort,
            report_resolver: LegacyReportConfigResolverService  # [FIX] 1. Inject resolvernya di sini
    ):
        self.token_decoder = token_decoder
        self.db_config_resolver = db_config_resolver
        self.db_provider_factory = db_provider_factory
        self.report_generator = report_generator
        self.temp_files = local_file_mgr
        self.master_data_provider = memory_cache_mgr
        self.report_resolver = report_resolver  # [FIX] 2. Simpan sebagai instance variable

    async def execute(self, token: str) -> GeneratedFile:
        start_exec = time.time()

        # --- 0. Decode Token ---
        ctx = await self.token_decoder.decode(token)
        log.info(f"Processing report: '{ctx.reportName}' for Company ID: {ctx.companyId}")

        # --- 1. Resolve Tenant DB Config ---
        tenant_db_config = await self.db_config_resolver.get_db_config_by_company_id(int(ctx.companyId))
        log.debug(f"Resolved DB Host: {tenant_db_config.host} (Schema: {ctx.tenantId})")

        # --- 3. Resolve SQL Template ---
        raw_query = await self.report_resolver.resolve(ctx.tenantId, ctx.reportName)

        log.info(f"Raw query length: {len(raw_query) if raw_query else 'None'}")
        log.info(f"Raw query preview: {repr(raw_query[:100]) if raw_query else 'None'}")

        if not raw_query:
            # Kasih proteksi kalau query kosong/gak ketemu di bucket
            raise MissingReportParameter(f"File SQL untuk report {ctx.reportName} tidak ditemukan di Cloudflare R2")

        log.debug(f"SQL Template resolved for {ctx.reportName}")

        # [FIX] 4. Gunakan fungsi scan dari resolver
        injected = {}
        sys_queries = self.report_resolver.scan_params_data_from_jb_system(raw_query)

        if sys_queries:
            log.info(f"Injecting {len(sys_queries)} system parameters from cache/master data")
            for key, q in sys_queries.items():
                rows = await self.master_data_provider.get_data(key, q)
                injected[key] = json.dumps(rows, default=str)

        # --- 5. Gabung Params & Bind SQL ---
        user_params = sanitize_params(ctx.params)
        params = {**user_params, **injected}

        if "@brands" in raw_query and "brands" not in params:
            log.warning(f"@brands parameter missing in {ctx.reportName}, injecting default empty array")
            params["brands"] = "[]"

        sql = raw_query.replace("{0}", str(tenant_db_config.schema) or "public")

        try:
            native_sql, ordered = bind_named_params(sql, params)
        except ValueError as e:
            log.error(f"Parameter binding failed for {ctx.reportName}: {str(e)}")
            raise MissingReportParameter(str(e))

        # --- Datetime Parsing Logic ---
        parsed_params = []
        for val in ordered:
            # (Logika parsing lu tetep sama...)
            if isinstance(val, str):
                if "T" in val and len(val) >= 19:
                    try:
                        clean_val = val.replace('Z', '+00:00')
                        parsed_params.append(datetime.fromisoformat(clean_val))
                        continue
                    except ValueError:
                        pass
                elif re.match(r"^\d{2}/\d{2}/\d{4} \d{2}\.\d{2}\.\d{2} [+-]\d{2}:\d{2}$", val):
                    try:
                        parsed_params.append(datetime.strptime(val, "%d/%m/%Y %H.%M.%S %z"))
                        continue
                    except ValueError:
                        pass
            parsed_params.append(val)

        # --- 6. Generate Excel (Via Rust OpenReport Engine) ---
        output_path = self.temp_files.create_temp_xlsx(ctx.reportName)
        dsn = (
            f"postgres://{tenant_db_config.username}:{tenant_db_config.password}"
            f"@{tenant_db_config.host}:{tenant_db_config.port}/{tenant_db_config.database}"
        )

        log.info(f"Starting Excel Engine for {ctx.reportName}...")
        engine_start = time.time()

        try:
            await self.report_generator.generate_xlsx(
                dsn=dsn,
                sql=native_sql,
                params=parsed_params,
                output_path=output_path
            )

            engine_duration = (time.time() - engine_start) * 1000
            total_duration = (time.time() - start_exec) * 1000

            log.ok(
                f"Excel generated: {ctx.reportName}.xlsx (Engine: {engine_duration:.2f}ms | Total: {total_duration:.2f}ms)")

        except Exception as e:
            log.error(f"Rust Engine failed for {ctx.reportName}: {str(e)}", exc_info=True)
            self.temp_files.cleanup(output_path)
            raise ReportGenerationFailed(str(e))

        return GeneratedFile(
            path=output_path,
            filename=f"{ctx.reportName}.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
