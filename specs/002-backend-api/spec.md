# Feature Specification: Backend REST API & Persistent Data Layer

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-08
**Status**: Draft
**Input**: User description: "Backend REST API & Persistent Data Layer (Todo App)

Target audience:
Hackathon evaluators reviewing backend architecture, data modeling, and secure API design

Focus:
- FastAPI-based REST backend
- Persistent task storage using SQLModel and Neon PostgreSQL
- Strict user-level data isolation using JWT-derived identity
- Clean, standards-compliant API behavior

Success criteria:
- All task-related REST endpoints are implemented and functional
- Each API request is authenticated via verified JWT
- Task ownership is enforced on every database operation
- Users can only read, modify, or delete their own tasks
- Data persists correctly across sessions and restarts
- API responses follow HTTP standards and expected schemas

Functional scope:
- FastAPI application setup
- SQLModel models for Task (with user ownership)
- Neon Serverless PostgreSQL integration
- Database session and dependency management
- REST API endpoints:
  - GET    /api/{user_id}/tasks
  - POST   /api/{user_id}/tasks
  - GET    /api/{user_id}/tasks/{id}
  - PUT    /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH  /api/{user_id}/tasks/{id}/complete
- JWT verification dependency/middleware
- Filtering all queries by authenticated user ID

Constraints:
- No unauthenticated access to any endpoint
- User ID from JWT must match resource ownership
- No in-memory or mock storage
- SQLModel must be used as ORM
- PostgreSQL must be the single source of truth
- No manual SQL queries unless required by SQLModel

Timeline:
- Designed to fit within hackathon Phase-2 backend scope

Not building:
- Admin-level APIs
- Cross-user task sharing
- Background jobs or schedulers
- Search, tags, or task categories
- Analytics or reporting endpoints"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated User Task Management (Priority: P1)

An authenticated user wants to manage their personal tasks via API endpoints. They can create, read, update, delete, and mark tasks as complete, with all operations restricted to their own data through JWT authentication.

**Why this priority**: This is the core functionality of the backend API - providing authenticated access to user-specific task data.

**Independent Test**: An authenticated user can perform all basic task operations (CRUD + completion toggle) on their personal tasks via API calls.

**Acceptance Scenarios**:
1. Given an authenticated user makes a POST request to /api/{user_id}/tasks with valid task data, when the JWT token matches the user_id, then the task is created in the database and returned with a 201 status.
2. Given an authenticated user makes a GET request to /api/{user_id}/tasks, when the JWT token matches the user_id, then all tasks owned by that user are returned with a 200 status.

---

### User Story 2 - Task Ownership Enforcement (Priority: P1)

An authenticated user attempts to access tasks belonging to another user. The system must reject these requests and only allow access to tasks owned by the authenticated user.

**Why this priority**: Critical security requirement to ensure user data isolation and privacy.

**Independent Test**: When a user attempts to access another user's tasks, the system returns a 404 or 403 error.

**Acceptance Scenarios**:
1. Given a user with JWT token for user_id=A makes a GET request to /api/B/tasks (where B ≠ A), when the request is processed, then the system returns a 403 Forbidden or 404 Not Found response.
2. Given a user with JWT token for user_id=A makes a GET request to /api/A/tasks/{task_id} where task_id belongs to user B, when the request is processed, then the system returns a 404 Not Found response.

---

### User Story 3 - Task State Management (Priority: P2)

An authenticated user wants to update the completion status of their tasks. The system provides a dedicated endpoint to toggle the completion state of a task.

**Why this priority**: Essential functionality for task management workflow.

**Independent Test**: An authenticated user can update the completion status of their tasks via the PATCH endpoint.

**Acceptance Scenarios**:
1. Given an authenticated user makes a PATCH request to /api/{user_id}/tasks/{id}/complete, when the task exists and belongs to the user, then the task's completion status is toggled and the updated task is returned.
2. Given an authenticated user makes a PUT request to /api/{user_id}/tasks/{id} with updated task data, when the task exists and belongs to the user, then the task is updated and returned with a 200 status.

### Edge Cases

- What happens when a user attempts to access a non-existent task ID?
- How does system handle expired JWT tokens?
- What occurs when database connection fails during operations?
- How does the system handle concurrent access to the same task?
- What happens when a user attempts to create a task with invalid data?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a FastAPI application with health check endpoint
- **FR-002**: System MUST authenticate all API requests via verified JWT tokens
- **FR-003**: System MUST enforce user ownership on all task operations using JWT-derived user ID
- **FR-004**: System MUST provide GET endpoint at /api/{user_id}/tasks to retrieve user's tasks
- **FR-005**: System MUST provide POST endpoint at /api/{user_id}/tasks to create new tasks
- **FR-006**: System MUST provide GET endpoint at /api/{user_id}/tasks/{id} to retrieve specific task
- **FR-007**: System MUST provide PUT endpoint at /api/{user_id}/tasks/{id} to update tasks
- **FR-008**: System MUST provide DELETE endpoint at /api/{user_id}/tasks/{id} to delete tasks
- **FR-009**: System MUST provide PATCH endpoint at /api/{user_id}/tasks/{id}/complete to toggle completion status
- **FR-010**: System MUST store task data persistently in PostgreSQL using SQLModel
- **FR-011**: System MUST validate all input data according to task schema requirements
- **FR-012**: System MUST return appropriate HTTP status codes for all operations
- **FR-013**: System MUST implement proper error handling with descriptive error messages
- **FR-014**: System MUST ensure data integrity and consistency across all operations
- **FR-015**: System MUST filter all database queries by authenticated user ID

### Key Entities *(include if feature involves data)*

- **Task**: Represents individual tasks created by users, containing title, description, completion status, creation timestamp, and user ownership reference
- **User**: Represents authenticated users of the system, identified by user ID extracted from JWT token
- **JWT Token**: Represents authentication tokens that verify user identity and grant access to user-specific resources
- **Database Connection**: Represents the connection to PostgreSQL database for persistent storage

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 required REST endpoints are implemented and accessible with proper authentication
- **SC-002**: 100% of authenticated requests successfully validate JWT and enforce user ownership
- **SC-003**: Users can only access, modify, or delete their own tasks with zero cross-user data access
- **SC-004**: Data persists correctly across application restarts with no data loss
- **SC-005**: All API responses follow HTTP standards with appropriate status codes (200, 201, 401, 403, 404, 500)
- **SC-006**: Task CRUD operations complete with sub-500ms response time under normal load
- **SC-007**: System handles at least 100 concurrent users without degradation in performance
- **SC-008**: All input validation passes successfully and rejects invalid data with 400 status codes
