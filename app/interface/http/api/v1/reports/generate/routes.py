import time
from fastapi import APIRouter, Query, BackgroundTasks, Request
from fastapi.responses import FileResponse
from app.application.exceptions.html_exceptions import HTMLError
from app.core.logger import log

router = APIRouter()

@router.get("/generate", response_class=FileResponse)
async def generate_report(
        request: Request,
        background_tasks: BackgroundTasks,
        token: str = Query(...),
):
    start_time = time.time()
    client_ip = request.client.host if request.client else "Unknown"

    log.request(request.method, str(request.url.path), client_ip)
    log.info(f"Mulai generate report dengan token: {token[:15]}...")

    # AMBIL DARI STATE CUY (Persis Axum)
    # cara ambil state -> request.app.state.ext.{x} dimana {x} adalah atribut (lihat core/state.py)
    use_case = request.app.state.ext.generate_excel_use_case
    local_file_manager = request.app.state.ext.local_file_mgr

    try:
        # Eksekusi
        result = await use_case.execute(token=token)

        # Cleanup
        background_tasks.add_task(local_file_manager.cleanup, result.path)

        duration = (time.time() - start_time) * 1000
        log.ok(f"Report berhasil di-generate di path: {result.path}")
        log.response(request.method, str(request.url.path), 200, duration)

        return FileResponse(
            path=result.path,
            filename=result.filename,
            media_type=result.content_type,
        )

    except Exception as e:
        duration = (time.time() - start_time) * 1000
        log.error(f"Gagal generate report Excel: {str(e)}", exc_info=True)
        log.response(request.method, str(request.url.path), 500, duration)
        raise HTMLError(str(e))