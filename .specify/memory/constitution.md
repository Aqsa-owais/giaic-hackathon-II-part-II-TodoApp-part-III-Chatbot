<!-- Sync Impact Report:
Version change: N/A -> 1.0.0
Added sections: All principles and sections based on the multi-user todo app specifications
Removed sections: Template placeholders
Templates requiring updates: N/A (this is the initial constitution)
Follow-up TODOs: None
-->
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
