# Backend REST API & Data Layer

This is the backend API for the Multi-User Todo Web Application with JWT-based authentication. The implementation follows the architecture standards with a Python FastAPI backend using SQLModel ORM. All user data is properly isolated through JWT verification on every request, ensuring users can only access their own tasks. The system uses PostgreSQL for persistent storage and provides full CRUD operations with proper authentication and authorization.

## Features

- JWT-based authentication for all API requests
- User data isolation through JWT verification on every request
- Full CRUD operations for tasks with ownership enforcement
- RESTful API design with standard HTTP methods and status codes
- SQLModel ORM for database operations with PostgreSQL
- Proper error handling and validation

## Prerequisites

- Python 3.11+
- PostgreSQL-compatible database (Neon recommended)
- Better Auth compatible environment

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

### 3. Database Setup
```bash
# Run database migrations
alembic upgrade head
```

### 4. Running the Application
```bash
# Start backend server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- Health check: `GET /health`
- Task operations: `GET/POST/PUT/DELETE/PATCH /api/{user_id}/tasks/*` (require authentication)
- Chat API: `POST /api/v1/users/{user_id}/chat` (require authentication)

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (min 32 chars)
- `FRONTEND_URL`: Allowed origin for CORS
- `OPENAI_API_KEY`: OpenAI API key for AI agent functionality
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `MCP_TOOLS_BASE_URL`: Base URL for MCP tools (default: http://localhost:8000)
- `MCP_TOOLS_TIMEOUT`: Timeout for MCP tool calls in seconds (default: 30)

## AI Agent & Chat API

The AI Agent & Chat API provides a natural language interface for managing todo tasks. Users can interact with the AI assistant using conversational language to add, list, update, complete, and delete tasks.

### Natural Language Commands

The AI agent understands various task management commands:

- **Adding Tasks**: "Add a task to buy groceries", "Create a task to call John"
- **Listing Tasks**: "Show my tasks", "What tasks do I have?"
- **Updating Tasks**: "Update task 1 to 'Buy organic groceries'"
- **Completing Tasks**: "Mark task 1 as complete", "Finish the grocery task"
- **Deleting Tasks**: "Delete task 1", "Remove the grocery task"

### Architecture

- **Stateless Design**: All conversation state is stored in the database, not in memory
- **Separation of Concerns**: AI agent handles reasoning, MCP tools handle data operations
- **User Isolation**: Users can only access their own conversations and tasks
- **Rate Limiting**: Prevents abuse with configurable limits (default: 10 requests per minute per user)
- **Monitoring**: Built-in metrics collection for performance tracking