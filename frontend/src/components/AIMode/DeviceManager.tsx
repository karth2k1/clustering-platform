import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getDevices, createDevice, deleteDevice, syncDevice } from '../../services/api';
import '../common/styles.css';

interface DeviceManagerProps {
  selectedDevice: string | null;
  onDeviceSelect: (deviceId: string | null) => void;
}

interface Device {
  id: string;
  name: string;
  device_type: string;
  api_endpoint?: string;
  is_active: boolean;
  last_sync?: string;
}

function DeviceManager({ selectedDevice, onDeviceSelect }: DeviceManagerProps) {
  const [showAddForm, setShowAddForm] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<{ deviceId: string; saveFiles: boolean } | null>(null);
  const queryClient = useQueryClient();

  const { data: devices = [], isLoading } = useQuery<Device[]>({
    queryKey: ['devices'],
    queryFn: () => getDevices(),
  });

  const createMutation = useMutation({
    mutationFn: createDevice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['devices'] });
      setShowAddForm(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: ({ deviceId, saveFiles }: { deviceId: string; saveFiles: boolean }) =>
      deleteDevice(deviceId, saveFiles),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['devices'] });
      queryClient.invalidateQueries({ queryKey: ['files'] });
      setDeleteConfirm(null);
      if (selectedDevice === deleteConfirm?.deviceId) {
        onDeviceSelect(null);
      }
    },
  });

  const syncMutation = useMutation({
    mutationFn: syncDevice,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['devices'] });
      queryClient.invalidateQueries({ queryKey: ['files'] });
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    createMutation.mutate({
      name: formData.get('name') as string,
      device_type: formData.get('device_type') as string,
      api_endpoint: formData.get('api_endpoint') as string || undefined,
      api_key: formData.get('api_key') as string || undefined,
    });
  };

  const handleDelete = (deviceId: string) => {
    deleteMutation.mutate({
      deviceId,
      saveFiles: deleteConfirm?.saveFiles ?? true,
    });
  };

  const handleSync = (deviceId: string) => {
    syncMutation.mutate(deviceId);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2>Device Management</h2>
        <button 
          className="button"
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? 'Cancel' : '+ Add Device'}
        </button>
      </div>

      {showAddForm && (
        <form onSubmit={handleSubmit} className="device-form">
          <label className="label">
            Device Name *
            <input 
              type="text" 
              name="name" 
              className="input" 
              required 
            />
          </label>
          <label className="label">
            Device Type *
            <select name="device_type" className="input" required>
              <option value="">Select type...</option>
              <option value="Intersight">Intersight</option>
              <option value="Custom">Custom API</option>
            </select>
          </label>
          <label className="label">
            API Endpoint
            <input 
              type="url" 
              name="api_endpoint" 
              className="input" 
              placeholder="https://api.example.com"
            />
          </label>
          <label className="label">
            API Key
            <input 
              type="password" 
              name="api_key" 
              className="input" 
              placeholder="Enter API key"
            />
          </label>
          <button 
            type="submit" 
            className="button"
            disabled={createMutation.isPending}
          >
            {createMutation.isPending ? 'Creating...' : 'Create Device'}
          </button>
          {createMutation.isError && (
            <div className="error">
              Failed to create device: {createMutation.error instanceof Error ? createMutation.error.message : 'Unknown error'}
            </div>
          )}
        </form>
      )}

      {isLoading ? (
        <div className="loading">Loading devices...</div>
      ) : devices.length === 0 ? (
        <p className="empty-state">No devices configured. Add a device to fetch data via WebAPI.</p>
      ) : (
        <div className="device-list">
          {devices.map((device) => (
            <div 
              key={device.id} 
              className={`device-item ${selectedDevice === device.id ? 'selected' : ''}`}
              onClick={() => onDeviceSelect(device.id === selectedDevice ? null : device.id)}
            >
              <div className="device-info">
                <h3>{device.name}</h3>
                <p className="device-type">{device.device_type}</p>
                {device.last_sync && (
                  <p className="device-sync">Last sync: {new Date(device.last_sync).toLocaleString()}</p>
                )}
              </div>
              <div className="device-actions">
                <button
                  className="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleSync(device.id);
                  }}
                  disabled={syncMutation.isPending || !device.is_active}
                >
                  {syncMutation.isPending ? 'Syncing...' : 'Sync'}
                </button>
                <button
                  className="button button-danger"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteConfirm({ deviceId: device.id, saveFiles: true });
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {deleteConfirm && (
        <div className="modal-overlay" onClick={() => setDeleteConfirm(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Delete Device</h3>
            <p>What would you like to do with data files from this device?</p>
            <div className="modal-actions">
              <button
                className="button button-success"
                onClick={() => handleDelete(deleteConfirm.deviceId)}
                disabled={deleteMutation.isPending}
              >
                Save Files & Delete Device
              </button>
              <button
                className="button button-danger"
                onClick={() => {
                  setDeleteConfirm({ ...deleteConfirm, saveFiles: false });
                  handleDelete(deleteConfirm.deviceId);
                }}
                disabled={deleteMutation.isPending}
              >
                Delete Files & Device
              </button>
              <button
                className="button"
                onClick={() => setDeleteConfirm(null)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DeviceManager;

