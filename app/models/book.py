from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
<<<<<<< HEAD
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
=======
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
>>>>>>> working_branch
    author = db.relationship("Author", back_populates="books")
