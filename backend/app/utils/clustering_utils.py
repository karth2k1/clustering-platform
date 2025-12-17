"""Clustering utilities"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from typing import Tuple, Optional, Dict, Any, List
import hdbscan


def preprocess_data(df: pd.DataFrame) -> Tuple[Optional[np.ndarray], List[str]]:
    """
    Preprocess data for clustering
    
    Returns:
        Tuple of (processed_data_array, feature_names)
    """
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Filter out columns that are all NaN or have no variance
    valid_numeric_cols = []
    for col in numeric_cols:
        col_data = df[col]
        # Skip if all NaN or constant (no variance)
        if col_data.notna().sum() > 0 and col_data.nunique() > 1:
            valid_numeric_cols.append(col)
    
    numeric_cols = valid_numeric_cols
    
    if not numeric_cols:
        # If no valid numeric columns, encode categorical
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if not categorical_cols:
            return None, []
        
        # Filter categorical columns that have some variance
        valid_categorical_cols = []
        for col in categorical_cols:
            if df[col].nunique() > 1:  # At least 2 unique values
                valid_categorical_cols.append(col)
        
        if not valid_categorical_cols:
            return None, []
        
        # Encode categorical variables
        data = df[valid_categorical_cols].copy()
        for col in valid_categorical_cols:
            le = LabelEncoder()
            # Fill NaN with a placeholder before encoding
            data[col] = le.fit_transform(data[col].fillna('__MISSING__').astype(str))
        numeric_cols = valid_categorical_cols
    else:
        data = df[numeric_cols].copy()
    
    # Handle missing values - drop rows where ALL values are NaN
    # But keep rows where at least one value is present
    data = data.dropna(how='all')
    
    # Also drop columns that became all NaN after row drops
    data = data.dropna(axis=1, how='all')
    
    # Update numeric_cols to match remaining columns
    numeric_cols = [col for col in numeric_cols if col in data.columns]
    
    if len(data) == 0 or len(numeric_cols) == 0:
        return None, []
    
    # Fill remaining NaN values with column median (for numeric) or mode (for encoded categorical)
    for col in data.columns:
        if data[col].isna().any():
            if data[col].dtype in [np.number]:
                data[col].fillna(data[col].median(), inplace=True)
            else:
                data[col].fillna(data[col].mode()[0] if len(data[col].mode()) > 0 else 0, inplace=True)
    
    # Scale features
    scaler = StandardScaler()
    processed = scaler.fit_transform(data.values)
    
    return processed, numeric_cols


def select_algorithm(data: np.ndarray, metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Automatically select clustering algorithm based on data characteristics
    
    Args:
        data: Preprocessed data array
        metadata: File metadata
    
    Returns:
        Algorithm name
    """
    n_samples, n_features = data.shape
    
    # Heuristics for algorithm selection
    if n_samples < 10:
        return "K-Means"  # Too small for density-based
    
    # Check for noise (high variance, many outliers)
    if n_samples > 100:
        # For larger datasets with potential noise, prefer HDBSCAN
        return "HDBSCAN"
    elif n_samples > 50:
        # Medium datasets - DBSCAN or HDBSCAN
        return "DBSCAN"
    else:
        # Small datasets - K-Means
        return "K-Means"


def execute_clustering(
    data: np.ndarray,
    algorithm: str,
    custom_parameters: Optional[Dict[str, Any]] = None
) -> Tuple[np.ndarray, Any, Dict[str, Any]]:
    """
    Execute clustering algorithm
    
    Returns:
        Tuple of (cluster_labels, model, parameters_used)
    """
    n_samples = len(data)
    
    # Default parameters
    params = custom_parameters or {}
    
    if algorithm == "K-Means":
        n_clusters = params.get("n_clusters", min(3, n_samples // 3))
        n_clusters = max(2, min(n_clusters, n_samples))
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = model.fit_predict(data)
        return labels, model, {"n_clusters": n_clusters}
    
    elif algorithm == "DBSCAN":
        eps = params.get("eps", 0.5)
        min_samples = params.get("min_samples", max(5, n_samples // 20))
        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(data)
        return labels, model, {"eps": eps, "min_samples": min_samples}
    
    elif algorithm == "HDBSCAN":
        min_cluster_size = params.get("min_cluster_size", max(5, n_samples // 20))
        min_samples = params.get("min_samples", max(3, min_cluster_size // 2))
        model = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
        labels = model.fit_predict(data)
        return labels, model, {"min_cluster_size": min_cluster_size, "min_samples": min_samples}
    
    elif algorithm == "Hierarchical":
        n_clusters = params.get("n_clusters", min(3, n_samples // 3))
        n_clusters = max(2, min(n_clusters, n_samples))
        linkage = params.get("linkage", "ward")
        model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        labels = model.fit_predict(data)
        return labels, model, {"n_clusters": n_clusters, "linkage": linkage}
    
    elif algorithm == "GMM":
        n_components = params.get("n_components", min(3, n_samples // 3))
        n_components = max(2, min(n_components, n_samples))
        covariance_type = params.get("covariance_type", "full")
        model = GaussianMixture(n_components=n_components, covariance_type=covariance_type, random_state=42)
        labels = model.fit_predict(data)
        return labels, model, {"n_components": n_components, "covariance_type": covariance_type}
    
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def calculate_metrics(data: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
    """Calculate clustering metrics"""
    if len(set(labels)) < 2:
        return {}
    
    try:
        silhouette = silhouette_score(data, labels)
        davies_bouldin = davies_bouldin_score(data, labels)
        calinski_harabasz = calinski_harabasz_score(data, labels)
        
        return {
            "silhouette_score": float(silhouette),
            "davies_bouldin_index": float(davies_bouldin),
            "calinski_harabasz_index": float(calinski_harabasz),
            "n_clusters": int(len(set(labels))),
            "n_noise": int(np.sum(labels == -1)) if -1 in labels else 0
        }
    except Exception:
        return {}

