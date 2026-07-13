# 📚 Personal Book Library — Flask CRUD App

Aplikasi web sederhana untuk mengelola koleksi buku pribadi, dibuat dengan **Python (Flask)** dan **SQLite**. Cocok dijadikan proyek portofolio karena mendemonstrasikan operasi **CRUD (Create, Read, Update, Delete)** secara penuh, ditambah fitur pencarian dan filter status.

## ✨ Fitur

- **Create** — Tambah buku baru (judul, penulis, genre, tahun, status baca, rating)
- **Read** — Lihat daftar semua buku, statistik koleksi, dan detail per buku
- **Update** — Edit informasi buku yang sudah ada
- **Delete** — Hapus buku dari koleksi (dengan konfirmasi)
- Pencarian berdasarkan judul/penulis
- Filter berdasarkan status baca (Belum Dibaca / Sedang Dibaca / Selesai Dibaca)
- Tampilan rating bintang
- UI responsif dengan Bootstrap 5 + desain custom

## 🛠️ Teknologi

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **Database**: SQLite (otomatis dibuat saat pertama kali dijalankan)
- **Frontend**: HTML, Jinja2 Templates, Bootstrap 5, Font Awesome

## 🚀 Cara Menjalankan

1. Clone / download folder proyek ini, lalu masuk ke direktorinya:

   ```bash
   cd book_library
   ```

2. (Opsional tapi disarankan) Buat virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Mac/Linux
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:

   ```bash
   python app.py
   ```

5. Buka browser dan akses:
   ```
   http://127.0.0.1:5000
   ```

Database `library.db` akan otomatis terbuat di folder proyek saat pertama kali dijalankan.

## 📁 Struktur Proyek

```
book_library/
├── app.py                 # Aplikasi Flask utama (routes + model)
├── requirements.txt
├── library.db              # Database SQLite (dibuat otomatis)
├── static/
│   └── css/
│       └── style.css       # Styling custom
└── templates/
    ├── base.html            # Layout dasar (navbar, flash messages)
    ├── index.html           # Halaman daftar buku
    ├── form.html            # Form tambah/edit (dipakai bersama)
    └── detail.html          # Halaman detail buku
```

## 💡 Ide Pengembangan Lanjutan

Beberapa hal yang bisa ditambahkan untuk memperkaya proyek ini di portofolio:

- Autentikasi user (login/register) agar tiap user punya koleksi sendiri
- Upload gambar sampul buku
- Export data ke CSV/PDF
- API RESTful (JSON) di samping tampilan web
- Deploy ke Render/Railway/PythonAnywhere agar bisa diakses publik

---

Dibuat sebagai contoh proyek CRUD sederhana menggunakan Flask.
