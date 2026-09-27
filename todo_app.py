"""Codveda Level 2 - Task 1: Feature-rich To-Do Application.

A command-line productivity app with JSON persistence, priorities,
categories, search, filtering, editing, statistics, and bulk cleanup.
"""

import json
import os
import tempfile
import warnings
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"
PRIORITIES = ("Low", "Medium", "High")
CATEGORIES = ("Personal", "College", "Work", "Other")


def _is_valid_positive_id(task_id: object) -> bool:
    """Return True only for positive integer IDs."""
    return isinstance(task_id, int) and not isinstance(task_id, bool) and task_id > 0


def load_tasks(data_file: Path = DEFAULT_DATA_FILE) -> List[Dict]:
    """Load valid tasks from JSON storage."""
    try:
        with data_file.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        return []
    except (PermissionError, OSError, json.JSONDecodeError) as exc:
        warnings.warn(f"Unable to read tasks from {data_file}: {exc}")
        return []

    if not isinstance(tasks, list):
        warnings.warn(f"Tasks data in {data_file} is not a JSON list; ignoring invalid file content.")
        return []

    valid_tasks = []
    seen_ids = set()
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            warnings.warn(f"Skipping invalid task at index {index}: entry is not a dictionary.")
            continue
        task_id = task.get("id")
        if not _is_valid_positive_id(task_id):
            warnings.warn(f"Skipping invalid task at index {index}: id must be a positive integer.")
            continue
        if task_id in seen_ids:
            warnings.warn(f"Skipping duplicate task ID {task_id} at index {index}.")
            continue
        title = task.get("title")
        if not isinstance(title, str):
            warnings.warn(f"Skipping invalid task at index {index}: title must be a string.")
            continue
        cleaned_title = title.strip()
        if not cleaned_title:
            warnings.warn(f"Skipping invalid task at index {index}: title cannot be empty.")
            continue
        completed = task.get("completed")
        if not isinstance(completed, bool):
            warnings.warn(f"Skipping invalid task at index {index}: completed must be a boolean.")
            continue

        task["id"] = task_id
        task["title"] = cleaned_title
        task["completed"] = completed
        task.setdefault("priority", "Medium")
        task.setdefault("category", "Other")
        if task["priority"] not in PRIORITIES:
            task["priority"] = "Medium"
        if task["category"] not in CATEGORIES:
            task["category"] = "Other"
        valid_tasks.append(task)
        seen_ids.add(task_id)
    return valid_tasks


def save_tasks(tasks: List[Dict], data_file: Path = DEFAULT_DATA_FILE) -> None:
    """Save tasks to JSON storage using atomic replace."""
    data_file.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(data_file.parent), delete=False) as file:
            temp_path = Path(file.name)
            json.dump(tasks, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp_path, data_file)
    except OSError:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink(missing_ok=True)
        raise


def add_task(tasks: List[Dict], title: str, priority: str = "Medium",
             category: str = "Other") -> Dict:
    """Add a task with priority and category."""
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    if priority not in PRIORITIES:
        raise ValueError("Priority must be Low, Medium, or High.")
    if category not in CATEGORIES:
        raise ValueError("Invalid category.")

    next_id = 1
    while any(task.get("id") == next_id for task in tasks):
        next_id += 1

    task = {"id": next_id, "title": title, "completed": False,
            "priority": priority, "category": category}
    tasks.append(task)
    return task


def find_task(tasks: List[Dict], task_id: int) -> Dict:
    """Find a task by ID or raise a clear error."""
    if not _is_valid_positive_id(task_id):
        raise ValueError("Task ID must be a positive whole number.")
    for task in tasks:
        if task.get("id") == task_id:
            return task
    raise ValueError(f"Task with ID {task_id} not found.")


def complete_task(tasks: List[Dict], task_id: int) -> Dict:
    """Mark a task as completed."""
    task = find_task(tasks, task_id)
    task["completed"] = True
    return task


def delete_task(tasks: List[Dict], task_id: int) -> Dict:
    """Delete and return a task."""
    task = find_task(tasks, task_id)
    tasks.remove(task)
    return task


def edit_task(tasks: List[Dict], task_id: int, title: Optional[str] = None,
              priority: Optional[str] = None, category: Optional[str] = None) -> Dict:
    """Edit selected task fields."""
    task = find_task(tasks, task_id)
    if title is not None:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task["title"] = title
    if priority is not None:
        if priority not in PRIORITIES:
            raise ValueError("Priority must be Low, Medium, or High.")
        task["priority"] = priority
    if category is not None:
        if category not in CATEGORIES:
            raise ValueError("Invalid category.")
        task["category"] = category
    return task


def search_tasks(tasks: List[Dict], keyword: str) -> List[Dict]:
    """Return tasks whose title or category matches a keyword."""
    keyword = keyword.strip().lower()
    if not keyword:
        return tasks
    return [task for task in tasks
            if keyword in task["title"].lower()
            or keyword in task["category"].lower()]


def filter_tasks(tasks: List[Dict], status: str = "all",
                 priority: str = "all") -> List[Dict]:
    """Filter tasks by completion status and priority."""
    if status not in ("all", "pending", "completed"):
        raise ValueError("Status must be all, pending, or completed.")
    if priority != "all" and priority not in PRIORITIES:
        raise ValueError("Invalid priority filter.")
    result = tasks
    if status == "pending":
        result = [task for task in result if not task["completed"]]
    elif status == "completed":
        result = [task for task in result if task["completed"]]
    if priority != "all":
        result = [task for task in result if task["priority"] == priority]
    return result


def clear_completed(tasks: List[Dict]) -> int:
    """Remove all completed tasks and return the number removed."""
    completed_count = sum(1 for task in tasks if task.get("completed") is True)
    if completed_count == 0:
        print("No completed tasks to remove.")
        return 0

    print(f"{completed_count} completed task(s) will be removed. Continue? (y/n): ")
    confirmation = input().strip().lower()
    if confirmation not in ("y", "yes"):
        print("Completed tasks were not removed.")
        return 0

    before = len(tasks)
    tasks[:] = [task for task in tasks if not task.get("completed")]
    return before - len(tasks)


def get_stats(tasks: List[Dict]) -> Dict[str, int]:
    """Return basic productivity statistics."""
    total = len(tasks)
    completed = sum(task["completed"] for task in tasks)
    return {"total": total, "completed": completed, "pending": total - completed,
            "high_priority": sum(task["priority"] == "High" and not task["completed"]
                                 for task in tasks)}


def display_tasks(tasks: List[Dict], heading: str = "Your Tasks") -> None:
    """Display tasks in a readable table."""
    if not tasks:
        print("\nNo tasks found.")
        return
    print(f"\n{heading}:")
    print("-" * 78)
    print(f'{"ID":<5}{"Task":<30}{"Priority":<12}{"Category":<12}Status')
    print("-" * 78)
    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        title = task["title"][:28] + ".." if len(task["title"]) > 30 else task["title"]
        print(f'{task["id"]:<5}{title:<30}{task["priority"]:<12}'
              f'{task["category"]:<12}{status}')
    print("-" * 78)


def get_task_id(action: str) -> int:
    """Read a task ID safely."""
    raw_value = input(f"Enter the task ID to {action}: ").strip()
    try:
        task_id = int(raw_value)
    except ValueError as exc:
        raise ValueError("Task ID must be a whole number.") from exc
    if task_id <= 0:
        raise ValueError("Task ID must be a positive whole number.")
    return task_id


def choose_priority() -> str:
    """Read and validate a priority."""
    while True:
        value = input("Priority (Low/Medium/High) [Medium]: ").strip().title()
        value = value or "Medium"
        if value in PRIORITIES:
            return value
        print("Invalid priority. Please choose Low, Medium, or High.")


def choose_category() -> str:
    """Read and validate a category."""
    while True:
        value = input("Category (Personal/College/Work/Other) [Other]: ").strip().title()
        value = value or "Other"
        if value in CATEGORIES:
            return value
        print("Invalid category. Please choose Personal, College, Work, or Other.")


def get_menu_choice() -> str:
    """Display the main menu and read a choice."""
    print("\n" + "=" * 48 + "\n              TO-DO COMMAND CENTER\n" + "=" * 48)
    print("1. Add task\n2. View all tasks\n3. Mark task as complete\n"
          "4. Edit task\n5. Delete task\n6. Search tasks\n7. Filter tasks\n"
          "8. Productivity statistics\n9. Clear completed tasks\n10. Exit")
    return input("\nChoose an option: ").strip()


def main(data_file: Path = DEFAULT_DATA_FILE) -> None:
    """Run the interactive to-do application."""
    tasks = load_tasks(data_file)
    print("=" * 48 + "\n              TO-DO COMMAND CENTER\n" + "=" * 48)
    print("Your tasks are saved automatically.")
    while True:
        choice = get_menu_choice()
        try:
            if choice == "1":
                task = add_task(tasks, input("Enter task title: "),
                                choose_priority(), choose_category())
                save_tasks(tasks, data_file)
                print(f'\nAdded: "{task["title"]}" [{task["priority"]}]')
            elif choice == "2":
                display_tasks(tasks)
            elif choice == "3":
                task = complete_task(tasks, get_task_id("complete"))
                save_tasks(tasks, data_file)
                print(f'Task completed: "{task["title"]}"')
            elif choice == "4":
                task_id = get_task_id("edit")
                task = find_task(tasks, task_id)
                title = input(f'New title [{task["title"]}]: ').strip() or task["title"]
                priority = input(f'New priority [{task["priority"]}] (Low/Medium/High): ').strip().title() or task["priority"]
                category = input(f'New category [{task["category"]}] (Personal/College/Work/Other): ').strip().title() or task["category"]
                edit_task(tasks, task_id, title, priority, category)
                save_tasks(tasks, data_file)
                print("Task updated successfully.")
            elif choice == "5":
                task = delete_task(tasks, get_task_id("delete"))
                save_tasks(tasks, data_file)
                print(f'Task deleted: "{task["title"]}"')
            elif choice == "6":
                display_tasks(search_tasks(tasks, input("Search keyword: ")), "Search Results")
            elif choice == "7":
                status = input("Status (all/pending/completed) [all]: ").strip().lower() or "all"
                priority = input("Priority (all/Low/Medium/High) [all]: ").strip().title() or "all"
                display_tasks(filter_tasks(tasks, status, priority), "Filtered Tasks")
            elif choice == "8":
                stats = get_stats(tasks)
                print(f'\nTotal: {stats["total"]} | Completed: {stats["completed"]} | '
                      f'Pending: {stats["pending"]} | Pending high-priority tasks: {stats["high_priority"]}')
            elif choice == "9":
                removed = clear_completed(tasks)
                if removed:
                    save_tasks(tasks, data_file)
                    print(f"Removed {removed} completed task(s).")
            elif choice == "10":
                print("Goodbye! Keep getting things done.")
                break
            else:
                print("Invalid option. Please choose 1-10.")
        except (ValueError, OSError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
