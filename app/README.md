# Struktur Folder `app/`

Folder `app/` adalah root utama aplikasi backend. Di dalamnya dibagi berdasarkan prinsip Clean Architecture agar
tanggung jawab tiap bagian jelas dan terpisah.

```
app/
├── application/
├── core/
├── domain/
├── infrastructure/
├── interface/
```

---

## `application/`

Berisi logika tingkat aplikasi (use case).

Isi folder ini biasanya:

* Use case / service orchestration
* Port (interface / abstract class)
* DTO internal
* Flow eksekusi bisnis

Folder ini:

* Mengatur alur proses
* Menggunakan entity dari `domain`
* Tidak tahu detail implementasi teknis (DB, file system, framework)

Contoh:

* `report_generator_port.py`
* `generate_report_usecase.py`

---

## `domain/`

Berisi inti model bisnis.

Isi folder ini biasanya:

* Entity
* Value Object
* Enum
* Aturan bisnis murni

Folder ini:

* Tidak boleh bergantung pada framework
* Tidak tahu soal database
* Tidak tahu soal HTTP

Ini adalah layer paling stabil dan paling independen.

---

## `infrastructure/`

Berisi implementasi teknis dari abstraction di `application`.

Isi folder ini biasanya:

* Adapter database (PostgreSQL)
* Implementasi file writer (XLSX)
* Integrasi library eksternal
* External service client

Folder ini:

* Berinteraksi langsung dengan dunia luar
* Menggunakan library pihak ketiga
* Mengimplementasikan port dari `application`

Contoh:

* `open_report_adapter.py`
* `postgres_repository.py`

---

## `interface/`

Berisi layer komunikasi dengan client (API).

Isi folder ini biasanya:

* FastAPI router
* Controller
* Request schema
* Response schema

Folder ini:

* Menerima HTTP request
* Validasi input
* Memanggil use case dari `application`
* Mengembalikan response

Contoh:

* `report_controller.py`
* `report_router.py`

---

## `core/`

Berisi utilitas umum yang digunakan lintas layer.

Isi folder ini biasanya:

* Helper function
* Sanitizer
* Logger setup
* Konfigurasi global
* Shared constant

Folder ini:

* Tidak mengandung logika bisnis utama
* Tidak mengandung orchestration use case

---

## Dependency Direction

Arah dependency selalu mengarah ke dalam:

```
interface → application → domain
infrastructure → application → domain
```

* `domain` tidak bergantung pada siapa pun
* `application` bergantung pada `domain`
* `interface` dan `infrastructure` bergantung pada `application`