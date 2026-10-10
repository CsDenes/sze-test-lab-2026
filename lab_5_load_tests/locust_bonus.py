import random
from locust import HttpUser, task, between

class TodoUser(HttpUser):
    # Simulate a wait time between 1 and 2.5 seconds after each task
    wait_time = between(1, 2.5)

    # List to store the IDs of todo items created by this user
    created_task_ids = []

    def on_start(self):
        """
        This method runs once when each virtual user starts.
        Initializes the list of task IDs created by this user.
        """
        self.created_task_ids = []
        # The default, fixed IDs that we can also use in tests
        self.static_task_ids = [1, 2]

    @task(3)
    def get_all_todos(self):
        """
        Simulates a user fetching the list of all todos.
        """
        self.client.get("/todos", name="/todos (GET)")

    @task(2)
    def get_single_todo(self):
        """
        Simulates a user fetching a single todo item.
        It randomly picks from the static IDs or an ID this user has created.
        """
        todo_id = random.choice([1, 2])
        self.client.get(f"/todos/{todo_id}", name="/todos/{id} (GET)")

    @task(2)
    def create_todo(self):
        """
        Simulates a user creating a new todo item and saving its ID.
        Hint: using catch_response=True you can read the new item's ID from the response
        and save it to the self.created_task_ids list.
        """
        new_task_name = f"New task from user {random.randint(1, 1000)}"
        self.client.post(
            "/todos",
            json={"task": new_task_name},
            name="/todos (POST)"
        )

    @task(1)
    def update_todo(self):
        """
        Simulates a user updating an existing todo item.
        """
        todo_id_to_update = random.choice([1, 2])
        new_done_status = random.choice([True, False])

        self.client.put(
            f"/todos/{todo_id_to_update}",
            json={"done": new_done_status},
            name="/todos/{id} (PUT)"
        )

    @task(1)
    def delete_todo(self):
        """
        Simulates a user DELETING a todo item.
        Only delete items from the self.created_task_ids list
        to avoid deleting non-existent items (404 error).
        """
        # TODO: Implement the DELETE task!
        # 1. If created_task_ids is empty, return
        # 2. Pick a random ID from the list
        # 3. Send a DELETE request to /todos/{id}
        # 4. On successful deletion (204), remove the ID from the list
        pass

    @task(1)
    def get_root(self):
        """
        Simulates a user hitting the welcome page.
        """
        self.client.get("/", name="/ (GET)")
