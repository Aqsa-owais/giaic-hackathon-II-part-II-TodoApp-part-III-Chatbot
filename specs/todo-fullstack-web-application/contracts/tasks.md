# API Contract: Task Management Endpoints

## Overview
Task management endpoints provide CRUD operations for user tasks. All endpoints require JWT authentication in the Authorization header.

## Common Headers
- `Authorization: Bearer {jwt_token}` - Required for all endpoints

## Common Responses
- `401`: Unauthorized (missing or invalid JWT)
- `403`: Forbidden (user not authorized for resource)
- `404`: Not found (resource doesn't exist)

## Endpoints

### Get All Tasks
- **URL**: `GET /api/tasks`
- **Description**: Retrieve all tasks for the authenticated user
- **Authentication**: JWT required
- **Query Parameters**: None
- **Request Body**: None
- **Responses**:
  - `200`: Success
    ```json
    {
      "tasks": [
        {
          "id": "string (UUID)",
          "title": "string",
          "description": "string",
          "completed": "boolean",
          "user_id": "string (UUID)",
          "created_at": "ISO 8601 datetime",
          "updated_at": "ISO 8601 datetime"
        }
      ]
    }
    ```

### Create Task
- **URL**: `POST /api/tasks`
- **Description**: Create a new task for the authenticated user
- **Authentication**: JWT required
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-255 chars)",
    "description": "string (optional, 0-1000 chars)",
    "completed": "boolean (optional, default false)"
  }
  ```
- **Responses**:
  - `201`: Task created successfully
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
  - `400`: Invalid input
  - `422`: Validation error

### Get Task
- **URL**: `GET /api/tasks/{task_id}`
- **Description**: Retrieve a specific task for the authenticated user
- **Authentication**: JWT required
- **Path Parameters**:
  - `task_id`: string (UUID) - Task identifier
- **Request Body**: None
- **Responses**:
  - `200`: Success
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
  - `404`: Task not found

### Update Task
- **URL**: `PUT /api/tasks/{task_id}`
- **Description**: Update a specific task for the authenticated user
- **Authentication**: JWT required
- **Path Parameters**:
  - `task_id`: string (UUID) - Task identifier
- **Request Body**:
  ```json
  {
    "title": "string (required, 1-255 chars)",
    "description": "string (optional, 0-1000 chars)",
    "completed": "boolean (required)"
  }
  ```
- **Responses**:
  - `200`: Task updated successfully
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
  - `400`: Invalid input
  - `404`: Task not found
  - `422`: Validation error

### Toggle Task Completion
- **URL**: `PATCH /api/tasks/{task_id}/complete`
- **Description**: Toggle the completion status of a task
- **Authentication**: JWT required
- **Path Parameters**:
  - `task_id`: string (UUID) - Task identifier
- **Request Body**:
  ```json
  {
    "completed": "boolean (required)"
  }
  ```
- **Responses**:
  - `200`: Task updated successfully
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
  - `400`: Invalid input
  - `404`: Task not found

### Delete Task
- **URL**: `DELETE /api/tasks/{task_id}`
- **Description**: Delete a specific task for the authenticated user
- **Authentication**: JWT required
- **Path Parameters**:
  - `task_id`: string (UUID) - Task identifier
- **Request Body**: None
- **Responses**:
  - `204`: Task deleted successfully
  - `404`: Task not found