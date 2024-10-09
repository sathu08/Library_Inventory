from lib.lib import *
app = Flask(__name__)

# Helper function to interact with the database
def connect_data():
    conn = sqlite3.connect("/home/saturam/Desktop/Python_Project_Folder/pythonProject/library_inventory/database/library.db")
    return conn

# Get all books, with optional filters for genre, author, and year
@app.route("/books", methods=['GET'])
def show_data():
    con = connect_data()
    cur = con.cursor()
    genre = request.args.get('genre')
    author = request.args.get('author')
    year = request.args.get('year')
    sqlite3_query = "Select * from books where 1=1 "
    fileter = []
    if genre:
        sqlite3_query+="And genre=?"
        fileter.append(genre.capitalize())
    if author:
        sqlite3_query+="And author=?"
        fileter.append(author.capitalize())
    if year:
        sqlite3_query+="And year=?"
        fileter.append(year)
    book_details = cur.execute(sqlite3_query,fileter).fetchall()
    con.close()
    return jsonify(book_details),200

# Update book details
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_books(book_id):
    data = request.json
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    year = data.get('year')
    availability = data.get("availability")
    conn = connect_data()
    cur = conn.cursor()
    update_book_query = 'UPDATE books SET '
    update_filter = []
    if title:
        update_book_query += "title=?,"
        update_filter.append(title)
    if author:
        update_book_query += "author=?,"
        update_filter.append(author)
    if genre:
        update_book_query += "genre=?,"
        update_filter.append(genre)
    if year:
        update_book_query += "year=?,"
        update_filter.append(year)
    if availability:
        update_book_query += "availability=?,"
        update_filter.append(availability)
    update_book_query = update_book_query.rstrip(',')
    update_book_query += " WHERE id=?"
    update_filter.append(book_id)
    cur.execute(update_book_query, update_filter)
    if cur.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Book not found'}), 404
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book updated successfully'}), 200

# Add a new book
@app.route("/books", methods=['POST'])
def add_books():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    genre = data.get('genre')
    year = data.get('year')
    availability = data.get("availability")
    if not title or not author:
        return jsonify({'error': 'Title and author are required'}), 400
    con = connect_data()
    cur = con.cursor()
    cur.execute("insert into books (title,author,genre,year,availability) values (?,?,?,?,?)",
                (title,author,genre,year,availability))
    con.commit()
    con.close()
    return jsonify({'message': 'Book added successfully'}), 201

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = connect_data()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Book not found'}), 404
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book delete successfully'}), 201

if __name__ =="__main__":
    app.run(debug=True)