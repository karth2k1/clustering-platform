"""Clustering service with automatic algorithm selection"""
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, Tuple, List
from pathlib import Path
from app.models import DataFile, ClusteringResult, FileType, ProcessingStatus
from app.services.file_service import FileService
from app.utils.json_parser import parse_json_file
from app.utils.clustering_utils import (
    select_algorithm,
    preprocess_data,
    execute_clustering,
    calculate_metrics
)
from app.config import settings


class ClusteringService:
    """Service for clustering operations"""
    
    @staticmethod
    def auto_cluster(
        db: Session,
        data_file_id: str,
        algorithm: Optional[str] = None,
        custom_parameters: Optional[Dict[str, Any]] = None
    ) -> Tuple[Optional[ClusteringResult], Optional[str]]:
        """
        Automatically cluster data from a file
        
        Args:
            db: Database session
            data_file_id: Data file ID
            algorithm: Optional algorithm name (if None, auto-select)
            custom_parameters: Optional custom parameters
        
        Returns:
            Tuple of (ClusteringResult, error_message)
        """
        try:
            # Get data file
            data_file = FileService.get_file(db, data_file_id)
            if not data_file:
                return None, "Data file not found"
            
            if data_file.processing_status != ProcessingStatus.COMPLETED:
                return None, f"File processing not completed. Status: {data_file.processing_status}"
            
            # Load data
            file_path = FileService.get_file_path_for_download(data_file)
            if not file_path.exists():
                return None, "File not found on disk"
            
            # Load DataFrame
            if data_file.file_type == FileType.JSON:
                df, error = parse_json_file(file_path)
            else:
                df, error = pd.read_csv(file_path), None
            
            if error:
                return None, f"Error loading file: {error}"
            
            if df.empty:
                return None, "Data file is empty"
            
            # Preprocess data
            processed_data, feature_names = preprocess_data(df)
            
            if processed_data is None or len(processed_data) == 0:
                return None, "Preprocessing failed or resulted in empty data"
            
            # Select algorithm if not specified
            if not algorithm:
                algorithm = select_algorithm(processed_data, data_file.metadata)
            
            # Execute clustering
            cluster_labels, model, parameters = execute_clustering(
                processed_data,
                algorithm,
                custom_parameters
            )
            
            if cluster_labels is None:
                return None, "Clustering failed"
            
            # Calculate metrics (only if we have valid clusters)
            metrics = None
            if len(set(cluster_labels)) > 1 and -1 not in cluster_labels:
                metrics = calculate_metrics(processed_data, cluster_labels)
            elif len(set([l for l in cluster_labels if l != -1])) > 1:
                # Filter out noise for metrics
                valid_mask = np.array(cluster_labels) != -1
                if valid_mask.sum() > 1:
                    metrics = calculate_metrics(
                        processed_data[valid_mask],
                        np.array(cluster_labels)[valid_mask]
                    )
            
            # Save visualization (optional, can be done async)
            visualization_path = None  # TODO: Generate and save visualization
            
            # Create clustering result
            result = ClusteringResult(
                data_file_id=data_file_id,
                algorithm=algorithm,
                parameters=parameters,
                cluster_labels=cluster_labels.tolist() if isinstance(cluster_labels, np.ndarray) else cluster_labels,
                metrics=metrics,
                visualization_path=visualization_path
            )
            
            db.add(result)
            db.commit()
            db.refresh(result)
            
            return result, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error during clustering: {str(e)}"
    
    @staticmethod
    def get_clustering_results(db: Session, data_file_id: str) -> List[ClusteringResult]:
        """Get all clustering results for a data file"""
        return db.query(ClusteringResult).filter(
            ClusteringResult.data_file_id == data_file_id
        ).order_by(ClusteringResult.created_at.desc()).all()
    
    @staticmethod
    def get_clustering_result(db: Session, result_id: str) -> Optional[ClusteringResult]:
        """Get clustering result by ID"""
        return db.query(ClusteringResult).filter(ClusteringResult.id == result_id).first()

