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
            
            # Analyze clusters - convert numpy types to Python native types
            unique_clusters = sorted([int(c) for c in set(cluster_labels) if c != -1])
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
                "total_clusters": int(len(unique_clusters)),
                "noise_points": int(noise_count),
                "total_points": int(len(df))
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
                    # Convert numpy types to Python native types
                    count_int = int(count) if hasattr(count, 'item') else int(count)
                    top_values[col] = {
                        "value": str(top_val),
                        "count": count_int,
                        "percentage": float((count_int / cluster_size) * 100)
                    }
        
        # Generate cluster description
        description = ClusterAnalysisService._generate_cluster_description(
            cluster_id, cluster_size, top_values
        )
        
        return {
            "cluster_id": int(cluster_id),
            "size": int(cluster_size),
            "percentage": float(round(percentage, 1)),
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
                "description": f"{int(largest_cluster['size'])} alarms ({float(largest_cluster['percentage'])}%) share similar characteristics: {largest_cluster['description']}"
            })
        
        if severity_counts:
            critical_count = int(severity_counts.get('Critical', 0))
            if critical_count > 0:
                critical_clusters = len([c for c in cluster_insights if c['characteristics'].get('OrigSeverity', {}).get('value') == 'Critical'])
                insights.append({
                    "type": "critical",
                    "title": "Critical Alarms",
                    "description": f"{critical_count} critical alarms identified across {int(critical_clusters)} clusters"
                })
        
        if noise_count > 0:
            noise_pct = float((noise_count / total_points) * 100)
            insights.append({
                "type": "info",
                "title": "Unique Cases",
                "description": f"{int(noise_count)} alarms ({noise_pct:.1f}%) are unique and don't fit into major patterns - may require individual attention"
            })
        
        return {
            "title": f"Alarm Analysis: {filename}",
            "overview": f"Analyzed {int(total_points)} alarms and identified {int(len(cluster_insights))} distinct patterns",
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
        critical_count = int(severity_counts.get('Critical', 0))
        if critical_count > 0:
            recommendations.append(
                f"Prioritize investigation of {critical_count} critical alarms - these represent the highest risk"
            )
        
        # Check for large clusters
        large_clusters = [c for c in cluster_insights if c['percentage'] > 20]
        if large_clusters:
            pct = float(large_clusters[0]['percentage'])
            recommendations.append(
                f"Focus on the largest cluster(s) - addressing root causes here could resolve {pct:.1f}% of alarms"
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
    
    @staticmethod
    def get_cluster_details(
        db: Session,
        result_id: str,
        cluster_id: int
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific cluster including all alarms
        
        Returns:
            Dictionary with cluster details and alarm data
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
            
            # Filter alarms for this cluster
            cluster_data = df[df['cluster'] == cluster_id].copy()
            
            if len(cluster_data) == 0:
                return {"error": f"Cluster {cluster_id} not found"}
            
            # Get cluster insight
            insight = ClusterAnalysisService._analyze_single_cluster(
                cluster_id, cluster_data, len(df)
            )
            
            # Extract alarm details
            alarms = []
            for idx, row in cluster_data.iterrows():
                alarm = {
                    "index": int(idx),
                    "code": str(row.get('Code', 'N/A')),
                    "name": str(row.get('Name', 'N/A')),
                    "severity": str(row.get('OrigSeverity', 'N/A')),
                    "description": str(row.get('Description', 'N/A')),
                    "affected_mo_type": str(row.get('AffectedMoType', 'N/A')),
                    "affected_mo_display_name": str(row.get('AffectedMoDisplayName', 'N/A')),
                    "affected_mo_id": str(row.get('AffectedMoId', 'N/A')),
                    "acknowledge": str(row.get('Acknowledge', 'N/A')),
                    "create_time": str(row.get('CreateTime', 'N/A')),
                    "last_transition_time": str(row.get('LastTransitionTime', 'N/A')),
                }
                
                # Add nested object information if available
                if pd.notna(row.get('AffectedMo')):
                    affected_mo = row.get('AffectedMo')
                    if isinstance(affected_mo, dict):
                        alarm["affected_mo_details"] = {
                            "moid": str(affected_mo.get('Moid', 'N/A')),
                            "object_type": str(affected_mo.get('ObjectType', 'N/A')),
                            "link": str(affected_mo.get('link', 'N/A'))
                        }
                
                # Add all other fields as additional info
                additional_info = {}
                for col in cluster_data.columns:
                    if col not in ['cluster'] and col not in alarm:
                        val = row.get(col)
                        if pd.notna(val):
                            # Convert to string, handle complex types
                            if isinstance(val, (dict, list)):
                                additional_info[col] = str(val)
                            else:
                                additional_info[col] = str(val)
                
                alarm["additional_info"] = additional_info
                alarms.append(alarm)
            
            # Generate importance explanation
            importance = ClusterAnalysisService._generate_cluster_importance(insight, len(df))
            
            return {
                "cluster_id": int(cluster_id),
                "insight": insight,
                "importance": importance,
                "alarm_count": int(len(alarms)),
                "alarms": alarms
            }
            
        except Exception as e:
            return {"error": f"Error getting cluster details: {str(e)}"}
    
    @staticmethod
    def get_noise_points(
        db: Session,
        result_id: str
    ) -> Dict[str, Any]:
        """
        Get all noise points (alarms that don't fit into any cluster)
        
        Returns:
            Dictionary with noise point details and alarm data
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
            
            # Filter noise points (cluster_id == -1)
            noise_data = df[df['cluster'] == -1].copy()
            
            if len(noise_data) == 0:
                return {"error": "No noise points found"}
            
            # Extract alarm details (same format as cluster details)
            alarms = []
            for idx, row in noise_data.iterrows():
                alarm = {
                    "index": int(idx),
                    "code": str(row.get('Code', 'N/A')),
                    "name": str(row.get('Name', 'N/A')),
                    "severity": str(row.get('OrigSeverity', 'N/A')),
                    "description": str(row.get('Description', 'N/A')),
                    "affected_mo_type": str(row.get('AffectedMoType', 'N/A')),
                    "affected_mo_display_name": str(row.get('AffectedMoDisplayName', 'N/A')),
                    "affected_mo_id": str(row.get('AffectedMoId', 'N/A')),
                    "acknowledge": str(row.get('Acknowledge', 'N/A')),
                    "create_time": str(row.get('CreateTime', 'N/A')),
                    "last_transition_time": str(row.get('LastTransitionTime', 'N/A')),
                }
                
                # Add nested object information if available
                if pd.notna(row.get('AffectedMo')):
                    affected_mo = row.get('AffectedMo')
                    if isinstance(affected_mo, dict):
                        alarm["affected_mo_details"] = {
                            "moid": str(affected_mo.get('Moid', 'N/A')),
                            "object_type": str(affected_mo.get('ObjectType', 'N/A')),
                            "link": str(affected_mo.get('link', 'N/A'))
                        }
                
                # Add all other fields as additional info
                additional_info = {}
                for col in noise_data.columns:
                    if col not in ['cluster'] and col not in alarm:
                        val = row.get(col)
                        if pd.notna(val):
                            if isinstance(val, (dict, list)):
                                additional_info[col] = str(val)
                            else:
                                additional_info[col] = str(val)
                
                alarm["additional_info"] = additional_info
                alarms.append(alarm)
            
            # Analyze noise points
            unique_codes = noise_data['Code'].nunique() if 'Code' in noise_data.columns else 0
            code_distribution = dict(noise_data['Code'].value_counts().head(10)) if 'Code' in noise_data.columns else {}
            
            return {
                "alarm_count": int(len(alarms)),
                "unique_alarm_codes": int(unique_codes),
                "code_distribution": {str(k): int(v) for k, v in code_distribution.items()},
                "alarms": alarms,
                "explanation": {
                    "title": "Why These Are Unique Cases",
                    "description": f"These {len(alarms)} alarms don't fit into any major cluster pattern. They may represent:",
                    "reasons": [
                        "Rare or one-off issues that don't follow common patterns",
                        "Alarms with unique combinations of features that differ significantly from clustered alarms",
                        "Potential new or emerging issues that haven't formed patterns yet",
                        "Edge cases that require individual investigation"
                    ],
                    "recommendation": "Review these alarms individually to identify if they represent new patterns or require special attention."
                }
            }
            
        except Exception as e:
            return {"error": f"Error getting noise points: {str(e)}"}
    
    @staticmethod
    def _generate_cluster_importance(insight: Dict[str, Any], total_alarms: int) -> Dict[str, Any]:
        """Generate explanation of why this cluster is important"""
        importance_reasons = []
        priority = "medium"
        
        # Check size
        if insight['percentage'] > 30:
            importance_reasons.append({
                "type": "size",
                "title": "Large Cluster",
                "description": f"This cluster represents {insight['percentage']}% of all alarms, making it a high-priority issue."
            })
            priority = "high"
        elif insight['percentage'] > 10:
            importance_reasons.append({
                "type": "size",
                "title": "Significant Cluster",
                "description": f"This cluster represents {insight['percentage']}% of alarms, indicating a recurring pattern."
            })
        
        # Check severity
        if 'OrigSeverity' in insight.get('characteristics', {}):
            severity = insight['characteristics']['OrigSeverity']['value']
            if severity == 'Critical':
                importance_reasons.append({
                    "type": "severity",
                    "title": "Critical Severity",
                    "description": "All alarms in this cluster are marked as Critical, requiring immediate attention."
                })
                priority = "high"
            elif severity == 'Warning':
                importance_reasons.append({
                    "type": "severity",
                    "title": "Warning Severity",
                    "description": "These alarms indicate potential issues that should be monitored."
                })
        
        # Check if it's a specific alarm code pattern
        if 'Code' in insight.get('characteristics', {}):
            code = insight['characteristics']['Code']['value']
            code_pct = insight['characteristics']['Code']['percentage']
            if code_pct > 80:
                importance_reasons.append({
                    "type": "pattern",
                    "title": "Consistent Alarm Pattern",
                    "description": f"{code_pct:.0f}% of alarms share the same code ({code}), suggesting a systemic issue."
                })
        
        # Default if no specific reasons
        if not importance_reasons:
            importance_reasons.append({
                "type": "general",
                "title": "Pattern Identified",
                "description": "This cluster represents a distinct pattern of alarms that may share common root causes."
            })
        
        return {
            "priority": priority,
            "reasons": importance_reasons,
            "summary": f"This cluster contains {insight['size']} alarms ({insight['percentage']}% of total) with similar characteristics."
        }

