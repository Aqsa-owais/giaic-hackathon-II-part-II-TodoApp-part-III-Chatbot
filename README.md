# Multi-User Todo Web Application

A secure multi-user Todo web application with JWT-based authentication. The implementation follows a clear separation of concerns with a Next.js frontend and FastAPI backend. All user data is properly isolated through JWT verification on every request, ensuring users can only access their own tasks. The system uses SQLModel ORM with Neon PostgreSQL for persistent storage and Better Auth for JWT-based authentication.

## Features

- User registration and authentication via JWT
- Secure todo management with user isolation
- Full CRUD operations for todo tasks
- Responsive web interface
- JWT-based session management

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLModel, Better Auth
- **Frontend**: Next.js 16+, TypeScript/JavaScript, React
- **Database**: PostgreSQL (via Neon Serverless)
- **Authentication**: JWT with Better Auth
- **API**: RESTful API with standard HTTP methods and status codes

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

## API Endpoints

- Authentication: `/auth/register`, `/auth/login`
- Todo operations: `/api/todos/*` (requires authentication)

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (must be at least 32 characters)
- `FRONTEND_URL`: Allowed origin for CORS

### Frontend
- `NEXT_PUBLIC_API_URL`: URL of the backend API

## Development

### Backend
The backend is built with FastAPI and provides:
- JWT-based authentication
- User registration and login
- Todo CRUD operations with user ownership enforcement
- Proper validation and error handling

### Frontend
The frontend is built with Next.js and provides:
- User registration and login forms
- Dashboard for managing todos
- Responsive UI for task management
- JWT token management

## Security

- All API endpoints require valid JWT authentication
- Users can only access their own data
- Passwords are securely hashed using bcrypt
- Input validation is performed on both frontend and backend
- CORS is properly configured

## Architecture

The application follows a clear separation of concerns:
- **Frontend**: Next.js application for user interface
- **Backend**: FastAPI application for API endpoints and business logic
- **Authentication**: JWT-based using Better Auth
- **Data Layer**: SQLModel ORM with PostgreSQL
- **Security**: Middleware for authentication and authorization