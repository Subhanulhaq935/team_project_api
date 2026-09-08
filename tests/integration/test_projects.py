def test_create_project_success(client, create_user):
    mgr = create_user("alex.mgr@example.com", role="manager")

    response = client.post(
        "/api/v1/projects",
        json={
            "name": "E-Commerce App",
            "description": "API backend for shop",
            "status": "active"
        },
        headers=mgr["headers"]
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "E-Commerce App"
    assert "id" in data


def test_create_project_invalid_data(client, create_user):
    mgr = create_user("alex_invalid@example.com", role="manager")
    # Missing required name
    response = client.post(
        "/api/v1/projects",
        json={"description": "Missing required fields"},
        headers=mgr["headers"]
    )
    assert response.status_code == 422


def test_get_project_unauthorized(client):
    # Access without Bearer token
    response = client.get("/api/v1/projects/999")
    assert response.status_code == 401


def test_get_projects_list_forbidden_for_regular_user(client, create_user):
    normal_user = create_user("normal@example.com", role="user")

    # Regular users cannot list all projects (requires admin/manager)
    response = client.get(
        "/api/v1/projects",
        headers=normal_user["headers"]
    )
    assert response.status_code == 403


def test_update_project_not_found(client, create_user):
    admin = create_user("admin_update@example.com", role="admin")
    response = client.patch(
        "/api/v1/projects/99999",
        json={"name": "Updated Name"},
        headers=admin["headers"]
    )
    assert response.status_code == 404
