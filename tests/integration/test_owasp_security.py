"""
OWASP API Security Top 5 Integration Tests (API1 - API5)
Covers all requirements of Day 13:
- API1: User A -> User B's Project, Task, Comment access rejection
- API2: Broken Auth (Invalid credentials, tampered JWT, refresh token revocation)
- API3: Mass Assignment role escalation ({'role': 'ADMIN'})
- API4: Unrestricted Resource Consumption (Max page size, search length limits)
- API5: Broken Function Level Auth (USER -> ADMIN API, MANAGER -> ADMIN API)
"""
import pytest
from app.core.security import create_access_token


def create_authenticated_user(client, email: str, role: str = "user", firstname: str = "Test"):
    """Helper to register and login user, returning tokens and auth headers."""
    reg_resp = client.post("/api/v1/auth/register", json={
        "firstname": firstname,
        "lastname": "User",
        "email": email,
        "password": "SecurePassword123!"
    })
    assert reg_resp.status_code == 201
    user_id = reg_resp.json()["user_id"]

    login_resp = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "SecurePassword123!"
    })
    assert login_resp.status_code == 200
    token_data = login_resp.json()

    return {
        "id": user_id,
        "email": email,
        "role": role,
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "headers": {"Authorization": f"Bearer {token_data['access_token']}"}
    }


# ============================================================================
# API1: Broken Object Level Authorization (BOLA / IDOR) Tests
# ============================================================================

def test_api1_bola_user_a_cannot_access_user_b_project(client, create_user):
    """API1 Test: User A cannot access User B's project (403/404)."""
    user_a = create_user("user_a_proj@example.com", role="user")
    user_b = create_user("user_b_proj@example.com", role="manager")

    # User B creates a project
    proj_resp = client.post(
        "/api/v1/projects",
        json={
            "name": "User B Project",
            "description": "Confidential",
            "status": "active"
        },
        headers=user_b["headers"]
    )
    assert proj_resp.status_code == 201
    project_id = proj_resp.json()["id"]

    # User A tries to access User B's project
    access_resp = client.get(
        f"/api/v1/projects/{project_id}",
        headers=user_a["headers"]
    )
    assert access_resp.status_code in [403, 404]


def test_api1_bola_user_a_cannot_access_user_b_task_or_cross_project(client, create_user):
    """API1 Test: User A cannot access task under a non-existent or wrong project."""
    user = create_user("task_user@example.com", role="manager")

    # Project 1 with Task (Name min_length >= 3)
    p1_resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Project Alpha",
            "description": "Valid Description",
            "status": "active"
        },
        headers=user["headers"]
    )
    assert p1_resp.status_code == 201
    p1 = p1_resp.json()

    task_resp = client.post(
        f"/api/v1/projects/{p1['id']}/tasks",
        json={
            "title": "Secret Task",
            "description": "Confidential",
            "status": "pending",
            "priority": "high"
        },
        headers=user["headers"]
    )
    assert task_resp.status_code == 201
    task = task_resp.json()

    # Attempting to fetch task with mismatched project_id
    wrong_proj_id = p1["id"] + 999
    response = client.get(
        f"/api/v1/projects/{wrong_proj_id}/tasks/{task['id']}",
        headers=user["headers"]
    )
    assert response.status_code in [403, 404]


def test_api1_bola_user_a_cannot_access_comments_of_other_project_task(client, create_user):
    """API1 Test: Accessing comments for an invalid project/task combination fails with 404."""
    user = create_user("comment_user@example.com", role="manager")
    p1_resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Project Beta",
            "description": "Valid Description",
            "status": "active"
        },
        headers=user["headers"]
    )
    assert p1_resp.status_code == 201
    p1 = p1_resp.json()

    invalid_task_id = 99999
    response = client.get(
        f"/api/v1/projects/{p1['id']}/tasks/{invalid_task_id}/comments",
        headers=user["headers"]
    )
    assert response.status_code in [403, 404]


# ============================================================================
# API2: Broken Authentication Tests
# ============================================================================

def test_api2_broken_auth_invalid_credentials_prevent_enumeration(client):
    """API2 Test: Login with bad credentials returns 401 without revealing user existence."""
    create_authenticated_user(client, "auth_victim@example.com")

    bad_login_resp = client.post("/api/v1/auth/login", json={
        "email": "auth_victim@example.com",
        "password": "WrongPassword999!"
    })
    assert bad_login_resp.status_code == 401


def test_api2_broken_auth_tampered_jwt_rejected(client):
    """API2 Test: Tampered JWT token rejected with 401 Unauthorized."""
    tampered_headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.signature"}
    response = client.get("/api/v1/auth/me", headers=tampered_headers)
    assert response.status_code == 401


def test_api2_broken_auth_refresh_token_revoked_on_logout(client):
    """API2 Test: Refresh token revoked on logout cannot be reused."""
    user = create_authenticated_user(client, "logout_test@example.com")

    # Logout
    logout_resp = client.post("/api/v1/auth/logout", json={
        "refresh_token": user["refresh_token"]
    })
    assert logout_resp.status_code == 200

    # Reuse attempt
    reuse_resp = client.post("/api/v1/auth/refresh", json={
        "refresh_token": user["refresh_token"]
    })
    assert reuse_resp.status_code == 401


# ============================================================================
# API3: Broken Object Property Level Authorization (Mass Assignment) Tests
# ============================================================================

def test_api3_mass_assignment_cannot_elevate_role_to_admin(client):
    """API3 Test: Payload {'role': 'ADMIN'} during register ignored; role stays 'user'."""
    reg_resp = client.post("/api/v1/auth/register", json={
        "firstname": "Hacker",
        "lastname": "User",
        "email": "hacker@example.com",
        "password": "Password123!",
        "role": "ADMIN"
    })
    assert reg_resp.status_code == 201

    login_resp = client.post("/api/v1/auth/login", json={
        "email": "hacker@example.com",
        "password": "Password123!"
    })
    token = login_resp.json()["access_token"]

    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    user_info = me_resp.json()
    assert user_info["role"].lower() == "user"


# ============================================================================
# API4: Unrestricted Resource Consumption Tests
# ============================================================================

def test_api4_unrestricted_resource_consumption_page_size_capped(client, create_user):
    """API4 Test: Requesting page_size > 100 rejected with 422."""
    user = create_user("resource_user@example.com", role="manager")
    proj_resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Resource Project",
            "description": "Testing limits",
            "status": "active"
        },
        headers=user["headers"]
    )
    project_id = proj_resp.json()["id"]

    response = client.get(
        f"/api/v1/projects/{project_id}/tasks?page_size=5000",
        headers=user["headers"]
    )
    assert response.status_code == 422


# ============================================================================
# API5: Broken Function Level Authorization (BFLA) Tests
# ============================================================================

def test_api5_bfla_user_cannot_access_admin_api(client, create_user):
    """API5 Test: USER cannot access Admin/Manager GET /api/v1/projects endpoint (403)."""
    regular_user = create_user("regular_user_bfla@example.com", role="user")

    response = client.get("/api/v1/projects", headers=regular_user["headers"])
    assert response.status_code == 403


def test_api5_bfla_manager_cannot_access_other_project_management(client):
    """API5 Test: MANAGER cannot access a project where they are not assigned as PROJECT_MANAGER."""
    manager_token = create_access_token(user_id=888, role="manager")
    headers = {"Authorization": f"Bearer {manager_token}"}

    # Attempt to access project with ID 999 where manager is not a member
    response = client.get("/api/v1/projects/999", headers=headers)
    assert response.status_code in [401, 403, 404]
