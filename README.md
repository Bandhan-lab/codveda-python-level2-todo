# To-Do Application

A simple command-line To-Do Application built for the **Codveda Technology Python Development Internship — Level 2, Task 1**.

## Features

- Add new tasks
- View all tasks
- Mark tasks as complete
- Delete tasks
- Persist tasks in a JSON file
- Handle empty task names and invalid task IDs
- Keep data available after restarting the application

## Requirements

- Python 3.8 or newer
- No external packages are required

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

## Run the Application

```bash
python3 todo_app.py
```

The application stores tasks in `data/tasks.json`. The file is created automatically when you add, complete, or delete a task.

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```

## Internship

**Organization:** Codveda Technology  
**Domain:** Python Development  
**Level:** 2 — Intermediate  
**Task:** Task 1 — To-Do Application

## Author

**Bandhan Kumar Sahoo**
