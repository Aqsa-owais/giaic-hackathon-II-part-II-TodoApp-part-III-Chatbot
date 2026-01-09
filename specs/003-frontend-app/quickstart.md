# Quickstart Guide: Frontend Application & User Experience

## Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend (if running locally)
- PostgreSQL-compatible database (Neon recommended)
- Better Auth compatible environment

## Setup Instructions

### 1. Clone and Initialize
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Navigate to frontend directory
cd frontend
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend API URL
```

### 3. Running the Application
```bash
# Start frontend development server
npm run dev
```

## Key Features
- JWT-based authentication with Better Auth
- User data isolation through JWT verification
- Full CRUD operations for tasks with ownership enforcement
- Responsive web interface using Next.js App Router

## API Endpoints Used
- Authentication: `/auth/register`, `/auth/login`
- Task operations: `/api/{user_id}/tasks/*` (requires authentication)

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL for frontend/backend communication