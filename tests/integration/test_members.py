def test_add_project_member_success(client, create_user):
    mgr = create_user("owner@example.com", role="manager")
    dev = create_user("dev@example.com", role="user")

    proj = client.post(
        "/api/v1/projects",
        json={"name": "Team Collab"},
        headers=mgr["headers"]
    ).json()

    # Add dev as developer
    response = client.post(
        f"/api/v1/projects/{proj['id']}/members",
        json={
            "user_id": dev["id"],
            "project_role": "DEVELOPER"
        },
        headers=mgr["headers"]
    )
    assert response.status_code == 201
    assert response.json()["user_id"] == dev["id"]


def test_add_member_duplicate_conflict(client, create_user):
    mgr = create_user("owner_a@example.com", role="manager")
    dev = create_user("dev_b@example.com", role="user")

    proj = client.post(
        "/api/v1/projects",
        json={"name": "Duplicate Test"},
        headers=mgr["headers"]
    ).json()

    client.post(
        f"/api/v1/projects/{proj['id']}/members",
        json={"user_id": dev["id"], "project_role": "DEVELOPER"},
        headers=mgr["headers"]
    )

    # Adding again should return 409 Conflict
    response = client.post(
        f"/api/v1/projects/{proj['id']}/members",
        json={"user_id": dev["id"], "project_role": "DEVELOPER"},
        headers=mgr["headers"]
    )
    assert response.status_code == 409


def test_add_member_invalid_project_or_user(client, create_user):
    admin = create_user("admin_member@example.com", role="admin")
    response = client.post(
        "/api/v1/projects/9999/members",
        json={"user_id": 9999, "project_role": "DEVELOPER"},
        headers=admin["headers"]
    )
    assert response.status_code == 404
