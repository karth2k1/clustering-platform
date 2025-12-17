"""Notebook generation service"""
import nbformat as nbf
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Tuple, Optional
from app.models import NotebookSession, NotebookStatus, DataFile
from app.services.file_service import FileService
from app.config import settings, NOTEBOOK_DIR
from datetime import datetime


class NotebookService:
    """Service for notebook generation and management"""
    
    @staticmethod
    def create_notebook(
        db: Session,
        data_file_id: str
    ) -> Tuple[Optional[NotebookSession], str, Optional[str]]:
        """
        Create a notebook from a data file
        
        Returns:
            Tuple of (NotebookSession, notebook_url, error_message)
        """
        try:
            # Get data file
            data_file = FileService.get_file(db, data_file_id)
            if not data_file:
                return None, "", "Data file not found"
            
            # Generate notebook
            notebook_path = NotebookService._generate_notebook(data_file)
            
            # Create notebook session
            session = NotebookSession(
                data_file_id=data_file_id,
                notebook_path=str(notebook_path.relative_to(NOTEBOOK_DIR)),
                status=NotebookStatus.CREATED
            )
            
            db.add(session)
            db.commit()
            db.refresh(session)
            
            # Generate Jupyter URL
            notebook_url = f"{settings.JUPYTER_SERVER_URL}/notebooks/{notebook_path.name}"
            if settings.JUPYTER_TOKEN:
                notebook_url += f"?token={settings.JUPYTER_TOKEN}"
            
            return session, notebook_url, None
            
        except Exception as e:
            db.rollback()
            return None, "", f"Error creating notebook: {str(e)}"
    
    @staticmethod
    def _generate_notebook(data_file: DataFile) -> Path:
        """Generate notebook file from template"""
        # Create notebook
        nb = nbf.v4.new_notebook()
        
        # Add cells
        nb.cells.append(nbf.v4.new_markdown_cell(
            f"# Clustering Analysis - {data_file.original_filename}\n\n"
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ))
        
        # Imports cell
        nb.cells.append(nbf.v4.new_code_cell(
            """# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
import hdbscan
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score"""
        ))
        
        # Data loading cell
        file_path = FileService.get_file_path_for_download(data_file)
        nb.cells.append(nbf.v4.new_code_cell(
            f"""# Load Data
file_path = r"{file_path}"
"""
            + (f"""
# Load JSON file
import json
with open(file_path, 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)
""" if data_file.file_type.value == "JSON" else f"""
# Load CSV file
df = pd.read_csv(file_path)
""") + """
print(f"Data shape: {df.shape}")
print(f"\\nColumns: {df.columns.tolist()}")
df.head()
"""
        ))
        
        # Data exploration cell
        nb.cells.append(nbf.v4.new_code_cell(
            """# Data Exploration
df.info()
df.describe()
df.isnull().sum()
"""
        ))
        
        # Preprocessing cell
        nb.cells.append(nbf.v4.new_code_cell(
            """# Preprocessing
# Select numeric columns
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
data = df[numeric_cols].dropna()

# Scale features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data)
scaled_df = pd.DataFrame(scaled_data, columns=numeric_cols)

print(f"Processed data shape: {scaled_df.shape}")
"""
        ))
        
        # Clustering cell
        nb.cells.append(nbf.v4.new_code_cell(
            """# Clustering
# Example: HDBSCAN
import hdbscan
clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=3)
cluster_labels = clusterer.fit_predict(scaled_data)

print(f"Number of clusters: {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)}")
print(f"Number of noise points: {int(np.sum(cluster_labels == -1))}")
"""
        ))
        
        # Visualization cell
        nb.cells.append(nbf.v4.new_code_cell(
            """# Visualization
# Reduce dimensions for visualization
pca = PCA(n_components=2)
data_2d = pca.fit_transform(scaled_data)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(data_2d[:, 0], data_2d[:, 1], c=cluster_labels, cmap='viridis', alpha=0.7)
plt.colorbar(scatter)
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('Clustering Results')
plt.show()
"""
        ))
        
        # Metrics cell
        nb.cells.append(nbf.v4.new_code_cell(
            """# Metrics
# Filter out noise for metrics
valid_mask = cluster_labels != -1
if valid_mask.sum() > 1 and len(set(cluster_labels[valid_mask])) > 1:
    silhouette = silhouette_score(scaled_data[valid_mask], cluster_labels[valid_mask])
    davies_bouldin = davies_bouldin_score(scaled_data[valid_mask], cluster_labels[valid_mask])
    calinski_harabasz = calinski_harabasz_score(scaled_data[valid_mask], cluster_labels[valid_mask])
    
    print(f"Silhouette Score: {silhouette:.4f}")
    print(f"Davies-Bouldin Index: {davies_bouldin:.4f}")
    print(f"Calinski-Harabasz Index: {calinski_harabasz:.4f}")
"""
        ))
        
        # Save notebook
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        notebook_filename = f"clustering_{data_file.id[:8]}_{timestamp}.ipynb"
        notebook_path = NOTEBOOK_DIR / notebook_filename
        
        with open(notebook_path, 'w') as f:
            nbf.write(nb, f)
        
        return notebook_path
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[NotebookSession]:
        """Get notebook session by ID"""
        return db.query(NotebookSession).filter(NotebookSession.id == session_id).first()

