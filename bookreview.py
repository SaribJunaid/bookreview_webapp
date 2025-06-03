from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Local memory DB for books and reviews
book_db: Dict[str, dict] = {}

# Book schema
class Book(BaseModel):
    title: str
    author: str
    genre: str

# Review schema
class Review(BaseModel):
    title: str  # Book title to associate the review with
    reviewer: str
    rating: int
    comment: str

# Add a new book
@app.post("/add_book")
def add_book(book: Book):
    if book.title in book_db:
        return {"message": "Book already exists."}
    
    book_db[book.title] = {
        "book": {
            "author": book.author,
            "genre": book.genre
        },
        "reviews": []
    }
    return {"message": "Book successfully added.", "data": book_db[book.title]}

# Add a review for a book
@app.post("/add_review")
def add_review(review: Review):
    if review.title not in book_db:
        return {"message": "Book does not exist."}
    
    book_db[review.title]["reviews"].append({
        "reviewer": review.reviewer,
        "rating": review.rating,
        "comment": review.comment
    })
    return {
        "message": "Review successfully added.",
        "data": book_db[review.title]["reviews"]  
    }

# View reviews for a specific book
@app.get("/view_reviews")
def view_reviews(title: str):
    if title not in book_db:
        return {"message": "Book does not exist."}
    return {"data": book_db[title]["reviews"]}

# Delete a book and its reviews
@app.delete("/book/{title}")
def delete_book(title: str):
    if title in book_db:
        del book_db[title]
        return {"message": "Book and its reviews deleted."}
    return {"error": "Book not found."}
