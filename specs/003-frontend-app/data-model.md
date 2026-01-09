# Data Model: Frontend Application & User Experience

## User Session Entity
- **Fields**:
  - id: String (user identifier from JWT)
  - email: String (user's email address)
  - token: String (JWT access token)
  - expires_at: DateTime (token expiration timestamp)
  - is_authenticated: Boolean (whether session is currently valid)

- **Validation rules**:
  - Token must be valid JWT format
  - Session must not be expired
  - Email must be valid email format

- **State transitions**:
  - is_authenticated can transition from false to true (after successful login)
  - is_authenticated can transition from true to false (after logout or token expiry)

## Task Entity (as represented in frontend state)
- **Fields**:
  - id: String (UUID from backend)
  - title: String (task title, required, max length 255)
  - description: String (optional task description)
  - is_completed: Boolean (completion status, default: false)
  - created_at: DateTime (timestamp from backend)
  - updated_at: DateTime (timestamp from backend)
  - user_id: String (owner reference from backend)

- **Validation rules**:
  - Title must not be empty
  - Title must be less than 255 characters
  - User_id must match authenticated user (enforced by backend)

- **State transitions**:
  - is_completed can transition from false to true (marking complete)
  - is_completed can transition from true to false (marking incomplete)

## API Response Entity
- **Fields**:
  - status: String (HTTP status, e.g., "success", "error")
  - data: Object (response payload)
  - message: String (optional message for user)
  - error_code: String (optional error code)

- **Validation rules**:
  - Status must be either "success" or "error"
  - Data must be present when status is "success"
  - Error code and message should be present when status is "error"

## Protected Route Entity (Conceptual)
- **Components**:
  - Route path: String (the path that requires authentication)
  - Required permissions: Array (permissions needed to access route)
  - Redirect path: String (where to redirect if not authenticated)

- **Validation rules**:
  - Route must require valid authentication token
  - User must have necessary permissions to access route
  - Must redirect to login if not authenticated