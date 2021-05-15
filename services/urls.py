from sqlalchemy.orm import Session
from schemas import urls
from models.urls import Url
from .users import user_service
from fastapi import HTTPException


class UrlService:
    def create_url(self, db: Session, schema: urls.BaseUrlSchema, user):
        url_data = schema.dict()
        url = self.get_url_by_link(db, url_data.get("link"))
        if url is None:
            url_data.update(owner_id=user.id)
            url = Url(**url_data)
            db.add(url)
            db.commit()
            shorted_link = self.url_shortner(db, url.id)
            setattr(url, "short_link", shorted_link)
            db.commit()
            db.refresh(url)
        return url

    def get_url_by_link(self, db: Session, original_link: str):
        url = db.query(Url).filter(Url.link == original_link).first()
        return url

    def get_all_urls(self, db: Session):
        urls = db.query(Url).all()
        return urls

    def url_shortner(self, db: Session, id):
        shorten_url = self.encode(id)
        return shorten_url

    def encode(self, id):
        characters = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        base = len(characters)

        ret = []

        while id > 0:
            val = id % base
            ret.append(characters[val])
            id = id // base

        return "".join(ret[::-1])

    def update_url(self, db: Session, pk: int, schema: urls.BaseUrlSchema):
        updated_data = schema.dict(exclude_unset=True)
        url = self.get_url_by_id(db, pk)
        for field, value in updated_data.items():
            setattr(url, field, value)
        db.commit()
        db.refresh(url)
        return url

    def get_url_by_id(self, db: Session, pk: int):
        url = db.query(Url).filter(Url.id == pk).first()
        if url is None:
            raise HTTPException(404, detail={"message": "url not found"})
        return url


url_service = UrlService()
