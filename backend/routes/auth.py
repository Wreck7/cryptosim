from fastapi import APIRouter
from backend.db import db

router = APIRouter()

@router.post("/register")
def register_user(email, name, username, password, gender, age, phone):
    check = db.table('users').select('*').or_(f"username.eq.{username},email.eq.{email}").execute()
    if check.data:
        return {"success": False, "message": "User already exists"}
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
        return {"success": True, "message": "User registered successfully"}


@router.post("/login")
def login_user(identifier,password):
    check = db.table('users').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").execute()

    user = check.data[0] if check.data else None

    if user and user['password'] == password:
        return {"success": True, "message": "Login successful", "user": user}
    else:
        return {"success": False, "message": "Invalid username/email or password"}
