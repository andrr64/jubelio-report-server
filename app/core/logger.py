import sys

from loguru import logger as _logger

from app.core.config import settings

# 1. Hapus logger bawaan
_logger.remove()

# 2. Daftarkan Custom Levels (Biar warnanya beda-beda di terminal)
# Level no (nomor urut) menentukan prioritas. Makin tinggi makin penting.
_logger.level("REQUEST", no=21, color="<cyan>")
_logger.level("RESPONSE", no=22, color="<blue>")
_logger.level("OK", no=25, color="<green><bold>")  # Hijau tebal biar mantap

# 3. Format Log
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 4. Tambah Handler Terminal
_logger.add(
    sys.stdout,
    level="DEBUG" if settings.DEBUG else "INFO",
    format=log_format
)

# 5. Tambah Handler File (Rotasi)
_logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="50 MB",  # [FIX] Cukup taruh ukurannya di sini
    retention="30 days",  # Hapus otomatis file yang lebih tua dari 30 hari
    level="INFO",
    compression="zip"
)


# ==========================================
# WRAPPER CLASS BIAR LU TINGGAL PANGGIL
# ==========================================
class AppLogger:
    @staticmethod
    def request(method: str, url: str, client_ip: str):
        _logger.log("REQUEST", f"{method} {url} | IP: {client_ip}")

    @staticmethod
    def response(method: str, url: str, status_code: int, duration_ms: float):
        _logger.log("RESPONSE", f"{method} {url} | Status: {status_code} | Time: {duration_ms:.2f}ms")

    @staticmethod
    def ok(message: str):
        _logger.log("OK", message)

    @staticmethod
    def info(message: str):
        _logger.info(message)

    @staticmethod
    def warning(message: str):
        _logger.warning(message)

    @staticmethod
    def error(message: str, exc_info: bool = False):
        """
        exc_info=True akan menge-print seluruh traceback (garis merah error)
        sangat berguna pas nangkep exception try-except!
        """
        if exc_info:
            _logger.exception(message)
        else:
            _logger.error(message)

    @staticmethod
    def debug(message: str):
        _logger.debug(message)


# 6. Export instance-nya biar bisa dipakai di semua file
log = AppLogger()
