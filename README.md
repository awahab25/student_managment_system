# Student Management System

## Overview
A simple Student Management System built with Python OOP and Streamlit. Supports CRUD, JSON storage, search and filters.

## Requirements
- Python 3.9+
- pip install -r requirements.txt
  - streamlit
  - pandas

## Run
1. `pip install streamlit pandas`
2. `streamlit run ui/app.py`

## Structure
- `models/student.py` — Student dataclass + validation
- `services/manager.py` — Manager (CRUD + JSON storage)
- `ui/app.py` — Streamlit frontend
- `data/students.json` — sample data

## Notes
- Default GPA bounds are 0–100. Adjust validation if you want 0–4 scale.
- For production use, consider switching to a database (SQLite/Postgres).
