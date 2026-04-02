from fastapi.responses import HTMLResponse
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent
from typing import Any
import json
import re


def render_download_ui_if_available(response: Any) -> Any:
    """If response contains a file_path_download link, return rich HTML UI embed.

    For all other responses, return as-is to preserve original behavior.
    """
    parsed = None

    if isinstance(response, str):
        try:
            parsed = json.loads(response)
        except Exception:
            parsed = None
    elif isinstance(response, dict):
        parsed = response

    if isinstance(parsed, dict) and "file_path_download" in parsed:
        markdown_link = str(parsed.get("file_path_download", ""))

        # Try to parse [label](href)
        match = re.search(r"\[(.*?)\]\((.*?)\)", markdown_link)
        if match:
            label = match.group(1)
            href = match.group(2)
        else:
            label = "Download file"
            href = markdown_link

        safe_label = label.replace('"', '&quot;')

        html = f"""<!DOCTYPE html>
        <html lang='en'>
        <head>
            <meta charset='UTF-8'>
            <title>Descarga generada</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: #fdfdfd;
                    color: #202020;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .card {{
                    border-radius: 14px;
                    border: 1px solid #e0e0e0;
                    background: linear-gradient(145deg, #ffffff 0%, #f5f7ff 100%);
                    box-shadow: 0 6px 18px rgba(50, 60, 80, 0.08);
                    padding: 18px;
                    max-width: 640px;
                    margin: 0 auto;
                }}
                .headline {{
                    font-size: 1.05rem;
                    font-weight: 700;
                    color: #2b2f41;
                    margin-bottom: 10px;
                }}
                .download-btn {{
                    display: inline-flex;
                    align-items: center;
                    gap: 10px;
                    font-size: 0.98rem;
                    font-weight: 700;
                    border: 0;
                    border-radius: 10px;
                    background: linear-gradient(90deg, #3366ff 0%, #3869ff 100%);
                    color: #fff;
                    padding: 10px 18px;
                    text-decoration: none;
                    box-shadow: 0 5px 14px rgba(51, 102, 255, 0.31);
                    transition: transform 0.16s ease, filter 0.16s ease;
                }}
                .download-btn:hover {{
                    transform: translateY(-1px);
                    filter: brightness(1.08);
                }}
                .download-btn:active {{
                    transform: translateY(0);
                }}
                .info {{
                    margin-top: 14px;
                    font-size: 0.94rem;
                    color: #475272;
                }}
                .status {{
                    margin-top: 12px;
                    font-size: 0.93rem;
                    color: #1266ff;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <div class='card'>
                <div class='headline'>✅ Documento listo para descarga</div>
                <a id='btnDownload' class='download-btn' href='{href}' target='_blank' rel='noopener noreferrer'>
                    ⬇️ {safe_label}
                </a>
                <p class='info'>Haz clic en el botón para descargar tu archivo. Si no inicia en automático, pulsa nuevamente.</p>
                <p id='statusMessage' class='status'>⏳ Aún no se ha hecho clic.</p>
            </div>

            <script>
                function reportHeight() {{
                    const h = document.documentElement.scrollHeight;
                    parent.postMessage({{ type: 'iframe:height', height: h }}, '*');
                }}

                window.addEventListener('load', reportHeight);
                new ResizeObserver(reportHeight).observe(document.body);

                document.getElementById('btnDownload').addEventListener('click', function() {{
                    const status = document.getElementById('statusMessage');
                    status.textContent = '✅ Clic registrado. La descarga debería comenzar ahora.';
                    status.style.color = '#0d8d6f';

                    setTimeout(function() {{
                        status.textContent = '📥 Si no se inicia automáticamente, usa el enlace del botón.';
                    }}, 1500);
                }});
            </script>
        </body>
        </html>
        """

        # According to RICH_UI.md, for tools we should return HTMLResponse with inline headers.
        return HTMLResponse(content=html, headers={"Content-Disposition": "inline", "Content-Type": "text/html"})

    return response