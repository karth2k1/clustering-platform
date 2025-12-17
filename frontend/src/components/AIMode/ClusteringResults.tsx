import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getClusteringResults, getClusterAnalysis } from '../../services/api';
import ClusterDetailDrawer from './ClusterDetailDrawer';
import '../common/styles.css';

interface ClusteringResultsProps {
  fileId: string;
}

type ViewMode = 'executive' | 'scientist';

function ClusteringResults({ fileId }: ClusteringResultsProps) {
  const [viewMode, setViewMode] = useState<ViewMode>('executive');
  const [selectedResultId, setSelectedResultId] = useState<string | null>(null);
  const [selectedCluster, setSelectedCluster] = useState<{resultId: string, clusterId: number, clusterInfo: any} | null>(null);

  const { data: results, isLoading } = useQuery({
    queryKey: ['clustering-results', fileId],
    queryFn: () => getClusteringResults(fileId),
  });

  // Get analysis for the first result (or selected result)
  const resultId = selectedResultId || results?.[0]?.id;
  const { data: analysis, isLoading: analysisLoading, error: analysisError } = useQuery({
    queryKey: ['cluster-analysis', resultId],
    queryFn: () => getClusterAnalysis(resultId!),
    enabled: !!resultId && viewMode === 'executive',
  });

  if (isLoading) {
    return (
      <div className="clustering-results">
        <div className="loading">Loading results...</div>
      </div>
    );
  }

  if (!results || results.length === 0) {
    return (
      <div className="clustering-results">
        <p className="empty-state">No clustering results yet. Run clustering to see results.</p>
      </div>
    );
  }

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const currentResult = results.find((r: any) => r.id === resultId) || results[0];

  return (
    <div className="clustering-results">
      <div className="results-header">
        <h3>Clustering Results</h3>
        <div className="view-toggle">
          <button
            className={`toggle-btn ${viewMode === 'executive' ? 'active' : ''}`}
            onClick={() => setViewMode('executive')}
          >
            📊 Executive View
          </button>
          <button
            className={`toggle-btn ${viewMode === 'scientist' ? 'active' : ''}`}
            onClick={() => setViewMode('scientist')}
          >
            🔬 Data Scientist View
          </button>
        </div>
      </div>

      {viewMode === 'executive' ? (
        <ExecutiveView 
          result={currentResult} 
          analysis={analysis} 
          analysisLoading={analysisLoading}
          analysisError={analysisError}
          results={results}
          onResultSelect={setSelectedResultId}
          onClusterClick={(clusterId, clusterInfo) => 
            setSelectedCluster({ resultId: resultId!, clusterId, clusterInfo })
          }
        />
      ) : (
        <DataScientistView 
          result={currentResult}
          results={results}
          onResultSelect={setSelectedResultId}
          apiBaseUrl={API_BASE_URL}
        />
      )}

      {/* Cluster Detail Drawer */}
      {selectedCluster && (
        <ClusterDetailDrawer
          resultId={selectedCluster.resultId}
          clusterId={selectedCluster.clusterId}
          clusterInfo={selectedCluster.clusterInfo}
          isOpen={!!selectedCluster}
          onClose={() => setSelectedCluster(null)}
        />
      )}
    </div>
  );
}

function ExecutiveView({ 
  result, 
  analysis, 
  analysisLoading,
  analysisError,
  results,
  onResultSelect,
  onClusterClick
}: any) {
  return (
    <div className="executive-view">
      {results.length > 1 && (
        <div className="result-selector">
          <label>Select Analysis:</label>
          <select 
            value={result.id} 
            onChange={(e) => onResultSelect(e.target.value)}
            className="result-select"
          >
            {results.map((r: any) => (
              <option key={r.id} value={r.id}>
                {r.algorithm} - {new Date(r.created_at).toLocaleDateString()}
              </option>
            ))}
          </select>
        </div>
      )}

      {analysisLoading ? (
        <div className="loading">Analyzing clusters...</div>
      ) : analysisError ? (
        <div className="error">
          Error loading analysis: {analysisError instanceof Error ? analysisError.message : 'Unknown error'}
          <br />
          <small>Please check the browser console for details.</small>
        </div>
      ) : analysis?.executive_summary ? (
        <div className="executive-summary">
          <div className="summary-header">
            <h2>{analysis.executive_summary.title}</h2>
            <p className="summary-overview">{analysis.executive_summary.overview}</p>
          </div>

          <div className="insights-section">
            <h3>Key Insights</h3>
            <div className="insights-grid">
              {analysis.executive_summary.insights.map((insight: any, idx: number) => (
                <div key={idx} className={`insight-card insight-${insight.type}`}>
                  <div className="insight-icon">
                    {insight.type === 'critical' ? '⚠️' : insight.type === 'primary' ? '🎯' : 'ℹ️'}
                  </div>
                  <div className="insight-content">
                    <h4>{insight.title}</h4>
                    <p>{insight.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="clusters-section">
            <h3>Cluster Breakdown</h3>
            <div className="clusters-grid">
              {analysis.cluster_insights.map((cluster: any) => (
                <div 
                  key={cluster.cluster_id} 
                  className="cluster-card clickable"
                  onClick={() => onClusterClick(cluster.cluster_id, cluster)}
                >
                  <div className="cluster-header">
                    <h4>Cluster {cluster.cluster_id}</h4>
                    <span className="cluster-size">{cluster.size} alarms ({cluster.percentage}%)</span>
                  </div>
                  <p className="cluster-description">{cluster.description}</p>
                  <div className="cluster-attributes">
                    {cluster.key_attributes.map((attr: string, idx: number) => (
                      <span key={idx} className="attribute-tag">{attr}</span>
                    ))}
                  </div>
                  <div className="cluster-action-hint">Click to view details →</div>
                </div>
              ))}
              {analysis.noise_points > 0 && (
                <div className="cluster-card cluster-noise">
                  <div className="cluster-header">
                    <h4>Unique Cases</h4>
                    <span className="cluster-size">{analysis.noise_points} alarms</span>
                  </div>
                  <p className="cluster-description">
                    These alarms don't fit into major patterns and may require individual attention
                  </p>
                </div>
              )}
            </div>
          </div>

          {analysis.executive_summary.recommendations && analysis.executive_summary.recommendations.length > 0 && (
            <div className="recommendations-section">
              <h3>Recommendations</h3>
              <ul className="recommendations-list">
                {analysis.executive_summary.recommendations.map((rec: string, idx: number) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="visualization-preview">
            <h3>Visualization</h3>
            {result.visualization_path && (
              <iframe
                src={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/${result.visualization_path}`}
                title="Clustering visualization"
                className="visualization-iframe"
                style={{
                  width: '100%',
                  height: '600px',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  marginTop: '10px',
                }}
              />
            )}
          </div>
        </div>
      ) : (
        <div className="error">Unable to load cluster analysis</div>
      )}
    </div>
  );
}

function DataScientistView({ 
  result, 
  results,
  onResultSelect,
  apiBaseUrl 
}: any) {
  return (
    <div className="scientist-view">
      {results.length > 1 && (
        <div className="result-selector">
          <label>Select Result:</label>
          <select 
            value={result.id} 
            onChange={(e) => onResultSelect(e.target.value)}
            className="result-select"
          >
            {results.map((r: any) => (
              <option key={r.id} value={r.id}>
                {r.algorithm} - {new Date(r.created_at).toLocaleDateString()}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="result-card">
        <div className="result-header">
          <h4>{result.algorithm}</h4>
          <span className="result-date">
            {new Date(result.created_at).toLocaleString()}
          </span>
        </div>

        {result.parameters && (
          <div className="result-parameters">
            <strong>Parameters:</strong>
            <pre>{JSON.stringify(result.parameters, null, 2)}</pre>
          </div>
        )}

        {result.metrics && (
          <div className="result-metrics">
            <strong>Metrics:</strong>
            <div className="metrics-grid">
              {result.metrics.silhouette_score !== undefined && (
                <div className="metric-item">
                  <span className="metric-label">Silhouette Score:</span>
                  <span className="metric-value">{result.metrics.silhouette_score.toFixed(4)}</span>
                </div>
              )}
              {result.metrics.davies_bouldin_index !== undefined && (
                <div className="metric-item">
                  <span className="metric-label">Davies-Bouldin Index:</span>
                  <span className="metric-value">{result.metrics.davies_bouldin_index.toFixed(4)}</span>
                </div>
              )}
              {result.metrics.calinski_harabasz_index !== undefined && (
                <div className="metric-item">
                  <span className="metric-label">Calinski-Harabasz Index:</span>
                  <span className="metric-value">{result.metrics.calinski_harabasz_index.toFixed(2)}</span>
                </div>
              )}
              {result.metrics.n_clusters !== undefined && (
                <div className="metric-item">
                  <span className="metric-label">Number of Clusters:</span>
                  <span className="metric-value">{result.metrics.n_clusters}</span>
                </div>
              )}
              {result.metrics.n_noise !== undefined && result.metrics.n_noise > 0 && (
                <div className="metric-item">
                  <span className="metric-label">Noise Points:</span>
                  <span className="metric-value">{result.metrics.n_noise}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {result.visualization_path && (
          <div className="result-visualization">
            <strong>Interactive Visualization:</strong>
            <p className="visualization-hint">
              Use the controls in the visualization to zoom, pan, and explore cluster patterns.
              Hover over points to see detailed information.
            </p>
            <iframe
              src={`${apiBaseUrl}/${result.visualization_path}`}
              title={`Clustering visualization for ${result.algorithm}`}
              className="visualization-iframe"
              style={{
                width: '100%',
                height: '800px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                marginTop: '10px',
              }}
            />
          </div>
        )}

        <div className="result-summary">
          <strong>Summary:</strong>
          <p>
            {result.cluster_labels && Array.isArray(result.cluster_labels) && (
              <>
                Total points: {result.cluster_labels.length}, 
                Unique clusters: {new Set(result.cluster_labels).size}
                {result.cluster_labels.includes(-1) && (
                  <> (including {result.cluster_labels.filter((l: number) => l === -1).length} noise points)</>
                )}
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}

export default ClusteringResults;
