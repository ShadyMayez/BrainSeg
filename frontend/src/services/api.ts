import axios from 'axios';
import type { PredictionResponse, HealthStatus } from '@/types';

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 600000, // 10 minutes for large file uploads
  headers: {
    'Content-Type': 'application/json',
  },
  maxContentLength: Infinity,
  maxBodyLength: Infinity,
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('[API] Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const healthApi = {
  async check(): Promise<HealthStatus> {
    const response = await api.get('/health/');
    return response.data;
  },

  async checkModel(): Promise<{
    model_path: string;
    exists: boolean;
    loaded: boolean;
  }> {
    const response = await api.get('/health/model');
    return response.data;
  },

  async getConfig() {
    const response = await api.get('/health/config');
    return response.data;
  },

  async getEnvironment() {
    const response = await api.get('/health/environment');
    return response.data;
  },
};

export const predictionApi = {
  async predict(files: {
    flair: File;
    t1ce: File;
  }): Promise<PredictionResponse> {
    const formData = new FormData();
    formData.append('flair', files.flair);
    formData.append('t1ce', files.t1ce);

    const response = await api.post<PredictionResponse>('/predict/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      },
    });
    return response.data;
  },

  async getClasses(): Promise<Record<number, string>> {
    const response = await api.get('/predict/classes');
    return response.data;
  },

  async getModalities(): Promise<{
    modalities: string[];
    count: number;
    description: string;
  }> {
    const response = await api.get('/predict/modalities');
    return response.data;
  },

  async getModelInfo() {
    const response = await api.get('/predict/model-info');
    return response.data;
  },
};

export const dataApi = {
  async getDatasetInfo() {
    const response = await api.get('/data/dataset-info');
    return response.data;
  },

  async getFeatureStatistics() {
    const response = await api.get('/data/feature-statistics');
    return response.data;
  },

  async getTrainingMetrics() {
    const response = await api.get('/data/training-metrics');
    return response.data;
  },
};

export default api;
