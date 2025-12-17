# How to Run the Clustering Platform

Complete guide to running both backend and frontend components.

## Prerequisites

- Python 3.9+ with virtual environment
- Node.js 16+ and npm
- Backend and frontend run simultaneously

## Quick Start (Both Components)

### Terminal 1: Backend

```bash
# Navigate to project root
cd /Users/kkarupas/cursor/projects/clustering-platform

# Activate virtual environment
source venv/bin/activate

# Navigate to backend
cd backend

# Install dependencies (first time only)
pip install -r requirements.txt

# Initialize database (first time only)
python -c "from app.database import init_db; init_db()"

# Run backend server
python run.py
```

Backend will start on **http://localhost:8000**

### Terminal 2: Frontend

```bash
# Navigate to frontend directory
cd /Users/kkarupas/cursor/projects/clustering-platform/frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

Frontend will start on **http://localhost:5173**

## Access the Application

1. **Frontend UI**: http://localhost:5173
   - AI-Assisted Mode: http://localhost:5173/ai-mode
   - Advanced Mode: http://localhost:5173/advanced-mode

2. **Backend API Docs**: 
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Features Overview

### AI-Assisted Mode (`/ai-mode`)
1. **Device Management**: Add/manage devices (Intersight, Custom APIs)
2. **File Upload**: Drag-and-drop CSV/JSON files
3. **Data Ingestion**: View uploaded files
4. **Auto Clustering**: Click "Run Auto Clustering" on any completed file
5. **View Results**: See clustering metrics and interactive visualizations

### Advanced Mode (`/advanced-mode`)
1. **Data File Browser**: Browse all ingested files
2. **Notebook Launcher**: Create Jupyter notebooks with pre-populated code

## Step-by-Step Usage Example

1. **Start Backend** (Terminal 1)
   ```bash
   cd backend && python run.py
   ```

2. **Start Frontend** (Terminal 2)
   ```bash
   cd frontend && npm run dev
   ```

3. **Upload a File**
   - Go to http://localhost:5173/ai-mode
   - Drag and drop a CSV or JSON file
   - Wait for processing to complete

4. **Run Clustering**
   - In "Data Ingestion & Auto Clustering" section
   - Click "Run Auto Clustering" on your file
   - Results will appear below with:
     - Algorithm used
     - Clustering metrics
     - Interactive Plotly visualization

5. **View Results**
   - Scroll down to see clustering results
   - Metrics include: Silhouette Score, Davies-Bouldin Index, etc.
   - Interactive visualization shows clusters in 2D space

## Configuration

### Backend Configuration
Edit `backend/app/config.py` or create `.env` file:
- `DATABASE_URL`: Database connection (default: SQLite)
- `UPLOAD_DIR`: Upload directory (default: `uploads`)
- `VISUALIZATIONS_DIR`: Visualizations directory (default: `visualizations`)
- `MAX_FILE_SIZE`: Max file size (default: 100MB)

### Frontend Configuration
Create `frontend/.env` file:
```
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Edit backend/run.py to change port, or:
uvicorn app.main:app --reload --port 8001
```

**Database errors:**
```bash
cd backend
rm clustering_platform.db  # if exists
python -c "from app.database import init_db; init_db()"
```

**Import errors:**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**Port 5173 already in use:**
- Vite will automatically use next available port

**CORS errors:**
- Make sure backend is running
- Check `VITE_API_URL` in `frontend/.env` matches backend URL

**API connection errors:**
- Verify backend is running on http://localhost:8000
- Check browser console for detailed errors
- Ensure CORS is enabled in backend (already configured)

### Visualization Issues

**Visualizations not loading:**
- Check that `backend/visualizations/` directory exists
- Verify backend static file serving is working
- Check browser console for 404 errors

## Production Build

### Backend
```bash
cd backend
# Use production WSGI server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run build
# Serve dist/ folder with a web server
```

## Directory Structure

```
clustering-platform/
├── backend/
│   ├── app/              # Backend application
│   ├── uploads/          # Uploaded files
│   ├── notebooks/        # Generated notebooks
│   ├── visualizations/   # Generated visualizations
│   └── run.py           # Run script
├── frontend/
│   ├── src/             # Frontend source
│   └── dist/            # Built files
└── venv/                # Python virtual environment
```

## Next Steps

- Upload your data files
- Run clustering analysis
- View interactive visualizations
- Explore Advanced Mode for custom analysis

