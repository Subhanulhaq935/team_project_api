def test_full_end_to_end_workflow(client):
    """
    E2E Test Flow:
    1. Register User & Manager
    2. Login to obtain JWT Token
    3. Create Project
    4. Add Member to Project
    5. Create Task in Project
    6. Add Comment to Task
    7. Get Project Summary & Metrics
    """
    # 1. Register Admin/Manager & Developer
    reg_mgr = client.post("/api/v1/auth/register", json={
        "firstname": "Alice",
        "lastname": "Manager",
        "email": "alice.manager@example.com",
        "password": "SecurePassword123!"
    })
    assert reg_mgr.status_code == 201
    mgr_id = reg_mgr.json()["user_id"]

    reg_dev = client.post("/api/v1/auth/register", json={
        "firstname": "Bob",
        "lastname": "Developer",
        "email": "bob.dev@example.com",
        "password": "SecurePassword123!"
    })
    assert reg_dev.status_code == 201
    dev_id = reg_dev.json()["user_id"]

    # 2. Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "alice.manager@example.com",
        "password": "SecurePassword123!"
    })
    assert login_resp.status_code == 200
    access_token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Verify /me endpoint
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "alice.manager@example.com"

    # 3. Create Project
    proj_resp = client.post("/api/v1/projects", json={
        "name": "Mobile Banking App",
        "description": "Next-gen banking application",
        "status": "active",
        "user_id": mgr_id
    })
    assert proj_resp.status_code == 201
    project_id = proj_resp.json()["id"]

    # 4. Add Member
    member_resp = client.post(f"/api/v1/projects/{project_id}/members", json={
        "user_id": dev_id,
        "project_role": "DEVELOPER"
    })
    assert member_resp.status_code == 201
    assert member_resp.json()["user_id"] == dev_id

    # 5. Create Task
    task_resp = client.post(f"/api/v1/projects/{project_id}/tasks", json={
        "title": "Setup OAuth2",
        "description": "Implement Google login",
        "status": "pending",
        "priority": "high",
        "assigned_to_user_id": dev_id
    })
    assert task_resp.status_code == 201
    task_id = task_resp.json()["id"]

    # 6. Add Comment
    comment_resp = client.post(
        f"/api/v1/projects/{project_id}/tasks/{task_id}/comments?user_id={dev_id}",
        json={"comment": "OAuth integration completed, PR submitted."}
    )
    assert comment_resp.status_code == 201
    assert comment_resp.json()["task_id"] == task_id

    # 7. Get Project Summary & Verify Stats
    summary_resp = client.get(f"/api/v1/projects/{project_id}/summary")
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    assert "statistics" in summary
    stats = summary["statistics"]
    assert stats["total_tasks"] == 1
    assert stats["total_members"] == 2  # Owner + Developer
    assert stats["total_comments"] == 1
