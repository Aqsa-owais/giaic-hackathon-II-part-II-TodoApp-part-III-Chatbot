# Todo Full-Stack Web Application Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-09

## Active Technologies

- Frontend: Next.js 16+, React, TypeScript
- Backend: Python 3.11, FastAPI, SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Package Manager: npm

## Project Structure

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

## Commands

### Backend Commands
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/

# Run database migrations
alembic upgrade head
```

### Frontend Commands
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Use async/await for asynchronous operations
- Use SQLModel for database models
- Use Pydantic for request/response validation

### JavaScript/TypeScript (Frontend)
- Use functional components with hooks
- Follow Next.js conventions for routing and data fetching
- Use TypeScript for type safety
- Follow React best practices for state management
- Use CSS Modules or Tailwind CSS for styling

## Recent Changes

- Todo Full-Stack Web Application: Implemented authentication system with Better Auth, created backend API with JWT verification, designed task data model with user ownership, and established API contracts for task operations.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->