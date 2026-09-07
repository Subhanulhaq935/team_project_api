def test_create_task_success(client):
    u = client.post("/api/v1/auth/register", json={
        "firstname": "Task", "lastname": "Creator",
        "email": "taskuser@example.com", "password": "Password123!"
    }).json()["user_id"]

    proj = client.post("/api/v1/projects", json={
        "name": "Task Project", "user_id": u
    }).json()

    response = client.post(f"/api/v1/projects/{proj['id']}/tasks", json={
        "title": "Build Auth Flow",
        "description": "Implement JWT endpoints",
        "status": "pending",
        "priority": "high"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Build Auth Flow"
    assert data["project_id"] == proj["id"]


def test_create_task_invalid_data(client):
    response = client.post("/api/v1/projects/1/tasks", json={
        "title": "AB"  # min length is 3
    })
    assert response.status_code == 422


def test_get_task_not_found(client):
    response = client.get("/api/v1/projects/1/tasks/99999")
    assert response.status_code == 404
