import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ganti-dengan-secret-key-kamu-sendiri'
DATABASE = 'library.db'


# ------------------- DATABASE HELPERS -------------------
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT,
                year INTEGER,
                status TEXT DEFAULT 'Belum Dibaca',
                rating INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        db.commit()


# ------------------- READ (semua) -------------------
@app.route('/')
def index():
    db = get_db()
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')

    sql = 'SELECT * FROM book WHERE 1=1'
    params = []

    if search_query:
        sql += ' AND (title LIKE ? OR author LIKE ?)'
        params.extend([f'%{search_query}%', f'%{search_query}%'])

    if status_filter:
        sql += ' AND status = ?'
        params.append(status_filter)

    sql += ' ORDER BY created_at DESC'

    books = db.execute(sql, params).fetchall()

    total_books = db.execute('SELECT COUNT(*) FROM book').fetchone()[0]
    total_read = db.execute(
        "SELECT COUNT(*) FROM book WHERE status = 'Selesai Dibaca'"
    ).fetchone()[0]

    return render_template(
        'index.html',
        books=books,
        search_query=search_query,
        status_filter=status_filter,
        total_books=total_books,
        total_read=total_read
    )


# ------------------- CREATE -------------------
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        year = request.form.get('year')
        status = request.form.get('status')
        rating = request.form.get('rating', 0)

        if not title or not author:
            flash('Judul dan Penulis wajib diisi!', 'danger')
            return redirect(url_for('add_book'))

        db = get_db()
        db.execute(
            '''INSERT INTO book (title, author, genre, year, status, rating, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                title,
                author,
                genre or None,
                int(year) if year else None,
                status,
                int(rating) if rating else 0,
                datetime.utcnow().isoformat()
            )
        )
        db.commit()
        flash(f'Buku "{title}" berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', book=None, action='Tambah')


# ------------------- READ (detail satu buku) -------------------
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    db = get_db()
    book = db.execute('SELECT * FROM book WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        flash('Buku tidak ditemukan.', 'danger')
        return redirect(url_for('index'))
    return render_template('detail.html', book=book)


# ------------------- UPDATE -------------------
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    db = get_db()
    book = db.execute('SELECT * FROM book WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        flash('Buku tidak ditemukan.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()

        if not title or not author:
            flash('Judul dan Penulis wajib diisi!', 'danger')
            return redirect(url_for('edit_book', book_id=book_id))

        genre = request.form.get('genre', '').strip()
        year = request.form.get('year')
        status = request.form.get('status')
        rating = request.form.get('rating', 0)

        db.execute(
            '''UPDATE book SET title=?, author=?, genre=?, year=?, status=?, rating=?
               WHERE id=?''',
            (
                title,
                author,
                genre or None,
                int(year) if year else None,
                status,
                int(rating) if rating else 0,
                book_id
            )
        )
        db.commit()
        flash(f'Buku "{title}" berhasil diperbarui!', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', book=book, action='Edit')


# ------------------- DELETE -------------------
@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    db = get_db()
    book = db.execute('SELECT * FROM book WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        flash('Buku tidak ditemukan.', 'danger')
        return redirect(url_for('index'))

    db.execute('DELETE FROM book WHERE id = ?', (book_id,))
    db.commit()
    flash(f'Buku "{book["title"]}" berhasil dihapus.', 'success')
    return redirect(url_for('index'))


# ------------------- JINJA FILTER (format tanggal) -------------------
@app.template_filter('format_date')
def format_date(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%d %B %Y, %H:%M')
    except (ValueError, TypeError):
        return value


init_db()


if __name__ == '__main__':
    app.run(debug=True)
