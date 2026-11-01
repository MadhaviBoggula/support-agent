from pydantic import BaseModel, EmailStr


# ============================================================
# REGISTER REQUEST
# ============================================================

class RegisterRequest(BaseModel):

    name: str
    email: EmailStr
    password: str
    mobile: str


# ============================================================
# LOGIN REQUEST
# ============================================================

class LoginRequest(BaseModel):

    email: EmailStr
    password: str


# ============================================================
# LOGIN RESPONSE
# ============================================================

class LoginResponse(BaseModel):

    message: str
    access_token: str
    token_type: str