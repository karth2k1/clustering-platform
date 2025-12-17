import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getClusteringFeatures, getClusterAnalysis } from '../../services/api';
import '../common/styles.css';

interface DataScientistControlsProps {
  resultId: string;
}

function DataScientistControls({ resultId }: DataScientistControlsProps) {
  const [activeTab, setActiveTab] = useState<'features' | 'clusters' | 'export'>('features');

  const { data: featuresData, isLoading: featuresLoading } = useQuery({
    queryKey: ['clustering-features', resultId],
    queryFn: () => getClusteringFeatures(resultId),
    enabled: activeTab === 'features',
  });

  const { data: analysisData } = useQuery({
    queryKey: ['cluster-analysis', resultId],
    queryFn: () => getClusterAnalysis(resultId),
    enabled: activeTab === 'clusters',
  });

  const handleExport = (format: 'json' | 'csv') => {
    // TODO: Implement export functionality
    alert(`Export to ${format.toUpperCase()} - Feature coming soon!`);
  };

  return (
    <div className="scientist-controls">
      <div className="controls-tabs">
        <button
          className={`control-tab ${activeTab === 'features' ? 'active' : ''}`}
          onClick={() => setActiveTab('features')}
        >
          🔍 Features
        </button>
        <button
          className={`control-tab ${activeTab === 'clusters' ? 'active' : ''}`}
          onClick={() => setActiveTab('clusters')}
        >
          📊 Cluster Stats
        </button>
        <button
          className={`control-tab ${activeTab === 'export' ? 'active' : ''}`}
          onClick={() => setActiveTab('export')}
        >
          💾 Export
        </button>
      </div>

      <div className="controls-content">
        {activeTab === 'features' && (
          <div className="features-panel">
            <h3>Features Used for Clustering</h3>
            {featuresLoading ? (
              <div className="loading">Loading feature information...</div>
            ) : featuresData?.error ? (
              <div className="error">{featuresData.error}</div>
            ) : featuresData ? (
              <>
                <div className="feature-summary">
                  <div className="summary-item">
                    <strong>Total Features:</strong> {featuresData.total_features}
                  </div>
                  <div className="summary-item">
                    <strong>Data Shape:</strong> {featuresData.data_shape?.rows} rows × {featuresData.data_shape?.columns} columns
                  </div>
                  <div className="summary-item">
                    <strong>Processed:</strong> {featuresData.data_shape?.processed_rows} rows × {featuresData.data_shape?.processed_features} features
                  </div>
                </div>

                <div className="preprocessing-info">
                  <h4>Preprocessing</h4>
                  <ul>
                    <li><strong>Scaling:</strong> {featuresData.preprocessing_info?.scaling}</li>
                    <li><strong>Encoding:</strong> {featuresData.preprocessing_info?.encoding}</li>
                  </ul>
                </div>

                <div className="features-list">
                  <h4>Feature Details</h4>
                  <div className="features-table">
                    <div className="table-header">
                      <span>Feature Name</span>
                      <span>Type</span>
                      <span>Unique Values</span>
                      <span>Missing</span>
                    </div>
                    {featuresData.feature_details?.slice(0, 20).map((feat: any, idx: number) => (
                      <div key={idx} className="table-row">
                        <span className="feature-name" title={feat.name}>{feat.name}</span>
                        <span className={`feature-type ${feat.is_categorical ? 'categorical' : 'numeric'}`}>
                          {feat.is_categorical ? 'Categorical' : 'Numeric'}
                        </span>
                        <span>{feat.unique_values}</span>
                        <span>{feat.missing_count}</span>
                      </div>
                    ))}
                    {featuresData.feature_details && featuresData.feature_details.length > 20 && (
                      <div className="table-footer">
                        Showing first 20 of {featuresData.feature_details.length} features
                      </div>
                    )}
                  </div>
                </div>
              </>
            ) : null}
          </div>
        )}

        {activeTab === 'clusters' && (
          <div className="clusters-stats-panel">
            <h3>Cluster Statistics</h3>
            {analysisData?.error ? (
              <div className="error">{analysisData.error}</div>
            ) : analysisData?.cluster_insights ? (
              <>
                <div className="cluster-stats-summary">
                  <div className="stat-card">
                    <div className="stat-value">{analysisData.total_clusters}</div>
                    <div className="stat-label">Total Clusters</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{analysisData.noise_points}</div>
                    <div className="stat-label">Noise Points</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{analysisData.total_points}</div>
                    <div className="stat-label">Total Points</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">
                      {((analysisData.total_points - analysisData.noise_points) / analysisData.total_points * 100).toFixed(1)}%
                    </div>
                    <div className="stat-label">Clustered</div>
                  </div>
                </div>

                <div className="cluster-size-distribution">
                  <h4>Cluster Size Distribution</h4>
                  <div className="distribution-chart">
                    {analysisData.cluster_insights
                      .sort((a: any, b: any) => b.size - a.size)
                      .map((cluster: any) => (
                        <div key={cluster.cluster_id} className="distribution-bar">
                          <div className="bar-label">Cluster {cluster.cluster_id}</div>
                          <div className="bar-container">
                            <div 
                              className="bar-fill" 
                              style={{ width: `${(cluster.size / analysisData.total_points) * 100}%` }}
                            >
                              <span className="bar-value">{cluster.size}</span>
                            </div>
                          </div>
                          <div className="bar-percentage">{cluster.percentage}%</div>
                        </div>
                      ))}
                  </div>
                </div>
              </>
            ) : (
              <div className="loading">Loading cluster statistics...</div>
            )}
          </div>
        )}

        {activeTab === 'export' && (
          <div className="export-panel">
            <h3>Export Options</h3>
            <div className="export-options">
              <div className="export-option">
                <h4>Export Clustering Results</h4>
                <p>Download cluster assignments and metrics</p>
                <div className="export-buttons">
                  <button className="export-btn" onClick={() => handleExport('json')}>
                    Export as JSON
                  </button>
                  <button className="export-btn" onClick={() => handleExport('csv')}>
                    Export as CSV
                  </button>
                </div>
              </div>
              <div className="export-option">
                <h4>Export Cluster Analysis</h4>
                <p>Download detailed cluster insights and recommendations</p>
                <div className="export-buttons">
                  <button className="export-btn" onClick={() => handleExport('json')}>
                    Export Analysis (JSON)
                  </button>
                </div>
              </div>
              <div className="export-option">
                <h4>Export Visualization</h4>
                <p>Download the clustering visualization</p>
                <div className="export-buttons">
                  <button className="export-btn" onClick={() => {
                    // Open visualization in new tab for download
                    window.open(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/visualizations/clustering_${resultId}.html`, '_blank');
                  }}>
                    Open Visualization
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default DataScientistControls;

