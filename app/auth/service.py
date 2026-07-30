from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str
):

    hashed_password = pwd_context.hash(password)

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user