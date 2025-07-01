from fastapi import FastAPI
from backend.routes.auth import router as auth_router
from backend.routes.dashboard import router as dashboard_router
from backend.routes.profile import router as profile_router
from backend.routes.portfolio import router as portfolio_router
from backend.routes.wallet import router as wallet_router
from backend.routes.transactions import router as transactions_router
from backend.routes.wishlist import router as wishlist_router


app = FastAPI(title="Crypto Dashboard API")

# @app.get("/")
# def read_root():
#     return {"message": "Hello, world!"}

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(dashboard_router)
app.include_router(portfolio_router)
app.include_router(wallet_router)
app.include_router(transactions_router)
app.include_router(wishlist_router)

