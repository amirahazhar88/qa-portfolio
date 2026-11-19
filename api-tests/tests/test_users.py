import pytest

from conftest import PASSWORD, unique, user_payload

pytestmark = pytest.mark.usefixtures("api")


class TestRegistration:
    @pytest.mark.smoke
    def test_register_returns_the_new_user_with_a_token(self, api):
        payload = user_payload()

        response = api.post("/users", json=payload)

        assert response.status_code == 200
        body = response.json()["user"]
        assert body["username"] == payload["user"]["username"]
        assert body["email"] == payload["user"]["email"]
        assert body["token"]
        assert "password" not in body

    @pytest.mark.parametrize("field", ["username", "email"])
    def test_a_duplicate_username_or_email_is_a_conflict(self, api, user, field):
        payload = user_payload()
        payload["user"][field] = getattr(user, field)

        response = api.post("/users", json=payload)

        assert response.status_code == 409

    @pytest.mark.parametrize("missing", ["username", "email", "password"])
    def test_a_missing_field_is_rejected(self, api, missing):
        payload = user_payload()
        del payload["user"][missing]

        assert api.post("/users", json=payload).status_code == 422

    def test_an_empty_body_is_rejected(self, api):
        assert api.post("/users", json={}).status_code == 422

    def test_a_weak_password_is_rejected(self, api):
        response = api.post("/users", json=user_payload(password="a"))

        assert response.status_code in (400, 422)

    @pytest.mark.xfail(strict=True, reason="BUG-005: register accepts an invalid email address")
    def test_an_invalid_email_is_rejected(self, api):
        response = api.post("/users", json=user_payload(email="not-an-email"))

        assert response.status_code == 422


class TestLogin:
    @pytest.mark.smoke
    def test_login_returns_a_token_that_works(self, api, user):
        response = api.post("/users/login", json={"user": {"email": user.email, "password": user.password}})

        assert response.status_code == 200
        token = response.json()["user"]["token"]
        assert api.get("/user", token=token).json()["user"]["username"] == user.username

    def test_a_wrong_password_is_unauthorized(self, api, user):
        response = api.post("/users/login", json={"user": {"email": user.email, "password": "wrong"}})

        assert response.status_code == 401

    def test_an_unknown_email_is_not_found(self, api):
        response = api.post("/users/login", json={"user": {"email": f"{unique()}@example.com", "password": PASSWORD}})

        assert response.status_code == 404

    def test_a_missing_password_is_rejected(self, api, user):
        assert api.post("/users/login", json={"user": {"email": user.email}}).status_code == 422


class TestCurrentUser:
    def test_get_current_user(self, api, user):
        response = api.get("/user", token=user.token)

        assert response.status_code == 200
        assert response.json()["user"]["email"] == user.email

    def test_no_token_is_unauthorized(self, api):
        assert api.get("/user").status_code == 401

    def test_a_garbage_token_is_unauthorized(self, api):
        assert api.get("/user", token="garbage").status_code == 401

    def test_the_token_scheme_must_be_bearer(self, api, user):
        response = api.get("/user", headers={"Authorization": f"Token {user.token}"})

        assert response.status_code == 401


class TestUpdateUser:
    def test_update_the_bio(self, api, user):
        response = api.put("/user", token=user.token, json={"user": {"bio": "I test APIs."}})

        assert response.status_code == 200
        assert api.get("/user", token=user.token).json()["user"]["bio"] == "I test APIs."

    def test_a_new_password_works_and_the_old_one_does_not(self, api, user):
        new_password = "N3wPassw0rd!456"
        assert api.put("/user", token=user.token, json={"user": {"password": new_password}}).status_code == 200

        login = lambda password: api.post("/users/login", json={"user": {"email": user.email, "password": password}})
        assert login(new_password).status_code == 200
        assert login(user.password).status_code == 401

    def test_an_invalid_email_is_rejected(self, api, user):
        assert api.put("/user", token=user.token, json={"user": {"email": "nope"}}).status_code == 422

    def test_a_short_password_is_rejected(self, api, user):
        assert api.put("/user", token=user.token, json={"user": {"password": "a"}}).status_code == 422

    @pytest.mark.xfail(strict=True, reason="BUG-004: duplicate email on update returns 500, not 409")
    def test_a_taken_email_is_a_conflict(self, api, user, other_user):
        response = api.put("/user", token=user.token, json={"user": {"email": other_user.email}})

        assert response.status_code == 409

    @pytest.mark.xfail(strict=True, reason="BUG-004: duplicate username on update returns 500, not 409")
    def test_a_taken_username_is_a_conflict(self, api, user, other_user):
        response = api.put("/user", token=user.token, json={"user": {"username": other_user.username}})

        assert response.status_code == 409

    @pytest.mark.xfail(strict=True, reason="BUG-002: an empty bio is rejected with 422")
    def test_an_empty_bio_can_be_saved(self, api, user):
        response = api.put("/user", token=user.token, json={"user": {"bio": ""}})

        assert response.status_code == 200
