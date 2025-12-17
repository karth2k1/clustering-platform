import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getFiles } from '../../services/api';
import '../common/styles.css';

interface DataFileBrowserProps {
  selectedFileId: string | null;
  onFileSelect: (fileId: string | null) => void;
}

function DataFileBrowser({ selectedFileId, onFileSelect }: DataFileBrowserProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');

  const { data: filesData, isLoading } = useQuery({
    queryKey: ['files', searchTerm, filterType, filterStatus],
    queryFn: () => getFiles({
      file_type: filterType || undefined,
      status: filterStatus || undefined,
      page: 1,
      page_size: 100,
    }),
  });

  const files = filesData?.files || [];
  const filteredFiles = files.filter((file: any) =>
    file.original_filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="card">
      <h2>Data File Browser</h2>
      <p className="section-description">
        Browse and select data files to open in Jupyter notebook playground.
      </p>

      <div className="browser-controls">
        <input
          type="text"
          placeholder="Search files..."
          className="input"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select
          className="input"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
        >
          <option value="">All Types</option>
          <option value="CSV">CSV</option>
          <option value="JSON">JSON</option>
        </select>
        <select
          className="input"
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
        >
          <option value="">All Status</option>
          <option value="COMPLETED">Completed</option>
          <option value="PENDING">Pending</option>
          <option value="PROCESSING">Processing</option>
          <option value="FAILED">Failed</option>
        </select>
      </div>

      {isLoading ? (
        <div className="loading">Loading files...</div>
      ) : filteredFiles.length === 0 ? (
        <p className="empty-state">No files found.</p>
      ) : (
        <div className="file-grid">
          {filteredFiles.map((file: any) => (
            <div
              key={file.id}
              className={`file-card ${selectedFileId === file.id ? 'selected' : ''}`}
              onClick={() => onFileSelect(file.id === selectedFileId ? null : file.id)}
            >
              <div className="file-card-header">
                <h4>{file.original_filename}</h4>
                <span className={`status-badge status-${file.processing_status.toLowerCase()}`}>
                  {file.processing_status}
                </span>
              </div>
              <div className="file-card-body">
                <p className="file-type">{file.file_type}</p>
                <p className="file-size">{formatFileSize(file.file_size)}</p>
                {file.file_metadata && (
                  <p className="file-shape">
                    {file.file_metadata.shape?.[0]} rows × {file.file_metadata.shape?.[1]} columns
                  </p>
                )}
                <p className="file-date">
                  Uploaded: {new Date(file.upload_timestamp).toLocaleDateString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

export default DataFileBrowser;

