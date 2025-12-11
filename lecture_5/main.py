from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Collection API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.get("/books/search/", response_model=List[schemas.Book])
def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    books = crud.search_books(db, title=title, author=author, year=year)
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.update_book(db, book_id=book_id, book_update=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
