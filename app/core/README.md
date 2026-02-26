# Core Layer

Folder `core/` berisi komponen pendukung umum yang digunakan lintas layer dalam aplikasi.

Layer ini tidak berisi logika bisnis utama dan tidak merepresentasikan use case.
Tujuannya adalah menyediakan utilitas dan konfigurasi yang reusable.

```text
core/
├── config.py
```

---

## Tujuan Core Layer

* Menyimpan konfigurasi global aplikasi
* Menyediakan utilitas bersama
* Menghindari duplikasi kode
* Menjadi tempat komponen yang tidak termasuk domain, application, atau infrastructure

Core bersifat teknikal-support, bukan business-driven.

---

## `config.py`

Berisi konfigurasi aplikasi.

Digunakan untuk:

* Membaca environment variable
* Menyimpan default configuration
* Menyusun konfigurasi sistem (database, cache, dsb)

File ini biasanya menjadi pusat pengaturan runtime aplikasi.

Contoh tanggung jawab:

* Memuat DSN database
* Menentukan mode environment (dev / prod)
* Menyediakan settings object

---

## Karakteristik Core

* Tidak mengandung entity bisnis
* Tidak mengandung use case
* Tidak mengimplementasikan port
* Tidak bergantung pada layer infrastructure secara spesifik

Core boleh digunakan oleh:

* application
* infrastructure
* interface

Namun tetap harus dijaga agar tidak menjadi “tempat buang semua hal”.

---

## Prinsip Penggunaan

Jika suatu file:

* Tidak mengandung aturan bisnis
* Tidak mengandung orchestration use case
* Tidak mengakses sistem eksternal secara langsung
* Bersifat reusable dan general

Maka file tersebut dapat ditempatkan di `core/`