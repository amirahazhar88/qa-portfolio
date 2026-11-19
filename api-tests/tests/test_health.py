import pytest


@pytest.mark.smoke
def test_the_health_check_is_up(api):
    response = api.get("/health-check")

    assert response.status_code == 200
