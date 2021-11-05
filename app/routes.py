from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from flask import Blueprint, jsonify, request, make_response

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")
genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

# BOOKS

@books_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_books():
    if request.method == "GET":
        title_query = request.args.get('title')
        if title_query:
            books = Book.query.filter_by(title=title_query)
            book_exists = False
            for book in books:
                book_exists = True
                break
            if not book_exists:
                return make_response("", 404)
        else:
            books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append(book.to_dict())
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"], description=request_body["description"])

        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_book(book_id):
    book_id = int(book_id)
    book = Book.query.get(book_id)
    if book is None:
        return make_response("", 404)
    if request.method == "GET":
        return book.to_dict()
    elif request.method == "PUT":
        form_data = request.get_json()
        if form_data.get("title"):
            book.title = form_data["title"]
        if form_data.get("description"):
            book.description = form_data["description"]

        db.session.commit()
        return make_response(f"Book #{book.id} successfully updated")
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book #{book.id} successfully deleted")

# AUTHORS

@authors_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_authors():
    if request.method == "GET":
        authors = Author.query.all()
        authors_response = []
        for author in authors:
            authors_response.append({
                "id": author.id,
                "name": author.name
            })
        return jsonify(authors_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_author = Author(name=request_body["name"])

        db.session.add(new_author)
        db.session.commit()

        return make_response(f"Author {new_author.name} successfully created", 201)

# AUTHORS x BOOKS

@authors_bp.route("/<author_id>/books", methods=["GET", "POST"], strict_slashes=False)
def handle_authors_books(author_id):
    author = Author.query.get(author_id)
    if author == None:
        return "Author not found", 404

    if request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"], description=request_body["description"], author=author)
        db.session.add(new_book)
        db.session.commit()
        return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)

    elif request.method == "GET":
        books_response = []
        for book in Book.query.filter(Book.author == author):
            books_response.append({
                "title": book.title,
                "id": book.id,
                "description": book.description
            })
        return jsonify(books_response)

# GENRES

@genres_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_genres():
    if request.method == "POST":
        request_body = request.get_json()
        new_genre = Genre(name=request_body["name"])
        db.session.add(new_genre)
        db.session.commit()
        return new_genre.to_dict(), 201
    elif request.method == "GET":
        genres = Genre.query.all()
        return jsonify([genre.to_dict() for genre in genres])

# BOOKS x GENRES

@books_bp.route("/<book_id>/assign_genres", methods=["PATCH"], strict_slashes=False)
def assign_genres(book_id):
    request_body = request.get_json()
    book = Book.query.get_or_404(book_id)
    for id in request_body["genres"]:
        book.genres.append(Genre.query.get(id))
    
    db.session.commit()
    return make_response("Genres successfully added", 200)
    
