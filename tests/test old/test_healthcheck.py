import pytest

@pytest.mark.django_db
def test_home_200(client):
    """
    Smoke test: la app responde en "/".
    (200 si renderiza, 302 si redirige.)
    """
    r = client.get("/")
    assert r.status_code in (200, 302)
