# Context

You as a developer get to see this code.
What would you do differently and why?

**⚠You can change everything you want however you would like to.**

# Alternatives

You can choose between the different languages:

- Javascript
- Java
- C#
- C++
- Python

There are also excercises concerning:

- Dockerization
- Test automation

# The Use Case

We can book tickets for some kind of entertainment show and might get some kind of reward for booking a larger amount of tickets

# Refactoring Solutions

This repository contains various branches demonstrating different approaches and stages of refactoring the Python codebase. Each branch represents a specific step in evolving the application from a legacy script to a clean, architectural solution.

## Branches Overview

- `simple-refactor`
- `feature/new-architecture`
- `feature/next-step/db-abc-func`
- `feature/analysis-domain`

## Branch Descriptions

### `simple-refactor`
**Reason:** 
To establish a baseline for clean code and improve readability before attempting major structural changes.

**Description:** 
Initial cleanup and basic refactor of the legacy code.
- **Pydantic Models:** Introduced for robust data verification and easier manipulation.
- **IO Helper:** Created `io_helper` to manage data loading, saving, and formatting, utilizing a encoder and `os.linesep` for cross-platform compatibility.
- **Universal Formula:** Rewrote the computational logic to use a universal calculation formula, moving away from hardcoded logic.
- **Coefficients Structure:** Implemented a new data structure to manage coefficients for the universal formula.

### `feature/new-architecture`
**Reason:** 
To decouple business logic from infrastructure and external dependencies, making the system more testable, maintainable, and scalable.

**Description:** 
Implementation of a scalable Clean Architecture.
- **Goal:** Designed to support business growth and ease of extension, with a structure ready for potential microservices migration.
- **Architecture:** Tasks are distributed by roles (Data-Driven/Layered).
- **Client:** Implemented a command handler client for interaction.
- **Tests:** Added basic tests to ensure stability.
- **Features:** Added capability to save statements to `.txt` files.

**Project Tree:**
```text
theater/
├── application/
│   └── statement_service.py
├── domain/
│   ├── statement_calculator.py
│   └── statements_generator_service.py
├── infrastructure/
│   ├── repository.py
│   └── text_renderer.py
├── interfaces/
│   └── client.py
└── models/
    ├── invoice.py
    ├── play.py
    └── statement.py
```

### `feature/next-step/db-abc-func`
**Reason:** 
JSON files are inefficient for large datasets and lack strict schema enforcement, leading to potential data corruption and slow performance. Additionally, tightly coupled code made it difficult to introduce new calculation rules or storage methods without modifying the core business logic.

**Description:** 
Integration of SQL and Logic Abstraction.
- **SQL Database:** Replaced JSON storage with a SQL database using `SQLModel` for better data integrity and Pydantic compatibility.
- **Abstract Base Classes (ABC):** Implemented for Repositories and Calculators to provide flexibility.
- **Factory Pattern:** Services now use Factories to select specific implementations (subclasses) while interacting through a universal interface. This applies to both Repositories and Calculators.

**Project Tree:**
```text
data/
shared/infrastructure/
    └── database.py
theater/
├── domain/
│   ├── calculators/
│   │   ├── calculator_factory.py
│   │   ├── calculator_interface.py
│   │   ├── comedy_calculator.py
│   │   └── tragedy_calculator.py
│   └── statements_generator_service.py
├── infrastructure/
│   ├── repositories/
│   │   ├── json_repository.py
│   │   ├── orm_models.py
│   │   ├── repository_factory.py
│   │   ├── repository_interface.py
│   │   └── sql_repository.py
│   └── text_renderer.py
└── interfaces/
    └── client.py
```

### `feature/analysis-domain`
**Reason:** 
To improve performance and maintainability of data-heavy operations/reports by leveraging efficient columnar processing instead of slow Python loops.

**Description:** 
Domain Separation and High-Performance Analytics.
- **Concept:** Addressed the performance bottlenecks of processing large datasets row-by-row (Pydantic).
- **Domain Separation:**
    - **Sales Domain (Cashier):** Handles order acceptance, persistence, and individual statement generation.
    - **Analytics Domain:** Responsible for global analysis and reporting.
- **Technique:** Operations are performed on entire columns (SQL/Tables) rather than rows.
- **Polars:** Integrated `polars` for high-performance table management, universal calculation formulas, and report generation, adhering to the Data-Driven philosophy.

**Project Tree:**
```text
domains/
├── analytics/
│   ├── domain/
│   │   ├── calculators/
│   │   └── revenue_calculator.py
│   ├── infrastructure/
│   │   └── analytics_repository.py
│   ├── interfaces/
│   │   └── cli.py
│   └── services/
│       └── analytics_service.py
└── sales/
    ├── application/
    │   ├── invoice_service.py
    │   └── statement_service.py
    ├── domain/
    │   ├── calculators/
    │   └── statements_generator_service.py
    ├── infrastructure/
    │   ├── repositories/
    │   └── text_renderer.py
    └── interfaces/
        └── client.py
```
