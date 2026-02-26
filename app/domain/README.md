# Domain Layer

Folder `domain/` adalah pusat atau "jantung" dari Clean Architecture. Namun, untuk *Reporting Server* ini, layer ini **sengaja dibiarkan kosong** (untuk saat ini).

## Kenapa Kosong?

Aplikasi *reporting* pada umumnya bersifat **Data-Driven Orchestration**. Tugas utama dari sistem ini adalah membaca data mentah (dari PostgreSQL), melakukan *binding* parameter (dari *request*), dan menuliskannya ke format `.xlsx` secara *streaming*. 

Sistem ini tidak secara aktif memutasi state bisnis utama (seperti memotong stok, memvalidasi transaksi, atau mengubah status pesanan). Seluruh logika bisnis yang kompleks sebagian besar sudah diselesaikan di tingkat *Query SQL* atau di dalam sistem *core backend*.

---

## Apa yang seharusnya diletakkan di sini? (Jika berevolusi)

Jika di masa depan aplikasi ini membutuhkan logika bisnis murni tingkat tinggi (*enterprise business rules*), komponen-komponen berikut akan dimasukkan ke dalam folder ini:

### 1. `entities/`
Objek bisnis utama yang memiliki identitas (ID) unik dan memiliki siklus hidup.
*Contoh: Objek `Tenant` murni, `ReportTemplate`.*

### 2. `value_objects/`
Objek yang didefinisikan berdasarkan atributnya saja (tidak punya identitas unik). Jika nilainya sama, objek tersebut dianggap sama.
*Contoh: `ReportDateRange` (untuk memvalidasi rentang tanggal laporan tidak boleh lebih dari 1 tahun), `QueryString`.*

---

## Aturan Emas Layer Domain (The Golden Rule)

Walaupun saat ini kosong, jika ada *engineer* yang menambahkan kode ke folder ini di masa depan, **wajib mematuhi aturan berikut**:

1. **Zero Framework Dependencies:** Tidak boleh ada *import* dari library eksternal atau *framework* (seperti FastAPI, Pydantic, Psycopg2, aioboto3).
2. **Pure Python:** Hanya boleh menggunakan fitur bawaan Python (`dataclasses`, `enum`, `datetime`, `typing`).
3. **Total Isolation:** Layer ini sama sekali tidak boleh tahu dari mana data berasal (Database/R2) dan ke mana data dikirim (Excel/HTTP).