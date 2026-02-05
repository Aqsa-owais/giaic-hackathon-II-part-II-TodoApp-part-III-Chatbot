# Implementation Plan: AI Agent & Chat API Layer

**Feature**: 1-ai-agent-chat-api
**Created**: 2026-01-20
**Status**: Draft
**Plan Version**: 1.0

## Technical Context

This implementation will create a stateless chat API using OpenAI Agents SDK that interprets natural language and manages todos via MCP tools. The system will follow the constitution principles of statelessness, clear separation of concerns, and tool-based operations.

### Technology Stack
- **Backend**: Python FastAPI
- **AI Agent**: OpenAI Agents SDK
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT-based
- **MCP Tools**: Remote procedure calls for todo operations

### Architecture Overview
- API endpoint accepts chat messages and user authentication
- Conversation history retrieved from database
- AI agent processes natural language with registered MCP tools
- Agent responses and tool calls persisted to database
- Results returned to user

### Unknowns
- Specific OpenAI model to use for the agent
- Exact structure of MCP tool definitions
- Rate limiting and concurrency handling specifics

## Constitution Check

Based on the project constitution, this implementation must satisfy:

- ✅ **Agent Controls Reasoning, MCP Controls Data**: AI agent will handle natural language processing but all data operations will go through MCP tools
- ✅ **Stateless Server Architecture**: No conversation state stored in memory, all data persisted to database
- ✅ **Deterministic Tool-Based Operations**: All task operations will use MCP tools (add_task, list_tasks, update_task, complete_task, delete_task)
- ✅ **Clear Separation of Concerns**: AI agent handles NLP and tool selection, MCP tools handle data operations
- ✅ **Zero Hallucination Principle**: Agent will only use information confirmed through MCP tools
- ✅ **Statelessness Requirements**: No conversation state in server memory, all context from database
- ✅ **MCP Tool Standards**: Tools will be idempotent where applicable with proper validation

## Gates

### Pre-Implementation Gates

1. **Architecture Gate**: System design must ensure no direct database access from AI agent
   - Status: PASS - Design requires all data operations through MCP tools only

2. **Security Gate**: JWT authentication must be enforced and user isolation maintained
   - Status: PASS - Authentication will be verified at API entry point with user ID validation

3. **Statelessness Gate**: No server-side conversation state in memory
   - Status: PASS - All conversation context will be loaded from and saved to database

4. **Separation of Concerns Gate**: MCP tools must handle all data operations
   - Status: PASS - AI agent will only orchestrate tool calls, not access data directly

## Phase 0: Research & Discovery

### Research Tasks

#### R1: OpenAI Agents SDK Implementation
**Decision**: Use OpenAI Assistant API with function calling capabilities
**Rationale**: Best fits the requirement for natural language processing with tool integration
**Alternatives considered**:
- Direct OpenAI API calls with manual parsing (more complex)
- Third-party agent frameworks (less control)

#### R2: MCP Tool Integration Pattern
**Decision**: Implement tools as remote procedure calls using HTTP clients
**Rationale**: Maintains clear separation between agent and data operations
**Alternatives considered**:
- Direct Python imports (violates separation principle)
- Message queues (unnecessary complexity for this scope)

#### R3: Conversation State Management
**Decision**: Load full conversation history for each request, save incremental updates
**Rationale**: Ensures consistency and supports server restarts
**Alternatives considered**:
- Partial history loading (could miss context)
- In-memory caching (violates statelessness principle)

## Phase 1: Design & Contracts

### Data Model Design

#### Conversation Entity
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to user)
- `created_at`: DateTime
- `updated_at`: DateTime
- `title`: String (optional, auto-generated from first message)

#### Message Entity
- `id`: UUID (primary key)
- `conversation_id`: UUID (foreign key to conversation)
- `role`: Enum (user, assistant, tool)
- `content`: Text
- `timestamp`: DateTime
- `tool_calls`: JSON (optional, for assistant tool calls)
- `tool_responses`: JSON (optional, for tool call results)

### API Contract Design

#### POST /api/v1/users/{user_id}/chat
**Description**: Process a chat message and return AI response

**Request**:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "uuid-string", // optional, creates new if not provided
  "metadata": {} // optional additional context
}
```

**Response**:
```json
{
  "conversation_id": "uuid-string",
  "response": "I've added the task 'buy groceries' for you.",
  "status": "success",
  "timestamp": "2026-01-20T10:00:00Z",
  "actions_taken": [
    {
      "tool": "add_task",
      "result": {"task_id": "uuid", "description": "buy groceries"}
    }
  ]
}
```

**Authentication**: JWT Bearer token required
**Authorization**: User must match the user_id in the path

### Quick Start Guide

1. **Environment Setup**:
   - Set OPENAI_API_KEY environment variable
   - Configure database connection
   - Set JWT secret for authentication

2. **Service Dependencies**:
   - MCP tools service must be running and accessible
   - Database must be initialized with required schemas

3. **Initial Configuration**:
   - Define system prompt for the AI agent
   - Register all required MCP tools
   - Set up authentication middleware

## Phase 2: Implementation Approach

### Component Breakdown

1. **Authentication Layer**: JWT verification middleware
2. **API Endpoint**: Chat handler with request/response validation
3. **Data Access Layer**: Repository pattern for Conversation/Message operations
4. **Agent Service**: OpenAI agent with MCP tool integration
5. **Tool Registry**: Dynamic registration of MCP tools
6. **Response Formatter**: Construct user-friendly responses

### Implementation Order

1. Set up data models and database access
2. Implement authentication and API endpoint structure
3. Create MCP tool registry and integration
4. Develop agent service with natural language processing
5. Connect all components and implement response formatting
6. Add error handling and validation

### Risk Mitigation

- **AI Response Quality**: Implement fallback responses for when agent fails to understand intent
- **MCP Tool Availability**: Add retry logic and graceful degradation when tools are unavailable
- **Performance**: Monitor API response times and implement caching where appropriate while maintaining statelessness