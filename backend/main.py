from fastapi import FastAPI
from backend.routes.auth import router as auth_router

app = FastAPI(title="Crypto Dashboard API")



app.include_router(auth_router)

