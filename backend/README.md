# Clustering Platform Backend

FastAPI backend for the Clustering Platform web application.

## Setup

### Option 1: Using Setup Script (Recommended)

```bash
cd backend
bash setup.sh
```

This will:
- Activate/create virtual environment
- Install all dependencies
- Initialize the database

### Option 2: Manual Setup

1. **Activate Virtual Environment**
   ```bash
   cd /Users/kkarupas/cursor/projects/clustering-platform
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

## Running the Server

### Option 1: Using Run Script
```bash
cd backend
bash run.sh
```

### Option 2: Manual Run
```bash
# Activate virtual environment first
source ../venv/bin/activate

# Run the server
python run.py
```

### Option 3: Using Uvicorn Directly
```bash
source ../venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Import Errors
If you get import errors, make sure:
1. Virtual environment is activated
2. You're in the `backend` directory
3. All dependencies are installed: `pip install -r requirements.txt`

### Database Errors
If database errors occur:
1. Delete `clustering_platform.db` if it exists
2. Reinitialize: `python -c "from app.database import init_db; init_db()"`

### Port Already in Use
If port 8000 is already in use:
```bash
# Change port in run.py or use:
uvicorn app.main:app --reload --port 8001
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # REST API endpoints
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database setup
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI app
├── uploads/              # Uploaded files
├── notebooks/            # Generated notebooks
├── requirements.txt      # Dependencies
├── setup.sh              # Setup script
├── run.sh                # Run script
└── run.py                # Python run script
```
