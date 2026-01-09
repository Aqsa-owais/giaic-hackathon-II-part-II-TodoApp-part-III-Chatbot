# API Contract: Authentication Endpoints

## Overview
Authentication endpoints are handled by Better Auth. These endpoints provide user registration, login, and session management.

## Endpoints

### Register User
- **URL**: `POST /api/auth/register`
- **Description**: Creates a new user account
- **Authentication**: None required
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required, min 8 chars)"
  }
  ```
- **Responses**:
  - `200`: User created successfully
  - `400`: Invalid input
  - `409`: User already exists

### Login User
- **URL**: `POST /api/auth/login`
- **Description**: Authenticates user and returns session
- **Authentication**: None required
- **Request Body**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Responses**:
  - `200`: Login successful, session created
  - `400`: Invalid input
  - `401`: Invalid credentials

### Logout User
- **URL**: `POST /api/auth/logout`
- **Description**: Ends the current user session
- **Authentication**: Session required
- **Request Body**: None
- **Responses**:
  - `200`: Logout successful
  - `401`: Not authenticated