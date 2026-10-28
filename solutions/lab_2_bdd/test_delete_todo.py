import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from lab_2_bdd.app import app, todos

# Scenarios
scenarios('./features/delete_todo.feature')

# Fixtures
@pytest.fixture
def client():
    """Provides a test client for the Flask application."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def response(client):
    """A fixture to store the response from an API call."""
    return {}


# Given Steps
@given('the API has a to-do with id 2 and task "Build a Flask API"')
def setup_existing_todo():
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
    ]

@given('the API has a list of to-dos')
def setup_any_todos():
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
        {"id": 3, "task": "Example TODO", "done": False},
    ]


# When Steps
@when(parsers.parse('the user deletes the to-do with id {todo_id}'))
def delete_single_todo(client, response, todo_id):
    """Make a DELETE request to the /todos/<id> endpoint."""
    res = client.delete(f'/todos/{todo_id}')
    response['data'] = res.get_json()
    response['status_code'] = res.status_code


# Then Steps
@then(parsers.parse('the response status code should be {status_code:d}'))
def check_status_code(response, status_code):
    assert response['status_code'] == status_code

@then('the to-do with id 2 should no longer exist')
def check_todo_deleted(client):
    res = client.get('/todos/2')
    assert res.status_code == 404

@then('the response should contain a "not found" error message')
def check_response_for_not_found(response):
    assert 'error' in response['data']
    assert 'not found' in response['data']['error'].lower()
