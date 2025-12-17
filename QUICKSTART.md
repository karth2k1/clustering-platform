# Quick Start Guide

## Backend Setup & Run

### 1. Activate Virtual Environment
```bash
cd /Users/kkarupas/cursor/projects/clustering-platform
source venv/bin/activate
```

### 2. Navigate to Backend
```bash
cd backend
```

### 3. Install Dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### 4. Initialize Database (first time only)
```bash
python -c "from app.database import init_db; init_db()"
```

### 5. Run the Server
```bash
python run.py
```

The server will start on http://localhost:8000

### 6. Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Quick Test

Once the server is running, test it:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

## Troubleshooting

### Issue: `metadata` column error
**Fixed!** The `metadata` column has been renamed to `file_metadata` to avoid SQLAlchemy conflicts.

### Issue: Import errors
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Issue: Database errors
Reinitialize the database:
```bash
rm clustering_platform.db  # if exists
python -c "from app.database import init_db; init_db()"
```

