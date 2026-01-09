---
id: 1
title: Amend Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: claude-code
command: /sp.constitution
labels: [constitution, setup, governance]
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

```text
/sp.constitution

Project: Multi-user Todo Full-Stack Web Application (Agentic Dev Stack)

Objective:
Transform a single-user console Todo app into a modern, secure, multi-user web application using a fully spec-driven, agentic development workflow with no manual coding.

Core principles:
- Spec-first development (no implementation without approved specs)
- Security by design (authentication, authorization, user isolation)
- Deterministic behavior (same input → same output)
- Clear separation of concerns (frontend, backend, auth, data)
- End-to-end traceability (spec → plan → tasks → implementation)
- Zero manual coding (Claude Code generates all implementation)

Key standards:
- All functionality must map directly to a written spec requirement
- Every API endpoint must enforce authenticated user ownership
- JWT-based authentication must be verified on every backend request
- REST APIs must follow standard HTTP semantics
- Database schema must reflect user-task ownership explicitly
- Frontend must never access or infer other users' data
- Environment variables used for all secrets and credentials
- No hard-coded secrets or credentials allowed

Architecture standards:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT enabled)
- Authorization: JWT verification via shared secret
- API communication: REST over HTTP with Bearer tokens

Security constraints:
- All API routes require a valid JWT
- Requests without JWT return 401 Unauthorized
- User ID in JWT must match resource ownership
- JWT secret shared via environment variable (BETTER_AUTH_SECRET)
- Token expiry enforced (e.g., 7 days)
- No session-based auth on backend (stateless only)

Functional constraints:
- Implement all 5 Basic Level Todo features
- Full CRUD support for tasks
- Task completion toggle supported
- Each user can access only their own tasks
- Persistent storage required (no in-memory state)
- Multi-user support is mandatory

Development constraints:
- No manual coding at any stage
- Use Agentic Dev Stack workflow only:
  Spec → Plan → Tasks → Implementation
- Each phase must be reviewed before moving forward
- Claude Code is the only implementation agent

Quality standards:
- Backend APIs must be deterministic and idempotent where applicable
- Proper HTTP status codes required
- Input validation enforced on all endpoints
- Clear error messages for auth and validation failures
- Frontend must handle loading, error, and empty states

Success criteria:
- All specs are fully implemented and traceable
- Secure multi-user isolation is enforced
- Authentication works end-to-end
- All API endpoints function as specified
- Data persists correctly across sessions
- Project can be reviewed phase-by-phase (spec, plan, tasks, code)
- No security violations or cross-user data access possible
```

## Response snapshot

# Multi-user Todo Full-Stack Web Application Constitution

## Core Principles

### Spec-First Development
All functionality must map directly to a written spec requirement. No implementation without approved specs. This ensures deterministic behavior and clear traceability from requirements to implementation.

### Security by Design
Authentication and authorization must be enforced at every level. All API endpoints require valid JWT authentication. User ID in JWT must match resource ownership. No cross-user data access is permitted. Secrets must be managed via environment variables, never hard-coded.

### Deterministic Behavior
The system must exhibit consistent behavior: same input → same output. Backend APIs must be deterministic and idempotent where applicable. This ensures predictable system behavior and reliable testing.

### Clear Separation of Concerns
Frontend, backend, authentication, and data layers must be clearly separated. Frontend uses Next.js 16+ (App Router), backend uses Python FastAPI with SQLModel ORM, and authentication uses Better Auth with JWT. Each layer has distinct responsibilities.

### End-to-End Traceability
Complete traceability from spec → plan → tasks → implementation is mandatory. Every change must be traceable through this chain. Claude Code generates all implementation with zero manual coding.

### Zero Manual Coding
Claude Code is the only implementation agent. No manual coding at any stage. Use the Agentic Dev Stack workflow only: Spec → Plan → Tasks → Implementation. Each phase must be reviewed before moving forward.

## Additional Constraints and Standards

### Architecture Standards
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT enabled)
- Authorization: JWT verification via shared secret
- API communication: REST over HTTP with Bearer tokens

### Security Constraints
- All API routes require a valid JWT
- Requests without JWT return 401 Unauthorized
- User ID in JWT must match resource ownership
- JWT secret shared via environment variable (BETTER_AUTH_SECRET)
- Token expiry enforced (e.g., 7 days)
- No session-based auth on backend (stateless only)

### Functional Requirements
- Implement all 5 Basic Level Todo features
- Full CRUD support for tasks
- Task completion toggle supported
- Each user can access only their own tasks
- Persistent storage required (no in-memory state)
- Multi-user support is mandatory

## Development Workflow
- Spec → Plan → Tasks → Implementation workflow must be followed
- Each phase must be reviewed before moving forward
- Claude Code is the only implementation agent
- All changes must be small, testable, and reference code precisely
- Proper HTTP status codes required
- Input validation enforced on all endpoints
- Clear error messages for auth and validation failures

## Governance

All implementation must adhere to these principles. Deviations require explicit approval and documentation. Every API endpoint must enforce authenticated user ownership. Environment variables used for all secrets and credentials. Frontend must handle loading, error, and empty states appropriately. All functionality must map directly to written spec requirements.

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08

## Outcome

- ✅ Impact: Created initial constitution for multi-user todo app project with all specified principles and constraints
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific constitution
- 🔁 Next prompts: Plan and implement the multi-user todo app features
- 🧠 Reflection: Constitution successfully created with all required principles from the specifications

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A