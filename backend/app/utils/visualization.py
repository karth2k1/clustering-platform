"""Visualization utilities for clustering results"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
from pathlib import Path
from typing import Tuple, Optional
import json


def create_clustering_visualization(
    data: np.ndarray,
    cluster_labels: np.ndarray,
    feature_names: list[str],
    algorithm: str,
    output_path: Path
) -> bool:
    """
    Create and save a Plotly HTML visualization of clustering results
    
    Args:
        data: Preprocessed data array (n_samples, n_features)
        cluster_labels: Cluster labels array (n_samples,)
        feature_names: List of feature names
        algorithm: Algorithm name
        output_path: Path to save HTML file
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure data and labels are numpy arrays
        if not isinstance(data, np.ndarray):
            data = np.array(data)
        if not isinstance(cluster_labels, np.ndarray):
            cluster_labels = np.array(cluster_labels)
        
        # Reduce dimensions for visualization if needed
        if data.shape[1] > 2:
            pca = PCA(n_components=2, random_state=42)
            data_2d = pca.fit_transform(data)
            explained_var = pca.explained_variance_ratio_.sum()
            x_label = f'First Principal Component ({explained_var:.1%} variance)'
            y_label = 'Second Principal Component'
        elif data.shape[1] == 2:
            data_2d = data
            x_label = feature_names[0] if feature_names else 'Feature 1'
            y_label = feature_names[1] if feature_names else 'Feature 2'
        else:
            # Single dimension - create 2D by adding zeros
            data_2d = np.column_stack([data[:, 0], np.zeros(len(data))])
            x_label = feature_names[0] if feature_names else 'Feature 1'
            y_label = 'Value'
        
        # Create DataFrame for plotting
        plot_df = pd.DataFrame({
            'x': data_2d[:, 0],
            'y': data_2d[:, 1],
            'cluster': cluster_labels
        })
        
        # Separate noise points if any
        noise_mask = plot_df['cluster'] == -1
        clustered_mask = ~noise_mask
        
        # Create plotly figure
        fig = go.Figure()
        
        # Plot clusters
        unique_clusters = sorted([c for c in plot_df['cluster'].unique() if c != -1])
        colors = px.colors.qualitative.Set3
        
        for i, cluster_id in enumerate(unique_clusters):
            cluster_data = plot_df[plot_df['cluster'] == cluster_id]
            fig.add_trace(go.Scatter(
                x=cluster_data['x'],
                y=cluster_data['y'],
                mode='markers',
                name=f'Cluster {cluster_id}',
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)],
                    opacity=0.7,
                    line=dict(width=0.5, color='white')
                ),
                hovertemplate=f'Cluster {cluster_id}<br>X: %{{x:.2f}}<br>Y: %{{y:.2f}}<extra></extra>'
            ))
        
        # Plot noise points if any
        if noise_mask.any():
            noise_data = plot_df[noise_mask]
            fig.add_trace(go.Scatter(
                x=noise_data['x'],
                y=noise_data['y'],
                mode='markers',
                name='Noise',
                marker=dict(
                    size=6,
                    color='gray',
                    opacity=0.5,
                    symbol='x'
                ),
                hovertemplate='Noise<br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=f'Clustering Results - {algorithm}',
            xaxis_title=x_label,
            yaxis_title=y_label,
            hovermode='closest',
            width=900,
            height=700,
            template='plotly_white',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save as HTML
        fig.write_html(str(output_path))
        
        return True
        
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        return False

