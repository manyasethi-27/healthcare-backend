# 🏥 Healthcare Backend API

A secure, RESTful backend system for a healthcare application built with **Django**, **Django REST Framework**, and **PostgreSQL**.

---

## ✨ Features

- **JWT Authentication** — Secure login/registration using `djangorestframework-simplejwt`
- **Patient Management** — Full CRUD for patient records (owner-scoped)
- **Doctor Management** — Full CRUD for doctor records
- **Patient-Doctor Mapping** — Assign/remove doctors to patients, query by patient
- **Environment-based Configuration** — Sensitive data stored in `.env`
- **CORS Support** — Ready for frontend integration

---

## 🏗️ Project Structure

```
whatbytes/
├── healthcare_project/       # Core project settings & routing
│   ├── settings.py
│   └── urls.py
├── authentication/           # Register & Login APIs
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── patients/                 # Patient CRUD APIs
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── doctors/                  # Doctor CRUD APIs
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── mappings/                 # Patient-Doctor Assignment APIs
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── .env                      # Environment variables (DO NOT COMMIT)
├── .env.example              # Template for environment variables
├── requirements.txt
└── manage.py
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL installed and running

### 1. Clone & navigate
```bash
cd whatbytes
```

### 2. Create & activate a virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=your-very-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Create the PostgreSQL database
```sql
-- In psql shell:
CREATE DATABASE healthcare_db;
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create a superuser (optional, for Django Admin)
```bash
python manage.py createsuperuser
```

### 8. Start the development server
```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

---

## 📡 API Endpoints

All authenticated endpoints require the header:
```
Authorization: Bearer <access_token>
```

---

### 🔐 Authentication APIs

#### Register a new user
```
POST /api/auth/register/
```
**Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123"
}
```
**Response (201):**
```json
{
  "message": "User registered successfully.",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" }
}
```

#### Login
```
POST /api/auth/login/
```
**Body:**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```
**Response (200):**
```json
{
  "message": "Login successful.",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com" },
  "tokens": {
    "access": "<jwt_access_token>",
    "refresh": "<jwt_refresh_token>"
  }
}
```

---

### 🧑‍⚕️ Patient Management APIs

All endpoints require `Authorization: Bearer <token>`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/patients/` | Create a new patient |
| `GET` | `/api/patients/` | List all patients created by logged-in user |
| `GET` | `/api/patients/<id>/` | Get a specific patient |
| `PUT` | `/api/patients/<id>/` | Update a patient (partial update supported) |
| `DELETE` | `/api/patients/<id>/` | Delete a patient |

**POST /api/patients/ Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1990-05-15",
  "gender": "F",
  "address": "123 Main St, City",
  "medical_history": "Diabetes Type 2"
}
```

---

### 👨‍⚕️ Doctor Management APIs

All endpoints require `Authorization: Bearer <token>`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/doctors/` | Add a new doctor |
| `GET` | `/api/doctors/` | Retrieve all doctors |
| `GET` | `/api/doctors/<id>/` | Get a specific doctor |
| `PUT` | `/api/doctors/<id>/` | Update doctor details |
| `DELETE` | `/api/doctors/<id>/` | Delete a doctor |

**POST /api/doctors/ Body:**
```json
{
  "name": "Dr. Alice Brown",
  "email": "alice@hospital.com",
  "phone": "+9876543210",
  "specialization": "Cardiology",
  "license_number": "MED-001-2024",
  "experience_years": 10,
  "hospital": "City General Hospital",
  "bio": "Expert cardiologist with 10 years experience."
}
```

---

### 🔗 Patient-Doctor Mapping APIs

All endpoints require `Authorization: Bearer <token>`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/mappings/` | Assign a doctor to a patient |
| `GET` | `/api/mappings/` | List all patient-doctor mappings |
| `GET` | `/api/mappings/<patient_id>/` | Get all doctors for a specific patient |
| `DELETE` | `/api/mappings/delete/<id>/` | Remove a mapping by mapping ID |

**POST /api/mappings/ Body:**
```json
{
  "patient": 1,
  "doctor": 2,
  "notes": "Referred for cardiac evaluation"
}
```

---

## 🛡️ Security Notes

- Passwords are hashed using Django's built-in PBKDF2-SHA256
- JWT tokens expire after **24 hours** (access) / **7 days** (refresh)
- Patient records are **owner-scoped** — users can only view their own patients
- Change `SECRET_KEY` to a long, random value in production
- Set `DEBUG=False` in production

---

## 🧪 Testing with Postman

1. Import the base URL: `http://127.0.0.1:8000`
2. Register a user → `POST /api/auth/register/`
3. Login → `POST /api/auth/login/` → copy the `access` token
4. Set header `Authorization: Bearer <token>` for all subsequent requests
5. Test Patient, Doctor, and Mapping endpoints
