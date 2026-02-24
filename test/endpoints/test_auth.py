"""
Integration tests for the /api/v1/auth endpoints.
"""


class TestAuthEndpoints:
    """Integration tests for the Auth API."""

    # ------------------------------------------------------------------
    # POST /api/v1/auth/refresh-token
    # ------------------------------------------------------------------

    def test_refresh_token(self, client):
        """
        With get_current_user overridden to the seeded test user, the
        refresh-token endpoint should issue a new JWT and return user info.
        """
        resp = client.post("/api/v1/auth/refresh-token")
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    # ------------------------------------------------------------------
    # POST /api/v1/auth/login — wrong credentials
    # ------------------------------------------------------------------

    def test_login_wrong_credentials(self, client):
        """
        Sending the correct username but a wrong password should yield 401.
        The login endpoint looks up the test user via the overridden get_db
        dependency (SQLite session), verifies the password, and raises
        AuthErrorHandler.raise_invalid_credentials().
        """
        resp = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "wrongpassword"},
        )
        assert resp.status_code == 401, resp.text

    # ------------------------------------------------------------------
    # POST /api/v1/auth/logout
    # ------------------------------------------------------------------

    def test_logout(self, client_real_auth, test_user):
        """
        A valid JWT should be accepted, stored in the revoked_tokens blacklist,
        and the endpoint should return {"message": "Logged out successfully"}.
        A second request with the same token must be rejected with 401.

        Uses ``client_real_auth`` (only get_db overridden) so that the real
        get_current_user blacklist check runs on the second call.
        """
        from app.core.security import create_access_token  # pylint: disable=import-outside-toplevel
        token = create_access_token(data={"sub": str(test_user.id)})

        resp = client_real_auth.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["message"] == "Logged out successfully"

        # Token must now be blacklisted — any authenticated call should fail.
        resp2 = client_real_auth.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp2.status_code == 401, resp2.text
