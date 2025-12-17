# Clustering Platform

A comprehensive platform for testing various clustering algorithms with support for multiple use cases, data formats (JSON/CSV), and two operational modes: **AI-Assisted Mode** and **Advanced Mode**.

## Features

### AI-Assisted Mode
- **Automated Data Ingestion**: Drag-and-drop file upload (CSV/JSON)
- **Device Management**: Add/delete devices, fetch data via WebAPI
- **Automatic Clustering**: Smart algorithm selection and parameter tuning
- **Background Processing**: Async file processing and clustering
- **Device Integration**: Support for Intersight and custom APIs

### Advanced Mode
- **Jupyter Notebook Playground**: Full notebook environment
- **Pre-populated Code**: Analysis code generated from ingested data
- **Interactive Visualization**: Plotly and Matplotlib visualizations
- **Custom Clustering**: Full control over algorithms and parameters

### Core Capabilities
- **Multiple Algorithms**: K-Means, DBSCAN, HDBSCAN, Hierarchical Clustering, GMM
- **Data Formats**: CSV and JSON (including nested structures)
- **Use Case Management**: Create and manage clustering use cases
- **Comprehensive Metrics**: Silhouette Score, Davies-Bouldin Index, Calinski-Harabasz Index
- **Results Storage**: Save clustering results, configurations, and visualizations

## Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # REST API endpoints
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utilities
│   │   ├── models.py          # Database models
│   │   ├── schemas.py         # Pydantic schemas
│   │   └── main.py            # FastAPI app
│   ├── uploads/               # Uploaded files
│   ├── notebooks/             # Generated notebooks
│   └── requirements.txt
├── clustering_platform.ipynb  # Original Jupyter notebook
├── use_cases/                 # Use case definitions
│   ├── use_cases.json
│   └── intersight_alarms.json
└── README.md
```

## Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment** (Optional)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize Database**
   ```bash
   python -c "from app.database import init_db; init_db()"
   ```

4. **Run Backend Server**
   ```bash
   python run.py
   # or
   uvicorn app.main:app --reload
   ```

5. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Jupyter Notebook (Original)

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Jupyter**
   ```bash
   jupyter lab
   ```

3. **Open Notebook**
   - Open `clustering_platform.ipynb` in Jupyter Lab

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
- `DELETE /api/devices/{device_id}` - Delete device (with save/delete options)
- `POST /api/devices/{device_id}/sync` - Sync data from device

### Clustering
- `POST /api/clustering/auto` - Run automatic clustering
- `GET /api/clustering/results/{file_id}` - Get clustering results
- `GET /api/clustering/results/{file_id}/{result_id}` - Get specific result

### Notebooks
- `POST /api/notebooks/create` - Create notebook from data file
- `GET /api/notebooks/{session_id}` - Get notebook session

## Use Cases

### Intersight Alarms Clustering
Cluster alarms to identify underlying physical entities or root causes. Many alarms may be related to fewer physical entities than the number of alarms themselves.

**Recommended Algorithms**: HDBSCAN, DBSCAN

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database
- **Pandas**: Data manipulation
- **Scikit-learn**: Clustering algorithms
- **HDBSCAN**: HDBSCAN algorithm
- **Plotly**: Interactive visualizations

### Jupyter Notebook
- **Jupyter Lab**: Interactive notebook environment
- **IPywidgets**: Interactive widgets
- **Matplotlib/Seaborn**: Visualization
- **Plotly**: Interactive plots

## Development

### Backend Development
```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (when implemented)
pytest
```

### Database Migrations
```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Configuration

Key configuration options in `backend/app/config.py`:

- `DATABASE_URL`: Database connection string
- `UPLOAD_DIR`: Directory for uploaded files
- `MAX_FILE_SIZE`: Maximum file size (default: 100MB)
- `JUPYTER_SERVER_URL`: Jupyter server URL
- `SECRET_KEY`: Secret key for encryption
- `ENCRYPTION_KEY`: Key for encrypting device API keys

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is provided as-is for clustering experimentation and analysis.

## Roadmap

- [x] Frontend implementation (React)
- [x] Advanced visualization options
- [ ] User authentication and authorization
- [ ] Scheduled device sync
- [ ] Export clustering results in multiple formats
- [ ] Real-time clustering progress updates
- [ ] Comparison of multiple clustering algorithms
- [ ] Parameter optimization suggestions

## Support

For issues and questions, please open an issue on GitHub.
