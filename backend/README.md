# Reckless Spender Backend

This is the backend service for the Reckless Spender personal finance application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest
```

4. Start the development server:
```bash
uvicorn main:app --reload
```

## Project Structure

- `main.py`: FastAPI application entry point
- `models/`: Pydantic models for data validation
- `routes/`: API route handlers
- `services/`: Business logic
- `tests/`: Test files 