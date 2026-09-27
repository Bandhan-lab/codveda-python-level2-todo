# To-Do Command Center

A feature-rich command-line To-Do Application built for the **Codveda Technology Python Development Internship — Level 2, Task 1**.

## Features

- Add **multiple tasks** in one session
- Assign **priority**: Low, Medium, High
- Organize tasks by **category**: Personal, College, Work, Other
- View tasks in a clean table
- Mark tasks as complete
- Edit existing tasks
- Delete tasks
- Search by task title or category
- Filter by completion status and priority
- View productivity statistics
- Clear all completed tasks at once
- Automatically persist data in JSON
- Handle invalid IDs, empty titles, invalid priorities/categories, and corrupted JSON safely

## Requirements

- Python 3.8+
- No external packages

## Project Structure

```
codveda-python-level2-todo/
├── todo_app.py
├── tests/
│   └── test_todo_app.py
├── data/
│   └── tasks.json
├── README.md
└── .gitignore
```

## Run

```bash
python3 todo_app.py
```

Tasks are automatically saved to `data/tasks.json`.

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```

## Menu

1. Add task
2. View all tasks
3. Mark task as complete
4. Edit task
5. Delete task
6. Search tasks
7. Filter tasks
8. Productivity statistics
9. Clear completed tasks
10. Exit

## Internship

**Organization:** Codveda Technology  
**Domain:** Python Development  
**Level:** 2 — Intermediate  
**Task:** Task 1 — To-Do Application

## Author

**Bandhan Kumar Sahoo**
