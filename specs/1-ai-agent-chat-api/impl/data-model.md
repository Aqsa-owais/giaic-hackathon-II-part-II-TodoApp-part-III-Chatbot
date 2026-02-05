# Data Model: AI Agent & Chat API

**Feature**: 1-ai-agent-chat-api
**Date**: 2026-01-20

## Entities

### Conversation
Represents a user's chat session with the AI agent.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - Links to the user who owns this conversation
- `created_at`: DateTime - Timestamp when conversation was created
- `updated_at`: DateTime - Timestamp when conversation was last updated
- `title`: String (Optional) - Auto-generated from first message or user-provided

**Validation Rules**:
- `user_id` must exist in users table
- `created_at` set automatically on creation
- `updated_at` updated automatically on any change

**Relationships**:
- One-to-many with Message (one conversation, many messages)

### Message
Represents individual messages in a conversation, including user input and AI responses.

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the message
- `conversation_id`: UUID (Foreign Key) - Links to parent conversation
- `role`: Enum (String) - Values: "user", "assistant", "tool"
- `content`: Text - The actual message content
- `timestamp`: DateTime - When the message was created
- `tool_calls`: JSON (Optional) - Details of tools called by assistant
- `tool_responses`: JSON (Optional) - Results from tool executions

**Validation Rules**:
- `conversation_id` must exist in conversations table
- `role` must be one of allowed values
- `content` cannot be empty
- `timestamp` set automatically on creation

**Relationships**:
- Many-to-one with Conversation (many messages, one conversation)

### User (Referenced Entity)
Represents an authenticated user who owns conversations and tasks.
(This entity is assumed to exist from other parts of the system)

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String - User's email address
- `created_at`: DateTime - Account creation timestamp

## State Transitions

### Conversation States
- **Active**: New conversation created, ready to receive messages
- **Archived**: Conversation completed or marked as inactive (future enhancement)

### Message States
Messages don't have explicit states but follow this flow:
- Created with user role when user sends a message
- AI processes and creates assistant message with potential tool_calls
- Tool execution results in tool messages with tool_responses
- Final response sent to user

## Constraints

1. **User Isolation**: Users can only access their own conversations
2. **Referential Integrity**: Foreign keys must reference valid records
3. **Data Consistency**: Message timestamps must be sequential within conversations
4. **Size Limits**: Content fields have reasonable limits to prevent abuse