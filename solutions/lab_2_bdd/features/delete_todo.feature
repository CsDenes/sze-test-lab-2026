Feature: Delete a single To-Do item
  As a user of the API,
  I want to be able to delete a specific to-do item by its ID,
  so that I can remove completed or unwanted tasks.

  Scenario: A to-do item is deleted successfully
    Given the API has a to-do with id 2 and task "Build a Flask API"
    When the user deletes the to-do with id 2
    Then the response status code should be 200
    And the to-do with id 2 should no longer exist

  Scenario: Deleting a to-do item that does not exist
    Given the API has a list of to-dos
    When the user deletes the to-do with id 99
    Then the response status code should be 404
    And the response should contain a "not found" error message
