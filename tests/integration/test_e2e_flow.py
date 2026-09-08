def test_full_end_to_end_workflow(client, create_user):
    """
    E2E Test Flow:
    1. Create Manager & Developer
    2. Verify /me endpoint
    3. Create Project
    4. Add Member to Project
    5. Create Task in Project
    6. Add Comment to Task
    7. Get Project Summary & Metrics
    """
    # 1. Create Manager & Developer
    mgr = create_user("alice.manager@example.com", role="manager", firstname="Alice", lastname="Manager")
    dev = create_user("bob.dev@example.com", role="user", firstname="Bob", lastname="Developer")

    mgr_headers = mgr["headers"]

    # 2. Verify /me endpoint
    me_resp = client.get("/api/v1/auth/me", headers=mgr_headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "alice.manager@example.com"

    # 3. Create Project
    proj_resp = client.post(
        "/api/v1/projects",
        json={
            "name": "Mobile Banking App",
            "description": "Next-gen banking application",
            "status": "active"
        },
        headers=mgr_headers
    )
    assert proj_resp.status_code == 201
    project_id = proj_resp.json()["id"]

    # 4. Add Member
    member_resp = client.post(
        f"/api/v1/projects/{project_id}/members",
        json={
            "user_id": dev["id"],
            "project_role": "DEVELOPER"
        },
        headers=mgr_headers
    )
    assert member_resp.status_code == 201
    assert member_resp.json()["user_id"] == dev["id"]

    # 5. Create Task
    task_resp = client.post(
        f"/api/v1/projects/{project_id}/tasks",
        json={
            "title": "Setup OAuth2",
            "description": "Implement Google login",
            "status": "pending",
            "priority": "high",
            "assigned_to_user_id": dev["id"]
        },
        headers=mgr_headers
    )
    assert task_resp.status_code == 201
    task_id = task_resp.json()["id"]

    # 6. Add Comment
    comment_resp = client.post(
        f"/api/v1/projects/{project_id}/tasks/{task_id}/comments",
        json={"comment": "OAuth integration completed, PR submitted."},
        headers=mgr_headers
    )
    assert comment_resp.status_code == 201
    assert comment_resp.json()["task_id"] == task_id

    # 7. Get Project Summary & Verify Stats
    summary_resp = client.get(
        f"/api/v1/projects/{project_id}/summary",
        headers=mgr_headers
    )
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    assert "statistics" in summary
    stats = summary["statistics"]
    assert stats["total_tasks"] == 1
    assert stats["total_members"] == 2  # Owner + Developer
    assert stats["total_comments"] == 1
