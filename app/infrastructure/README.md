# Infrastructure Layer

Folder `infrastructure/` berisi implementasi teknis konkret dari abstraction yang didefinisikan di layer `application`.

Layer ini menangani interaksi dengan sistem eksternal seperti database, file system, cache, dan service lain.

```text
infrastructure/
├── adapters/
│   ├── cache/
│   ├── gateways/
│   ├── generators/
│   └── persistance/
├── README.md
```

---

## `adapters/`

Berisi implementasi konkret dari `ports` yang ada di layer `application`.

Adapter adalah jembatan antara abstraction (port) dan implementasi teknis.

---

### `cache/`

Berisi implementasi sistem caching.

Digunakan untuk:

* Menyimpan hasil sementara
* Mengurangi beban database
* Optimisasi performa

Contoh:

* Redis adapter
* In-memory cache adapter

---

### `gateways/`

Berisi adapter untuk komunikasi dengan sistem eksternal.

Digunakan untuk:

* HTTP client
* External API integration
* Service-to-service communication

Folder ini menangani komunikasi keluar sistem.

---

### `generators/`

Berisi implementasi pembuat file atau output eksternal.

Digunakan untuk:

* XLSX generator
* PDF generator
* File writer

Contoh:

* Implementasi `ReportGeneratorPort`
* OpenReport adapter

---

### `persistance/`

Berisi implementasi akses data.

Digunakan untuk:

* Repository implementation
* Query execution
* Database connection handling

Folder ini berinteraksi langsung dengan database.

---

## Tanggung Jawab Layer Infrastructure

* Mengimplementasikan interface dari `application`
* Berinteraksi dengan dunia luar (DB, file, API, cache)
* Menggunakan library pihak ketiga
* Tidak mengandung aturan bisnis inti

---

## Dependency Rule

Infrastructure:

* Boleh bergantung pada `application`
* Tidak boleh dipanggil langsung oleh `domain`
* Tidak mengandung logika bisnis utama