---
description: "Task list for Backend REST API & Data Layer implementation"
---

# Tasks: Backend REST API & Data Layer

**Input**: Design documents from `/specs/002-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test requirements in feature specification - tests are NOT included in this task list.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure with src/models/, src/services/, src/api/, src/middleware/
- [X] T002 Create requirements.txt with FastAPI, SQLModel, psycopg2-binary, python-jose, passlib, bcrypt, uvicorn dependencies
- [X] T003 Create .env.example file with DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL variables
- [X] T004 Create alembic/ directory structure for database migrations

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup SQLModel base and database engine in backend/src/models/base.py
- [X] T006 [P] Create Task model in backend/src/models/task.py with all required fields from data model
- [X] T007 [P] Create User model in backend/src/models/user.py with all required fields from data model
- [X] T008 Setup JWT authentication framework using python-jose in backend/src/api/main.py
- [X] T009 Create JWT verification middleware in backend/src/middleware/jwt_auth_middleware.py
- [X] T10 [P] Create database session dependencies in backend/src/api/database.py
- [X] T011 Setup environment configuration management in backend/src/config.py
- [X] T012 Create base API router setup in backend/src/api/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authenticated User Task Management (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to manage their personal tasks via API endpoints with JWT authentication

**Independent Test**: An authenticated user can perform all basic task operations (CRUD + completion toggle) on their personal tasks via API calls.

### Implementation for User Story 1

- [X] T013 [P] [US1] Create TaskService in backend/src/services/task_service.py with CRUD operations
- [X] T014 [P] [US1] Create TaskRouter in backend/src/api/task_router.py with task endpoints
- [X] T015 [US1] Implement user ownership validation in backend/src/services/task_service.py
- [X] T016 [US1] Connect task router to main app in backend/src/api/main.py
- [X] T017 [P] [US1] Implement task creation endpoint in backend/src/api/task_router.py
- [X] T018 [P] [US1] Implement task listing endpoint in backend/src/api/task_router.py
- [X] T019 [US1] Implement task detail retrieval with ownership check in backend/src/api/task_router.py
- [X] T020 [US1] Implement task update endpoint with validation in backend/src/api/task_router.py
- [X] T021 [US1] Implement task deletion with ownership enforcement in backend/src/api/task_router.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Ownership Enforcement (Priority: P1)

**Goal**: Ensure the system rejects requests to access tasks belonging to other users, only allowing access to tasks owned by the authenticated user

**Independent Test**: When a user attempts to access another user's tasks, the system returns a 404 or 403 error.

### Implementation for User Story 2

- [X] T022 [P] [US2] Enhance TaskService with ownership verification methods in backend/src/services/task_service.py
- [X] T023 [US2] Implement ownership validation in all task endpoints in backend/src/api/task_router.py
- [X] T024 [US2] Add proper error responses for ownership violations in backend/src/api/task_router.py
- [X] T025 [US2] Test cross-user access prevention with different JWT tokens

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task State Management (Priority: P2)

**Goal**: Provide a dedicated endpoint to toggle the completion state of a user's tasks

**Independent Test**: An authenticated user can update the completion status of their tasks via the PATCH endpoint.

### Implementation for User Story 3

- [X] T026 [P] [US3] Add task completion toggle method to TaskService in backend/src/services/task_service.py
- [X] T027 [P] [US3] Implement task completion toggle endpoint in backend/src/api/task_router.py
- [X] T028 [US3] Connect PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/task_router.py
- [X] T029 [US3] Add completion status validation in backend/src/services/task_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T030 Create alembic migration files for Task and User models
- [X] T031 Add comprehensive error handling to backend services
- [X] T032 Implement proper HTTP status codes for all responses
- [X] T033 Add input validation and sanitization to all API endpoints
- [X] T034 Add logging to backend services
- [X] T035 Create health check endpoint in backend/src/api/main.py
- [X] T036 Add CORS configuration for frontend/backend communication
- [X] T037 Create README.md with setup and deployment instructions
- [X] T038 Run quickstart.md validation to ensure all steps work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 with ownership enforcement
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds upon US1 with completion toggle

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence