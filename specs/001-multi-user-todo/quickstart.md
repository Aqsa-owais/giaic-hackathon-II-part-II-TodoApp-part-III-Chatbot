# Quickstart Guide: Multi-User Todo Web Application

## Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL-compatible database (Neon recommended)
- Better Auth compatible environment

## Setup Instructions

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Navigate to project root
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database URL and JWT secret
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend API URL
```

### 4. Database Configuration
```bash
# From backend directory
# Run database migrations
alembic upgrade head
```

### 5. Running the Application
```bash
# Terminal 1: Start backend
cd backend
uvicorn src.api.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## Key Features
- User registration and authentication via JWT
- Secure todo management with user isolation
- Full CRUD operations for todo tasks
- Responsive web interface

## API Endpoints
- Authentication: `/auth/register`, `/auth/login`
- Todo operations: `/api/todos/*` (requires authentication)

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret
- `FRONTEND_URL`: Allowed origin for CORS