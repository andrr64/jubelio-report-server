# Interface Layer

Folder `interface/` adalah lapisan terluar (*Delivery Mechanism*) dari aplikasi. Layer ini bertugas sebagai pintu masuk (*entry point*) yang menjembatani dunia luar (seperti *client browser* atau API konsumen) dengan sistem internal kita.

Layer ini **sama sekali tidak boleh berisi logika bisnis**. Tugasnya hanya menerjemahkan HTTP *request* menjadi perintah untuk *Application Layer*, dan mengubah hasil dari *Application Layer* kembali menjadi HTTP *response*.

```text
interface/
└── http/
    └── api/
        ├── errors/
        │   └── error.py
        └── v1/
            ├── router.py
            └── reports/
                └── generate/
                    └── routes.py

```

---

## `http/api/errors/`

Berisi *handler* untuk menangani *error* dan pengecualian (exceptions) yang terjadi di dalam aplikasi, lalu menerjemahkannya ke dalam format HTTP *response* yang sesuai.

* **Isi:** `error.py` (Berisi fungsi seperti `custom_html_error_handler` untuk mengubah *exception* tingkat *Application* seperti `HTMLError` menjadi halaman HTML atau JSON *response* dengan status *code* yang tepat).

---

## `http/api/v1/`

Folder utama untuk API versi 1. Semua *routing* dan *endpoints* FastAPI untuk V1 diletakkan di dalam struktur ini.

### 1. `router.py`

Bertindak sebagai *aggregator* atau pengumpul semua *sub-router* yang ada di dalam V1. File ini yang nantinya akan di-*include* langsung ke objek utama aplikasi FastAPI di `main.py`.

### 2. `reports/generate/routes.py`

Berisi definisi *endpoint* API (contoh: `@router.get("/generate")`).
Tugas utama *controller/route* di sini adalah:

1. Menerima *request* HTTP (parameter URL, *headers*, atau *body*).
2. Membaca *Dependency Injection* atau *Global State* (seperti `request.app.state.ext`).
3. Memanggil *Use Case* dari layer `Application` dengan parameter yang sudah divalidasi.
4. Mengembalikan hasil (contoh: `FileResponse` untuk mengunduh file `.xlsx`).

---

## Aturan Layer Interface (The Delivery Rule)

* **No Business Logic:** Dilarang melakukan *query database* atau validasi aturan bisnis di dalam *route*. Pindahkan ke *Use Case*.
* **Validation Only:** Layer ini hanya boleh melakukan validasi format *input* (apakah tipe datanya benar, apakah token string ada, dsb).
* **Framework Dependant:** Layer ini adalah satu-satunya tempat di mana *framework web* (FastAPI, Starlette) boleh diekspos secara mendalam.