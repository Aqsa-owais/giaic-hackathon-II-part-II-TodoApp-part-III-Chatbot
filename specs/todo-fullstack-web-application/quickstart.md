# Quickstart Guide: Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL-compatible database (Neon recommended)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
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
# Edit .env.local with your API URL and auth settings
```

### 4. Database Setup

```bash
# From backend directory
cd backend

# Run database migrations
alembic upgrade head
```

### 5. Running the Application

#### Backend (Terminal 1)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-min-32-chars
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

## API Endpoints

### Authentication (Handled by Better Auth)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Operations (Require Authentication)
- `GET /api/tasks` - Get all user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `PATCH /api/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/tasks/{task_id}` - Delete a task

## Usage

1. Visit the frontend at `http://localhost:3000`
2. Register or login with your credentials
3. Create, view, update, and delete tasks
4. Mark tasks as complete/incomplete

## Building for Production

### Backend
```bash
# No special build step needed for Python
# Just deploy the source with dependencies
```

### Frontend
```bash
npm run build
npm start  # Runs the production server
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```