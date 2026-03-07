from fastapi import HTTPException, Depends
from db.connection import read_query, insert_query, update_query
from auth.password_hash import hash_pass, check_pass
from auth.jwt_handler import create_jwt
from models.user_models import UserCreate
from fastapi.security import OAuth2PasswordRequestForm


def get_by_username(username: str):

    sql = """
        SELECT * FROM users
        WHERE username = ?
    """

    result = read_query(sql, (username,))

    if result:
        return result[0]

    return None

def get_by_id(user_id: int):

    sql = """
    SELECT * FROM users
    WHERE id = ?
    """

    result = read_query(sql, (user_id,))

    if result:
        return result[0]

    return None

def create_user(username: str, password_hash: str, role_id):

    sql = """
    INSERT INTO users(username, password_hash, role_id)
    VALUES (?, ?, ?)
    """

    insert_query(sql, (username, password_hash, role_id))


def register(user: UserCreate) -> UserCreate:
    
    existing = get_by_username(user.username)


    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")       

    password_hash = hash_pass(user.password)
    user_count = get_users_count()
    
    role_id = 1 if user_count == 0 else 2
        
    create_user(user.username, password_hash, role_id)   

    return {"message": "User registered successfully"}


def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    db_user = get_by_username(form_data.username)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not check_pass(form_data.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt(db_user["username"], db_user["role_id"])

    return {"access_token": token, "token_type": "bearer"}


def promote_to_admin(user_id: int):

    user = get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=403, detail="User not found")
    
    if user["role_id"] == 1:
        raise HTTPException(status_code=400, detail="User is already admin")
    
    if user == 1:
        raise HTTPException(status_code=400, detail="User is Admin")

    sql = """
    UPDATE users
    SET role_id = 1
    WHERE id = ?
    """

    update_query(sql, (user_id,))

    return {"message": "User promoted to ADMIN"}

def demote_admin(user_id: int):

    user = get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=403, detail="User not found")
    
    if user_id == 1:
        raise HTTPException(status_code=400, detail="User is super user")

    sql = """
    UPDATE users
    SET role_id = 2
    WHERE id = ?
    """

    update_query(sql, (user_id,))

    return {"message": "Admin rights removed"}

def get_users_count():
    sql = "SELECT COUNT(*) AS count FROM users"
    result = read_query(sql)
    return result[0]["count"]