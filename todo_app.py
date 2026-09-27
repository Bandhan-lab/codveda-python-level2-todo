"""Codveda Level 2 - Task 1: To-Do Application.

A simple command-line to-do application with JSON persistence.
"""

import json
from pathlib import Path
from typing import Dict, List


DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"


def load_tasks(data_file: Path = DEFAULT_DATA_FILE) -> List[Dict]:
    """Load tasks from JSON storage.

    Returns an empty list when the file does not exist or contains invalid
    JSON, while keeping the application usable.
    """
    try:
        with data_file.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(tasks, list):
        return []

    valid_tasks = []
    for task in tasks:
        if (
            isinstance(task, dict)
            and isinstance(task.get("id"), int)
            and isinstance(task.get("title"), str)
            and isinstance(task.get("completed"), bool)
        ):
            valid_tasks.append(task)

    return valid_tasks


def save_tasks(tasks: List[Dict], data_file: Path = DEFAULT_DATA_FILE) -> None:
    """Save all tasks to JSON storage."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with data_file.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def add_task(tasks: List[Dict], title: str) -> Dict:
    """Add a new task and return it.

    Raises ValueError when the title is empty.
    """
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")

    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    return task


def get_tasks(tasks: List[Dict]) -> List[Dict]:
    """Return the current tasks."""
    return tasks


def complete_task(tasks: List[Dict], task_id: int) -> Dict:
    """Mark a task as completed and return it."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    raise ValueError(f"Task with ID {task_id} not found.")


def delete_task(tasks: List[Dict], task_id: int) -> Dict:
    """Delete a task by ID and return the deleted task."""
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            return tasks.pop(index)
    raise ValueError(f"Task with ID {task_id} not found.")


def display_tasks(tasks: List[Dict]) -> None:
    """Display all tasks in a readable format."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nYour Tasks:")
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        print(f'{task["id"]}. {task["title"]} - {status}')


def get_menu_choice() -> str:
    """Read the user's menu selection."""
    return input(
        "\n1. Add task\n"
        "2. View tasks\n"
        "3. Mark task as complete\n"
        "4. Delete task\n"
        "5. Exit\n"
        "Choose an option: "
    ).strip()


def get_task_id(action: str) -> int:
    """Read a task ID from the user."""
    try:
        return int(input(f"Enter the task ID to {action}: ").strip())
    except ValueError as exc:
        raise ValueError("Task ID must be a whole number.") from exc


def main(data_file: Path = DEFAULT_DATA_FILE) -> None:
    """Run the interactive to-do application."""
    tasks = load_tasks(data_file)

    print("=" * 38)
    print("          TO-DO APPLICATION")
    print("=" * 38)

    while True:
        choice = get_menu_choice()

        try:
            if choice == "1":
                title = input("Enter task title: ")
                task = add_task(tasks, title)
                save_tasks(tasks, data_file)
                print(f'Task added: "{task["title"]}"')

            elif choice == "2":
                display_tasks(tasks)

            elif choice == "3":
                task_id = get_task_id("complete")
                complete_task(tasks, task_id)
                save_tasks(tasks, data_file)
                print("Task marked as complete.")

            elif choice == "4":
                task_id = get_task_id("delete")
                deleted = delete_task(tasks, task_id)
                save_tasks(tasks, data_file)
                print(f'Task deleted: "{deleted["title"]}"')

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please choose a number from 1 to 5.")

        except ValueError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
