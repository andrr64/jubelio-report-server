# Jubelio Report Server

A high-performance, multi-tenant XLSX reporting service designed to replace legacy .NET/Telerik-based systems. Built with Clean Architecture to ensure scalability, memory efficiency (streaming-first), and long-term maintainability.

## 🚀 Quick Start

Ensure you have Python 3.11+ installed.

```bash
pip install -r requirements.txt
python main.py

```

## 🏗️ Architecture Overview

The dependency rule is strictly enforced: `interface → application → domain` and `infrastructure → application`.

* **`app/domain/`**: Pure business entities and models. Framework-agnostic.
* **`app/application/`**: Use cases, business workflow orchestration, and repository contracts (ports).
* **`app/infrastructure/`**: Technical implementations (PostgreSQL, XLSX generation, file I/O).
* **`app/interface/`**: Delivery mechanism (FastAPI endpoints, routing, HTTP schemas).
* **`app/core/`**: Shared utilities (configuration, logging, dependency providers).

## 🔄 Execution Flow

Designed to prevent OOM during large exports by streaming database rows directly into the XLSX writer.

`Client Request` ➔ `FastAPI Endpoint` ➔ `Use Case` ➔ `psycopg2 (Stream rows)` ➔ `xlsxwriter (Incremental write)` ➔ `Generated XLSX`

## 🗄️ Database Strategy

* **System Database:** Stores tenant configurations and metadata.
* **Tenant Databases:** Accessed dynamically using tenant-specific credentials via server-side cursors.

## 🛠️ Technology Stack

* **API Framework:** FastAPI
* **Database Driver:** psycopg2
* **XLSX Engine:** xlsxwriter
* **Language:** Python 3.11+
* **Design:** Clean Architecture