# Data Model: Todo Full-Stack Web Application

## Entity Models

### User Entity
- **id**: String (UUID) - Primary key, unique identifier
- **email**: String - User's email address, unique, required
- **password**: String - Hashed password, required
- **created_at**: DateTime - Account creation timestamp
- **updated_at**: DateTime - Last update timestamp

### Task Entity
- **id**: String (UUID) - Primary key, unique identifier
- **title**: String - Task title, required, max length 255
- **description**: String - Task description, optional, max length 1000
- **completed**: Boolean - Completion status, default false
- **user_id**: String (UUID) - Foreign key to User, required for ownership
- **created_at**: DateTime - Task creation timestamp
- **updated_at**: DateTime - Last update timestamp

## Relationships

### User → Task (One-to-Many)
- One user can own many tasks
- Tasks are deleted when user is deleted (cascade delete)
- All API operations require user_id to match authenticated user

## Validation Rules

### User Validation
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (handled by Better Auth)

### Task Validation
- Title must be 1-255 characters
- Description can be 0-1000 characters
- User_id must reference an existing user
- Only the task owner can modify/delete the task

## State Transitions

### Task State Transitions
- `incomplete` → `completed` (via PATCH /tasks/{id}/complete with completed=true)
- `completed` → `incomplete` (via PATCH /tasks/{id}/complete with completed=false)

## Database Schema

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

## API Data Contracts

### Task Creation Request
```json
{
  "title": "string (required, 1-255 chars)",
  "description": "string (optional, 0-1000 chars)",
  "completed": "boolean (optional, default false)"
}
```

### Task Response
```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "string (UUID)",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

### Task Update Request
```json
{
  "title": "string (optional, 1-255 chars)",
  "description": "string (optional, 0-1000 chars)",
  "completed": "boolean (optional)"
}
```