<!-- Sync Impact Report:
Version change: 1.0.0 -> 1.1.0
Added sections: Agent/MCP architecture principles, Statelessness requirements, Natural Language Processing constraints
Removed sections: Frontend/backend specific stack requirements (replaced with agent/MCP architecture)
Templates requiring updates: .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Phase III – Todo AI Chatbot (Agent + MCP) Constitution

## Core Principles

### Agent Controls Reasoning, MCP Controls Data
The AI agent is responsible for understanding natural language intent and selecting appropriate tools, while the MCP server is responsible for all data operations and persistence. This separation ensures clean architecture with distinct responsibilities.

### Stateless Server Architecture
The chatbot server must be stateless with all conversation state stored in the database, not in memory. This enables horizontal scaling and ensures conversation persistence across server restarts.

### Deterministic Tool-Based Operations
All task operations must go through well-defined MCP tools (add_task, list_tasks, update_task, complete_task, delete_task). The AI agent must never mutate data directly, ensuring a single source of truth.

### Clear Separation of Concerns
AI agent handles natural language processing and tool selection, while MCP tools handle data validation, persistence, and user isolation. Each component has distinct responsibilities with well-defined interfaces.

### End-to-End Traceability
Complete traceability from user intent → agent reasoning → tool selection → MCP operation → database persistence is mandatory. Every action must be traceable through this chain.

### Zero Hallucination Principle
The AI agent must never fabricate or infer task state that hasn't been confirmed through MCP tools. All task information must come from reliable data sources via MCP tools.

## Additional Constraints and Standards

### Architecture Standards
- AI Agent: OpenAI Agents SDK
- MCP Server: Python-based with stateless architecture
- Database: PostgreSQL with SQLModel ORM
- Communication: JSON-based tool calls between agent and MCP
- Authentication: JWT-based user isolation in MCP tools

### Statelessness Requirements
- No conversation state stored in server memory
- All conversation context persisted to database
- System must resume conversations correctly after restart
- Horizontal scaling must be supported without data loss

### Natural Language Processing Constraints
- Agent must accurately interpret natural language task requests
- Tool selection must be precise and context-aware
- Responses must be friendly and confirm all actions taken
- Error handling must be graceful and informative

### MCP Tool Standards
- All tools must be idempotent where applicable
- Input validation must be enforced at MCP layer
- User isolation must be enforced in all tools
- Structured, reliable outputs required from all tools
- Database persistence required for all state changes

### Functional Requirements
- Todos fully manageable via natural language
- Conversation context persists across requests
- MCP tools act as single source of truth
- System passes statelessness review
- Natural language understanding covers all CRUD operations

## Development Workflow
- Spec → Plan → Tasks → Implementation workflow must be followed
- Each phase must be reviewed before moving forward
- Claude Code is the only implementation agent
- All changes must be small, testable, and reference code precisely
- Proper error handling required for all operations
- Input validation enforced on all MCP tools
- Clear confirmations for every user action

## Governance

All implementation must adhere to these principles. Deviations require explicit approval and documentation. Every MCP tool must enforce user isolation. Environment variables used for all secrets and credentials. Agent must confirm all actions with user-friendly responses. All functionality must map directly to written spec requirements.

**Version**: 1.1.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-20
