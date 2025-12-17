import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { uploadFile, uploadMultipleFiles } from '../../services/api';
import '../common/styles.css';

interface FileUploadProps {
  deviceId?: string;
}

function FileUpload({ deviceId }: FileUploadProps) {
  const [uploadProgress, setUploadProgress] = useState<Record<string, number>>({});
  const queryClient = useQueryClient();

  const uploadMutation = useMutation({
    mutationFn: async (files: File[]) => {
      if (files.length === 1) {
        return await uploadFile(files[0], deviceId);
      } else {
        return await uploadMultipleFiles(files, deviceId);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['files'] });
      setUploadProgress({});
    },
  });

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    // Initialize progress
    const progress: Record<string, number> = {};
    acceptedFiles.forEach(file => {
      progress[file.name] = 0;
    });
    setUploadProgress(progress);

    try {
      await uploadMutation.mutateAsync(acceptedFiles);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  }, [deviceId]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/json': ['.json'],
    },
    multiple: true,
  });

  return (
    <div className="card">
      <h2>Upload Files</h2>
      <p className="section-description">
        Drag and drop CSV or JSON files here, or click to select files.
      </p>

      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="dropzone-content">
          {isDragActive ? (
            <p>Drop files here...</p>
          ) : (
            <>
              <p>📁 Drag & drop files here, or click to select</p>
              <p className="dropzone-hint">Supports CSV and JSON files</p>
            </>
          )}
        </div>
      </div>

      {uploadMutation.isPending && (
        <div className="loading">Uploading files...</div>
      )}

      {uploadMutation.isError && (
        <div className="error">
          Upload failed: {uploadMutation.error instanceof Error ? uploadMutation.error.message : 'Unknown error'}
        </div>
      )}

      {uploadMutation.isSuccess && (
        <div className="success">
          Files uploaded successfully!
        </div>
      )}

      {Object.keys(uploadProgress).length > 0 && (
        <div className="upload-progress">
          {Object.entries(uploadProgress).map(([filename, progress]) => (
            <div key={filename} className="progress-item">
              <span>{filename}</span>
              <div className="progress-bar">
                <div 
                  className="progress-fill" 
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FileUpload;

