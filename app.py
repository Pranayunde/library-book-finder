from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction"},
    {"id": 2, "title": "Wings of Fire", "author": "A. P. J. Abdul Kalam", "category": "Biography"},
    {"id": 3, "title": "Atomic Habits", "author": "James Clear", "category": "Self-help"},
    {"id": 4, "title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "category": "Finance"},
    {"id": 5, "title": "Ikigai", "author": "Héctor García and Francesc Miralles", "category": "Self-help"},
]


@app.route("/")
def index():
    return render_template("index.html", books=BOOKS)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/books")
def get_books():
    query = request.args.get("q", "").strip().lower()
    results = [
        book for book in BOOKS
        if query in book["title"].lower()
        or query in book["author"].lower()
        or query in book["category"].lower()
    ] if query else BOOKS
    return jsonify(results)


@app.route("/api/books/<int:book_id>")
def get_book(book_id):
    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
