import { useState } from 'react';
import DataFileBrowser from './DataFileBrowser';
import NotebookLauncher from './NotebookLauncher';
import '../common/styles.css';

function AdvancedMode() {
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);

  return (
    <div className="advanced-mode">
      <h1>Advanced Mode</h1>
      <p className="mode-description">
        Select a data file and launch a Jupyter notebook playground with pre-populated analysis code.
      </p>

      <div className="mode-sections">
        <div className="section">
          <DataFileBrowser 
            selectedFileId={selectedFileId}
            onFileSelect={setSelectedFileId}
          />
        </div>

        {selectedFileId && (
          <div className="section">
            <NotebookLauncher fileId={selectedFileId} />
          </div>
        )}
      </div>
    </div>
  );
}

export default AdvancedMode;

