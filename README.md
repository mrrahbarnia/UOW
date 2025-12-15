# Bookkeeper

**Bookkeeper** is a reference Python project inspired by **Architecture patterns with Python** book.

---

## Table of Contents

- [Overview](#overview)  
- [Architecture](#architecture)  
- [Features](#features)  
- [Project Structure](#project-structure)  
- [Setup](#setup)  
- [Usage](#usage)  
- [Testing](#testing)  
- [Contributing](#contributing)  

---

## Overview

Bookkeeper is a minimalistic service for managing books in a library system. It focuses on the architecture and design rather than complex business logic. This makes it a great reference for learning or prototyping **clean and scalable Python applications**.

---

## Architecture

The project is inspired by several modern architecture patterns:

### 1. **Domain-Driven Design (DDD)**
- All business logic resides in the **domain layer**.
- Entities and Value Objects are implemented with dataclasses.
- Domain events are dispatched in the use case/service layer and handled in handlers.

### 2. **Clean / Hexagonal Architecture**
- **Adapters**: Implement database access, external services, and notifications.
- **Use Cases / Services**: Encapsulate business operations (e.g., borrowing a book).
- **Entry Points / API**: Only handle HTTP requests and responses, translating them to domain operations.
- Dependencies flow **inwards**, keeping the core domain isolated from infrastructure.

### 3. **Unit of Work Pattern**
- Ensures that all operations on repositories are committed or rolled back as a single atomic transaction.
- Supports async operations with SQLAlchemy.

### 4. **Dependency Injection**
- Uses a DI container (`punq`) to inject dependencies like notification services.
- Allows easy substitution of implementations (e.g., EmailNotification vs TestNotification).

---

## Features

- Async API with **FastAPI**
- **PostgreSQL** backend with SQLAlchemy ORM
- Domain events and handlers
- Borrow and return books with **pessimistic locking**
- Configurable and testable dependency injection
- Clear separation of **domain**, **infrastructure**, and **application layers**
- Ready for unit and integration testing