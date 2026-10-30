from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import Base, BookDB
from app.schemas import BookCreate, BookRead, BookUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/books", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookDB(**book.model_dump())
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Book already exists")
    return db_book


@app.get("/api/books", response_model=list[BookRead])
def get_books(author: Optional[str] = None, db: Session = Depends(get_db)):
    statement = select(BookDB).order_by(BookDB.id)
    if author is not None:
        statement = statement.where(BookDB.author == author)
    return db.execute(statement).scalars().all()


@app.get("/api/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.get(BookDB, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.patch("/api/books/{book_id}", response_model=BookRead)
def update_book(book_id: int, changes: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.get(BookDB, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in changes.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.get(BookDB, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()

