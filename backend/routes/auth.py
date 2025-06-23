from fastapi import APIRouter
from backend.db import db

router = APIRouter()

@router.post("/register")
def register_user(email, name, username, password, gender, age, phone):
    check = db.table('users').select('*').or_(f"username.eq.{username},email.eq.{email}").execute()
    if check.data:
        return False
    else:
        data = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,
            'gender': gender,
            'age': age,
            'phone': phone
        }
        res = db.table('users').insert(data).execute()
        return True


    @router.post("/login")
    def login_user():
        print