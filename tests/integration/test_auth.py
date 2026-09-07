def test_register_user_success(client):
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john.doe@example.com",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert "user_id" in data


def test_register_duplicate_email(client):
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "duplicate@example.com",
        "password": "Password123!"
    }
    client.post("/api/v1/auth/register", json=payload)
    # Duplicate registration
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    # Register first
    client.post("/api/v1/auth/register", json={
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "jane.doe@example.com",
        "password": "Password123!"
    })
    # Login
    response = client.post("/api/v1/auth/login", json={
        "email": "jane.doe@example.com",
        "password": "Password123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post("/api/v1/auth/register", json={
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "jane2@example.com",
        "password": "Password123!"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "jane2@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401


def test_register_invalid_data_validation_error(client):
    # Missing required password field
    response = client.post("/api/v1/auth/register", json={
        "firstname": "John",
        "lastname": "Doe",
        "email": "not-an-email"
    })
    assert response.status_code == 422
