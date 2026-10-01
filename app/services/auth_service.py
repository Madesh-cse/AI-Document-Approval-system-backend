from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return db.execute(statement).scalar_one_or_none()


def create_user(
    db: Session,
    email: str,
    full_name: str,
    organization: str,
    workflow_domain: str,
    role: UserRole,
    password: str,
) -> User:

    user = User(
        email=email,
        full_name=full_name,
        organization=organization,
        workflow_domain=workflow_domain,
        role=role,
        password_hash=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user