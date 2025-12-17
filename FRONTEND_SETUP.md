# Frontend Setup & Run Guide

## Quick Start

### 1. Navigate to Frontend Directory
```bash
cd /Users/kkarupas/cursor/projects/clustering-platform/frontend
```

### 2. Install Dependencies (if not already done)
```bash
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

The frontend will start on **http://localhost:5173** (or next available port)

## Features Available

### AI-Assisted Mode (`/ai-mode`)
- **File Upload**: Drag-and-drop CSV/JSON files
- **Device Management**: Add/delete devices, configure WebAPI
- **Data Ingestion**: View uploaded files and run automatic clustering
- **Device Sync**: Fetch data from devices via WebAPI

### Advanced Mode (`/advanced-mode`)
- **Data File Browser**: Browse all ingested files with search and filters
- **Notebook Launcher**: Create and launch Jupyter notebooks with pre-populated code

## Backend Connection

Make sure the backend is running:
```bash
cd /Users/kkarupas/cursor/projects/clustering-platform
source venv/bin/activate
cd backend
python run.py
```

Backend should be running on **http://localhost:8000**

## Configuration

If backend is on a different port, create `.env` file in `frontend/`:
```
VITE_API_URL=http://localhost:8000
```

## Build for Production

```bash
npm run build
```

Built files will be in `frontend/dist/`

## Troubleshooting

### CORS Errors
Make sure backend CORS is configured to allow requests from frontend origin (http://localhost:5173)

### API Connection Errors
- Verify backend is running
- Check `VITE_API_URL` in `.env` matches backend URL
- Check browser console for detailed error messages

### Build Errors
```bash
# Clear cache and rebuild
rm -rf node_modules dist
npm install
npm run build
```

