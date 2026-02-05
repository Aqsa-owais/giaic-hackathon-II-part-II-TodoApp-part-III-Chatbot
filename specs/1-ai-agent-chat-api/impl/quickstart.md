# Quick Start Guide: AI Agent & Chat API

**Feature**: 1-ai-agent-chat-api
**Date**: 2026-01-20

## Prerequisites

### Environment Variables
Set these environment variables before starting:

```bash
# OpenAI API configuration
OPENAI_API_KEY="your-openai-api-key"

# Database configuration
DATABASE_URL="postgresql://username:password@localhost:5432/todo_chatbot"

# JWT authentication
JWT_SECRET="your-jwt-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# MCP Tools endpoint
MCP_TOOLS_BASE_URL="http://localhost:8001"
```

### External Dependencies
- PostgreSQL database server
- MCP tools service running and accessible
- OpenAI API access

## Setup Instructions

### 1. Database Initialization
Run the database migrations to create required tables:

```bash
# Using alembic or similar migration tool
alembic upgrade head
```

Required tables:
- `conversations` - stores conversation metadata
- `messages` - stores individual messages in conversations

### 2. Install Dependencies
```bash
pip install fastapi uvicorn openai sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart
```

### 3. Service Configuration
Configure the application with the environment variables above, then start the service:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Usage Examples

### Making a Chat Request

```bash
curl -X POST "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": "123e4567-e89b-12d3-a456-426614174001"
  }'
```

### Expected Response
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174001",
  "response": "I've added the task 'buy groceries' for you.",
  "status": "success",
  "timestamp": "2026-01-20T10:00:00Z",
  "actions_taken": [
    {
      "tool": "add_task",
      "result": {
        "task_id": "123e4567-e89b-12d3-a456-426614174002",
        "description": "buy groceries"
      }
    }
  ]
}
```

## Architecture Components

### 1. Authentication Layer
- Validates JWT tokens in the Authorization header
- Extracts user ID for authorization checks
- Rejects requests with invalid or expired tokens

### 2. Conversation Management
- Loads existing conversation if ID provided
- Creates new conversation if no ID provided
- Retrieves full conversation history from database

### 3. AI Agent Service
- Initializes OpenAI Assistant with registered MCP tools
- Processes user message with full conversation context
- Executes appropriate MCP tools based on recognized intent
- Generates natural language response

### 4. MCP Tool Integration
- Defines function schemas that map to MCP tool endpoints
- Handles HTTP requests to external MCP services
- Processes tool execution results back to the agent

### 5. Response Construction
- Formats agent response for user consumption
- Captures actions taken during processing
- Updates conversation and message history in database

## Troubleshooting

### Common Issues

1. **OpenAI API Connection Errors**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check internet connectivity to OpenAI services

2. **MCP Tools Unavailable**
   - Confirm MCP tools service is running at configured URL
   - Check network connectivity between services

3. **JWT Authentication Failures**
   - Verify JWT token format and validity
   - Confirm `JWT_SECRET` matches token signing key

### Logging
The service logs important events to help with debugging:

- Request processing start/end
- MCP tool invocations and results
- Authentication successes/failures
- Error conditions with stack traces