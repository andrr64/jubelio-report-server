# Domain Layer

Folder `domain/` berisi inti model bisnis sistem.
Layer ini bersifat independen dan tidak memiliki ketergantungan pada framework, database, atau teknologi eksternal.

```text
domain/
├── entities/
│   ├── db_config.py
│   ├── report_config.py
│   ├── report_context.py
│   └── README.md
```

---

## Tujuan Domain Layer

* Menyimpan struktur data inti sistem
* Merepresentasikan konsep bisnis utama
* Menjadi pusat aturan dan model yang stabil
* Tidak bergantung pada layer lain

Domain tidak mengetahui:

* FastAPI
* Database
* XLSX writer
* Infrastructure implementation

---

# Entities

Folder `entities/` berisi representasi objek inti yang digunakan dalam sistem.

Entity menggambarkan konsep utama yang dipakai dalam proses bisnis report.

---

## `db_config.py`

Berisi definisi konfigurasi database dalam bentuk entity.

Digunakan untuk:

* Menyimpan struktur DSN / connection parameter
* Representasi konfigurasi koneksi
* Digunakan oleh application sebelum diteruskan ke infrastructure

Entity ini hanya menyimpan data, bukan membuka koneksi.

---

## `report_config.py`

Berisi konfigurasi report.

Digunakan untuk:

* Menyimpan parameter report
* Menentukan query, output format, dan pengaturan lain
* Menjadi blueprint report sebelum dieksekusi

Entity ini tidak menjalankan report, hanya mendefinisikan strukturnya.

---

## `report_context.py`

Berisi context eksekusi report.

Digunakan untuk:

* Membawa informasi runtime report
* Menyimpan parameter yang sedang berjalan
* Menghubungkan config dengan proses eksekusi

Context membantu memisahkan definisi report dengan proses eksekusinya.

---

## Karakteristik Entity

* Tidak mengakses database
* Tidak membaca/menulis file
* Tidak tahu HTTP
* Tidak tahu framework

Entity hanya merepresentasikan data dan aturan yang melekat pada data tersebut.

---

## Dependency Rule

Domain:

* Tidak boleh mengimpor infrastructure
* Tidak boleh mengimpor interface
* Tidak boleh mengimpor implementation detail

Domain hanya boleh digunakan oleh layer di atasnya.