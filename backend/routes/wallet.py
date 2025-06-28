from fastapi import APIRouter
from backend.db import db

router = APIRouter()

@router.get('/wallet')
def get_balance(token):
    users = db.table('users').select('id').eq('login_token', token).execute()
    user_id = users.data[0]['id']
    print(user_id)
    res = db.table('wallet').select('*').eq('user_id', user_id).execute()
    return res.data[0]['balance']