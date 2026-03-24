from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import logging
import uuid

app = Flask(__name__)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)

api = Api(
    app,
    version='1.0',
    title='Readify API',
    description='A RESTful Bookstore API for Readify Ltd.',
    doc='/docs'
)

# Namespaces
books_ns = api.namespace('books', description='Book operations')
authors_ns = api.namespace('authors', description='Author operations')

# In-memory storage
books = {}
authors = {}

# Models for OpenAPI documentation
author_model = api.model('Author', {
    'id': fields.String(readonly=True),
    'name': fields.String(required=True, description='Author name'),
    'bio': fields.String(description='Author biography')
})

book_model = api.model('Book', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True, description='Book title'),
    'author_id': fields.String(required=True, description='Author ID'),
    'isbn': fields.String(description='ISBN number'),
    'price': fields.Float(description='Book price')
})

book_update_model = api.model('BookUpdate', {
    'title': fields.String(description='Book title'),
    'author_id': fields.String(description='Author ID'),
    'isbn': fields.String(description='ISBN number'),
    'price': fields.Float(description='Book price')
})

# ── AUTHORS ──────────────────────────────────────────────

@authors_ns.route('/')
class AuthorList(Resource):
    @authors_ns.marshal_list_with(author_model)
    def get(self):
        """List all authors"""
        logger.info('GET /authors')
        return list(authors.values())

    @authors_ns.expect(author_model)
    @authors_ns.marshal_with(author_model, code=201)
    def post(self):
        """Add a new author"""
        data = request.json
        if not data or not data.get('name'):
            api.abort(400, 'Author name is required')
        author_id = str(uuid.uuid4())
        author = {'id': author_id, 'name': data['name'], 'bio': data.get('bio', '')}
        authors[author_id] = author
        logger.info(f'Created author {author_id}')
        return author, 201

# ── BOOKS ────────────────────────────────────────────────

@books_ns.route('/')
class BookList(Resource):
    @books_ns.marshal_list_with(book_model)
    def get(self):
        """List all books"""
        logger.info('GET /books')
        return list(books.values())

    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model, code=201)
    def post(self):
        """Add a new book"""
        data = request.json
        if not data or not data.get('title'):
            api.abort(400, 'Book title is required')
        if not data.get('author_id'):
            api.abort(400, 'Author ID is required')
        book_id = str(uuid.uuid4())
        book = {
            'id': book_id,
            'title': data['title'],
            'author_id': data['author_id'],
            'isbn': data.get('isbn', ''),
            'price': data.get('price', 0.0)
        }
        books[book_id] = book
        logger.info(f'Created book {book_id}')
        return book, 201

@books_ns.route('/<string:id>')
class Book(Resource):
    @books_ns.marshal_with(book_model)
    def get(self, id):
        """Retrieve a book by ID"""
        logger.info(f'GET /books/{id}')
        if id not in books:
            api.abort(404, 'Book not found')
        return books[id]

    @books_ns.expect(book_model)
    @books_ns.marshal_with(book_model)
    def put(self, id):
        """Replace a book entirely"""
        if id not in books:
            api.abort(404, 'Book not found')
        data = request.json
        if not data or not data.get('title'):
            api.abort(400, 'Book title is required')
        if not data.get('author_id'):
            api.abort(400, 'Author ID is required')
        books[id].update({
            'title': data['title'],
            'author_id': data['author_id'],
            'isbn': data.get('isbn', ''),
            'price': data.get('price', 0.0)
        })
        logger.info(f'Updated book {id}')
        return books[id]

    @books_ns.expect(book_update_model)
    @books_ns.marshal_with(book_model)
    def patch(self, id):
        """Partially update a book"""
        if id not in books:
            api.abort(404, 'Book not found')
        data = request.json
        if data:
            books[id].update({k: v for k, v in data.items() if k != 'id'})
        logger.info(f'Patched book {id}')
        return books[id]

    def delete(self, id):
        """Delete a book"""
        if id not in books:
            api.abort(404, 'Book not found')
        del books[id]
        logger.info(f'Deleted book {id}')
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)