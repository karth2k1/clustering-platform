# Clustering Platform Backend

FastAPI backend for the Clustering Platform web application.

## Features

- File upload and management (CSV/JSON)
- Device management with WebAPI integration
- Automatic clustering with algorithm selection
- Notebook generation for Advanced mode
- RESTful API endpoints

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment (optional):
Create a `.env` file:
```
DATABASE_URL=sqlite:///./clustering_platform.db
UPLOAD_DIR=uploads
NOTEBOOK_DIR=notebooks
JUPYTER_SERVER_URL=http://localhost:8888
SECRET_KEY=your-secret-key
ENCRYPTION_KEY=your-encryption-key
```

3. Initialize database:
```bash
python -c "from app.database import init_db; init_db()"
```

4. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Files
- `POST /api/files/upload` - Upload single file
- `POST /api/files/upload-multiple` - Upload multiple files
- `GET /api/files` - List files (with filters)
- `GET /api/files/{file_id}` - Get file details
- `DELETE /api/files/{file_id}` - Delete file
- `GET /api/files/{file_id}/download` - Download file

### Devices
- `POST /api/devices` - Create device
- `GET /api/devices` - List devices
- `GET /api/devices/{device_id}` - Get device details
- `PUT /api/devices/{device_id}` - Update device
- `DELETE /api/devices/{device_id}` - Delete device
- `POST /api/devices/{device_id}/sync` - Sync data from device

### Clustering
- `POST /api/clustering/auto` - Run automatic clustering
- `GET /api/clustering/results/{file_id}` - Get clustering results
- `GET /api/clustering/results/{file_id}/{result_id}` - Get specific result

### Notebooks
- `POST /api/notebooks/create` - Create notebook from data file
- `GET /api/notebooks/{session_id}` - Get notebook session

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database setup
│   ├── config.py         # Configuration
│   └── main.py           # FastAPI app
├── uploads/              # Uploaded files
├── notebooks/            # Generated notebooks
└── requirements.txt      # Dependencies
```

