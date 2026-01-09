# Data Model: Backend REST API & Data Layer

## Task Entity
- **Fields**:
  - id: UUID (primary key)
  - title: String (required, max length 255)
  - description: String (optional)
  - is_completed: Boolean (default: false)
  - created_at: DateTime (required, auto-generated)
  - updated_at: DateTime (required, auto-generated)
  - user_id: UUID (foreign key to User, required for ownership)

- **Validation rules**:
  - Title must not be empty
  - Title must be less than 255 characters
  - User_id must reference an existing user
  - Users can only access tasks they own (enforced by user_id matching JWT)

- **State transitions**:
  - is_completed can transition from false to true (marking complete)
  - is_completed can transition from true to false (marking incomplete)

## User Entity (Referenced for ownership)
- **Fields**:
  - id: UUID (primary key)
  - email: String (unique, required)
  - created_at: DateTime (required)
  - updated_at: DateTime (required)

- **Validation rules**:
  - Email must be valid email format
  - Email must be unique across all users

- **Relationships**:
  - One-to-many with Task (user owns multiple tasks)

## JWT Token (Conceptual)
- **Components**:
  - Header: Algorithm and token type
  - Payload: User ID, expiration, issuer
  - Signature: Verified with shared secret

- **Validation rules**:
  - Must not be expired
  - Signature must match shared secret
  - User ID must exist in database