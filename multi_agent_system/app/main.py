from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import router as api_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(title="Multi-Agent Reasoning System", version="0.1.0")

app.include_router(api_router)
app.include_router(dashboard_router)

# Show real errors instead of plain "Internal Server Error"
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "path": str(request.url)}
    )
