from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import (
    PasswordResetConfirm,
    PasswordResetRequest,
    Token,
    TokenRefreshRequest,
    UserCreate,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a brand new user account."""
    # 1. Ensure the email isn't already registered
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # 2. Hash the plain text password before storing it
    db_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Log in to receive JWT Access and Refresh Tokens."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(payload: TokenRefreshRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
    )
    try:
        data = jwt.decode(
            payload.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if data.get("type") != "refresh":
            raise credentials_exception
        user_id: str = data.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/forgot-password")
def request_password_reset(
    body: PasswordResetRequest, db: Session = Depends(get_db)
):
    """Generate a password reset token (logs it to console for dev)."""
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        # Prevent email enumeration attacks by returning generic success message
        return {"message": "If that email exists, a reset link has been sent."}

    reset_token = create_password_reset_token(user.email)

    # Simulated email dispatch — token printed to dev console
    print(f"\n--- PASSWORD RESET TOKEN FOR {user.email} ---\n{reset_token}\n---------------------\n")

    return {"message": "If that email exists, a reset link has been sent."}


@router.post("/reset-password")
def reset_password(body: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Verify reset token and update password."""
    invalid_token_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired password reset token",
    )
    try:
        data = jwt.decode(
            body.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if data.get("type") != "reset":
            raise invalid_token_exception
        email: str = data.get("sub")
        if email is None:
            raise invalid_token_exception
    except JWTError:
        raise invalid_token_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise invalid_token_exception

    user.hashed_password = hash_password(body.new_password)
    db.commit()

    return {"message": "Password successfully updated. You can now log in."}