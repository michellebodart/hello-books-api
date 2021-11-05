from app import db

class BookGenre(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey("book_id"), primary_key=True, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre_id"), primary_key=True, nullable=False)