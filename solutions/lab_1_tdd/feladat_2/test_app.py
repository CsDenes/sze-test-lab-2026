import os
import tempfile
import pytest
from feladat_2.app import app, init_db, get_db

@pytest.fixture
def client():
    """
    Test client fixture. This sets up a temporary database for testing
    and yields a Flask test client.
    """
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()

    # Configure the app for testing
    app.config.update({
        "TESTING": True,
        "DATABASE": db_path,
    })

    # Initialize the database with the schema and seed a default todo
    with app.app_context():
        init_db()
        db = get_db()
        db.execute("INSERT INTO todos (task, done) VALUES (?, ?)", ("Default todo", 0))
        db.commit()

    # Yield the test client
    with app.test_client() as client:
        yield client

    # Clean up by closing the file and removing it
    os.close(db_fd)
    os.unlink(db_path)

def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_get_todos_returns_seeded_item(client):
    """Test GET /todos returns the default todo seeded by the fixture."""
    response = client.get('/todos')
    assert response.status_code == 200
    todos = response.json
    assert len(todos) == 1
    assert todos[0]['task'] == 'Default todo'
    assert todos[0]['done'] == 0

def test_create_todo(client):
    """Test creating a new to-do item via POST /todos."""
    # Create a new todo
    response = client.post('/todos', json={'task': 'My first test todo'})
    assert response.status_code == 201

    # Verify it was added alongside the seeded default todo
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.json) == 2
    tasks = [item['task'] for item in response.json]
    assert 'My first test todo' in tasks
