from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from app.models.user import User
from app.schemas.auth import LoginRequest
from app.services import auth_service


# Test 14: Login Success (Correct email + correct password)
@patch("app.services.auth_service.create_user_refresh_token")
@patch("app.services.auth_service.create_access_token")
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.user_repository.get_user_by_email")
def test_login_success(
    mock_get_user, mock_verify_pw, mock_access_token, mock_refresh_token, mock_db
):
    fake_user = User(id=1, email="john@example.com", password_hash="hashed_secret", role="USER")
    mock_get_user.return_value = fake_user
    mock_verify_pw.return_value = True
    mock_access_token.return_value = "jwt_access_token_xyz"
    mock_refresh_token.return_value = "raw_refresh_token_abc"

    payload = LoginRequest(email="john@example.com", password="correct_password")
    result = auth_service.login_user(mock_db, payload)

    assert result is not None
    assert result["access_token"] == "jwt_access_token_xyz"
    assert result["refresh_token"] == "raw_refresh_token_abc"
    mock_db.commit.assert_called_once()


# Test 15: Login Failed (Invalid password)
@patch("app.services.auth_service.verify_password")
@patch("app.services.auth_service.user_repository.get_user_by_email")
def test_login_invalid_password(mock_get_user, mock_verify_pw, mock_db):
    fake_user = User(id=1, email="john@example.com", password_hash="hashed_secret")
    mock_get_user.return_value = fake_user
    mock_verify_pw.return_value = False  # Wrong password!

    payload = LoginRequest(email="john@example.com", password="wrong_password")
    result = auth_service.login_user(mock_db, payload)

    assert result is None


# Test 16: Login Failed (User does not exist)
@patch("app.services.auth_service.user_repository.get_user_by_email")
def test_login_user_not_found(mock_get_user, mock_db):
    mock_get_user.return_value = None

    payload = LoginRequest(email="nonexistent@example.com", password="password123")
    result = auth_service.login_user(mock_db, payload)

    assert result is None


# Test 17: Expired Token Rejected
@patch("app.services.auth_service.verify_refresh_token")
@patch("app.services.auth_service.refresh_token_repository.get_all_active_refresh_tokens")
def test_expired_token(mock_get_active_tokens, mock_verify_refresh, mock_db):
    fake_token_record = MagicMock()
    fake_token_record.token_hash = "some_hash"
    # Token expired 2 hours ago
    fake_token_record.expires_at = datetime.utcnow() - timedelta(hours=2)

    mock_get_active_tokens.return_value = [fake_token_record]
    mock_verify_refresh.return_value = True

    result = auth_service.refresh_access_token(mock_db, "some_expired_token_string")

    assert result is None


# Test 18: Logout Success
@patch("app.services.auth_service.refresh_token_repository.revoke_refresh_token")
@patch("app.services.auth_service.verify_refresh_token")
@patch("app.services.auth_service.refresh_token_repository.get_all_active_refresh_tokens")
def test_logout_user_success(mock_get_tokens, mock_verify, mock_revoke, mock_db):
    fake_token = MagicMock()
    fake_token.token_hash = "hashed_refresh"
    mock_get_tokens.return_value = [fake_token]
    mock_verify.return_value = True

    result = auth_service.logout_user(mock_db, "valid_refresh_token")

    assert result is True
    mock_revoke.assert_called_once_with(mock_db, fake_token)
    mock_db.commit.assert_called_once()
