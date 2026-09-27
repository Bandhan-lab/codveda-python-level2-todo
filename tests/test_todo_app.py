import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import todo_app


class TestTodoApp(unittest.TestCase):
    def test_add_task(self):
        tasks = []
        task = todo_app.add_task(tasks, "Study Python")

        self.assertEqual(task, {"id": 1, "title": "Study Python", "completed": False})
        self.assertEqual(tasks, [task])

    def test_add_task_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            todo_app.add_task([], "   ")

    def test_complete_task(self):
        tasks = [{"id": 1, "title": "Study", "completed": False}]

        completed = todo_app.complete_task(tasks, 1)

        self.assertTrue(completed["completed"])
        self.assertTrue(tasks[0]["completed"])

    def test_delete_task(self):
        tasks = [
            {"id": 1, "title": "First", "completed": False},
            {"id": 2, "title": "Second", "completed": False},
        ]

        deleted = todo_app.delete_task(tasks, 1)

        self.assertEqual(deleted["title"], "First")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], 2)

    def test_missing_task_raises_error(self):
        with self.assertRaises(ValueError):
            todo_app.complete_task([], 99)

        with self.assertRaises(ValueError):
            todo_app.delete_task([], 99)

    def test_save_and_load_tasks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"
            tasks = [
                {"id": 1, "title": "Persistent task", "completed": True}
            ]

            todo_app.save_tasks(tasks, data_file)
            loaded = todo_app.load_tasks(data_file)

            self.assertEqual(loaded, tasks)

    def test_load_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "missing.json"
            self.assertEqual(todo_app.load_tasks(data_file), [])

    def test_load_invalid_json_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"
            data_file.write_text("{invalid json", encoding="utf-8")

            self.assertEqual(todo_app.load_tasks(data_file), [])

    @patch("builtins.input", side_effect=["1", "Buy milk", "5"])
    def test_main_adds_and_persists_task(self, _mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"

            with patch("builtins.print"):
                todo_app.main(data_file)

            self.assertEqual(
                todo_app.load_tasks(data_file),
                [{"id": 1, "title": "Buy milk", "completed": False}],
            )

    @patch("builtins.input", side_effect=["3", "bad", "5"])
    def test_main_handles_invalid_task_id(self, _mock_input):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "tasks.json"

            with patch("builtins.print") as mock_print:
                todo_app.main(data_file)

            mock_print.assert_any_call("Error: Task ID must be a whole number.")


if __name__ == "__main__":
    unittest.main()
