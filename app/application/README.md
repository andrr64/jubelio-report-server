# Application Layer

Folder `application/` berisi logika tingkat aplikasi (use case orchestration) dan abstraction yang menjadi penghubung
antara domain dan infrastructure.

Layer ini **tidak berisi implementasi teknis**, melainkan kontrak dan alur proses bisnis.

```
application/
├── dto/
├── exceptions/
├── prototcols/
├── services/
├── usecases/
```

---

## `dto/`

Berisi Data Transfer Object.

Digunakan untuk:

* Membawa data antar layer
* Membentuk struktur input/output use case
* Menghindari kebocoran entity domain ke layer luar

DTO tidak mengandung logika bisnis kompleks, hanya struktur data.

Contoh isi:

* `GenerateReportRequest`
* `GenerateReportResponse`

---

## `exceptions/`

Berisi custom exception tingkat aplikasi.

Digunakan untuk:

* Menangani error use case
* Membuat error lebih terstruktur
* Menghindari penggunaan exception generik

Contoh:

* `ReportGenerationError`
* `InvalidParameterError`

Exception di sini bersifat business/application level, bukan error teknis database.

---

## `prototcols/`

Berisi abstraction (interface / abstract class).

Digunakan untuk:

* Mendefinisikan kontrak yang harus diimplementasikan oleh infrastructure
* Memisahkan use case dari detail teknis

Contoh:

* `ReportGeneratorPort`
* `RepositoryPort`

Infrastructure layer wajib mengimplementasikan port ini.

---

## `services/`

Berisi service tingkat aplikasi.

Digunakan untuk:

* Menyimpan logika reusable antar use case
* Menggabungkan beberapa port dalam satu alur
* Helper orchestration tingkat aplikasi

Service di sini bukan entity domain, tapi logic coordinator.

---

## `usecases/`

Berisi implementasi use case utama sistem.

Digunakan untuk:

* Mengatur flow eksekusi bisnis
* Menggunakan entity dari domain
* Memanggil port untuk akses eksternal

Setiap use case biasanya merepresentasikan satu aksi bisnis.

Contoh:

* `GenerateReportUseCase`
* `ExportSalesReportUseCase`

---

## Tanggung Jawab Layer Application

* Mengatur alur proses bisnis
* Menggunakan domain sebagai pusat aturan
* Bergantung pada abstraction (prototcols)
* Tidak mengetahui implementasi teknis