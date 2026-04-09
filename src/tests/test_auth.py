import jwt

from app.core.auth import authenticate
from app.core.config import settings


class TestAuthenticate:
    def test_valid_token(self):
        token = jwt.encode(
            {"sub": "1", "role": "client"},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        result = authenticate(token)
        assert result is not None
        assert result["user_id"] == "1"
        assert result["role"] == "client"

    def test_admin_role(self):
        token = jwt.encode(
            {"sub": "2", "role": "admin"},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        result = authenticate(token)
        assert result is not None
        assert result["role"] == "admin"

    def test_no_token(self):
        assert authenticate("") is None
        assert authenticate(None) is None

    def test_invalid_token(self):
        assert authenticate("invalid.token.here") is None

    def test_wrong_secret(self):
        token = jwt.encode({"sub": "1", "role": "client"}, "wrong-secret", algorithm="HS256")
        assert authenticate(token) is None

    def test_missing_sub(self):
        token = jwt.encode(
            {"role": "client"}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        assert authenticate(token) is None

    def test_invalid_role(self):
        token = jwt.encode(
            {"sub": "1", "role": "superuser"},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        assert authenticate(token) is None
