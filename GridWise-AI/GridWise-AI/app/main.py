from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.optimize import router as optimize_router

app = FastAPI(title="GridWise AI")
app.include_router(health_router)
app.include_router(optimize_router)
