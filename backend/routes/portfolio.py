from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from datetime import datetime
from backend.db import db  # assuming you're using db-py

router = APIRouter()

# ---- Request Schemas ----

# class BuySellRequest(BaseModel):
#     user_id: str
#     coin_id: str
#     coin_name: str
#     quantity: float
#     price_per_unit: float  # Live price from frontend or API


# ---- Endpoint: Get Full Portfolio ----

@router.get("/portfolio")
def get_portfolio(token):
    portfolio = db.table("portfolio").select("*").eq("user_id", token).execute().data
    return {"portfolio": portfolio}


# ---- Endpoint: Buy Coin ----

@router.post("portfolio/buy")
def buy_coin(token, quantity, coin_id):
    user_getting = db.table("users").select('*').eq('login_token', token).execute()
    user_id = user_getting.data[0]['id']
    coin = db.table('coins').select('*').eq('coin_id', coin_id).execute()
    coin = coin.data[0]
    user = db.table("wallet").select("*").eq("user_id", user_id).single().execute().data
    if not user:
        # raise HTTPException(status_code=404, detail="User not found")
        return 'user not found'
    
    total_cost = quantity * coin['price']
    if user["balance"] < total_cost:
        # raise HTTPException(status_code=400, detail="Insufficient balance")
        return 'Insufficient balance'

    # Update or insert portfolio
    existing = db.table("portfolio").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute().data

    if existing:
        old = existing[0]
        new_qty = old["quantity"] + quantity
        new_total = (old["avg_price"] * old["quantity"]) + total_cost
        new_avg = new_total / new_qty
        db.table("portfolio").update({
            "quantity": new_qty,
            "avg_price": new_avg
        }).eq("id", old["id"]).execute()
    else:
        db.table("portfolio").insert({
            "user_id": user_id,
            "coin_id": coin_id,
            "coin_name": coin['coin_name'],
            "quantity": quantity,
            "avg_price": coin['price']
        }).execute()

    # Update balance
    db.table("wallet").update({
        "balance": user["balance"] - total_cost
    }).eq("user_id", user_id).execute()

    # Log transaction
    db.table("transactions").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "coin_name": coin['name'],
        "quantity": quantity,
        "price": coin['price'],
        "type": "buy",
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

    return {"message": "Coin bought successfully"}


# ---- Endpoint: Sell Coin ----

@router.post("/portfolio/sell")
def sell_coin(token, quantity, coin_id):
    user_getting = db.table("users").select('*').eq('login_token', token).execute()
    user_id = user_getting.data[0]['id']
    coin = db.table('coins').select('*').eq('coin_id', coin_id).execute()
    coin = coin.data[0]
    user = db.table("wallet").select("*").eq("user_id", user_id).single().execute().data
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.table("portfolio").select("*").eq("user_id", user_id).eq("coin_id", coin_id).execute().data
    if not existing:
        raise HTTPException(status_code=400, detail="You don't hold this coin")

    owned_coin = existing[0]
    if quantity > owned_coin["quantity"]:
        raise HTTPException(status_code=400, detail="Not enough quantity to sell")

    remaining_qty = owned_coin["quantity"] - quantity
    if remaining_qty == 0:
        db.table("portfolio").delete().eq("id", owned_coin["id"]).execute()
    else:
        db.table("portfolio").update({
            "quantity": remaining_qty
        }).eq("id", owned_coin["id"]).execute()

    # Update balance
    total_sell_value = quantity * coin['price']
    db.table("wallet").update({
        "balance": user["balance"] + total_sell_value
    }).eq("user_id", user_id).execute()

    # Log transaction
    db.table("transactions").insert({
        "user_id": user_id,
        "coin_id": coin_id,
        "coin_name": coin['name'],
        "quantity": quantity,
        "price": coin['price'],
        "type": "sell",
        "timestamp": datetime.utcnow().isoformat()
    }).execute()

    return {"message": "Coin sold successfully"}
