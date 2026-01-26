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