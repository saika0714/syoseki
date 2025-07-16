from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(host='localhost', user='saika', password='saika0714', db='book_management', cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

from flask import jsonify

@app.route('/students/<int:book_id>')
def get_students(book_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        if book['is_borrowed']:
            cursor.execute("SELECT * FROM students WHERE student_id = %s", (book['borrowed_by'],))
        else:
            cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
    conn.close()
    return jsonify(students)

@app.route('/borrow', methods=['POST'])
def borrow():
    book_id = request.form['book_id']
    student_id = request.form['student_id']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE books SET is_borrowed = 1, borrowed_by = %s WHERE id = %s", (student_id, book_id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/return', methods=['POST'])
def return_book():
    book_id = request.form['book_id']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE books SET is_borrowed = 0, borrowed_by = NULL WHERE id = %s", (book_id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO books (title, author, is_borrowed) VALUES (%s, %s, 0)", (title, author))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

