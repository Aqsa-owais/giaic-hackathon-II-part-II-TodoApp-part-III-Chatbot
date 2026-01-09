# Research: Todo Full-Stack Web Application

## Phase 0: Research and Clarification

### 1. Authentication System Research

**Decision**: Use Better Auth with JWT for authentication
**Rationale**: Better Auth provides a complete authentication solution that works well with Next.js and can generate JWTs that can be verified by the backend. It handles user registration, login, password reset, and session management.
**Alternatives considered**:
- NextAuth.js: Popular but doesn't have as strong backend integration story
- Auth0: More complex for this use case
- Custom JWT implementation: More work and security considerations

### 2. Database Connection Strategy

**Decision**: Use Neon Serverless PostgreSQL with SQLModel
**Rationale**: Neon provides serverless PostgreSQL with auto-scaling and smart caching. SQLModel is built on top of SQLAlchemy and Pydantic, providing type safety and validation.
**Alternatives considered**:
- SQLite: Simpler but less scalable
- MongoDB: Would require different ORM approach
- Supabase: Could work but Neon integrates better with the Python backend

### 3. API Communication Pattern

**Decision**: REST API with Bearer token authentication
**Rationale**: REST is well-understood, works well with FastAPI, and provides clear patterns for CRUD operations. JWT Bearer tokens provide stateless authentication.
**Alternatives considered**:
- GraphQL: More complex for this use case
- WebSocket: Not needed for basic CRUD operations

### 4. Frontend Architecture

**Decision**: Next.js 16+ with App Router
**Rationale**: App Router is the modern Next.js approach with better performance, nested routing, and improved data fetching. Works well with TypeScript.
**Alternatives considered**:
- Pages Router: Legacy approach
- React with Create React App: Would require more manual setup
- Other frameworks: Less suitable for full-stack with Python backend

### 5. Task Model Design

**Decision**: Task model with id, title, description, completed status, and user_id for ownership
**Rationale**: This matches the functional requirements for a todo app while including user_id for proper data isolation.
**Fields**:
- id: Primary key, auto-generated
- title: String, required
- description: String, optional
- completed: Boolean, default false
- user_id: Foreign key to user, required for ownership

### 6. JWT Token Structure

**Decision**: JWT with user id and email claims
**Rationale**: Provides necessary information for backend verification while keeping tokens lightweight.
**Claims**:
- sub: user id (for identification)
- email: user email (for reference)
- iat: issued at time
- exp: expiration time (7 days)

### 7. Error Handling Strategy

**Decision**: Consistent HTTP status codes with meaningful error messages
**Rationale**: Standard approach that's well-understood by developers and provides clear feedback to users.
**Status codes**:
- 200: Success for GET/PUT/PATCH
- 201: Created for POST
- 401: Unauthorized (missing/invalid JWT)
- 403: Forbidden (user not authorized for resource)
- 404: Not found (resource doesn't exist)
- 422: Validation error (invalid input)

### 8. Environment Configuration

**Decision**: Use environment variables for all secrets and configuration
**Rationale**: Standard security practice to keep sensitive information out of code.
**Variables needed**:
- BETTER_AUTH_SECRET: JWT signing secret
- DATABASE_URL: PostgreSQL connection string
- NEXT_PUBLIC_API_URL: Backend API URL for frontend
- FRONTEND_URL: Allowed origin for CORS

### 9. Frontend API Client

**Decision**: Create a centralized API client that automatically attaches JWT
**Rationale**: Ensures consistent authentication across all API calls and centralizes error handling.
**Implementation**: Axios or fetch with interceptors to add Authorization header

### 10. UI State Management

**Decision**: Use React state management for UI state, API calls for persistence
**Rationale**: Simple approach that works well with Next.js data fetching patterns.
**Approach**: useState/useReducer for local state, SWR or React Query for server state