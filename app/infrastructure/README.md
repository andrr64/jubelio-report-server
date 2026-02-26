# Infrastructure Layer

Folder `infrastructure/` berisi detail implementasi teknis dari sistem. Layer ini bertanggung jawab penuh untuk berkomunikasi dengan "dunia luar" (Database, File System, Cloud Storage, dan External Engine).

Semua *class* di layer ini **wajib mengimplementasikan *protocols* (interface)** yang sudah didefinisikan di layer `Application`.

```text
infrastructure/
└── adapters/
    ├── cache/
    ├── persistance/
    │   ├── bucket/
    │   ├── database/
    │   ├── local/
    │   └── repository/
    ├── report_generator/
    └── security/

```

---

## `adapters/`

Berisi implementasi konkret (*adapter*) dari setiap *port* aplikasi.

### 1. `cache/`

Menangani mekanisme *caching* data untuk optimasi performa.

* **Isi:** `memory_cache.py` (In-memory cache untuk menyimpan master data secara sementara).

### 2. `persistance/`

Menangani segala bentuk persistensi dan penyimpanan data (Cloud, DB, Lokal).

* **`bucket/`:** Integrasi ke *cloud object storage* (`cloudflare_r2.py`).
* **`database/`:** *Wrapper* koneksi dan eksekusi level bawah ke *database* (`postgres.py`, `mysql.py`, `mongodb.py`).
* **`local/`:** Manajemen *file system* server lokal, biasanya untuk file *temporary* (`local_fm_adapter.py`).
* **`repository/`:** Implementasi *repository pattern* yang menggunakan *database adapter* untuk mengembalikan data spesifik (`tenant_repository_postgres.py`).

### 3. `report_generator/`

Integrasi dengan *engine* pembuat *report* pihak ketiga.

* **Isi:** `open_report.py` (Implementasi komunikasi dengan *Rust OpenReport engine* atau library XLSX).

### 4. `security/`

Menangani implementasi teknis terkait autentikasi dan otorisasi.

* **Isi:** `auth/token_decoder.py` (Logika *decoding* dan verifikasi token/JWT dari *request*).

---

## Aturan Layer Infrastructure (The Infrastructure Rule)

* **Hanya Eksekusi Teknis:** Dilarang keras menaruh logika bisnis (*if-else* alur bisnis) di sini. Layer ini hanya peduli *bagaimana* cara melakukan *query* SQL, *bagaimana* cara memanggil R2, atau *bagaimana* cara *write* file.
* **Dependency Inversion:** Infrastructure bergantung pada Application (mengimplementasikan `protocols`), bukan sebaliknya.
* **Plug & Play:** Setiap *adapter* harus didesain agar mudah diganti (misal: ganti PostgreSQL ke MySQL, atau R2 ke AWS S3) tanpa perlu menyentuh satu baris pun kode di layer `Application`.