from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


# ============================================================
# JWT SETTINGS
# ============================================================

SECRET_KEY = "my-super-secret-key-change-this"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ============================================================
# HASH PASSWORD
# ============================================================

def hash_password(password: str):
    return pwd_context.hash(password)


# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ============================================================
# CREATE JWT TOKEN
# ============================================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token