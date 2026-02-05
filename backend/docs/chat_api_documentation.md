# AI Agent Chat API Documentation

## Overview
The AI Agent Chat API provides a natural language interface for managing todo tasks. Users can interact with the AI assistant using conversational language to add, list, update, complete, and delete tasks.

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer {your-jwt-token}
```

## API Endpoints

### POST /api/v1/users/{user_id}/chat
Process a chat message and return AI response.

#### Path Parameters
- `user_id` (string, required): The ID of the authenticated user. Must match the user ID in the JWT token.

#### Request Body
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "metadata": {}
}
```

**Fields:**
- `message` (string, required): The user's message to the AI agent
- `conversation_id` (string, optional): ID of an existing conversation. If not provided, a new conversation is created.
- `metadata` (object, optional): Additional context for the request

#### Response
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "response": "I've added the task 'buy groceries' for you.",
  "status": "success",
  "timestamp": 1678886400,
  "actions_taken": [
    {
      "tool": "add_task",
      "result": {
        "id": "task-uuid",
        "title": "buy groceries",
        "status": "created"
      }
    }
  ]
}
```

**Response Fields:**
- `conversation_id` (string): The ID of the conversation
- `response` (string): The AI agent's response to the user
- `status` (string): Status of processing ("success", "partial_success", "error")
- `timestamp` (integer): Unix timestamp when the response was generated
- `actions_taken` (array): List of actions performed by the AI agent

## Available Commands
The AI agent understands natural language and can handle various task management commands:

### Adding Tasks
- "Add a task to buy groceries"
- "Create a task to call John"
- "Add a task to finish report due tomorrow"

### Listing Tasks
- "Show my tasks"
- "What tasks do I have?"
- "List all my tasks"

### Updating Tasks
- "Update task 1 to 'Buy organic groceries'"
- "Change the description of my first task"

### Completing Tasks
- "Mark task 1 as complete"
- "Finish the grocery task"
- "Complete task 'buy groceries'"

### Deleting Tasks
- "Delete task 1"
- "Remove the grocery task"
- "Cancel the appointment task"

## Conversation Persistence
- Conversations are stored in the database and persist across server restarts
- Each user has isolated conversations
- Conversation history is maintained for context

## Rate Limiting
- The API implements rate limiting to prevent abuse
- Default limit: 10 requests per minute per user
- Exceeding the limit returns a 429 Too Many Requests status

## Error Handling
Common error responses:
- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User attempting to access another user's resources
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server-side processing error

## Examples

### Starting a New Conversation
```bash
curl -X POST "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

### Continuing an Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show my tasks",
    "conversation_id": "87654321-e89b-12d3-a456-426614174001"
  }'
```

## Implementation Notes
- All data operations are performed through MCP tools, ensuring separation of concerns
- The AI agent does not directly access the database
- Conversation state is persisted in the database, not stored in memory
- All user data is isolated by user ID