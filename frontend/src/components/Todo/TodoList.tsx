'use client';

import { useState, useEffect } from 'react';
import { Task } from '../../utils/types';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';
import todoService from '../../services/todoService';
import authService from '../../services/authService';
import Button from '../UI/Button';

interface TodoListProps {
  userId: string;
}

export default function TodoList({ userId }: TodoListProps) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Load tasks when component mounts
  useEffect(() => {
    fetchTasks();
  }, [userId]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const userTasks = await todoService.getUserTasks(userId);
      setTasks(userTasks);
    } catch (err: any) {
      setError(err.message || 'Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (taskData: { title: string; description?: string }) => {
    try {
      const newTask = await todoService.createTask(userId, taskData);
      setTasks([...tasks, newTask]);
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (taskId: string, taskUpdates: Partial<Task>) => {
    try {
      const updatedTask = await todoService.updateTask(userId, taskId, taskUpdates);
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleToggleCompletion = async (taskId: string) => {
    try {
      const updatedTask = await todoService.toggleTaskCompletion(userId, taskId);
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err: any) {
      setError(err.message || 'Failed to toggle task completion');
      console.error('Error toggling task completion:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await todoService.deleteTask(userId, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <TodoForm onAddTask={handleAddTask} />

      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Your Tasks ({tasks.length})</h2>

        {tasks.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">No tasks yet. Add your first task above!</p>
          </div>
        ) : (
          <ul className="space-y-3">
            {tasks.map((task) => (
              <TodoItem
                key={task.id}
                task={task}
                onUpdate={handleUpdateTask}
                onToggleCompletion={handleToggleCompletion}
                onDelete={handleDeleteTask}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}