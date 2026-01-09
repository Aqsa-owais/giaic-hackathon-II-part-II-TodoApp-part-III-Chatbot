'use client';

import { useState } from 'react';
import { TaskCreate } from '../../utils/types';
import Button from '../UI/Button';
import Input from '../UI/Input';

interface TodoFormProps {
  onAddTask: (taskData: TaskCreate) => void;
}

export default function TodoForm({ onAddTask }: TodoFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await onAddTask({
        title: title.trim(),
        description: description.trim() || undefined,
      });

      // Reset form
      setTitle('');
      setDescription('');
    } catch (err: any) {
      setError(err.message || 'Failed to create task');
      console.error('Error creating task:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6">
      <h2 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h2>

      {error && (
        <div className="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Input
            label="Task Title"
            id="title"
            name="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            required
          />
        </div>

        <div>
          <Input
            label="Description (Optional)"
            id="description"
            name="description"
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Additional details..."
          />
        </div>

        <div>
          <Button
            type="submit"
            className="w-full"
            isLoading={loading}
            disabled={loading}
          >
            {loading ? 'Creating task...' : 'Create Task'}
          </Button>
        </div>
      </form>
    </div>
  );
}