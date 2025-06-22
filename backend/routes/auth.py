from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register_user():
    check = db.table('register').select('*').or_(f"username.eq.{username},email.eq.{email}").execute()
    if check.data:
        return False
    else:
        data = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,
            'age': age,
            'gender': gender
        }
        res = db.table('register').insert(data).execute()
        return True


    @router.post("/login")
    def login_user():
        print