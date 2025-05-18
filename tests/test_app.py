from app import app, db
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_register_and_list(client):
    response = client.post('/register', json={"username": "alice"})
    assert response.status_code == 201

    response = client.get('/users')
    data = response.get_json()
    assert "alice" in data


def test_register_duplicate(client):
    client.post('/register', json={"username": "bob"})
    response = client.post('/register', json={"username": "bob"})
    assert response.status_code == 409
