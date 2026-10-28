from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]

@app.route('/')
def index():
    return "Welcome"

@app.route('/todos')
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = {"id": len(todos) + 1, "task": data["task"], "done": False}
    todos.append(new_todo)
    return jsonify(new_todo), 201
