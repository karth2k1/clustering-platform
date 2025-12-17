import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getFiles, runAutoClustering } from '../../services/api';
import ClusteringResults from './ClusteringResults';
import '../common/styles.css';

interface DataIngestionProps {
  deviceId?: string;
}

function DataIngestion({ deviceId }: DataIngestionProps) {
  const queryClient = useQueryClient();
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);

  const { data: filesData, isLoading } = useQuery({
    queryKey: ['files', deviceId],
    queryFn: () => getFiles({ device_id: deviceId, page: 1, page_size: 50 }),
  });

  const clusteringMutation = useMutation({
    mutationFn: runAutoClustering,
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['clustering-results'] });
      queryClient.invalidateQueries({ queryKey: ['clustering-results', variables.data_file_id] });
      setSelectedFileId(variables.data_file_id);
    },
  });

  const handleAutoCluster = (fileId: string) => {
    clusteringMutation.mutate({ data_file_id: fileId });
  };

  if (isLoading) {
    return (
      <div className="card">
        <h2>Data Ingestion</h2>
        <div className="loading">Loading files...</div>
      </div>
    );
  }

  const files = filesData?.files || [];

  return (
    <div className="card">
      <h2>Data Ingestion & Auto Clustering</h2>
      <p className="section-description">
        View uploaded files and run automatic clustering analysis.
      </p>

      {files.length === 0 ? (
        <p className="empty-state">No files uploaded yet. Upload files to get started.</p>
      ) : (
        <div className="file-list">
          {files.map((file: any) => (
            <div key={file.id} className="file-item">
              <div className="file-info">
                <h4>{file.original_filename}</h4>
                <p className="file-meta">
                  {file.file_type} • {file.file_size} bytes • {file.processing_status}
                </p>
                {file.file_metadata && (
                  <p className="file-stats">
                    Shape: {file.file_metadata.shape?.[0]} rows × {file.file_metadata.shape?.[1]} columns
                  </p>
                )}
              </div>
              <div className="file-actions">
                <button
                  className="button"
                  onClick={() => handleAutoCluster(file.id)}
                  disabled={clusteringMutation.isPending || file.processing_status !== 'COMPLETED'}
                >
                  {clusteringMutation.isPending ? 'Clustering...' : 'Run Auto Clustering'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {clusteringMutation.isSuccess && (
        <div className="success">
          Clustering completed! Check results below.
        </div>
      )}

      {clusteringMutation.isError && (
        <div className="error">
          Clustering failed: {clusteringMutation.error instanceof Error ? clusteringMutation.error.message : 'Unknown error'}
        </div>
      )}

      {selectedFileId && (
        <div className="section" style={{ marginTop: '2rem' }}>
          <ClusteringResults fileId={selectedFileId} />
        </div>
      )}
    </div>
  );
}

export default DataIngestion;

