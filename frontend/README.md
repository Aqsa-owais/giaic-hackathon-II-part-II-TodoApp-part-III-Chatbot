# Frontend Application & User Experience (Todo App)

This is the frontend for the Multi-User Todo Web Application with JWT-based authentication. The implementation follows a clear separation of concerns with a Next.js 16+ frontend using App Router. The application provides secure user isolation through JWT verification on every request, ensuring users can only access their own tasks. The system integrates with a backend API for persistent storage and provides full CRUD operations with proper authentication and authorization.

## Features

- JWT-based authentication for all API requests
- User data isolation through JWT verification
- Full CRUD operations for tasks with ownership enforcement
- Responsive web interface using Next.js App Router
- Clean, standards-compliant API communication

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

- User registration and authentication via JWT
- Secure task management with user isolation
- Full CRUD operations for tasks with ownership enforcement
- Task completion toggle functionality
- Responsive web interface with clean UX

## API Endpoints Used

- Authentication: `/auth/register`, `/auth/login`
- Task operations: `/api/{user_id}/tasks/*` (requires authentication)

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API URL for frontend/backend communication