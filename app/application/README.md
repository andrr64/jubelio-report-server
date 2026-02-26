# Application Layer

Folder `application/` berisi logika tingkat aplikasi (use case orchestration) dan abstraction yang menjadi penghubung antara domain dan infrastructure.

Layer ini **tidak berisi implementasi teknis**, melainkan kontrak dan alur proses bisnis.

```text
application/
├── dto/
├── exceptions/
├── protocols/
├── services/
└── usecases/

```

---

## `dto/` (Data Transfer Objects)

Berisi objek representasi data murni.

Digunakan untuk:

* Membawa data antar layer.
* Membentuk struktur input/output use case.
* Menghindari kebocoran entity domain ke layer luar.

DTO tidak mengandung logika bisnis kompleks, hanya struktur data.

**Contoh isi:**

* `DBConfig` (`db_config.py`)
* `GeneratedFile` (`generated_file.py`)
* `ReportContext` (`report_context.py`)

---

## `exceptions/`

Berisi custom exception tingkat aplikasi.

Digunakan untuk:

* Menangani error use case secara spesifik.
* Membuat error lebih terstruktur sebelum dilempar ke layer *Interface*.
* Menghindari penggunaan exception bawaan Python secara generik.

**Contoh isi:**

* `html_exceptions.py` (Error terkait output HTML/Response)
* `report_exceptions.py` (Error spesifik kegagalan *generate report*, seperti parameter hilang)

---

## `protocols/`

Berisi abstraction (interface / Protocol).

Digunakan untuk:

* Mendefinisikan kontrak yang harus diimplementasikan oleh *Infrastructure layer* (Dependency Inversion).
* Memisahkan use case dari detail teknis (seperti koneksi DB atau Storage).

**Contoh isi:**

* `BucketRepository` (`bucket_repository.py`)
* `DatabaseProvider` (`database_port.py`)
* `ReportGeneratorPort` (`report_generator_port.py`)
* `TenantRepositoryPort` (`tenant_repository_port.py`)

---

## `services/`

Berisi service fungsional tingkat aplikasi dan *helper* spesifik *domain logic*.

Digunakan untuk:

* Menyimpan logika terisolasi yang *reusable* antar use case.
* Memisahkan tanggung jawab parsial agar use case tidak terlalu gemuk (*bloated*).

**Sub-domain / Contoh isi:**

* **`resolver/`**: Logika penentuan konfigurasi report (`legacy_report_config_resolver.py`).
* **`sql/`**: Logika manipulasi *query* mentah (`sql_param_binder.py`, `params_sanitizer.py`).

---

## `usecases/`

Berisi implementasi *use case* utama sistem.

Digunakan untuk:

* Mengatur flow eksekusi bisnis dari awal request hingga selesai.
* Mengorkestrasi pemanggilan ke berbagai `protocols` (DB, Cache, Storage, Engine).

Setiap file *use case* biasanya merepresentasikan satu aksi/fitur bisnis utama.

**Contoh isi:**

* `GenerateExcelReportUseCase` (`GenerateExcelReport.py`)

---

## Tanggung Jawab Layer Application

* Mengatur alur proses bisnis secara prosedural.
* Menjadi pusat pengatur (orkestrator) bagi komponen teknis.
* Sangat bergantung pada abstraction (`protocols`).
* Sama sekali **tidak mengetahui detail implementasi teknis** (seperti AWS, R2, PostgreSQL, atau FastAPI).