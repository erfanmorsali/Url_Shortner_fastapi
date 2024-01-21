from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.get_db import get_db
from urls.dtos import urls
from urls.entities.urls import Url


class UrlService:
    db: Session

    def __init__(self):
        self.db = get_db()

    def create(self, model: urls.BaseUrlDto, user) -> Url:
        url_data = model.model_dump()
        url = self.get_by_link(url_data.get("link"))
        if url is None:
            url_data.update(owner_id=user.id)
            url = Url(**url_data)
            self.db.add(url)
            self.db.commit()
            shorted_link = self.encode(url.id)
            setattr(url, "short_link", shorted_link)
            self.db.commit()
            self.db.refresh(url)
        return url

    def get_by_link(self, original_link: str) -> Url:
        return self.db.query(Url).filter(Url.link == original_link).first()

    def get_all(self) -> list[Type[Url]]:
        return self.db.query(Url).all()

    def update(self, pk: int, model: urls.BaseUrlDto) -> Url:
        updated_data = model.model_dump(exclude_unset=True)
        url = self.get_by_id(pk)
        for field, value in updated_data.items():
            setattr(url, field, value)
        self.db.commit()
        self.db.refresh(url)
        return url

    def get_by_id(self, pk: int) -> Url:
        url = self.db.query(Url).filter(Url.id == pk).first()
        if url is None:
            raise HTTPException(404, detail={"message": "url not found"})
        return url

    def get_by_short_link(self, short_link: str) -> Url:
        url = self.db.query(Url).filter(Url.short_link == short_link).first()
        if url is None:
            raise HTTPException(404, detail={"message": "url not found"})
        return url

    def get_by_owner_id(self, owner_id: int) -> list[Url]:
        return self.db.query(Url).filter(Url.owner_id == owner_id)

    def delete(self, url: Url):
        self.db.delete(url)
        self.db.commit()

    @staticmethod
    def encode(id: int) -> str:
        characters = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        base = len(characters)

        ret = []

        while id > 0:
            val = id % base
            ret.append(characters[val])
            id = id // base

        return "".join(ret[::-1])


url_service = UrlService()
