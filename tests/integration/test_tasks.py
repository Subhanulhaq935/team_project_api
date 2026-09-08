def test_create_task_success(client, create_user):
    mgr = create_user("task_mgr@example.com", role="manager")

    proj_resp = client.post(
        "/api/v1/projects",
        json={"name": "Task Project", "status": "active"},
        headers=mgr["headers"]
    )
    proj = proj_resp.json()

    response = client.post(
        f"/api/v1/projects/{proj['id']}/tasks",
        json={
            "title": "Build Auth Flow",
            "description": "Implement JWT endpoints",
            "status": "pending",
            "priority": "high"
        },
        headers=mgr["headers"]
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Build Auth Flow"
    assert data["project_id"] == proj["id"]


def test_create_task_invalid_data(client, create_user):
    mgr = create_user("task_mgr2@example.com", role="manager")
    proj = client.post(
        "/api/v1/projects",
        json={"name": "Valid Project"},
        headers=mgr["headers"]
    ).json()

    response = client.post(
        f"/api/v1/projects/{proj['id']}/tasks",
        json={"title": "AB"},  # min length is 3
        headers=mgr["headers"]
    )
    assert response.status_code == 422


def test_get_task_not_found(client, create_user):
    admin = create_user("task_admin@example.com", role="admin")
    response = client.get(
        "/api/v1/projects/1/tasks/99999",
        headers=admin["headers"]
    )
    assert response.status_code == 404
