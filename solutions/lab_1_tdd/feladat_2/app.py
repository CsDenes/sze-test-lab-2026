import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DATABASE = 'todos.db'

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        # Use the DATABASE config value so tests can inject a temporary path
        db = g._database = sqlite3.connect(app.config.get('DATABASE', DATABASE))
        # This allows accessing columns by name
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initializes the database by creating the necessary table.
    This function should be run from the command line once before
    starting the server for the first time: `python -c 'from app_persistent import init_db; init_db()'`
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def index():
    """Welcome page."""
    return 'Welcome to the TODO app!'


@app.route('/todos', methods=['GET'])
def get_todos():
    """Return all todo items as a JSON array."""
    db = get_db()
    todos = db.execute('SELECT id, task, done FROM todos').fetchall()
    # Convert Row objects to plain dicts so jsonify can serialize them
    return jsonify([dict(row) for row in todos])


@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo item from the JSON request body and return it."""
    data = request.get_json()
    db = get_db()
    cursor = db.execute('INSERT INTO todos (task, done) VALUES (?, ?)', (data['task'], 0))
    db.commit()
    new_todo = {'id': cursor.lastrowid, 'task': data['task'], 'done': 0}
    return jsonify(new_todo), 201
