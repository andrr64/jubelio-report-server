# File: app/core/state.py

from app.application.dto.db_config import DBConfig
from app.application.services.resolver.legacy_report_config_resolver import LegacyReportConfigResolverService
from app.core.config import settings, get_settings
from app.infrastructure.adapters.cache.memory_cache import InMemoryMemoryCacheAdapter
from app.infrastructure.adapters.persistance.bucket.cloudflare_r2 import CloudflareR2Bucket
from app.infrastructure.adapters.persistance.database.postgres import PostgresAdapter
from app.infrastructure.adapters.persistance.local.local_fm_adapter import LocalFileManagerAdapter
from app.infrastructure.adapters.persistance.repository.tenant_repository_postgres import PostgresTenantRepository
from app.infrastructure.adapters.report_generator.open_report import get_report_generator
from app.infrastructure.adapters.security.auth.token_decoder import TokenDecoderAdapter
from app.application.usecases.GenerateExcelReport import GenerateExcelReportUseCase

class AppState:
    def __init__(self):
        # 1. Init Config
        self.system_db_config = DBConfig(
            host=settings.DB_HOST_SYSTEM,
            port=settings.DB_PORT,
            username=settings.DB_USERNAME,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME_SYSTEM
        )
        self.app_settings = get_settings()

        # 2. Init Providers & Adapters (Level Bawah)
        self.db_provider = PostgresAdapter(config=self.system_db_config)
        self.master_data_cache = InMemoryMemoryCacheAdapter(
            db_fetcher=self.db_provider,
            ttl_seconds=300
        )
        self.token_decoder = TokenDecoderAdapter()
        self.local_file_mgr = LocalFileManagerAdapter()
        self.bucket_storage = CloudflareR2Bucket(
            self.app_settings.AWS_ENDPOINT_URL,
            self.app_settings.AWS_ACCESS_KEY_ID,
            self.app_settings.AWS_SECRET_ACCESS_KEY,
            self.app_settings.AWS_BUCKET_NAME,
        )
        self.tenant_repo = PostgresTenantRepository(db_provider=self.db_provider)

        # Helper buat factory dinamis (kalau butuh spawn DB baru per tenant)
        self.db_provider_factory = lambda config: PostgresAdapter(config=config)

        # Services
        self.report_resolver_svc = LegacyReportConfigResolverService(
            bucket_repo=self.bucket_storage
        )

        # 3. Init Use Cases (Tinggal inject dari adapter di atas)
        self.generate_excel_use_case = GenerateExcelReportUseCase(
            token_decoder=self.token_decoder,
            db_config_resolver=self.tenant_repo,
            db_provider_factory=self.db_provider_factory,
            memory_cache_mgr=self.master_data_cache,
            report_generator=get_report_generator(),
            local_file_mgr=self.local_file_mgr,
            report_resolver=self.report_resolver_svc  # [TAMBAH INI] Masukin resolvernya
        )