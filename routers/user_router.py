from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user_models import  UserCreate
from services.user_service import register, login,promote_to_admin, demote_admin
from auth.security import admin_required

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(user:UserCreate):
    return register(user)


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return login(form_data)


@router.put("/promote/{user_id}")
def promote_user(user_id: int, current_user=Depends(admin_required)):
    
    if current_user:
        return promote_to_admin(user_id)
    
@router.put("/demote/{user_id}")
def demote_user(user_id: int, current_user=Depends(admin_required)):
    return demote_admin(user_id)