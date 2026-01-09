---
description: "Task list for Multi-User Todo Web Application implementation"
---

# Tasks: Multi-User Todo Web Application

**Input**: Design documents from `/specs/001-multi-user-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit test requirements in feature specification - tests are NOT included in this task list.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure with src/models/, src/services/, src/api/, src/middleware/
- [X] T002 Create frontend directory structure with src/components/, src/pages/, src/services/, src/utils/
- [X] T003 [P] Initialize backend with FastAPI, SQLModel, and Better Auth dependencies in requirements.txt
- [X] T004 [P] Initialize frontend with Next.js, React dependencies in package.json
- [X] T005 Create backend .env.example file with DATABASE_URL, BETTER_AUTH_SECRET, FRONTEND_URL variables
- [X] T006 Create frontend .env.local.example file with NEXT_PUBLIC_API_URL variable

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Setup database schema and migrations framework using SQLModel in backend/src/models/base.py
- [X] T008 [P] Create User model in backend/src/models/user.py with all required fields from data model
- [X] T009 [P] Create TodoTask model in backend/src/models/todo_task.py with all required fields from data model
- [X] T010 Setup JWT authentication framework using Better Auth in backend/src/api/main.py
- [X] T011 Create JWT verification middleware in backend/src/middleware/jwt_auth_middleware.py
- [X] T012 Create database configuration and connection utilities in backend/src/api/database.py
- [X] T013 Setup environment configuration management in backend/src/config.py
- [X] T014 Create base API router setup in backend/src/api/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with email and password

**Independent Test**: A new user can complete the registration process by providing required information and gain access to their personal todo space.

### Implementation for User Story 1

- [X] T015 [P] [US1] Create UserService in backend/src/services/user_service.py with user registration logic
- [X] T016 [P] [US1] Create AuthRouter in backend/src/api/auth_router.py with register endpoint
- [X] T017 [US1] Implement password hashing and validation in backend/src/services/user_service.py
- [X] T018 [US1] Connect auth router to main app in backend/src/api/main.py
- [X] T019 [P] [US1] Create Register page component in frontend/src/pages/register.tsx
- [X] T020 [P] [US1] Create API client service for auth in frontend/src/services/apiClient.ts
- [X] T021 [US1] Create authentication service in frontend/src/services/authService.ts
- [X] T022 [US1] Implement form validation and submission in frontend/src/pages/register.tsx
- [X] T023 [US1] Add registration success/error handling in frontend/src/pages/register.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Authentication (Priority: P1)

**Goal**: Allow existing users to sign in with credentials and be authenticated via JWT

**Independent Test**: An existing user can log in with their credentials and gain access to their personal todo space.

### Implementation for User Story 2

- [X] T024 [P] [US2] Add login endpoint to AuthRouter in backend/src/api/auth_router.py
- [X] T025 [P] [US2] Implement login authentication logic in backend/src/services/user_service.py
- [X] T026 [US2] Add JWT token generation for login in backend/src/services/user_service.py
- [X] T027 [P] [US2] Create Login page component in frontend/src/pages/login.tsx
- [X] T028 [US2] Implement login form and authentication flow in frontend/src/pages/login.tsx
- [X] T029 [US2] Add JWT token storage and retrieval in frontend/src/services/authService.ts
- [X] T030 [US2] Implement protected route handling in frontend/src/utils/types.ts
- [X] T031 [US2] Add login success/error handling in frontend/src/pages/login.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Todo Management (Priority: P1)

**Goal**: Allow authenticated users to create, read, update, delete, and mark tasks as complete, with all actions scoped to their own data

**Independent Test**: An authenticated user can perform all basic todo operations (CRUD + completion toggle) on their personal tasks.

### Implementation for User Story 3

- [X] T032 [P] [US3] Create TodoService in backend/src/services/todo_service.py with CRUD operations
- [X] T033 [P] [US3] Create TodoRouter in backend/src/api/todo_router.py with todo endpoints
- [X] T034 [US3] Implement user ownership validation in backend/src/services/todo_service.py
- [X] T035 [US3] Connect todo router to main app in backend/src/api/main.py
- [X] T036 [P] [US3] Create Todo API service in frontend/src/services/apiClient.ts
- [X] T037 [P] [US3] Create Todo components in frontend/src/components/Todo/
- [X] T038 [US3] Create Dashboard page in frontend/src/pages/dashboard.tsx
- [X] T039 [US3] Implement todo creation UI in frontend/src/components/Todo/
- [X] T040 [US3] Implement todo list display in frontend/src/components/Todo/
- [X] T041 [US3] Implement todo completion toggle in frontend/src/components/Todo/
- [X] T042 [US3] Implement todo deletion in frontend/src/components/Todo/
- [X] T043 [US3] Add user authentication context in frontend/src/utils/types.ts
- [X] T44 [US3] Implement error handling and loading states in frontend components

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 Create frontend Layout components in frontend/src/components/Layout/
- [X] T046 Add navigation between pages in frontend/src/components/Layout/
- [X] T047 Implement error boundaries and global error handling in frontend
- [X] T048 Add input validation and sanitization in backend API routes
- [X] T049 Create Alembic migration files for User and TodoTask models
- [X] T050 Add comprehensive logging to backend services
- [X] T051 Implement proper error responses with appropriate HTTP status codes
- [X] T052 Add CORS configuration for frontend/backend communication
- [X] T053 Create README.md with setup and deployment instructions
- [X] T054 Run quickstart.md validation to ensure all steps work correctly

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

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