import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import todo_app


class TestTodoApp(unittest.TestCase):
    def test_add_multiple_tasks_with_metadata(self):
        tasks = []
        first = todo_app.add_task(tasks, "Study Python", "High", "College")
        second = todo_app.add_task(tasks, "Buy groceries", "Low", "Personal")
        self.assertEqual(first["id"], 1)
        self.assertEqual(second["id"], 2)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(first["priority"], "High")
        self.assertEqual(second["category"], "Personal")

    def test_add_task_rejects_invalid_data(self):
        with self.assertRaises(ValueError):
            todo_app.add_task([], "   ")
        with self.assertRaises(ValueError):
            todo_app.add_task([], "Task", "Urgent", "College")
        with self.assertRaises(ValueError):
            todo_app.add_task([], "Task", "High", "Invalid")

    def test_complete_and_delete_task(self):
        tasks = [{"id": 1, "title": "Study", "completed": False,
                  "priority": "High", "category": "College"}]
        completed = todo_app.complete_task(tasks, 1)
        self.assertTrue(completed["completed"])
        deleted = todo_app.delete_task(tasks, 1)
        self.assertEqual(deleted["title"], "Study")
        self.assertEqual(tasks, [])

    def test_missing_task_raises_error(self):
        with self.assertRaises(ValueError):
            todo_app.complete_task([], 99)
        with self.assertRaises(ValueError):
            todo_app.delete_task([], 99)

    def test_edit_task(self):
        tasks = []
        todo_app.add_task(tasks, "Old title")
        updated = todo_app.edit_task(tasks, 1, "New title", "High", "Work")
        self.assertEqual(updated["title"], "New title")
        self.assertEqual(updated["priority"], "High")
        self.assertEqual(updated["category"], "Work")

    def test_search_and_filter(self):
        tasks = [
            {"id": 1, "title": "Python assignment", "completed": False,
             "priority": "High", "category": "College"},
            {"id": 2, "title": "Buy milk", "completed": True,
             "priority": "Low", "category": "Personal"},
            {"id": 3, "title": "Python project", "completed": False,
             "priority": "Medium", "category": "College"},
        ]
        self.assertEqual(len(todo_app.search_tasks(tasks, "python")), 2)
        self.assertEqual(len(todo_app.filter_tasks(tasks, "pending")), 2)
        self.assertEqual(len(todo_app.filter_tasks(tasks, "completed")), 1)
        self.assertEqual(len(todo_app.filter_tasks(tasks, "all", "High")), 1)

    def test_clear_completed(self):
        tasks = [
            {"id": 1, "title": "Done", "completed": True,
             "priority": "Low", "category": "Other"},
            {"id": 2, "title": "Pending", "completed": False,
             "priority": "High", "category": "College"},
        ]
        removed = todo_app.clear_completed(tasks)
        self.assertEqual(removed, 1)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Pending")

    def test_statistics(self):
        tasks = [
            {"id": 1, "title": "Done", "completed": True,
             "priority": "High", "category": "College"},
            {"id": 2, "title": "Pending", "completed": False,
             "priority": "High", "category": "College"},
            {"id": 3, "title": "Low", "completed": False,
             "priority": "Low", "category": "Personal"},
        ]
        self.assertEqual(
            todo_app.get_stats(tasks),
            {"total": 3, "completed": 1, "pending": 2, "high_priority": 1},
        )

    def test_save_and_load_tasks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"
            tasks = [{"id": 1, "title": "Persistent", "completed": True,
                      "priority": "High", "category": "Work"}]
            todo_app.save_tasks(tasks, data_file)
            self.assertEqual(todo_app.load_tasks(data_file), tasks)

    def test_load_missing_and_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "missing.json"
            self.assertEqual(todo_app.load_tasks(data_file), [])
            data_file.write_text("{invalid json", encoding="utf-8")
            self.assertEqual(todo_app.load_tasks(data_file), [])

    @patch("builtins.input", side_effect=[
        "1", "Buy milk", "Low", "Personal",
        "1", "Study", "High", "College",
        "10",
    ])
    def test_main_can_add_multiple_tasks(self, _mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"
            with patch("builtins.print"):
                todo_app.main(data_file)
            tasks = todo_app.load_tasks(data_file)
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[1]["title"], "Study")
            self.assertEqual(tasks[1]["priority"], "High")

    @patch("builtins.input", side_effect=["3", "bad", "10"])
    def test_main_handles_invalid_task_id(self, _mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"
            with patch("builtins.print") as mock_print:
                todo_app.main(data_file)
            mock_print.assert_any_call("Error: Task ID must be a whole number.")


if __name__ == "__main__":
    unittest.main()
