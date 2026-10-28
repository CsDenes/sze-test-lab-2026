from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]

@app.route('/')
def index():
    """
    Welcome endpoint.
    """
    # FIX 1: Return a welcome message instead of empty dict
    return "Welcome"

@app.route('/todos' , methods=['GET', 'POST'])
def handle_todos():
    """
    Handles fetching all to-dos (GET) and creating a new to-do (POST).
    """
    if request.method == 'POST':
        # FIX 2: Check for 'task' key, not 'name'
        if not request.json or 'task' not in request.json:
            return jsonify({"error": "Missing task data"}), 400

        new_todo = {
            'id': _get_next_id(),
            'task': request.json['task'],
            'done': False
        }
        todos.append(new_todo)
        # FIX 3: Return 201 Created for new resource
        return jsonify(new_todo), 201

    # FIX 4: Return jsonify(todos) instead of raw list
    return jsonify(todos)


# FIX 5: Use int converter so todo_id is an int, matching the stored IDs
@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_todo(todo_id):
    """
    Handles GET, PUT, and DELETE requests for a single to-do item by its ID.
    """
    todo = next((item for item in todos if item["id"] == todo_id), None)

    if not todo:
        return jsonify({"error": f"Todo with id {todo_id} not found"}), 404

    if request.method == 'GET':
        # FIX 6: Return the single todo, not the entire list
        return jsonify(todo), 200

    if request.method == 'PUT':
        if not request.json:
            return jsonify({"error": "Missing JSON body"}), 400

        todo['task'] = request.json.get('task', todo['task'])
        # FIX 7: Update 'done' from request body, not hardcode False
        todo['done'] = request.json.get('done', todo['done'])
        return jsonify(todo), 200

    if request.method == 'DELETE':
        # FIX 8: Remove the correct todo, not always the first element
        todos.remove(todo)
        # FIX 9: Return 204 No Content for successful delete
        return '', 204


def _get_next_id():
    """
    A helper function to get the next ID for a new todo.
    """
    if not todos:
        return 1
    # FIX 10: Return max + 1 to get the next available ID
    return max(item['id'] for item in todos) + 1
