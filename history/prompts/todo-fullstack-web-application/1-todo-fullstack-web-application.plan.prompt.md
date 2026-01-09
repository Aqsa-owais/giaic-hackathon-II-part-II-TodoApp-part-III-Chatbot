---
id: 1
title: "Todo Full-Stack Web Application Plan"
stage: plan
date: "2026-01-09"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "todo-fullstack-web-application"
branch: "todo-fullstack-web-application"
user: "user"
command: "/sp.plan Todo Full-Stack Web Application (Master Plan)"
labels: ["planning", "architecture", "fullstack", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "specs/todo-fullstack-web-application/plan.md"
  - "specs/todo-fullstack-web-application/research.md"
  - "specs/todo-fullstack-web-application/data-model.md"
  - "specs/todo-fullstack-web-application/quickstart.md"
  - "specs/todo-fullstack-web-application/contracts/auth.md"
  - "specs/todo-fullstack-web-application/contracts/tasks.md"
  - ".claude/agent-context.md"
tests: []
---

# Prompt

```
/sp.plan Todo Full-Stack Web Application (Master Plan)

Planning objective:
Produce a single, deterministic execution plan that coordinates all three approved specs
(Authentication, Backend API, Frontend UI) into a coherent, agent-driven build process
suitable for Claude Code with zero manual coding.

Execution strategy:
- Build identity and trust first
- Enforce security at the backend before UI consumption
- Integrate frontend only after backend contracts are stable
- Verify each layer independently, then end-to-end

Global rules:
- No phase may begin before its dependencies are complete
- Every task must map to exactly one spec requirement
- Authentication is mandatory for all user-facing and API-facing steps
- Claude Code is the only implementation agent

--------------------------------------------------
PHASE 1 — Project & Environment Foundation
(Supports all specs)

1. Initialize repository structure (frontend + backend separation)
2. Define shared environment variables:
   - BETTER_AUTH_SECRET
   - DATABASE_URL
   - API_BASE_URL
3. Configure development and production environments
4. Verify environment isolation and secret handling

--------------------------------------------------
PHASE 2 — Authentication & Identity Layer (Spec 1)

5. Initialize Next.js authentication setup
6. Integrate Better Auth in frontend
7. Enable JWT issuance via Better Auth plugin
8. Validate JWT payload structure (user id, email)
9. Store JWT securely for API usage
10. Define frontend auth flows (signup, signin, signout)

--------------------------------------------------
PHASE 3 — Backend Security & JWT Verification (Spec 1 → Spec 2)

11. Initialize FastAPI backend project
12. Configure JWT verification using shared secret
13. Implement auth dependency/middleware
14. Reject unauthenticated requests with 401
15. Extract authenticated user from JWT context

--------------------------------------------------
PHASE 4 — Database & Data Modeling (Spec 2)

16. Configure Neon PostgreSQL connection
17. Initialize SQLModel engine and session
18. Define Task model with:
    - id
    - title
    - description
    - completed
    - user_id (ownership)
19. Create database tables
20. Verify persistence across restarts

--------------------------------------------------
PHASE 5 — Backend Task APIs (Spec 2)

21. Implement POST /tasks (user-scoped creation)
22. Implement GET /tasks (user-scoped listing)
23. Implement GET /tasks/{id} with ownership check
24. Implement PUT /tasks/{id} with validation
25. Implement DELETE /tasks/{id} with ownership enforcement
26. Implement PATCH /tasks/{id}/complete
27. Add consistent error handling (401, 403, 404, 422)

--------------------------------------------------
PHASE 6 — Frontend API Client & Protection (Spec 3)

28. Create frontend API client abstraction
29. Attach JWT to all outgoing requests
30. Implement protected route handling
31. Prevent unauthenticated UI access

--------------------------------------------------
PHASE 7 — Frontend Task UI (Spec 3)

32. Implement task list UI
33. Implement task creation form
34. Implement task update/edit UI
35. Implement task deletion UI
36. Implement task completion toggle UI
37. Handle loading, empty, and error states
38. Ensure responsive layout

--------------------------------------------------
PHASE 8 — End-to-End Verification

39. Verify auth → API → DB → UI flow
40. Confirm user data isolation
41. Validate token expiry behavior
42. Confirm persistence across sessions
43. Final consistency and spec compliance check

--------------------------------------------------
Constraints:
- No manual code edits
- No skipping phases
- No speculative features
- No direct frontend DB access
- No unauthenticated API calls

Success criteria:
- All three specs are fully implemented
- Authentication and authorization are enforced everywhere
- Users can only access their own tasks
- Project is traceable spec → plan → tasks → implementation
- Hackathon reviewers can audit every phase clearly
```

# Response

I have successfully completed the planning phase for the Todo Full-Stack Web Application. Here's a summary of what was created:

## Planning Artifacts Created

1. **Implementation Plan** (`specs/todo-fullstack-web-application/plan.md`): Comprehensive plan outlining the approach, technical context, and project structure.

2. **Research Document** (`specs/todo-fullstack-web-application/research.md`): Detailed research covering authentication systems, database connections, API patterns, and other technical decisions.

3. **Data Model** (`specs/todo-fullstack-web-application/data-model.md`): Complete entity definitions for User and Task entities with relationships, validation rules, and API contracts.

4. **Quickstart Guide** (`specs/todo-fullstack-web-application/quickstart.md`): Step-by-step setup instructions for both backend and frontend.

5. **API Contracts** (`specs/todo-fullstack-web-application/contracts/`):
   - Authentication contracts (`auth.md`)
   - Task management contracts (`tasks.md`)

6. **Agent Context** (`.claude/agent-context.md`): Updated guidelines for the development team with technology stack and commands.

## Key Design Decisions

- Authentication: Using Better Auth with JWT for secure user management
- Backend: Python FastAPI with SQLModel ORM connecting to Neon PostgreSQL
- Frontend: Next.js 16+ with App Router for modern web development
- Security: JWT-based authentication with user ownership enforcement
- Architecture: Clean separation between frontend and backend with well-defined API contracts

## Compliance with Requirements

- ✅ Spec-first development approach
- ✅ Security by design with JWT authentication
- ✅ Clear separation of concerns
- ✅ End-to-end traceability
- ✅ Zero manual coding (all artifacts generated by Claude Code)
- ✅ Multi-user support with data isolation
- ✅ All API endpoints require authentication
- ✅ User data isolation through ownership checks

The plan is now ready for the next phase: task generation using `/sp.tasks`.