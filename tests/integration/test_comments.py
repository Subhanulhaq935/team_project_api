def test_create_comment_success(client):
    u = client.post("/api/v1/auth/register", json={
        "firstname": "Comment", "lastname": "User",
        "email": "commenter@example.com", "password": "Password123!"
    }).json()["user_id"]

    proj = client.post("/api/v1/projects", json={
        "name": "Comment Project", "user_id": u
    }).json()

    task = client.post(f"/api/v1/projects/{proj['id']}/tasks", json={
        "title": "Fix Bug", "description": "Details"
    }).json()

    response = client.post(
        f"/api/v1/projects/{proj['id']}/tasks/{task['id']}/comments?user_id={u}",
        json={"comment": "Working on this now"}
    )
    assert response.status_code == 201
    assert response.json()["comment"] == "Working on this now"


def test_create_comment_invalid_task_404(client):
    u = client.post("/api/v1/auth/register", json={
        "firstname": "User", "lastname": "Test",
        "email": "user404@example.com", "password": "Password123!"
    }).json()["user_id"]

    response = client.post(
        f"/api/v1/projects/1/tasks/99999/comments?user_id={u}",
        json={"comment": "No task"}
    )
    assert response.status_code == 404
