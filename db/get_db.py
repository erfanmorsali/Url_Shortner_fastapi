from typing import Generator

from db.session import SessionLocal


def get_db_generator() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
