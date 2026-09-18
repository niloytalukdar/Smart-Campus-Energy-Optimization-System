from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from app.routes import health, optimize
from app.config import OPENAI_API_KEY
import os

app = FastAPI(title="GridWise AI")

# Serve the simple single-page app UI under /app-ui
from fastapi.staticfiles import StaticFiles
app.mount("/app-ui-static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "app_ui")), name="app_ui_static")
# Serve the design prototypes under the workspace-level `system_ui` folder
system_ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "system_ui"))
if os.path.isdir(system_ui_path):
    app.mount("/system-ui-static", StaticFiles(directory=system_ui_path), name="system_ui_static")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": str(exc)},
    )

app.include_router(health.router)
app.include_router(optimize.router)

@app.get("/")
def root():
    # Redirect root to the single-page UI for a better developer experience
    return RedirectResponse(url="/app-ui")


@app.get("/app-ui")
def get_app_ui():
    index_path = os.path.join(os.path.dirname(__file__), "app_ui", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@app.get("/system-ui")
def get_system_ui():
    # Redirect to the first available HTML page in the `system_ui` folder
    if not os.path.isdir(system_ui_path):
        return RedirectResponse(url="/docs")
    for root, dirs, files in os.walk(system_ui_path):
        for f in files:
            if f.lower().endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, f), system_ui_path).replace('\\', '/')
                return RedirectResponse(url=f"/system-ui-static/{rel_path}")
    return RedirectResponse(url="/docs")


@app.get("/system-ui/ai-interpretation")
def get_ai_interpretation_ui():
    page_path = os.path.join(system_ui_path, "ai_interpretation", "code.html")
    if os.path.exists(page_path):
        return FileResponse(page_path, media_type="text/html")
    return RedirectResponse(url="/docs")

@app.get("/test", response_class=HTMLResponse)
def get_test_page():
    html_path = os.path.join(os.path.dirname(__file__), "static", "test.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()
