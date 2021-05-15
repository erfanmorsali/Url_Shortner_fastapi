import pdb

from models.users import User
from models.urls import Url
from db.session import Base, engine
import secrets


def init_db(db):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    user = db.query(User).first()
    if user is None:
        api_key = secrets.token_hex(25)
        user = User(email="erfanmorsali@gmail.com", password="12654778", api_key=api_key)
        db.add(user)
        db.commit()
        db.refresh(user)
