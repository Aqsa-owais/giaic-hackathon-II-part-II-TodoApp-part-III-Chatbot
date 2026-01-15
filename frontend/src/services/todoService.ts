import apiClient from './apiClient';
import { Task, TaskCreate, TaskUpdate } from '../utils/types';

class TodoService {
  /**
   * Get all tasks for a specific user
   */
  async getUserTasks(userId: string): Promise<Task[]> {
    try {
      const response = await apiClient.get(`/api/${userId}/tasks`);
      return response.data;
    } catch (error: any) {
      // More robust error handling
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail ||
                            error.response.data?.message ||
                            error.response.statusText ||
                            'Failed to fetch tasks';
        throw new Error(errorMessage);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to connect to server');
      } else {
        // Something else happened
        throw new Error(error.message || 'Failed to fetch tasks');
      }
    }
  }

  /**
   * Get a specific task by ID for a user
   */
  async getTaskById(userId: string, taskId: string): Promise<Task> {
    try {
      const response = await apiClient.get(`/api/${userId}/tasks/${taskId}`);
      return response.data;
    } catch (error: any) {
      // More robust error handling
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail ||
                            error.response.data?.message ||
                            error.response.statusText ||
                            'Failed to fetch task';
        throw new Error(errorMessage);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to connect to server');
      } else {
        // Something else happened
        throw new Error(error.message || 'Failed to fetch task');
      }
    }
  }

  /**
   * Create a new task for a user
   */
  async createTask(userId: string, taskData: TaskCreate): Promise<Task> {
    try {
      const response = await apiClient.post(`/api/${userId}/tasks`, taskData);
      return response.data;
    } catch (error: any) {
      // More robust error handling
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail ||
                            error.response.data?.message ||
                            error.response.statusText ||
                            'Failed to create task';
        throw new Error(errorMessage);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to connect to server');
      } else {
        // Something else happened
        throw new Error(error.message || 'Failed to create task');
      }
    }
  }

  /**
   * Update a specific task for a user
   */
  async updateTask(userId: string, taskId: string, taskData: TaskUpdate): Promise<Task> {
    try {
      const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, taskData);
      return response.data;
    } catch (error: any) {
      // More robust error handling
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail ||
                            error.response.data?.message ||
                            error.response.statusText ||
                            'Failed to update task';
        throw new Error(errorMessage);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to connect to server');
      } else {
        // Something else happened
        throw new Error(error.message || 'Failed to update task');
      }
    }
  }

  /**
   * Delete a specific task for a user
   */
  async deleteTask(userId: string, taskId: string): Promise<void> {
    try {
      await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
    } catch (error: any) {
      // More robust error handling
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail ||
                            error.response.data?.message ||
                            error.response.statusText ||
                            'Failed to delete task';
        throw new Error(errorMessage);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to connect to server');
      } else {
        // Something else happened
        throw new Error(error.message || 'Failed to delete task');
      }
    }
  }

  /**
   * Toggle the completion status of a specific task for a user
   */
  async toggleTaskCompletion(userId: string, taskId: string): Promise<Task> {
    try {
      const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/complete`);
      return response.data;
    } catch (error: any) {
      // More robust error handling
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail ||
                            error.response.data?.message ||
                            error.response.statusText ||
                            'Failed to toggle task completion';
        throw new Error(errorMessage);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('Network error: Unable to connect to server');
      } else {
        // Something else happened
        throw new Error(error.message || 'Failed to toggle task completion');
      }
    }
  }
}

const todoService = new TodoService();
export default todoService;