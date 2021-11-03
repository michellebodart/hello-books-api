from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, request, make_response

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

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
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
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
        return jsonify({
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                })
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

@authors_bp.route("", methods=["GET","POST"], strict_slashes=False)
def handle_authors():
    if request.method == "POST":
        request_body = request.get_json()
        new_author = Author(name=request_body["name"])

        db.session.add(new_author)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created", 201)

@authors_bp.route("/<author_id>/books", methods=["GET","POST"], strict_slashes=False)
def handle_authors_books(author_id):
    author = Author.query.get(id=author_id)
    if not author:
        return "Author not found", 404

    if request.method == "POST":
        request_body = request.get_json()

        new_book = Book(title=request_body["title"], description=request_body["description"], author=author)

        db.session.add(new_book)
        db.session.commit()
        return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)

