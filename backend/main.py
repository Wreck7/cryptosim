from fastapi import FastAPI
from backend.routes.auth import router as auth_router
from backend.routes.dashboard import router as dashboard_router
from backend.routes.profile import router as profile_router
from backend.routes.portfolio import router as portfolio_router


app = FastAPI(title="Crypto Dashboard API")



app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(dashboard_router)
app.include_router(portfolio_router)

