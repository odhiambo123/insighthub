🚀 InsightHub API

A production-ready FastAPI backend with JWT authentication, RBAC, and refresh token rotation.

🔧 Tech Stack
	•	FastAPI
	•	PostgreSQL
	•	SQLAlchemy + Alembic
	•	JWT (access + refresh)
	•	Passlib (bcrypt)
	•	Role-Based Access Control

🔐 Authentication Flow
	1.	User logs in with email/password
	2.	API returns:
	•	Short-lived access token
	•	DB-stored refresh token
	3.	Access token used for API calls
	4.	Refresh token rotates access tokens
	5.	Logout revokes refresh token

📌 Key Endpoints

POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout

POST   /api/v1/users        (admin only)
GET    /api/v1/users/me
GET    /api/v1/users/admin

🛡 Roles
	•	user
	•	admin

Recap:

	•	✅ A real authentication system
	•	✅ Proper RBAC
	•	✅ Token lifecycle management
	•	✅ Database-safe design
	•	✅ Clean architecture


🚀 Running the App Locally

1️⃣ Prerequisites

Make sure you have:
	•	Python 3.10+
	•	PostgreSQL 15
	•	pip / venv
	•	Homebrew (macOS) or equivalent package manager

2️⃣ Clone & set up environment
git clone https://github.com/ArgeliusLabs/Chasing-Your-Tail-NG.git
cd insighthub
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3️⃣ Configure environment variables

Create a .env file in the project root:

```python

DATABASE_URL=postgresql+psycopg2://insighthub:insighthub@localhost:5432/insighthub
SECRET_KEY=dev-secret-key-change-me

```

⚠️ SECRET_KEY is safe for local development only.

4️⃣ Start PostgreSQL

Ensure PostgreSQL is running:

brew services start postgresql@15


Verify by 

psql --version

5️⃣ Create database & run migrations

createdb insighthub
alembic upgrade head

6️⃣ Start the API

uvicorn app.main:app --reload

🔐 Authentication & Testing the API

1️⃣ Create a user

curl -X POST http://127.0.0.1:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Password123",
    "role": "admin"
  }'


2️⃣ Login and get tokens

curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Password123"

Response:

{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}

3️⃣ Call protected endpoints

curl http://127.0.0.1:8000/api/v1/users/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

4️⃣ Refresh access token

curl -X POST http://127.0.0.1:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<REFRESH_TOKEN>"}'

5️⃣ Role-based endpoints

curl http://127.0.0.1:8000/api/v1/users/admin \
  -H "Authorization: Bearer <ACCESS_TOKEN>"



	•	✅ admin role → allowed
	•	❌ user role → 403 Forbidden

⸻

🧪 Testing (Manual)

At this stage, the API is tested via:
	•	Swagger UI (/docs)
	•	curl
	•	Postman / Insomnia

Automated tests will be added in a future iteration.

⸻

🧱 Tech Stack
	•	FastAPI
	•	PostgreSQL
	•	SQLAlchemy
	•	Alembic
	•	JWT (Access + Refresh)
	•	RBAC via dependencies
