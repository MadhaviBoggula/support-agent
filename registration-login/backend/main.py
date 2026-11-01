from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt

import database
import models
import schemas

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Registration Login JWT API"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

models.Base.metadata.create_all(
    bind=database.engine
)


# ============================================================
# SECURITY
# ============================================================

security = HTTPBearer()


# ============================================================
# REGISTER
# ============================================================

@app.post("/register")
def register(
    user: schemas.RegisterRequest,
    db: Session = Depends(database.get_db)
):

    # Check whether email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password before storing
    hashed_password = hash_password(
        user.password
    )

    # Create new user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        mobile=user.mobile
    )

    # Save user
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "mobile": new_user.mobile
        }
    }


# ============================================================
# LOGIN
# ============================================================

@app.post(
    "/login",
    response_model=schemas.LoginResponse
)
def login(
    user: schemas.LoginRequest,
    db: Session = Depends(database.get_db)
):

    # Find user by email
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    # User not found
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    token = create_access_token({
        "sub": str(existing_user.id)
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# ============================================================
# PROFILE
# ============================================================

@app.get("/profile")
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(database.get_db)
):

    # Get token from Authorization header
    token = credentials.credentials

    try:

        # Decode JWT token
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get user ID from token
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # Find user in database
    user = db.query(models.User).filter(
        models.User.id == int(user_id)
    ).first()

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Token is valid",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile
        }
    }