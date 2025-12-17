# Clustering Platform Architecture & Design

## Overview

The Clustering Platform is a comprehensive system for analyzing alarm and event data using machine learning clustering algorithms. It provides both AI-assisted automated clustering and advanced manual analysis capabilities.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  AI Mode     │  │ Advanced Mode│  │  Components  │    │
│  │  - Upload    │  │ - Notebooks  │  │  - Drawers   │    │
│  │  - Cluster   │  │ - Analysis   │  │  - Views     │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI + Python)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  API Layer   │  │  Services    │  │  Utils       │    │
│  │  - Files     │  │  - Clustering│  │  - Parsing   │    │
│  │  - Devices   │  │  - Analysis  │  │  - Viz       │    │
│  │  - Clustering│  │  - Files     │  │  - Clustering│    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQLAlchemy ORM
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Database (SQLite)                         │
│  - DataFiles                                                │
│  - ClusteringResults                                         │
│  - Devices                                                  │
│  - NotebookSessions                                         │
└─────────────────────────────────────────────────────────────┘
```

## Clustering Approach

### Data Preprocessing Pipeline

#### 1. Data Ingestion
- **File Types Supported**: CSV, JSON (including nested structures)
- **JSON Parsing**: Handles multiple formats:
  - Array of objects: `[{...}, {...}]`
  - API response format: `{"Results": [{...}, {...}]}`
  - Nested objects with arrays
- **Flattening**: Nested JSON structures are flattened with separator (`_`)
  - Example: `AffectedMo.Moid` → `AffectedMo_Moid`

#### 2. Feature Selection & Encoding

**Step 1: Numeric Column Detection**
```python
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
```
- Identifies columns with numeric data types
- Filters out columns that are:
  - All NaN
  - Constant (no variance)

**Step 2: Categorical Encoding (if no numeric columns)**
```python
if not numeric_cols:
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    # Filter for variance (at least 2 unique values)
    # Encode using LabelEncoder
```
- Uses LabelEncoder to convert categorical strings to numeric values
- Handles missing values with placeholder (`__MISSING__`)

**Step 3: Feature Scaling**
```python
scaler = StandardScaler()
processed = scaler.fit_transform(data.values)
```
- Standardizes features to have mean=0 and std=1
- Critical for distance-based clustering algorithms

#### 3. Algorithm Selection

**Automatic Selection Logic**:
```python
if n_samples < 10:
    return "K-Means"  # Too small for density-based
elif n_samples > 100:
    return "HDBSCAN"  # Best for larger datasets with noise
elif n_samples > 50:
    return "DBSCAN"   # Medium datasets
else:
    return "K-Means"  # Small datasets
```

**Algorithm Characteristics**:

| Algorithm | Use Case | Handles Noise | Parameters |
|-----------|----------|---------------|------------|
| **HDBSCAN** | Large datasets (>100 samples) | Yes (returns -1) | min_cluster_size, min_samples |
| **DBSCAN** | Medium datasets (50-100) | Yes (returns -1) | eps, min_samples |
| **K-Means** | Small datasets (<50) | No | n_clusters |
| **Hierarchical** | Medium datasets | No | n_clusters, linkage |
| **GMM** | Medium datasets | No | n_components |

#### 4. Clustering Execution

**HDBSCAN (Default for large datasets)**:
```python
min_cluster_size = max(5, n_samples // 20)
min_samples = max(3, min_cluster_size // 2)
model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
labels = model.fit_predict(data)
```

**Why Same Alarm Codes Are in Different Clusters**:
- Clustering uses **all features** (typically 20-50+ encoded categorical columns)
- Alarms with same code but different:
  - Affected object types
  - Object identifiers (Moid, DisplayName)
  - Relationships and metadata
  - Temporal patterns
- Form separate clusters → helps identify **which specific objects/systems** are affected

#### 5. Metrics Calculation

**Metrics Computed**:
- **Silhouette Score**: Measures how similar objects are to their own cluster vs other clusters (-1 to 1, higher is better)
- **Davies-Bouldin Index**: Average similarity ratio of clusters (lower is better)
- **Calinski-Harabasz Index**: Ratio of between-cluster to within-cluster variance (higher is better)

**Noise Handling**:
- Noise points (label = -1) are excluded from metrics calculation
- Metrics computed only on valid clusters (>1 cluster, no noise)

### Visualization Generation

**Dimensionality Reduction**:
- If features > 2: Uses PCA to reduce to 2D
- Preserves explained variance information
- Creates interactive Plotly HTML visualizations

**Visualization Features**:
- Color-coded clusters
- Noise points shown in gray with 'x' marker
- Hover tooltips with coordinates
- Responsive layout

## Data Flow

### Clustering Request Flow

```
1. User uploads file → FileService.process_file()
   ├─ Validates file (type, size)
   ├─ Saves to disk
   ├─ Parses JSON/CSV
   └─ Extracts metadata (shape, columns, dtypes)

2. User clicks "Run Auto Clustering" → ClusteringService.auto_cluster()
   ├─ Loads data file
   ├─ Preprocesses data (preprocess_data())
   │  ├─ Selects/encodes features
   │  └─ Scales features
   ├─ Selects algorithm (select_algorithm())
   ├─ Executes clustering (execute_clustering())
   ├─ Calculates metrics (calculate_metrics())
   ├─ Generates visualization (create_clustering_visualization())
   └─ Saves result to database

3. User views results → ClusterAnalysisService.analyze_clusters()
   ├─ Loads original data
   ├─ Analyzes each cluster
   ├─ Generates executive summary
   └─ Returns insights and recommendations
```

## Database Schema

### Core Tables

**DataFile**:
- Stores uploaded file metadata
- Tracks processing status (PENDING, PROCESSING, COMPLETED, FAILED)
- Contains file metadata (shape, columns, dtypes)

**ClusteringResult**:
- Links to DataFile
- Stores algorithm, parameters, cluster_labels (JSON array)
- Contains metrics (JSON object)
- References visualization path

**Device**:
- Manages data source configurations
- Stores encrypted API keys
- Tracks sync status

## API Endpoints

### Clustering Endpoints

- `POST /api/clustering/auto` - Run automatic clustering
- `GET /api/clustering/results/{file_id}` - Get all results for a file
- `GET /api/clustering/results/{file_id}/{result_id}` - Get specific result
- `GET /api/clustering/analysis/{result_id}` - Get cluster analysis
- `GET /api/clustering/analysis/{result_id}/cluster/{cluster_id}` - Get cluster details
- `GET /api/clustering/analysis/{result_id}/noise` - Get noise points

## Frontend Architecture

### Component Structure

```
ClusteringResults (Main Container)
├─ View Toggle (Executive / Data Scientist)
├─ ExecutiveView
│  ├─ Cluster Cards (clickable)
│  ├─ Insights Section
│  └─ Recommendations
├─ DataScientistView
│  ├─ Metrics Display
│  ├─ Parameters
│  └─ Interactive Visualization
└─ ClusterDetailDrawer
   ├─ Importance Section
   ├─ Alarms List
   └─ Alarm Detail View
```

### State Management

- Uses React Query for server state
- Local state for UI (selected cluster, view mode)
- Props drilling for component communication

## Key Design Decisions

### 1. Multi-Dimensional Clustering
**Decision**: Use all available features, not just alarm code
**Rationale**: 
- Identifies patterns across multiple dimensions
- Same alarm code on different objects = different clusters
- Provides actionable insights (which objects affected)

### 2. Automatic Algorithm Selection
**Decision**: Auto-select algorithm based on dataset size
**Rationale**:
- HDBSCAN best for large datasets with noise
- K-Means simpler for small datasets
- Reduces user decision burden

### 3. Categorical Encoding
**Decision**: Encode all categorical columns when no numeric columns
**Rationale**:
- Enables clustering on text/categorical data
- Preserves information through encoding
- Handles missing values gracefully

### 4. Noise Point Handling
**Decision**: Use density-based algorithms that identify noise
**Rationale**:
- Real-world data has outliers
- Noise points may represent unique cases
- Provides visibility into edge cases

### 5. Dual View System
**Decision**: Separate Executive and Data Scientist views
**Rationale**:
- Different user personas need different information
- Executive: Business insights, recommendations
- Data Scientist: Technical metrics, controls

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Cluster details loaded only when drawer opens
2. **Query Caching**: React Query caches analysis results
3. **Pagination**: File lists paginated (default 100 per page)
4. **Async Processing**: File processing happens asynchronously
5. **Static File Serving**: Visualizations served as static HTML

### Scalability

- Database: SQLite suitable for single-instance deployment
- File Storage: Local filesystem (can be migrated to S3/Object storage)
- API: FastAPI handles async requests efficiently
- Frontend: React Query handles caching and refetching

## Security Considerations

### Data Protection

- API keys encrypted using cryptography library
- File uploads validated (type, size)
- SQL injection prevented via SQLAlchemy ORM
- CORS configured for frontend origin

### Best Practices

- No hardcoded credentials
- Environment variables for secrets
- Input validation on all endpoints
- Error messages don't expose internals

## Future Enhancements

### Planned Features

1. **Feature Selection UI**: Allow users to select which features to use
2. **Algorithm Tuning**: Interactive parameter adjustment
3. **Comparison View**: Compare multiple clustering results
4. **Export Functionality**: Export clusters and analysis
5. **Real-time Updates**: WebSocket for progress updates
6. **Advanced Metrics**: Additional clustering quality metrics
7. **Feature Importance**: Show which features drive clustering

### Technical Debt

- Migrate to PostgreSQL for production
- Add comprehensive test coverage
- Implement proper logging
- Add monitoring and alerting
- Refactor large service files

## References

- **HDBSCAN**: https://hdbscan.readthedocs.io/
- **Scikit-learn**: https://scikit-learn.org/
- **FastAPI**: https://fastapi.tiangolo.com/
- **React Query**: https://tanstack.com/query

