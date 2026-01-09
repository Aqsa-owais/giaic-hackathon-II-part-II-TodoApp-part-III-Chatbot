# Data Model: Multi-User Todo Web Application

## User Entity
- **Fields**:
  - id: UUID (primary key)
  - email: String (unique, required)
  - password_hash: String (required)
  - created_at: DateTime (required)
  - updated_at: DateTime (required)
  - is_active: Boolean (default: true)

- **Validation rules**:
  - Email must be valid email format
  - Password must meet security requirements (length, complexity)
  - Email must be unique across all users

- **Relationships**:
  - One-to-many with TodoTask (user owns multiple tasks)

## TodoTask Entity
- **Fields**:
  - id: UUID (primary key)
  - title: String (required)
  - description: String (optional)
  - is_completed: Boolean (default: false)
  - created_at: DateTime (required)
  - updated_at: DateTime (required)
  - user_id: UUID (foreign key to User, required)

- **Validation rules**:
  - Title must not be empty
  - User_id must reference an existing user
  - Users can only access tasks they own

- **State transitions**:
  - is_completed can transition from false to true (marking complete)
  - is_completed can transition from true to false (marking incomplete)

## JWT Token (Conceptual)
- **Components**:
  - Header: Algorithm and token type
  - Payload: User ID, expiration, issuer
  - Signature: Verified with shared secret

- **Validation rules**:
  - Must not be expired
  - Signature must match shared secret
  - User ID must exist in database

## Authentication Session (Conceptual)
- **Components**:
  - Token validity period
  - User identity verification
  - Access permissions validation

- **Validation rules**:
  - Session must be active
  - User must exist and be active
  - Token must be valid and unexpired