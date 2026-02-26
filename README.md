# Jubelio Report Server

A high-performance, multi-tenant XLSX reporting service designed to replace legacy .NET/Telerik-based reporting systems.

Built with a Clean Architecture approach to ensure strict separation of concerns, scalability, and long-term
maintainability.

---

# Architecture Overview

The system follows **Clean Architecture principles** and is organized into clear layers:

```text
report-server/
├── app/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── interface/
│   └── core/
├── .venv/
└── README.md
```

The dependency rule is strictly enforced:

```
interface → application → domain
infrastructure → application
core → shared utilities
```

Inner layers do not depend on outer layers.

---

# Layer Responsibilities

## 1. Domain Layer (`app/domain/`)

The heart of the system.

Contains:

* Business entities
* Domain models
* Pure business rules
* No framework or external dependency

Characteristics:

* Framework-agnostic
* Database-agnostic
* Fully testable in isolation

This layer defines **what the system is**, not how it runs.

---

## 2. Application Layer (`app/application/`)

Orchestrates use cases.

Contains:

* Use case services
* Application-level DTOs
* Ports (interfaces / abstractions)
* Business workflow coordination

Responsibilities:

* Defines report generation flow
* Defines repository contracts
* Coordinates database access and report execution

This layer defines **what the system does**.

---

## 3. Infrastructure Layer (`app/infrastructure/`)

Implements technical details.

Contains:

* PostgreSQL integration (`psycopg2`)
* XLSX generation (`xlsxwriter`)
* Concrete repository implementations
* External system adapters

Responsibilities:

* Execute SQL queries
* Stream database results
* Generate XLSX files incrementally
* Handle file I/O

This layer implements **how the system works technically**.

---

## 4. Interface Layer (`app/interface/`)

Delivery mechanism.

Contains:

* FastAPI endpoints
* HTTP request/response schemas
* Dependency injection wiring

Responsibilities:

* HTTP routing
* Authentication handling
* Tenant resolution
* Input validation
* Trigger application use cases

This layer is the **entry point of the system**.

---

## 5. Core (`app/core/`)

Shared utilities and cross-cutting concerns.

Contains:

* Configuration
* Dependency providers
* Logging setup
* Shared helpers

No business logic is placed here.

---

# Execution Flow

High-level flow for report generation:

```
Client Request
      ↓
FastAPI Endpoint (interface)
      ↓
Use Case Service (application)
      ↓
Repository / Report Port
      ↓
Infrastructure Implementation
      ↓
psycopg2 → Stream rows
      ↓
xlsxwriter → Write incrementally
      ↓
Generated XLSX File
```

The system is designed to:

* Stream database rows
* Avoid loading full result sets into memory
* Prevent OOM during large exports
* Support multi-tenant execution safely

---

# Database Strategy

## System Database

* Stores tenant configuration and metadata
* Accessed via psycopg2

## Tenant Databases

* Accessed dynamically using tenant-specific credentials
* Uses server-side cursor for streaming
* Data fetched incrementally
* Directly written into XLSX writer

---

# Technology Stack

| Component       | Technology         |
|-----------------|--------------------|
| API Layer       | FastAPI            |
| Database Driver | psycopg2           |
| XLSX Engine     | xlsxwriter         |
| Language        | Python 3.11+       |
| Architecture    | Clean Architecture |

---

# Design Principles

* Clean Architecture compliance
* Strict dependency direction
* Streaming-first data processing
* Multi-tenant safe-by-default
* Memory-efficient report generation
* Framework isolation from domain logic

---

# Non-Goals

* No ORM usage
* No heavy in-memory aggregation
* No tight coupling between API and infrastructure
* No direct framework dependency inside domain

---

# Intended Use Cases

* Large-scale XLSX exports
* Enterprise reporting workloads
* Multi-tenant SaaS environments
* Replacement for legacy .NET reporting engines