"""Service for analyzing clusters and generating insights"""
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from app.models import DataFile, ClusteringResult, FileType
from app.services.file_service import FileService
from app.utils.json_parser import parse_json_file
from collections import Counter


class ClusterAnalysisService:
    """Service for analyzing clustering results and generating insights"""
    
    @staticmethod
    def analyze_clusters(
        db: Session,
        result_id: str
    ) -> Dict[str, Any]:
        """
        Analyze clusters and generate insights
        
        Returns:
            Dictionary with cluster analysis and insights
        """
        try:
            # Get clustering result
            result = db.query(ClusteringResult).filter(ClusteringResult.id == result_id).first()
            if not result:
                return {"error": "Clustering result not found"}
            
            # Get data file
            data_file = FileService.get_file(db, result.data_file_id)
            if not data_file:
                return {"error": "Data file not found"}
            
            # Load original data
            file_path = FileService.get_file_path_for_download(data_file)
            if data_file.file_type == FileType.JSON:
                df, error = parse_json_file(file_path)
            else:
                df, error = pd.read_csv(file_path), None
            
            if error or df is None or df.empty:
                return {"error": f"Error loading data: {error}"}
            
            # Add cluster labels
            cluster_labels = np.array(result.cluster_labels)
            df['cluster'] = cluster_labels
            
            # Analyze clusters
            unique_clusters = sorted([c for c in set(cluster_labels) if c != -1])
            noise_count = int(np.sum(cluster_labels == -1))
            
            cluster_insights = []
            
            for cluster_id in unique_clusters:
                cluster_data = df[df['cluster'] == cluster_id]
                insight = ClusterAnalysisService._analyze_single_cluster(
                    cluster_id, cluster_data, len(df)
                )
                cluster_insights.append(insight)
            
            # Generate executive summary
            executive_summary = ClusterAnalysisService._generate_executive_summary(
                cluster_insights, noise_count, len(df), data_file.original_filename
            )
            
            return {
                "cluster_insights": cluster_insights,
                "executive_summary": executive_summary,
                "total_clusters": len(unique_clusters),
                "noise_points": noise_count,
                "total_points": len(df)
            }
            
        except Exception as e:
            return {"error": f"Error analyzing clusters: {str(e)}"}
    
    @staticmethod
    def _analyze_single_cluster(
        cluster_id: int,
        cluster_data: pd.DataFrame,
        total_rows: int
    ) -> Dict[str, Any]:
        """Analyze a single cluster"""
        cluster_size = len(cluster_data)
        percentage = (cluster_size / total_rows) * 100
        
        # Find key columns to analyze (common patterns)
        key_columns = [
            'Code', 'OrigSeverity', 'AffectedMoType', 'AffectedMoDisplayName',
            'Name', 'Description', 'Acknowledge', 'LifeCycleState'
        ]
        
        characteristics = {}
        top_values = {}
        
        for col in key_columns:
            if col in cluster_data.columns:
                value_counts = cluster_data[col].value_counts()
                if len(value_counts) > 0:
                    top_val = value_counts.index[0]
                    count = value_counts.values[0]
                    top_values[col] = {
                        "value": str(top_val),
                        "count": int(count),
                        "percentage": float((count / cluster_size) * 100)
                    }
        
        # Generate cluster description
        description = ClusterAnalysisService._generate_cluster_description(
            cluster_id, cluster_size, top_values
        )
        
        return {
            "cluster_id": cluster_id,
            "size": cluster_size,
            "percentage": round(percentage, 1),
            "characteristics": top_values,
            "description": description,
            "key_attributes": ClusterAnalysisService._extract_key_attributes(top_values)
        }
    
    @staticmethod
    def _generate_cluster_description(
        cluster_id: int,
        size: int,
        top_values: Dict[str, Any]
    ) -> str:
        """Generate human-readable cluster description"""
        parts = []
        
        # Severity
        if 'OrigSeverity' in top_values:
            severity = top_values['OrigSeverity']['value']
            parts.append(f"{severity} severity")
        
        # Alarm code
        if 'Code' in top_values:
            code = top_values['Code']['value']
            parts.append(f"alarm code {code}")
        
        # Affected object type
        if 'AffectedMoType' in top_values:
            mo_type = top_values['AffectedMoType']['value']
            # Clean up type name
            mo_type_clean = mo_type.split('.')[-1] if '.' in mo_type else mo_type
            parts.append(f"affecting {mo_type_clean} objects")
        
        if parts:
            return f"Cluster {cluster_id}: {size} alarms with {', '.join(parts)}"
        else:
            return f"Cluster {cluster_id}: {size} alarms"
    
    @staticmethod
    def _extract_key_attributes(top_values: Dict[str, Any]) -> List[str]:
        """Extract key attributes for quick reference"""
        attributes = []
        
        if 'Code' in top_values:
            attributes.append(f"Code: {top_values['Code']['value']}")
        if 'OrigSeverity' in top_values:
            attributes.append(f"Severity: {top_values['OrigSeverity']['value']}")
        if 'AffectedMoType' in top_values:
            mo_type = top_values['AffectedMoType']['value']
            mo_type_clean = mo_type.split('.')[-1] if '.' in mo_type else mo_type
            attributes.append(f"Type: {mo_type_clean}")
        
        return attributes
    
    @staticmethod
    def _generate_executive_summary(
        cluster_insights: List[Dict[str, Any]],
        noise_count: int,
        total_points: int,
        filename: str
    ) -> Dict[str, Any]:
        """Generate executive-friendly summary"""
        
        # Sort clusters by size
        sorted_clusters = sorted(cluster_insights, key=lambda x: x['size'], reverse=True)
        
        # Find largest cluster
        largest_cluster = sorted_clusters[0] if sorted_clusters else None
        
        # Count by severity
        severity_counts = {}
        for cluster in cluster_insights:
            if 'OrigSeverity' in cluster.get('characteristics', {}):
                severity = cluster['characteristics']['OrigSeverity']['value']
                severity_counts[severity] = severity_counts.get(severity, 0) + cluster['size']
        
        # Generate insights
        insights = []
        
        if largest_cluster:
            insights.append({
                "type": "primary",
                "title": "Largest Issue Group",
                "description": f"{largest_cluster['size']} alarms ({largest_cluster['percentage']}%) share similar characteristics: {largest_cluster['description']}"
            })
        
        if severity_counts:
            critical_count = severity_counts.get('Critical', 0)
            if critical_count > 0:
                insights.append({
                    "type": "critical",
                    "title": "Critical Alarms",
                    "description": f"{critical_count} critical alarms identified across {len([c for c in cluster_insights if c['characteristics'].get('OrigSeverity', {}).get('value') == 'Critical'])}) clusters"
                })
        
        if noise_count > 0:
            noise_pct = (noise_count / total_points) * 100
            insights.append({
                "type": "info",
                "title": "Unique Cases",
                "description": f"{noise_count} alarms ({noise_pct:.1f}%) are unique and don't fit into major patterns - may require individual attention"
            })
        
        return {
            "title": f"Alarm Analysis: {filename}",
            "overview": f"Analyzed {total_points} alarms and identified {len(cluster_insights)} distinct patterns",
            "insights": insights,
            "recommendations": ClusterAnalysisService._generate_recommendations(cluster_insights, severity_counts)
        }
    
    @staticmethod
    def _generate_recommendations(
        cluster_insights: List[Dict[str, Any]],
        severity_counts: Dict[str, int]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Check for critical issues
        critical_count = severity_counts.get('Critical', 0)
        if critical_count > 0:
            recommendations.append(
                f"Prioritize investigation of {critical_count} critical alarms - these represent the highest risk"
            )
        
        # Check for large clusters
        large_clusters = [c for c in cluster_insights if c['percentage'] > 20]
        if large_clusters:
            recommendations.append(
                f"Focus on the largest cluster(s) - addressing root causes here could resolve {large_clusters[0]['percentage']:.1f}% of alarms"
            )
        
        # Check for noise
        if any('noise' in str(c).lower() for c in cluster_insights):
            recommendations.append(
                "Review unique alarms individually - they may indicate new or emerging issues"
            )
        
        if not recommendations:
            recommendations.append(
                "Alarms are well-distributed across patterns - consider investigating each cluster systematically"
            )
        
        return recommendations

