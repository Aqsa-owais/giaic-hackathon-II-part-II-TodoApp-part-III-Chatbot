---
id: 1
title: Update Todo Chatbot Constitution
stage: constitution
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: claude-code
command: /sp.constitution
labels: [constitution, todo-chatbot, mcp, agent]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Phase III – Todo AI Chatbot (Agent + MCP)

Objective:
Build a stateless AI-powered chatbot that manages todos through natural
language using OpenAI Agents SDK and MCP server architecture.

Core Principles:
- Agent controls reasoning, MCP controls data
- Stateless server, persistent database
- Clear separation of concerns
- Deterministic, tool-driven task management
- No hallucinated or inferred task state

Architecture Rules:
- Chat endpoint handles conversation orchestration only
- AI agent must NEVER mutate data directly
- All task operations MUST go through MCP tools
- MCP tools are stateless and persist to database
- Conversation state stored in DB, not memory

Agent Responsibilities:
- Understand natural language intent
- Select correct MCP tool
- Build valid tool inputs
- Confirm actions with friendly responses
- Handle errors gracefully

MCP Responsibilities:
- Expose task tools:
  add_task, list_tasks, update_task, complete_task, delete_task
- Validate inputs and enforce user isolation
- Persist all state using SQLModel + PostgreSQL
- Return structured, reliable outputs

Constraints:
- No manual coding (Claude Code only)
- No shared state between requests
- No direct DB access from agent
- Tools must be idempotent where applicable

Quality Standards:
- Accurate tool invocation
- Clear confirmations for every action
- Graceful failure on invalid tasks
- Resume conversations after restart

Success Criteria:
- Todos fully manageable via natural language
- Conversation context persists across requests
- MCP tools act as single source of truth
- System passes statelessness review
```

## Response snapshot

Updated the project constitution to reflect the requirements for the Phase III – Todo AI Chatbot project with OpenAI Agents SDK and MCP server architecture. The new constitution emphasizes:

- Agent controls reasoning, MCP controls data
- Stateless server architecture with database persistence
- Deterministic tool-based operations through MCP tools
- Clear separation of concerns between AI agent and MCP server
- Zero hallucination principle requiring all data from MCP tools

The updated constitution removes the previous multi-user web application focus and replaces it with the specific architecture for the AI chatbot with MCP server.

## Outcome

- ✅ Impact: Updated constitution to reflect Todo AI Chatbot with MCP architecture
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Continue with spec, plan, and task creation for the Todo AI Chatbot
- 🧠 Reflection: Constitution now properly reflects the agent/MCP architecture requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec creation for the Todo AI Chatbot