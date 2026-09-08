# 📋 API Inventory & Endpoint Catalog

**API Version:** `v1`  
**Base URL:** `/api/v1`  
**Authentication Scheme:** `Bearer <JWT_ACCESS_TOKEN>`  
**Last Updated:** Day 14 Security Milestone

---

## 1. Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required | Request Body | Response Status | Rate Limit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register new user | ❌ Public | `RegisterRequest` | `201 Created` | 5 req / min |
| `POST` | `/api/v1/auth/login` | Authenticate & get tokens | ❌ Public | `LoginRequest` | `200 OK` | 5 req / min |
| `POST` | `/api/v1/auth/refresh` | Rotate access & refresh tokens | ❌ Public (Token in body) | `RefreshTokenRequest` | `200 OK` | 10 req / min |
| `POST` | `/api/v1/auth/logout` | Invalidate active refresh token | ❌ Public (Token in body) | `RefreshTokenRequest` | `200 OK` | 10 req / min |
| `GET` | `/api/v1/auth/me` | Fetch profile of current user | ✅ Bearer JWT | None | `200 OK` | 60 req / min |

---

## 2. Projects (`/api/v1/projects`)

| Method | Endpoint | Description | Auth & Roles Required | Request Body | Response Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects` | List all projects | ✅ `ADMIN`, `MANAGER` | None | `200 OK` |
| `POST` | `/api/v1/projects` | Create a new project | ✅ `ADMIN`, `MANAGER` | `ProjectCreate` | `201 Created` |
| `GET` | `/api/v1/projects/{id}` | Get project details | ✅ `ADMIN` or Assigned Project Member | None | `200 OK` |
| `PATCH` | `/api/v1/projects/{id}` | Update project info | ✅ `ADMIN` or `PROJECT_MANAGER` | `ProjectUpdate` | `200 OK` |
| `DELETE` | `/api/v1/projects/{id}` | Delete a project | ✅ `ADMIN` only | None | `204 No Content` |
| `GET` | `/api/v1/projects/{id}/summary` | Get project analytics & stats | ✅ `ADMIN` or Assigned Project Member | None | `200 OK` |

---

## 3. Project Members (`/api/v1/projects/{project_id}/members`)

| Method | Endpoint | Description | Auth & Roles Required | Request Body | Response Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects/{id}/members` | List members of project | ✅ Assigned Member / Admin | None | `200 OK` |
| `POST` | `/api/v1/projects/{id}/members` | Add member to project | ✅ `ADMIN` or `PROJECT_MANAGER` | `ProjectMemberCreate` | `201 Created` |
| `DELETE` | `/api/v1/projects/{id}/members/{user_id}` | Remove member from project | ✅ `ADMIN` or `PROJECT_MANAGER` | None | `204 No Content` |

---

## 4. Tasks (`/api/v1/projects/{project_id}/tasks`)

| Method | Endpoint | Description | Query Parameters | Response Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects/{id}/tasks` | Paginated tasks list | `page`, `page_size`, `status`, `priority`, `assigned_to`, `search`, `sort_by`, `sort_order` | `200 OK` |
| `POST` | `/api/v1/projects/{id}/tasks` | Create task in project | None (`TaskCreate` body) | `201 Created` |
| `GET` | `/api/v1/projects/{id}/tasks/{task_id}` | Get task by ID | None | `200 OK` |

---

## 5. Comments (`/api/v1/projects/{project_id}/tasks/{task_id}/comments`)

| Method | Endpoint | Description | Request Body | Response Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects/{p_id}/tasks/{t_id}/comments` | List comments for task | None | `200 OK` |
| `POST` | `/api/v1/projects/{p_id}/tasks/{t_id}/comments` | Add comment to task | `CommentCreate` | `201 Created` |

---

## 6. System & Health

| Method | Endpoint | Description | Auth Required | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/health` | Uptime check & service heartbeat | ❌ None | `{"status": "ok"}` |
| `GET` | `/docs` | Interactive Swagger UI (Dev only) | ❌ Public in Dev | HTML / OpenAPI |
| `GET` | `/redoc` | ReDoc OpenAPI documentation | ❌ Public in Dev | HTML / OpenAPI |
| `GET` | `/openapi.json` | OpenAPI schema specification | ❌ Public in Dev | JSON Schema |
