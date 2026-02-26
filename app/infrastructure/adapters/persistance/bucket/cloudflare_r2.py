import aioboto3
from botocore.config import Config
from app.application.protocols.bucket_repository import BucketRepository
from app.core.logger import log  # Import logger andalan kita

class CloudflareR2Bucket(BucketRepository):
    def __init__(self, endpoint_url: str, access_key: str, secret_key: str, bucket_name: str):
        log.info("🔥 CloudflareR2Bucket INIT TERPANGGIL 🔥")
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name

        # Bikin session aioboto3-nya di init
        self.session = aioboto3.Session()

    async def get_report_sql(self, tenant_id: str, file_name: str) -> str:
        """
        Ambil file .sql dari Cloudflare R2 secara Case-Insensitive.
        """
        prefix = f"Reports/{tenant_id}/"
        target_file_lower = file_name.lower()

        log.info("=== R2 DEBUG START ===")
        log.info(f"Endpoint URL: {self.endpoint_url}")
        log.info(f"Bucket Name: {self.bucket_name}")
        log.info(f"Tenant ID: {tenant_id}")
        log.info(f"Prefix yang dicari: {prefix}")
        log.info(f"File yang dicari (raw): {file_name}")
        log.info(f"File yang dicari (lower): {target_file_lower}")

        async with self.session.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version='s3v4'),
            region_name='auto'
        ) as s3_client:

            try:
                list_response = await s3_client.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=prefix
                )

                log.info(f"ListObjects response keys: {list(list_response.keys())}")

                if 'Contents' not in list_response:
                    log.error(f"Tidak ada isi folder untuk prefix: {prefix}")
                    raise Exception(f"Folder tenant {tenant_id} kosong atau tidak ada di bucket.")

                log.info("File ditemukan di folder:")
                for obj in list_response['Contents']:
                    log.info(f" - {obj['Key']}")

                exact_key = None
                for obj in list_response['Contents']:
                    file_in_bucket = obj['Key'].split('/')[-1]

                    log.info(f"Membandingkan: {file_in_bucket.lower()} == {target_file_lower}")

                    if file_in_bucket.lower() == target_file_lower:
                        exact_key = obj['Key']
                        break

                if not exact_key:
                    log.error(f"Tidak ditemukan file yang cocok untuk: {file_name}")
                    raise Exception(
                        f"File {file_name} tidak ditemukan di bucket walau sudah dicari secara case-insensitive."
                    )

                log.info(f"Exact key yang dipakai untuk get_object: {exact_key}")

                response = await s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key=exact_key
                )

                body_bytes = await response['Body'].read()
                sql_text = body_bytes.decode('utf-8')

                log.info("File SQL berhasil diambil dari R2")
                log.info("=== R2 DEBUG END ===")

                return sql_text

            except Exception as e:
                log.error(f"ERROR R2: {str(e)}")
                raise Exception(f"Gagal ngambil file dari R2: {str(e)}")