'use client';

import { useState } from 'react';
import { Task } from '../../utils/types';
import Button from '../UI/Button';
import Input from '../UI/Input';

interface TodoItemProps {
  task: Task;
  onUpdate: (taskId: string, taskUpdates: Partial<Task>) => void;
  onToggleCompletion: (taskId: string) => void;
  onDelete: (taskId: string) => void;
}

export default function TodoItem({ task, onUpdate, onToggleCompletion, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    setLoading(true);
    try {
      await onUpdate(task.id, {
        title: editTitle,
        description: editDescription,
      });
      setIsEditing(false);
    } catch (err) {
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async () => {
    try {
      await onToggleCompletion(task.id);
    } catch (err) {
      console.error('Error toggling task completion:', err);
    }
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      try {
        await onDelete(task.id);
      } catch (err) {
        console.error('Error deleting task:', err);
      }
    }
  };

  return (
    <li className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-grow">
          <input
            type="checkbox"
            checked={task.is_completed}
            onChange={handleToggle}
            className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />

          <div className="flex-grow">
            {isEditing ? (
              <div className="space-y-3">
                <Input
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="font-medium"
                />
                <Input
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  placeholder="Description (optional)"
                />
                <div className="flex space-x-2">
                  <Button
                    onClick={handleSave}
                    isLoading={loading}
                    disabled={loading}
                    size="sm"
                  >
                    Save
                  </Button>
                  <Button
                    onClick={() => setIsEditing(false)}
                    variant="secondary"
                    size="sm"
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div>
                <h3 className={`${task.is_completed ? 'line-through text-gray-500' : 'text-gray-900'} font-medium`}>
                  {task.title}
                </h3>
                {task.description && (
                  <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                )}
                <p className="mt-2 text-xs text-gray-500">
                  Created: {new Date(task.created_at).toLocaleDateString()}
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="flex space-x-2 ml-2">
          {!isEditing && (
            <Button
              onClick={() => setIsEditing(true)}
              variant="secondary"
              size="sm"
            >
              Edit
            </Button>
          )}
          <Button
            onClick={handleDelete}
            variant="danger"
            size="sm"
          >
            Delete
          </Button>
        </div>
      </div>
    </li>
  );
}