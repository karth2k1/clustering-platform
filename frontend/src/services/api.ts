/**
 * API Client for Clustering Platform Backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// File Upload
export const uploadFile = async (file: File, deviceId?: string) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const params = deviceId ? { device_id: deviceId } : {};
  
  const response = await apiClient.post('/api/files/upload', formData, {
    params,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const uploadMultipleFiles = async (files: File[], deviceId?: string) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file);
  });
  
  const params = deviceId ? { device_id: deviceId } : {};
  
  const response = await apiClient.post('/api/files/upload-multiple', formData, {
    params,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

// Files
export const getFiles = async (params?: {
  device_id?: string;
  file_type?: string;
  status?: string;
  page?: number;
  page_size?: number;
}) => {
  const response = await apiClient.get('/api/files', { params });
  return response.data;
};

export const getFile = async (fileId: string) => {
  const response = await apiClient.get(`/api/files/${fileId}`);
  return response.data;
};

export const deleteFile = async (fileId: string) => {
  const response = await apiClient.delete(`/api/files/${fileId}`);
  return response.data;
};

export const downloadFile = async (fileId: string) => {
  const response = await apiClient.get(`/api/files/${fileId}/download`, {
    responseType: 'blob',
  });
  return response.data;
};

// Devices
export const createDevice = async (deviceData: {
  name: string;
  device_type: string;
  api_endpoint?: string;
  api_key?: string;
  configuration?: Record<string, any>;
}) => {
  const response = await apiClient.post('/api/devices', deviceData);
  return response.data;
};

export const getDevices = async (activeOnly?: boolean) => {
  const params = activeOnly ? { active_only: true } : {};
  const response = await apiClient.get('/api/devices', { params });
  return response.data;
};

export const getDevice = async (deviceId: string) => {
  const response = await apiClient.get(`/api/devices/${deviceId}`);
  return response.data;
};

export const updateDevice = async (deviceId: string, deviceData: Partial<{
  name: string;
  device_type: string;
  api_endpoint: string;
  api_key: string;
  configuration: Record<string, any>;
  is_active: boolean;
}>) => {
  const response = await apiClient.put(`/api/devices/${deviceId}`, deviceData);
  return response.data;
};

export const deleteDevice = async (deviceId: string, saveDataFiles: boolean = true) => {
  const response = await apiClient.delete(`/api/devices/${deviceId}`, {
    data: { save_data_files: saveDataFiles },
  });
  return response.data;
};

export const syncDevice = async (deviceId: string) => {
  const response = await apiClient.post(`/api/devices/${deviceId}/sync`);
  return response.data;
};

// Clustering
export const runAutoClustering = async (data: {
  data_file_id: string;
  algorithm?: string;
  parameters?: Record<string, any>;
}) => {
  const response = await apiClient.post('/api/clustering/auto', data);
  return response.data;
};

export const getClusteringResults = async (fileId: string) => {
  const response = await apiClient.get(`/api/clustering/results/${fileId}`);
  return response.data;
};

export const getClusteringResult = async (fileId: string, resultId: string) => {
  const response = await apiClient.get(`/api/clustering/results/${fileId}/${resultId}`);
  return response.data;
};

export const getClusterAnalysis = async (resultId: string) => {
  const response = await apiClient.get(`/api/clustering/analysis/${resultId}`);
  return response.data;
};

export const getClusterDetails = async (resultId: string, clusterId: number) => {
  const response = await apiClient.get(`/api/clustering/analysis/${resultId}/cluster/${clusterId}`);
  return response.data;
};

export const getNoisePoints = async (resultId: string) => {
  const response = await apiClient.get(`/api/clustering/analysis/${resultId}/noise`);
  return response.data;
};

export const getClusteringFeatures = async (resultId: string) => {
  const response = await apiClient.get(`/api/clustering/analysis/${resultId}/features`);
  return response.data;
};

// Notebooks
export const createNotebook = async (dataFileId: string) => {
  const response = await apiClient.post('/api/notebooks/create', {
    data_file_id: dataFileId,
  });
  return response.data;
};

export const getNotebookSession = async (sessionId: string) => {
  const response = await apiClient.get(`/api/notebooks/${sessionId}`);
  return response.data;
};

export default apiClient;

