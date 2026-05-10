def test_app_can_import():
    from app.main import app

    assert app is not None
    assert app.title == "AStock Agent System"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
