# Core Layer

Folder `core/` berisi hal-hal yang bersifat *cross-cutting concerns* (konfigurasi sistem, utilitas global, dan inisialisasi aplikasi). 

Layer ini **tidak berisi logika bisnis**, melainkan fondasi teknis dasar yang digunakan oleh seluruh layer lain (terutama *Interface* dan *Infrastructure*).

```text
core/
├── config.py
├── logger.py
└── state.py

```

---

## `config.py`

Berisi pengaturan global sistem dan *environment variables*.

Digunakan untuk:

* Membaca file `.env` (biasanya menggunakan Pydantic `BaseSettings`).
* Menyimpan kredensial *default* (Database System, AWS/R2, dll).
* Menentukan *environment* aplikasi (Development, Staging, Production).

Semua pengaturan yang sifatnya dinamis dan bergantung pada server *deployment* harus diatur di sini.

---

## `logger.py`

Berisi konfigurasi *logging* global aplikasi.

Digunakan untuk:

* Membuat format log terpusat (contoh: log request API, durasi eksekusi, error handling).
* Mengatur *log level* (INFO, DEBUG, ERROR, OK).
* Memastikan semua pesan error dan status terekam dengan standar yang sama di *console* atau *file*.

Semua layer yang membutuhkan *print/logging* wajib mengimpor module `log` dari file ini.

---

## `state.py`

Berisi *container* untuk inisialisasi *Dependency Injection* dan *Global State*.

Digunakan untuk:

* Menyiapkan objek *singleton* saat aplikasi (FastAPI) baru menyala (*startup/lifespan*).
* Mem- *wiring* (menyambungkan) implementasi dari *Infrastructure* ke *Use Cases* di layer *Application*.
* Menyimpan instance koneksi *database global*, *cache*, dan *storage adapter* agar tidak di-*instantiate* berulang kali setiap ada *request*.

File ini adalah jantung dari integrasi Clean Architecture di aplikasi ini tanpa menggunakan *framework dependency injection* eksternal.

---

## Tanggung Jawab Layer Core

* Menangani *setup* dan *bootstrapping* aplikasi.
* Menyediakan fungsionalitas umum yang tidak terikat pada satu *domain/use case* spesifik.
* Menyimpan *secrets* dan pengaturan sistem.
* **Sama sekali tidak bergantung pada layer Domain, Application, atau Interface.**
