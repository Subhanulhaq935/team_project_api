def test_create_project_success(client):
    # Register user to own the project
    reg_resp = client.post("/api/v1/auth/register", json={
        "firstname": "Alex",
        "lastname": "Admin",
        "email": "alex@example.com",
        "password": "Password123!"
    })
    user_id = reg_resp.json()["user_id"]

    response = client.post("/api/v1/projects", json={
        "name": "E-Commerce App",
        "description": "API backend for shop",
        "status": "active",
        "user_id": user_id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "E-Commerce App"
    assert "id" in data


def test_create_project_invalid_data(client):
    # Missing required name & user_id
    response = client.post("/api/v1/projects", json={
        "description": "Missing required fields"
    })
    assert response.status_code == 422


def test_get_project_unauthorized(client):
    # Access without Bearer token
    response = client.get("/api/v1/projects/999")
    assert response.status_code == 401


def test_get_projects_list_forbidden_for_regular_user(client):
    # Register & Login normal user (default role is 'user')
    client.post("/api/v1/auth/register", json={
        "firstname": "Normal",
        "lastname": "User",
        "email": "normal@example.com",
        "password": "Password123!"
    })
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "normal@example.com",
        "password": "Password123!"
    })
    token = login_resp.json()["access_token"]

    # Regular users cannot list all projects (requires admin/manager)
    response = client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_update_project_not_found(client):
    response = client.patch("/api/v1/projects/99999", json={
        "name": "Updated Name"
    })
    assert response.status_code == 404
