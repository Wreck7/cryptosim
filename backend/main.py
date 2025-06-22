from fastapi import FastAPI

app = FastAPI(title="Crypto Dashboard API")

from routes.auth import router as auth_router



app.include_router(auth_router)

