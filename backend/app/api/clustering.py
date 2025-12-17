"""Clustering API endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.schemas import ClusteringRequest, ClusteringResultResponse
from app.services.clustering_service import ClusteringService
from app.services.cluster_analysis_service import ClusterAnalysisService

router = APIRouter(prefix="/api/clustering", tags=["clustering"])


@router.post("/auto", response_model=ClusteringResultResponse)
def auto_cluster(request: ClusteringRequest, db: Session = Depends(get_db)):
    """Run automatic clustering on a data file"""
    result, error = ClusteringService.auto_cluster(
        db=db,
        data_file_id=request.data_file_id,
        algorithm=request.algorithm,
        custom_parameters=request.parameters
    )
    
    if error:
        raise HTTPException(status_code=400, detail=error)
    
    return ClusteringResultResponse.model_validate(result)


@router.get("/results/{file_id}", response_model=List[ClusteringResultResponse])
def get_clustering_results(file_id: str, db: Session = Depends(get_db)):
    """Get all clustering results for a data file"""
    results = ClusteringService.get_clustering_results(db, file_id)
    return [ClusteringResultResponse.model_validate(r) for r in results]


@router.get("/results/{file_id}/{result_id}", response_model=ClusteringResultResponse)
def get_clustering_result(file_id: str, result_id: str, db: Session = Depends(get_db)):
    """Get specific clustering result"""
    result = ClusteringService.get_clustering_result(db, result_id)
    if not result or result.data_file_id != file_id:
        raise HTTPException(status_code=404, detail="Clustering result not found")
    return ClusteringResultResponse.model_validate(result)


@router.get("/analysis/{result_id}")
def get_cluster_analysis(result_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get cluster analysis and insights for a clustering result"""
    analysis = ClusterAnalysisService.analyze_clusters(db, result_id)
    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])
    return analysis

