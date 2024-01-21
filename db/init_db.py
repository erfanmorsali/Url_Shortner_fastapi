import secrets

from db.session import Base, engine
from urls.entities.urls import Url
from users.entities.users import User


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

    url = db.query(Url).first()
    if url is None:
        url = Url(link="www.google.com", short_link="abc")
        db.add(url)
        db.commit()
        db.refresh(url)
