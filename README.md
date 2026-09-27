# ✅ To-Do Command Center

> **Codveda Technology — Python Development Internship**  
> **Level 2 · Task 1 — To-Do Application**

A feature-rich command-line productivity application built with Python. It goes beyond a basic task list with priorities, categories, search, filtering, statistics, persistent JSON storage, validation, and a comprehensive automated test suite.

## ✨ Why This Project?

Instead of building a one-task-at-a-time demo, the **To-Do Command Center** is designed as a practical mini productivity tool.

~~~text
                    TO-DO COMMAND CENTER
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
     Manage             Organize           Analyze
     Tasks              Tasks              Progress
        │                  │                  │
   Add / Edit /       Priority /          Statistics
   Complete /         Category /           / Search
   Delete             Filter               / Filter
~~~

## 🚀 Features

### 📝 Task Management
- Add multiple tasks
- Edit existing tasks
- Mark tasks as complete
- Delete tasks
- Automatic task IDs

### 🎨 Organization
- **Priority:** Low · Medium · High
- **Category:** Personal · College · Work · Other
- Search by task title or category
- Filter by completion status and priority

### 📊 Productivity
- Total task count
- Completed tasks
- Pending tasks
- Pending high-priority tasks
- Clear completed tasks with confirmation

### 💾 Persistence & Reliability
- Automatic JSON persistence
- Safe atomic saving
- Validation of stored task data
- Corrupted/invalid JSON handling
- Positive task-ID validation
- Invalid input handling
- Friendly error messages

### 🧪 Testing
- Automated tests with unittest
- Persistence tests
- Validation tests
- CRUD tests
- Search/filter tests
- Statistics tests
- CLI behavior tests

## 🎯 Codveda Requirements

| Requirement | Implementation |
|---|---|
| Add tasks | ✅ Multiple tasks supported |
| View tasks | ✅ Clean terminal table |
| Delete tasks | ✅ Task-ID based |
| Mark complete | ✅ Supported |
| Persistent storage | ✅ JSON |
| Basic error handling | ✅ Robust validation and file handling |

The application also includes additional functionality beyond the minimum requirements.

## 🖥️ Menu

~~~text
================================================
              TO-DO COMMAND CENTER
================================================
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
~~~

## 🧰 Tech Stack

- 🐍 Python 3
- 📄 JSON
- 🧪 unittest
- 💻 Command-line interface
- 🌿 Git
- 🐙 GitHub

No external Python packages are required.

## 🚀 Getting Started

~~~bash
git clone https://github.com/Bandhan-lab/codveda-python-level2-todo.git
cd codveda-python-level2-todo
python3 todo_app.py
~~~

Tasks are automatically stored in **data/tasks.json**.

## 🧪 Run Tests

~~~bash
python3 -m unittest discover -s tests -v
~~~

The suite covers task creation, editing, completion, deletion, persistence, validation, search/filter behavior, statistics, corrupted data, and interactive CLI cases.

## 📁 Project Structure

~~~text
codveda-python-level2-todo/
├── todo_app.py
├── data/
│   └── tasks.json
├── README.md
├── .gitignore
└── tests/
    └── test_todo_app.py
~~~

## 🧠 What This Project Demonstrates

- Python modular programming
- CRUD operations
- JSON file persistence
- Data validation
- Exception handling
- Search and filtering
- State management
- CLI application design
- Automated testing
- Defensive programming
- Git/GitHub workflow

## 📌 Project Status

**Status:** ✅ Completed  
**Program:** Codveda Technology — Python Development Internship  
**Level:** 2 — Intermediate  
**Task:** 1 — To-Do Application

## 👨‍💻 Author

**Bandhan Kumar Sahoo**  
B.Tech — CSE (AI & ML)  
GITA Autonomous College, Bhubaneswar, Odisha, India

Built as part of the Codveda Technology Python Development Internship.

⭐ If you find the project useful, consider giving the repository a star.
