# Quickstart Guide: Backend REST API & Data Layer

## Prerequisites
- Python 3.11+
- PostgreSQL-compatible database (Neon recommended)
- JWT-compatible authentication system

## Setup Instructions

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Navigate to backend directory
cd backend
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database URL and JWT secret
```

### 3. Database Configuration
```bash
# Run database migrations
alembic upgrade head
```

### 4. Running the Application
```bash
# Start backend server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Key Features
- JWT-based authentication for all endpoints
- User data isolation through JWT verification
- Full CRUD operations for tasks with ownership enforcement
- RESTful API design with standard HTTP methods and status codes

## API Endpoints
- Task listing: `GET /api/{user_id}/tasks`
- Task creation: `POST /api/{user_id}/tasks`
- Task detail: `GET /api/{user_id}/tasks/{id}`
- Task update: `PUT /api/{user_id}/tasks/{id}`
- Task deletion: `DELETE /api/{user_id}/tasks/{id}`
- Task completion: `PATCH /api/{user_id}/tasks/{id}/complete`

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret
- `FRONTEND_URL`: Allowed origin for CORS