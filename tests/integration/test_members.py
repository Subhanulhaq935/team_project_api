def test_add_project_member_success(client):
    # Create User 1 (Project Creator) & User 2 (Member)
    u1 = client.post("/api/v1/auth/register", json={
        "firstname": "Owner", "lastname": "One",
        "email": "owner@example.com", "password": "Password123!"
    }).json()["user_id"]

    u2 = client.post("/api/v1/auth/register", json={
        "firstname": "Dev", "lastname": "Two",
        "email": "dev@example.com", "password": "Password123!"
    }).json()["user_id"]

    proj = client.post("/api/v1/projects", json={
        "name": "Team Collab", "user_id": u1
    }).json()

    # Add u2 as developer
    response = client.post(f"/api/v1/projects/{proj['id']}/members", json={
        "user_id": u2,
        "project_role": "DEVELOPER"
    })
    assert response.status_code == 201
    assert response.json()["user_id"] == u2


def test_add_member_duplicate_conflict(client):
    u1 = client.post("/api/v1/auth/register", json={
        "firstname": "Owner", "lastname": "A",
        "email": "owner_a@example.com", "password": "Password123!"
    }).json()["user_id"]

    u2 = client.post("/api/v1/auth/register", json={
        "firstname": "Dev", "lastname": "B",
        "email": "dev_b@example.com", "password": "Password123!"
    }).json()["user_id"]

    proj = client.post("/api/v1/projects", json={
        "name": "Duplicate Test", "user_id": u1
    }).json()

    client.post(f"/api/v1/projects/{proj['id']}/members", json={
        "user_id": u2, "project_role": "DEVELOPER"
    })

    # Adding again should return 409 Conflict
    response = client.post(f"/api/v1/projects/{proj['id']}/members", json={
        "user_id": u2, "project_role": "DEVELOPER"
    })
    assert response.status_code == 409


def test_add_member_invalid_project_or_user(client):
    response = client.post("/api/v1/projects/9999/members", json={
        "user_id": 9999,
        "project_role": "DEVELOPER"
    })
    assert response.status_code == 404
