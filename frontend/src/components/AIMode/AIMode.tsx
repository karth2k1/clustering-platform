import { useState } from 'react';
import FileUpload from './FileUpload';
import DeviceManager from './DeviceManager';
import DataIngestion from './DataIngestion';
import '../common/styles.css';

function AIMode() {
  const [selectedDevice, setSelectedDevice] = useState<string | null>(null);

  return (
    <div className="ai-mode">
      <h1>AI-Assisted Mode</h1>
      <p className="mode-description">
        Upload data files or fetch from devices. The system will automatically process and cluster your data.
      </p>

      <div className="mode-sections">
        <div className="section">
          <DeviceManager 
            selectedDevice={selectedDevice}
            onDeviceSelect={setSelectedDevice}
          />
        </div>

        <div className="section">
          <FileUpload deviceId={selectedDevice || undefined} />
        </div>

        <div className="section">
          <DataIngestion deviceId={selectedDevice || undefined} />
        </div>
      </div>
    </div>
  );
}

export default AIMode;

