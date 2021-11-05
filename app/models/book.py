from app import db
from app.models.genre import Genre
from app.models.book_genre import BookGenre

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")
    genres = db.relationship("Genre", secondary="books_genres", backref="books")

    def to_dict(self):
        genres = [genre.name for genre in self.genres]
        author = None if not self.author else self.author.name
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": author,
            "genres": genres
        }
