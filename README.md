## Notes_Space

## 📝 FastAPI Notes App with Tags & JWT Authentication

A simple and powerful Notes Management API built using FastAPI, SQLite, SQLAlchemy, and JWT Authentication.
Users can register, log in, and manage their notes with tags, enabling easy filtering and search.

## 🚀 Features

User Registration & Login (JWT Authentication)

Create, Read, Update & Delete Notes

Add multiple tags to notes (comma-separated)

Search notes by tags

Password hashing and secure token-based access

SQLite database (easily switchable to PostgreSQL/MySQL)

Modular project structure with routers

Fully documented API using Swagger UI



## 🛠️ Tech Stack


| Component         | Technology                     |
| ----------------- | ------------------------------ |
| Backend Framework | FastAPI                        |
| Database          | SQLite + SQLAlchemy ORM        |
| Authentication    | JWT (OAuth2 with Bearer Token) |
| Documentation     | Swagger UI / ReDoc             |
| Language          | Python 3.10+                   |


## 📦 Installation & Setup

#### 1️⃣ Clone the Repository

```
git clone https://github.com/rishee10/Note_Space.git
```

```
cd Note_Space
```

#### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

```
venv\Scripts\activate     # Windows
```

```
source venv/bin/activate  # Mac/Linux
```


#### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

#### 4️⃣ Run the server

```
uvicorn app.main:app --reload
```
