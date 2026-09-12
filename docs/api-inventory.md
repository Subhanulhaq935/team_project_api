# 📋 API Inventory & Endpoint Catalog

**API Version:** `v1`  
**Base URL:** `/api/v1`  
**Authentication Header:** `Authorization: Bearer <JWT_ACCESS_TOKEN>`  
**Interactive Documentation:** `/docs` (Swagger UI), `/redoc` (ReDoc)  

---

## 📑 Endpoint Inventory Table

| Tag / Resource | Method | Path | Summary / Description | Auth Required | Required Role / Scope |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Health** | `GET` | `/health` | Basic application heartbeat | ❌ Public | None |
| **Health** | `GET` | `/health/live` | Process liveness probe | ❌ Public | None |
| **Health** | `GET` | `/health/ready` | Database connection readiness probe | ❌ Public | None |
| **Health** | `GET` | `/api/v1/version` | Current release version, environment, & commit SHA | ❌ Public | None |
| **Authentication** | `POST` | `/api/v1/auth/register` | Register a new user account | ❌ Public | None |
| **Authentication** | `POST` | `/api/v1/auth/login` | Authenticate user & issue access/refresh token pair | ❌ Public | None |
| **Authentication** | `GET` | `/api/v1/auth/me` | Fetch authenticated user's profile | ✅ Bearer | Authenticated User |
| **Authentication** | `POST` | `/api/v1/auth/refresh` | Rotate and issue a new token pair | ❌ Public (Token Body) | Valid Refresh Token |
| **Authentication** | `POST` | `/api/v1/auth/logout` | Invalidate and revoke an active refresh token | ❌ Public (Token Body) | Valid Refresh Token |
| **Projects** | `GET` | `/api/v1/projects` | List all projects | ✅ Bearer | `admin`, `manager` |
| **Projects** | `POST` | `/api/v1/projects` | Create a new project (creator becomes `PROJECT_MANAGER`) | ✅ Bearer | `admin`, `manager` |
| **Projects** | `GET` | `/api/v1/projects/{project_id}` | Retrieve project details | ✅ Bearer | Assigned Member or `admin` |
| **Projects** | `PATCH` | `/api/v1/projects/{project_id}` | Update project details | ✅ Bearer | `PROJECT_MANAGER` or `admin` |
| **Projects** | `DELETE` | `/api/v1/projects/{project_id}` | Delete project | ✅ Bearer | `admin` only |
| **Project Summary** | `GET` | `/api/v1/projects/{project_id}/summary` | Aggregate project analytics (counts, tasks, comments) | ✅ Bearer | Assigned Member or `admin` |
| **Project Members** | `GET` | `/api/v1/projects/{project_id}/members` | List members of a project | ✅ Bearer | Assigned Member or `admin` |
| **Project Members** | `POST` | `/api/v1/projects/{project_id}/members` | Assign a user to project with role (`MEMBER`, `PROJECT_MANAGER`) | ✅ Bearer | `PROJECT_MANAGER` or `admin` |
| **Project Members** | `DELETE` | `/api/v1/projects/{project_id}/members/{user_id}` | Remove user from project | ✅ Bearer | `PROJECT_MANAGER` or `admin` |
| **Tasks** | `GET` | `/api/v1/projects/{project_id}/tasks` | Paginated, filtered, searchable, and sorted project tasks | ✅ Bearer | Assigned Member or `admin` |
| **Tasks** | `POST` | `/api/v1/projects/{project_id}/tasks` | Create task inside project (with priority and assignee) | ✅ Bearer | Assigned Member or `admin` |
| **Tasks** | `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}` | Retrieve specific task details | ✅ Bearer | Assigned Member or `admin` |
| **Comments** | `GET` | `/api/v1/projects/{project_id}/tasks/{task_id}/comments` | List all comments on a task | ✅ Bearer | Assigned Member or `admin` |
| **Comments** | `POST` | `/api/v1/projects/{project_id}/tasks/{task_id}/comments` | Post a comment on a task (authenticated user is author) | ✅ Bearer | Assigned Member or `admin` |

---

## 🔍 Detailed Route Specifications

### 1. Authentication Endpoints

#### `POST /api/v1/auth/register`
* **Status:** `201 Created`
* **Request Body:**
  ```json
  {
    "firstname": "John",
    "lastname": "Doe",
    "email": "johndoe@example.com",
    "password": "SecurePassword123!"
  }
  ```
* **Response Body:**
  ```json
  {
    "message": "User registered successfully",
    "user_id": 1
  }
  ```

#### `POST /api/v1/auth/login`
* **Status:** `200 OK`
* **Request Body:**
  ```json
  {
    "email": "johndoe@example.com",
    "password": "SecurePassword123!"
  }
  ```
* **Response Body:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "8g7df6a8s7d6f8a...",
    "token_type": "bearer"
  }
  ```

#### `POST /api/v1/auth/refresh`
* **Status:** `200 OK`
* **Request Body:**
  ```json
  {
    "refresh_token": "8g7df6a8s7d6f8a..."
  }
  ```
* **Response Body:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "new_rotated_refresh_token...",
    "token_type": "bearer"
  }
  ```

---

### 2. Projects & Tasks Endpoints

#### `GET /api/v1/projects/{project_id}/tasks`
* **Status:** `200 OK`
* **Query Parameters:**
  | Parameter | Type | Default | Constraints / Allowed Values | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `page` | `int` | `1` | `>= 1` | Page number |
  | `page_size` | `int` | `20` | `1` to `100` | Number of items per page |
  | `status` | `string` | `None` | e.g. `pending`, `in_progress`, `completed` | Filter by task status |
  | `priority` | `string` | `None` | `low`, `medium`, `high`, `urgent` | Filter by task priority |
  | `assigned_to` | `int` | `None` | User ID | Filter by assigned user |
  | `search` | `string` | `None` | `max_length: 100` | Search query across title & description |
  | `sort_by` | `string` | `created_at` | `created_at`, `due_date`, `priority`, `status`, `title`, `id` | Whitelisted sort column |
  | `sort_order` | `string` | `desc` | `asc`, `desc` | Sorting direction |
* **Response Body (`PaginatedResponse[TaskResponse]`):**
  ```json
  {
    "items": [
      {
        "id": 10,
        "project_id": 1,
        "title": "Design Database Schema",
        "description": "ERD diagram and schema migrations",
        "status": "in_progress",
        "priority": "high",
        "assigned_to_user_id": 3,
        "due_date": "2026-09-20T12:00:00",
        "created_at": "2026-09-12T10:00:00",
        "updated_at": "2026-09-12T10:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20,
    "total_pages": 1
  }
  ```

#### `GET /api/v1/projects/{project_id}/summary`
* **Status:** `200 OK`
* **Response Body:**
  ```json
  {
    "project_id": 1,
    "project_name": "Cloud Migration",
    "total_members": 3,
    "total_tasks": 5,
    "tasks_by_status": {
      "completed": 2,
      "in_progress": 2,
      "pending": 1
    },
    "total_comments": 8
  }
  ```

---

## 🚨 Error Envelope Standard

All application errors return a structured JSON response with tracing context:

```json
{
  "error": {
    "code": "INSUFFICIENT_PERMISSIONS",
    "message": "You are not a member of this project",
    "details": null,
    "request_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"
  }
}
```

### Common HTTP Status Codes:
* `400 Bad Request`: Validation failure or invalid query parameter.
* `401 Unauthorized`: Missing, expired, or malformed JWT access token.
* `403 Forbidden`: Insufficient role or unauthorized project access (BOLA/BFLA protection).
* `404 Not Found`: Project, Task, or Member resource does not exist.
* `422 Unprocessable Entity`: Request body failed Pydantic schema validation.
* `429 Too Many Requests`: Rate limit threshold exceeded.
* `500 Internal Server Error`: Sanitized server error (internal details logged securely with Request ID).
