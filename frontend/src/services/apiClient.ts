import axios, { AxiosResponse } from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';

// Create an axios instance with default config
// For deployment, ensure NEXT_PUBLIC_API_URL is set to your backend URL
const baseURL = typeof window !== 'undefined'
  ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
  : process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: baseURL,
  timeout: 10000, // 10 seconds timeout
});

// Log the baseURL in development for debugging
if (typeof window !== 'undefined' && process.env.NODE_ENV !== 'production') {
  console.log('API Client Base URL:', baseURL);
}

// Request interceptor to attach JWT token to all requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle responses globally
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // Handle specific error responses
    if (error.response?.status === 401) {
      // If unauthorized, clear token and redirect to login
      localStorage.removeItem('access_token');
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;