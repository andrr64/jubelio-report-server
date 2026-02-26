import re
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.application.exceptions.html_exceptions import HTMLError


async def custom_html_error_handler(request: Request, exc: HTMLError):
    # 1. Cari pola "LINE <angka>:" di dalam pesan error
    match = re.search(r"LINE (\d+):", exc.message)

    # 2. Jika ketemu, ambil angkanya. Jika tidak, kasih nilai default.
    line_number_text = match.group(1) if match else "Tidak diketahui"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error Report - Jubelio Server</title>
        <style>
            :root {{
                --bg-main: #0f172a;
                --bg-card: #1e293b;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --danger: #ef4444;
                --danger-bg: #7f1d1d33;
                --danger-border: #f8717144;
                --code-bg: #0b1120;
            }}

            body {{
                background-color: var(--bg-main);
                color: var(--text-main);
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                margin: 0;
                padding: 40px 20px;
                display: flex;
                justify-content: center;
                align-items: flex-start;
                min-height: 100vh;
            }}

            .container {{
                max-width: 768px;
                width: 100%;
            }}

            .error-card {{
                background-color: var(--bg-card);
                border-radius: 12px;
                border: 1px solid var(--danger-border);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
                overflow: hidden;
            }}

            .error-header {{
                background-color: var(--danger-bg);
                border-bottom: 1px solid var(--danger-border);
                padding: 20px 24px;
                display: flex;
                align-items: center;
                gap: 12px;
            }}

            .error-header svg {{
                color: var(--danger);
                width: 28px;
                height: 28px;
                flex-shrink: 0;
            }}

            .error-header h1 {{
                color: var(--danger);
                font-size: 1.25rem;
                font-weight: 600;
                margin: 0;
            }}

            .error-body {{
                padding: 24px;
            }}

            .error-location {{
                background-color: rgba(239, 68, 68, 0.1);
                border-left: 4px solid var(--danger);
                padding: 16px;
                border-radius: 0 6px 6px 0;
                margin-bottom: 24px;
                font-size: 1.05rem;
                color: #fca5a5;
                display: flex;
                flex-direction: column;
                gap: 4px;
            }}

            .error-location span {{
                font-size: 0.85rem;
                color: var(--danger);
                text-transform: uppercase;
                font-weight: 700;
                letter-spacing: 0.05em;
            }}

            .code-label {{
                font-size: 0.9rem;
                color: var(--text-muted);
                margin-bottom: 8px;
                font-weight: 500;
            }}

            .code-block {{
                background-color: var(--code-bg);
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 16px;
                overflow-x: auto;
            }}

            .code-block pre {{
                margin: 0;
                color: #e2e8f0;
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
                font-size: 0.9rem;
                line-height: 1.6;
                white-space: pre-wrap;
                word-break: break-all;
            }}

            .error-footer {{
                padding: 16px 24px;
                background-color: rgba(0,0,0,0.1);
                border-top: 1px solid #334155;
                display: flex;
            }}

            .back-btn {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                color: var(--text-main);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.9rem;
                background-color: #334155;
                padding: 8px 16px;
                border-radius: 6px;
                border: 1px solid #475569;
                transition: all 0.2s;
            }}

            .back-btn:hover {{
                background-color: #475569;
                border-color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error-card">
                <div class="error-header">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <h1>Query Execution Failed</h1>
                </div>

                <div class="error-body">
                    <div class="error-location">
                        <span>Lokasi Masalah</span>
                        <div>Terdapat error pada query di <strong>baris {line_number_text}</strong></div>
                    </div>

                    <div class="code-label">Detail Pesan Error:</div>
                    <div class="code-block">
                        <pre>{exc.message}</pre>
                    </div>
                </div>

                <div class="error-footer">
                    <a href="javascript:history.back()" class="back-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                        Kembali
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=400)