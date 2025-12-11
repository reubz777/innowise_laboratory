import models
import schemas
from sqlalchemy import or_
from sqlalchemy.orm import Session


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def search_books(db: Session, title: str = None, author: str = None, year: int = None):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.contains(title))
    if author:
        query = query.filter(models.Book.author.contains(author))
    if year:
        query = query.filter(models.Book.year == year)
    return query.all()


def update_book(db: Session, book_id: int, book_update: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in book_update.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
