import { useQuery } from '@tanstack/react-query';
import { getClusteringResults } from '../../services/api';
import '../common/styles.css';

interface ClusteringResultsProps {
  fileId: string;
}

function ClusteringResults({ fileId }: ClusteringResultsProps) {
  const { data: results, isLoading } = useQuery({
    queryKey: ['clustering-results', fileId],
    queryFn: () => getClusteringResults(fileId),
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

  return (
    <div className="clustering-results">
      <h3>Clustering Results</h3>
      {results.map((result: any) => (
        <div key={result.id} className="result-card">
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
              <strong>Visualization:</strong>
              <iframe
                src={`${API_BASE_URL}/${result.visualization_path}`}
                title={`Clustering visualization for ${result.algorithm}`}
                className="visualization-iframe"
                style={{
                  width: '100%',
                  height: '700px',
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
      ))}
    </div>
  );
}

export default ClusteringResults;

