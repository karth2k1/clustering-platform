"""
Dataset Loading Utilities

This module provides utilities to download, prepare, and load sample datasets
for demonstrating the clustering platform's capabilities.

Supports:
- Iris Dataset (classic ML dataset)
- Customer Segmentation (business use case)
- Network Intrusion Detection (cybersecurity use case)
- NYC Taxi Data (geographical/spatial clustering)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import json
import urllib.request
import ssl

# Base paths
DATASETS_DIR = Path(__file__).parent.parent.parent.parent / "datasets" / "sample_data"
DOCS_DIR = Path(__file__).parent.parent.parent.parent / "datasets" / "documentation"

# Ensure directories exist
DATASETS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)


class DatasetLoader:
    """Main class for loading and preparing sample datasets"""
    
    @staticmethod
    def list_available_datasets() -> Dict[str, Dict[str, Any]]:
        """
        List all available sample datasets with their metadata
        
        Returns:
            Dictionary with dataset names as keys and metadata as values
        """
        return {
            "iris": {
                "name": "Iris Flower Classification",
                "description": "Classic dataset with 150 iris flowers and 4 measurements",
                "size": "150 records",
                "features": 4,
                "use_case": "Species classification, algorithm validation",
                "difficulty": "Easy",
                "recommended_for": "First-time users, algorithm testing",
                "natural_clusters": 3,
                "file": "iris.csv"
            },
            "customer_segmentation": {
                "name": "Mall Customer Segmentation",
                "description": "Customer demographics and spending behavior",
                "size": "200 records",
                "features": 5,
                "use_case": "Business segmentation, marketing insights",
                "difficulty": "Easy",
                "recommended_for": "Business users, stakeholder demos",
                "natural_clusters": 5,
                "file": "customer_segmentation.csv"
            },
            "network_intrusion": {
                "name": "Network Intrusion Detection (NSL-KDD Sample)",
                "description": "Network traffic patterns for anomaly detection",
                "size": "5000 records (sample)",
                "features": 41,
                "use_case": "Cybersecurity, anomaly detection",
                "difficulty": "Medium",
                "recommended_for": "IT operations, security analysts",
                "natural_clusters": "2-5 (normal + attack types)",
                "file": "network_intrusion.csv"
            },
            "nyc_taxi": {
                "name": "NYC Taxi Trip Sample",
                "description": "Taxi pickup/dropoff locations and trip details",
                "size": "10000 records (sample)",
                "features": 8,
                "use_case": "Geographical clustering, pattern discovery",
                "difficulty": "Medium",
                "recommended_for": "Spatial analysis, urban planning",
                "natural_clusters": "Variable (by location)",
                "file": "nyc_taxi.csv"
            }
        }
    
    @staticmethod
    def load_iris() -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load the Iris dataset
        
        Returns:
            Tuple of (DataFrame, metadata dictionary)
        """
        try:
            # Try to use sklearn's dataset (most reliable)
            from sklearn.datasets import load_iris
            iris = load_iris()
            
            # Create DataFrame
            df = pd.DataFrame(
                data=iris.data,
                columns=iris.feature_names
            )
            df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
            
            # Save to file
            output_path = DATASETS_DIR / "iris.csv"
            df.to_csv(output_path, index=False)
            
            metadata = {
                "name": "Iris Dataset",
                "source": "UCI Machine Learning Repository (via scikit-learn)",
                "records": len(df),
                "features": list(df.columns),
                "numeric_features": [col for col in df.columns if col != 'species'],
                "categorical_features": ['species'],
                "description": "Famous dataset containing measurements of 150 iris flowers from 3 species",
                "clustering_features": [
                    "sepal length (cm)",
                    "sepal width (cm)",
                    "petal length (cm)",
                    "petal width (cm)"
                ],
                "expected_clusters": 3,
                "use_case": "Validate that clustering algorithms correctly identify the 3 species"
            }
            
            return df, metadata
            
        except ImportError:
            # Fallback: create synthetic Iris-like data
            print("scikit-learn not available, creating synthetic Iris data...")
            return DatasetLoader._create_synthetic_iris()
    
    @staticmethod
    def _create_synthetic_iris() -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Create synthetic Iris-like data if sklearn is not available"""
        np.random.seed(42)
        
        # Generate 3 clusters with different characteristics
        n_per_cluster = 50
        
        # Cluster 1: Setosa (small petals, wide sepals)
        cluster1 = pd.DataFrame({
            'sepal length (cm)': np.random.normal(5.0, 0.3, n_per_cluster),
            'sepal width (cm)': np.random.normal(3.4, 0.3, n_per_cluster),
            'petal length (cm)': np.random.normal(1.5, 0.2, n_per_cluster),
            'petal width (cm)': np.random.normal(0.2, 0.1, n_per_cluster),
            'species': 'setosa'
        })
        
        # Cluster 2: Versicolor (medium size)
        cluster2 = pd.DataFrame({
            'sepal length (cm)': np.random.normal(5.9, 0.5, n_per_cluster),
            'sepal width (cm)': np.random.normal(2.8, 0.3, n_per_cluster),
            'petal length (cm)': np.random.normal(4.3, 0.5, n_per_cluster),
            'petal width (cm)': np.random.normal(1.3, 0.2, n_per_cluster),
            'species': 'versicolor'
        })
        
        # Cluster 3: Virginica (large flowers)
        cluster3 = pd.DataFrame({
            'sepal length (cm)': np.random.normal(6.5, 0.6, n_per_cluster),
            'sepal width (cm)': np.random.normal(3.0, 0.3, n_per_cluster),
            'petal length (cm)': np.random.normal(5.5, 0.5, n_per_cluster),
            'petal width (cm)': np.random.normal(2.0, 0.3, n_per_cluster),
            'species': 'virginica'
        })
        
        df = pd.concat([cluster1, cluster2, cluster3], ignore_index=True)
        
        # Shuffle
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save to file
        output_path = DATASETS_DIR / "iris.csv"
        df.to_csv(output_path, index=False)
        
        metadata = {
            "name": "Iris Dataset (Synthetic)",
            "source": "Synthetic data based on Iris characteristics",
            "records": len(df),
            "features": list(df.columns),
            "numeric_features": [col for col in df.columns if col != 'species'],
            "categorical_features": ['species'],
            "description": "Synthetic dataset mimicking Iris flower measurements",
            "clustering_features": [
                "sepal length (cm)",
                "sepal width (cm)",
                "petal length (cm)",
                "petal width (cm)"
            ],
            "expected_clusters": 3,
            "use_case": "Validate clustering algorithms"
        }
        
        return df, metadata
    
    @staticmethod
    def load_customer_segmentation() -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load or create Customer Segmentation dataset
        
        Returns:
            Tuple of (DataFrame, metadata dictionary)
        """
        np.random.seed(42)
        
        # Create synthetic customer data with clear segments
        n_customers = 200
        
        # Segment 1: Young Low Earners (budget conscious)
        seg1_size = 40
        seg1 = pd.DataFrame({
            'CustomerID': range(1, seg1_size + 1),
            'Gender': np.random.choice(['Male', 'Female'], seg1_size),
            'Age': np.random.randint(18, 30, seg1_size),
            'Annual Income (k$)': np.random.randint(15, 40, seg1_size),
            'Spending Score (1-100)': np.random.randint(30, 60, seg1_size)
        })
        
        # Segment 2: Young High Earners (high spending)
        seg2_size = 40
        seg2 = pd.DataFrame({
            'CustomerID': range(seg1_size + 1, seg1_size + seg2_size + 1),
            'Gender': np.random.choice(['Male', 'Female'], seg2_size),
            'Age': np.random.randint(25, 35, seg2_size),
            'Annual Income (k$)': np.random.randint(70, 100, seg2_size),
            'Spending Score (1-100)': np.random.randint(70, 100, seg2_size)
        })
        
        # Segment 3: Middle Age Middle Income (moderate)
        seg3_size = 40
        seg3 = pd.DataFrame({
            'CustomerID': range(seg1_size + seg2_size + 1, seg1_size + seg2_size + seg3_size + 1),
            'Gender': np.random.choice(['Male', 'Female'], seg3_size),
            'Age': np.random.randint(35, 55, seg3_size),
            'Annual Income (k$)': np.random.randint(40, 70, seg3_size),
            'Spending Score (1-100)': np.random.randint(40, 70, seg3_size)
        })
        
        # Segment 4: High Income Low Spending (savers)
        seg4_size = 40
        seg4 = pd.DataFrame({
            'CustomerID': range(seg1_size + seg2_size + seg3_size + 1, 
                              seg1_size + seg2_size + seg3_size + seg4_size + 1),
            'Gender': np.random.choice(['Male', 'Female'], seg4_size),
            'Age': np.random.randint(30, 60, seg4_size),
            'Annual Income (k$)': np.random.randint(70, 100, seg4_size),
            'Spending Score (1-100)': np.random.randint(10, 40, seg4_size)
        })
        
        # Segment 5: Seniors (varied)
        seg5_size = 40
        seg5 = pd.DataFrame({
            'CustomerID': range(seg1_size + seg2_size + seg3_size + seg4_size + 1, n_customers + 1),
            'Gender': np.random.choice(['Male', 'Female'], seg5_size),
            'Age': np.random.randint(55, 75, seg5_size),
            'Annual Income (k$)': np.random.randint(30, 80, seg5_size),
            'Spending Score (1-100)': np.random.randint(20, 70, seg5_size)
        })
        
        df = pd.concat([seg1, seg2, seg3, seg4, seg5], ignore_index=True)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save to file
        output_path = DATASETS_DIR / "customer_segmentation.csv"
        df.to_csv(output_path, index=False)
        
        metadata = {
            "name": "Mall Customer Segmentation",
            "source": "Synthetic customer data",
            "records": len(df),
            "features": list(df.columns),
            "numeric_features": ['Age', 'Annual Income (k$)', 'Spending Score (1-100)'],
            "categorical_features": ['Gender'],
            "description": "Customer demographics and spending patterns for segmentation",
            "clustering_features": ['Age', 'Annual Income (k$)', 'Spending Score (1-100)'],
            "expected_clusters": 5,
            "segments": {
                "1": "Young Budget Shoppers",
                "2": "Young High Spenders",
                "3": "Middle Age Moderate",
                "4": "High Income Savers",
                "5": "Senior Varied"
            },
            "use_case": "Identify customer segments for targeted marketing campaigns"
        }
        
        return df, metadata
    
    @staticmethod
    def load_network_intrusion() -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load or create Network Intrusion Detection dataset (NSL-KDD sample)
        
        Returns:
            Tuple of (DataFrame, metadata dictionary)
        """
        np.random.seed(42)
        
        # Create synthetic network traffic data with normal and attack patterns
        n_records = 5000
        n_normal = 3500
        n_attacks = n_records - n_normal
        
        # Normal traffic patterns
        normal_data = {
            'duration': np.random.exponential(50, n_normal),
            'src_bytes': np.random.lognormal(8, 2, n_normal),
            'dst_bytes': np.random.lognormal(7, 2, n_normal),
            'land': np.zeros(n_normal),
            'wrong_fragment': np.random.poisson(0.1, n_normal),
            'urgent': np.zeros(n_normal),
            'hot': np.random.poisson(0.5, n_normal),
            'num_failed_logins': np.zeros(n_normal),
            'logged_in': np.ones(n_normal),
            'num_compromised': np.zeros(n_normal),
            'root_shell': np.zeros(n_normal),
            'su_attempted': np.zeros(n_normal),
            'num_root': np.random.poisson(0.2, n_normal),
            'num_file_creations': np.random.poisson(0.3, n_normal),
            'num_shells': np.random.poisson(0.1, n_normal),
            'num_access_files': np.random.poisson(0.2, n_normal),
            'is_host_login': np.zeros(n_normal),
            'is_guest_login': np.random.choice([0, 1], n_normal, p=[0.95, 0.05]),
            'count': np.random.poisson(10, n_normal),
            'srv_count': np.random.poisson(8, n_normal),
            'serror_rate': np.random.beta(1, 20, n_normal),
            'srv_serror_rate': np.random.beta(1, 20, n_normal),
            'rerror_rate': np.random.beta(1, 30, n_normal),
            'srv_rerror_rate': np.random.beta(1, 30, n_normal),
            'same_srv_rate': np.random.beta(20, 2, n_normal),
            'diff_srv_rate': np.random.beta(2, 20, n_normal),
            'srv_diff_host_rate': np.random.beta(2, 10, n_normal),
            'dst_host_count': np.random.poisson(50, n_normal),
            'dst_host_srv_count': np.random.poisson(40, n_normal),
            'dst_host_same_srv_rate': np.random.beta(20, 2, n_normal),
            'dst_host_diff_srv_rate': np.random.beta(2, 20, n_normal),
            'dst_host_same_src_port_rate': np.random.beta(10, 10, n_normal),
            'dst_host_srv_diff_host_rate': np.random.beta(2, 10, n_normal),
            'dst_host_serror_rate': np.random.beta(1, 20, n_normal),
            'dst_host_srv_serror_rate': np.random.beta(1, 20, n_normal),
            'dst_host_rerror_rate': np.random.beta(1, 30, n_normal),
            'dst_host_srv_rerror_rate': np.random.beta(1, 30, n_normal),
            'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], n_normal, p=[0.7, 0.2, 0.1]),
            'service': np.random.choice(['http', 'smtp', 'ftp', 'ssh', 'telnet'], n_normal),
            'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH'], n_normal, p=[0.7, 0.1, 0.1, 0.05, 0.05]),
            'attack_type': 'normal'
        }
        
        # Attack patterns (DoS, Probe, R2L, U2R)
        attack_types = ['DoS', 'Probe', 'R2L', 'U2R']
        attacks_per_type = n_attacks // 4
        
        attack_data_list = []
        
        for attack in attack_types:
            if attack == 'DoS':  # Denial of Service - high traffic volume
                attack_data = {
                    'duration': np.random.exponential(10, attacks_per_type),
                    'src_bytes': np.random.lognormal(10, 1.5, attacks_per_type),
                    'dst_bytes': np.random.lognormal(4, 1, attacks_per_type),
                    'land': np.random.choice([0, 1], attacks_per_type, p=[0.7, 0.3]),
                    'wrong_fragment': np.random.poisson(2, attacks_per_type),
                    'urgent': np.random.poisson(1, attacks_per_type),
                    'hot': np.random.poisson(3, attacks_per_type),
                    'num_failed_logins': np.zeros(attacks_per_type),
                    'logged_in': np.zeros(attacks_per_type),
                    'num_compromised': np.zeros(attacks_per_type),
                    'root_shell': np.zeros(attacks_per_type),
                    'su_attempted': np.zeros(attacks_per_type),
                    'num_root': np.zeros(attacks_per_type),
                    'num_file_creations': np.zeros(attacks_per_type),
                    'num_shells': np.zeros(attacks_per_type),
                    'num_access_files': np.zeros(attacks_per_type),
                    'is_host_login': np.zeros(attacks_per_type),
                    'is_guest_login': np.zeros(attacks_per_type),
                    'count': np.random.poisson(100, attacks_per_type),
                    'srv_count': np.random.poisson(100, attacks_per_type),
                    'serror_rate': np.random.beta(10, 2, attacks_per_type),
                    'srv_serror_rate': np.random.beta(10, 2, attacks_per_type),
                    'rerror_rate': np.random.beta(1, 10, attacks_per_type),
                    'srv_rerror_rate': np.random.beta(1, 10, attacks_per_type),
                    'same_srv_rate': np.random.beta(20, 2, attacks_per_type),
                    'diff_srv_rate': np.random.beta(1, 20, attacks_per_type),
                    'srv_diff_host_rate': np.random.beta(1, 20, attacks_per_type),
                    'dst_host_count': np.random.poisson(200, attacks_per_type),
                    'dst_host_srv_count': np.random.poisson(200, attacks_per_type),
                    'dst_host_same_srv_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_diff_srv_rate': np.random.beta(1, 20, attacks_per_type),
                    'dst_host_same_src_port_rate': np.random.beta(2, 20, attacks_per_type),
                    'dst_host_srv_diff_host_rate': np.random.beta(1, 20, attacks_per_type),
                    'dst_host_serror_rate': np.random.beta(10, 2, attacks_per_type),
                    'dst_host_srv_serror_rate': np.random.beta(10, 2, attacks_per_type),
                    'dst_host_rerror_rate': np.random.beta(1, 10, attacks_per_type),
                    'dst_host_srv_rerror_rate': np.random.beta(1, 10, attacks_per_type),
                    'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], attacks_per_type, p=[0.3, 0.3, 0.4]),
                    'service': np.random.choice(['http', 'smtp', 'ftp', 'ssh', 'telnet'], attacks_per_type),
                    'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH'], attacks_per_type, p=[0.1, 0.5, 0.2, 0.1, 0.1]),
                    'attack_type': 'DoS'
                }
            elif attack == 'Probe':  # Port scanning
                attack_data = {
                    'duration': np.random.exponential(2, attacks_per_type),
                    'src_bytes': np.random.lognormal(3, 1, attacks_per_type),
                    'dst_bytes': np.random.lognormal(2, 1, attacks_per_type),
                    'land': np.zeros(attacks_per_type),
                    'wrong_fragment': np.zeros(attacks_per_type),
                    'urgent': np.zeros(attacks_per_type),
                    'hot': np.zeros(attacks_per_type),
                    'num_failed_logins': np.zeros(attacks_per_type),
                    'logged_in': np.zeros(attacks_per_type),
                    'num_compromised': np.zeros(attacks_per_type),
                    'root_shell': np.zeros(attacks_per_type),
                    'su_attempted': np.zeros(attacks_per_type),
                    'num_root': np.zeros(attacks_per_type),
                    'num_file_creations': np.zeros(attacks_per_type),
                    'num_shells': np.zeros(attacks_per_type),
                    'num_access_files': np.zeros(attacks_per_type),
                    'is_host_login': np.zeros(attacks_per_type),
                    'is_guest_login': np.zeros(attacks_per_type),
                    'count': np.random.poisson(200, attacks_per_type),
                    'srv_count': np.random.poisson(5, attacks_per_type),
                    'serror_rate': np.random.beta(20, 2, attacks_per_type),
                    'srv_serror_rate': np.random.beta(20, 2, attacks_per_type),
                    'rerror_rate': np.random.beta(20, 2, attacks_per_type),
                    'srv_rerror_rate': np.random.beta(2, 2, attacks_per_type),
                    'same_srv_rate': np.random.beta(2, 20, attacks_per_type),
                    'diff_srv_rate': np.random.beta(20, 2, attacks_per_type),
                    'srv_diff_host_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_count': np.random.poisson(255, attacks_per_type),
                    'dst_host_srv_count': np.random.poisson(10, attacks_per_type),
                    'dst_host_same_srv_rate': np.random.beta(2, 20, attacks_per_type),
                    'dst_host_diff_srv_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_same_src_port_rate': np.random.beta(2, 20, attacks_per_type),
                    'dst_host_srv_diff_host_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_serror_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_srv_serror_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_rerror_rate': np.random.beta(20, 2, attacks_per_type),
                    'dst_host_srv_rerror_rate': np.random.beta(5, 5, attacks_per_type),
                    'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], attacks_per_type, p=[0.6, 0.2, 0.2]),
                    'service': np.random.choice(['http', 'smtp', 'ftp', 'ssh', 'telnet'], attacks_per_type),
                    'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH'], attacks_per_type, p=[0.1, 0.6, 0.2, 0.05, 0.05]),
                    'attack_type': 'Probe'
                }
            elif attack == 'R2L':  # Remote to Local attacks
                attack_data = {
                    'duration': np.random.exponential(100, attacks_per_type),
                    'src_bytes': np.random.lognormal(6, 2, attacks_per_type),
                    'dst_bytes': np.random.lognormal(5, 2, attacks_per_type),
                    'land': np.zeros(attacks_per_type),
                    'wrong_fragment': np.zeros(attacks_per_type),
                    'urgent': np.zeros(attacks_per_type),
                    'hot': np.random.poisson(1, attacks_per_type),
                    'num_failed_logins': np.random.poisson(3, attacks_per_type),
                    'logged_in': np.random.choice([0, 1], attacks_per_type, p=[0.8, 0.2]),
                    'num_compromised': np.random.poisson(1, attacks_per_type),
                    'root_shell': np.random.choice([0, 1], attacks_per_type, p=[0.9, 0.1]),
                    'su_attempted': np.random.choice([0, 1], attacks_per_type, p=[0.8, 0.2]),
                    'num_root': np.random.poisson(1, attacks_per_type),
                    'num_file_creations': np.random.poisson(0.5, attacks_per_type),
                    'num_shells': np.random.poisson(0.5, attacks_per_type),
                    'num_access_files': np.random.poisson(1, attacks_per_type),
                    'is_host_login': np.zeros(attacks_per_type),
                    'is_guest_login': np.random.choice([0, 1], attacks_per_type, p=[0.3, 0.7]),
                    'count': np.random.poisson(5, attacks_per_type),
                    'srv_count': np.random.poisson(4, attacks_per_type),
                    'serror_rate': np.random.beta(1, 20, attacks_per_type),
                    'srv_serror_rate': np.random.beta(1, 20, attacks_per_type),
                    'rerror_rate': np.random.beta(5, 10, attacks_per_type),
                    'srv_rerror_rate': np.random.beta(5, 10, attacks_per_type),
                    'same_srv_rate': np.random.beta(15, 5, attacks_per_type),
                    'diff_srv_rate': np.random.beta(5, 15, attacks_per_type),
                    'srv_diff_host_rate': np.random.beta(3, 10, attacks_per_type),
                    'dst_host_count': np.random.poisson(10, attacks_per_type),
                    'dst_host_srv_count': np.random.poisson(8, attacks_per_type),
                    'dst_host_same_srv_rate': np.random.beta(15, 5, attacks_per_type),
                    'dst_host_diff_srv_rate': np.random.beta(5, 15, attacks_per_type),
                    'dst_host_same_src_port_rate': np.random.beta(10, 10, attacks_per_type),
                    'dst_host_srv_diff_host_rate': np.random.beta(3, 10, attacks_per_type),
                    'dst_host_serror_rate': np.random.beta(1, 20, attacks_per_type),
                    'dst_host_srv_serror_rate': np.random.beta(1, 20, attacks_per_type),
                    'dst_host_rerror_rate': np.random.beta(5, 10, attacks_per_type),
                    'dst_host_srv_rerror_rate': np.random.beta(5, 10, attacks_per_type),
                    'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], attacks_per_type, p=[0.9, 0.08, 0.02]),
                    'service': np.random.choice(['http', 'smtp', 'ftp', 'ssh', 'telnet'], attacks_per_type, p=[0.3, 0.2, 0.3, 0.1, 0.1]),
                    'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH'], attacks_per_type, p=[0.6, 0.2, 0.1, 0.05, 0.05]),
                    'attack_type': 'R2L'
                }
            else:  # U2R - User to Root attacks
                attack_data = {
                    'duration': np.random.exponential(200, attacks_per_type),
                    'src_bytes': np.random.lognormal(7, 1.5, attacks_per_type),
                    'dst_bytes': np.random.lognormal(6, 1.5, attacks_per_type),
                    'land': np.zeros(attacks_per_type),
                    'wrong_fragment': np.zeros(attacks_per_type),
                    'urgent': np.zeros(attacks_per_type),
                    'hot': np.random.poisson(5, attacks_per_type),
                    'num_failed_logins': np.random.poisson(1, attacks_per_type),
                    'logged_in': np.ones(attacks_per_type),
                    'num_compromised': np.random.poisson(5, attacks_per_type),
                    'root_shell': np.random.choice([0, 1], attacks_per_type, p=[0.3, 0.7]),
                    'su_attempted': np.random.choice([0, 1], attacks_per_type, p=[0.2, 0.8]),
                    'num_root': np.random.poisson(10, attacks_per_type),
                    'num_file_creations': np.random.poisson(5, attacks_per_type),
                    'num_shells': np.random.poisson(3, attacks_per_type),
                    'num_access_files': np.random.poisson(5, attacks_per_type),
                    'is_host_login': np.zeros(attacks_per_type),
                    'is_guest_login': np.zeros(attacks_per_type),
                    'count': np.random.poisson(3, attacks_per_type),
                    'srv_count': np.random.poisson(2, attacks_per_type),
                    'serror_rate': np.random.beta(1, 30, attacks_per_type),
                    'srv_serror_rate': np.random.beta(1, 30, attacks_per_type),
                    'rerror_rate': np.random.beta(1, 30, attacks_per_type),
                    'srv_rerror_rate': np.random.beta(1, 30, attacks_per_type),
                    'same_srv_rate': np.random.beta(18, 3, attacks_per_type),
                    'diff_srv_rate': np.random.beta(3, 18, attacks_per_type),
                    'srv_diff_host_rate': np.random.beta(2, 15, attacks_per_type),
                    'dst_host_count': np.random.poisson(15, attacks_per_type),
                    'dst_host_srv_count': np.random.poisson(12, attacks_per_type),
                    'dst_host_same_srv_rate': np.random.beta(18, 3, attacks_per_type),
                    'dst_host_diff_srv_rate': np.random.beta(3, 18, attacks_per_type),
                    'dst_host_same_src_port_rate': np.random.beta(10, 10, attacks_per_type),
                    'dst_host_srv_diff_host_rate': np.random.beta(2, 15, attacks_per_type),
                    'dst_host_serror_rate': np.random.beta(1, 30, attacks_per_type),
                    'dst_host_srv_serror_rate': np.random.beta(1, 30, attacks_per_type),
                    'dst_host_rerror_rate': np.random.beta(1, 30, attacks_per_type),
                    'dst_host_srv_rerror_rate': np.random.beta(1, 30, attacks_per_type),
                    'protocol_type': np.random.choice(['tcp', 'udp', 'icmp'], attacks_per_type, p=[0.95, 0.04, 0.01]),
                    'service': np.random.choice(['http', 'smtp', 'ftp', 'ssh', 'telnet'], attacks_per_type, p=[0.2, 0.2, 0.3, 0.2, 0.1]),
                    'flag': np.random.choice(['SF', 'S0', 'REJ', 'RSTR', 'SH'], attacks_per_type, p=[0.8, 0.05, 0.05, 0.05, 0.05]),
                    'attack_type': 'U2R'
                }
            
            attack_data_list.append(pd.DataFrame(attack_data))
        
        # Combine all data
        normal_df = pd.DataFrame(normal_data)
        all_attacks_df = pd.concat(attack_data_list, ignore_index=True)
        df = pd.concat([normal_df, all_attacks_df], ignore_index=True)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Save to file
        output_path = DATASETS_DIR / "network_intrusion.csv"
        df.to_csv(output_path, index=False)
        
        # Count attacks by type
        attack_counts = df['attack_type'].value_counts().to_dict()
        
        metadata = {
            "name": "Network Intrusion Detection (NSL-KDD Sample)",
            "source": "Synthetic data based on NSL-KDD characteristics",
            "records": len(df),
            "features": [col for col in df.columns if col != 'attack_type'],
            "numeric_features": [col for col in df.columns if df[col].dtype in ['int64', 'float64'] and col != 'attack_type'],
            "categorical_features": ['protocol_type', 'service', 'flag'],
            "label_column": "attack_type",
            "description": "Network traffic data with normal and attack patterns for intrusion detection",
            "clustering_features": [
                "duration", "src_bytes", "dst_bytes", "count", "srv_count",
                "serror_rate", "rerror_rate", "same_srv_rate", "diff_srv_rate"
            ],
            "attack_distribution": attack_counts,
            "attack_types": {
                "normal": "Normal network traffic",
                "DoS": "Denial of Service - overwhelm resources",
                "Probe": "Port scanning/surveillance",
                "R2L": "Remote to Local - unauthorized access from remote",
                "U2R": "User to Root - privilege escalation"
            },
            "expected_clusters": "2-5 (normal + attack categories)",
            "use_case": "Identify attack patterns and anomalies in network traffic"
        }
        
        return df, metadata
    
    @staticmethod
    def load_nyc_taxi() -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Load or create NYC Taxi Trip dataset (sample)
        
        Returns:
            Tuple of (DataFrame, metadata dictionary)
        """
        np.random.seed(42)
        
        # Create synthetic NYC taxi trip data
        n_records = 10000
        
        # NYC Manhattan bounding box (approximate)
        lat_min, lat_max = 40.700, 40.800
        lon_min, lon_max = -74.020, -73.930
        
        # Generate pickup and dropoff locations (clustered around hotspots)
        # Hotspots: Times Square, Financial District, Midtown, Upper East/West Side
        hotspots = [
            (40.758, -73.985, 'Times Square'),
            (40.707, -74.013, 'Financial District'),
            (40.755, -73.975, 'Midtown'),
            (40.775, -73.960, 'Upper East Side'),
            (40.785, -73.975, 'Upper West Side')
        ]
        
        pickup_data = []
        dropoff_data = []
        trip_distances = []
        trip_durations = []
        fares = []
        
        for _ in range(n_records):
            # Pick random hotspot for pickup
            hotspot = hotspots[np.random.choice(len(hotspots))]
            pickup_lat = np.random.normal(hotspot[0], 0.01)
            pickup_lon = np.random.normal(hotspot[1], 0.01)
            
            # Dropoff location (sometimes same hotspot, sometimes different)
            if np.random.random() < 0.4:  # 40% same area
                dropoff_lat = np.random.normal(pickup_lat, 0.005)
                dropoff_lon = np.random.normal(pickup_lon, 0.005)
                distance = np.random.exponential(2)  # Short trip
            else:  # Different area
                other_hotspot = hotspots[np.random.choice(len(hotspots))]
                dropoff_lat = np.random.normal(other_hotspot[0], 0.01)
                dropoff_lon = np.random.normal(other_hotspot[1], 0.01)
                distance = np.random.exponential(5) + 2  # Longer trip
            
            duration = distance * np.random.normal(5, 1) + np.random.normal(0, 3)  # minutes
            duration = max(1, duration)
            
            # Fare calculation (base + per mile + per minute)
            fare = 2.50 + (distance * 2.50) + (duration * 0.50) + np.random.normal(0, 2)
            fare = max(3.0, fare)
            
            pickup_data.append((pickup_lat, pickup_lon))
            dropoff_data.append((dropoff_lat, dropoff_lon))
            trip_distances.append(distance)
            trip_durations.append(duration)
            fares.append(fare)
        
        # Create DataFrame
        df = pd.DataFrame({
            'pickup_latitude': [p[0] for p in pickup_data],
            'pickup_longitude': [p[1] for p in pickup_data],
            'dropoff_latitude': [d[0] for d in dropoff_data],
            'dropoff_longitude': [d[1] for d in dropoff_data],
            'trip_distance_miles': trip_distances,
            'trip_duration_minutes': trip_durations,
            'fare_amount': fares,
            'passenger_count': np.random.choice([1, 2, 3, 4, 5], n_records, p=[0.7, 0.15, 0.08, 0.05, 0.02])
        })
        
        # Save to file
        output_path = DATASETS_DIR / "nyc_taxi.csv"
        df.to_csv(output_path, index=False)
        
        metadata = {
            "name": "NYC Taxi Trip Sample",
            "source": "Synthetic data based on NYC taxi patterns",
            "records": len(df),
            "features": list(df.columns),
            "numeric_features": list(df.columns),
            "categorical_features": [],
            "description": "NYC taxi trip data with pickup/dropoff locations and trip details",
            "clustering_features": {
                "spatial": ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"],
                "trip_characteristics": ["trip_distance_miles", "trip_duration_minutes", "fare_amount"]
            },
            "hotspots": [h[2] for h in hotspots],
            "expected_clusters": "5-10 (based on geographical hotspots and trip patterns)",
            "use_cases": [
                "Identify popular pickup/dropoff locations",
                "Discover trip patterns and routes",
                "Optimize taxi dispatch locations",
                "Identify pricing zones"
            ],
            "geographical_bounds": {
                "latitude": f"{lat_min} to {lat_max}",
                "longitude": f"{lon_min} to {lon_max}",
                "area": "Manhattan, NYC"
            }
        }
        
        return df, metadata
    
    @staticmethod
    def save_metadata(dataset_name: str, metadata: Dict[str, Any]):
        """Save dataset metadata to JSON file"""
        output_path = DOCS_DIR / f"{dataset_name}_metadata.json"
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"Metadata saved to: {output_path}")
    
    @staticmethod
    def get_dataset_path(dataset_name: str) -> Path:
        """Get the file path for a dataset"""
        datasets = DatasetLoader.list_available_datasets()
        if dataset_name in datasets:
            return DATASETS_DIR / datasets[dataset_name]['file']
        return None


def generate_all_datasets():
    """
    Generate all sample datasets and their documentation
    Useful for initial setup
    """
    loader = DatasetLoader()
    
    print("=" * 60)
    print("GENERATING SAMPLE DATASETS FOR CLUSTERING PLATFORM")
    print("=" * 60)
    
    # 1. Iris Dataset
    print("\n1. Loading Iris Dataset...")
    iris_df, iris_meta = loader.load_iris()
    loader.save_metadata("iris", iris_meta)
    print(f"   ✓ Created: {len(iris_df)} records")
    print(f"   ✓ Features: {', '.join(iris_meta['numeric_features'])}")
    
    # 2. Customer Segmentation
    print("\n2. Creating Customer Segmentation Dataset...")
    customer_df, customer_meta = loader.load_customer_segmentation()
    loader.save_metadata("customer_segmentation", customer_meta)
    print(f"   ✓ Created: {len(customer_df)} records")
    print(f"   ✓ Segments: {len(customer_meta['segments'])}")
    
    # 3. Network Intrusion Detection
    print("\n3. Creating Network Intrusion Detection Dataset...")
    network_df, network_meta = loader.load_network_intrusion()
    loader.save_metadata("network_intrusion", network_meta)
    print(f"   ✓ Created: {len(network_df)} records")
    print(f"   ✓ Attack types: {list(network_meta['attack_distribution'].keys())}")
    
    # 4. NYC Taxi
    print("\n4. Creating NYC Taxi Dataset...")
    taxi_df, taxi_meta = loader.load_nyc_taxi()
    loader.save_metadata("nyc_taxi", taxi_meta)
    print(f"   ✓ Created: {len(taxi_df)} records")
    print(f"   ✓ Hotspots: {', '.join(taxi_meta['hotspots'])}")
    
    print("\n" + "=" * 60)
    print("DATASET GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nDatasets saved to: {DATASETS_DIR}")
    print(f"Documentation saved to: {DOCS_DIR}")
    print("\nAvailable datasets:")
    for name, info in loader.list_available_datasets().items():
        if (DATASETS_DIR / info['file']).exists():
            print(f"  ✓ {info['name']}")


if __name__ == "__main__":
    # Generate all datasets when run directly
    generate_all_datasets()

