def test_create_comment_success(client, create_user):
    mgr = create_user("comment_mgr@example.com", role="manager")

    proj = client.post(
        "/api/v1/projects",
        json={"name": "Comment Project"},
        headers=mgr["headers"]
    ).json()

    task = client.post(
        f"/api/v1/projects/{proj['id']}/tasks",
        json={"title": "Fix Bug", "description": "Details"},
        headers=mgr["headers"]
    ).json()

    response = client.post(
        f"/api/v1/projects/{proj['id']}/tasks/{task['id']}/comments",
        json={"comment": "Working on this now"},
        headers=mgr["headers"]
    )
    assert response.status_code == 201
    assert response.json()["comment"] == "Working on this now"


def test_create_comment_invalid_task_404(client, create_user):
    admin = create_user("comment_admin@example.com", role="admin")

    response = client.post(
        "/api/v1/projects/1/tasks/99999/comments",
        json={"comment": "No task"},
        headers=admin["headers"]
    )
    assert response.status_code == 404
