'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import authService from '@/services/authService';
import TodoList from '@/components/Todo/TodoList';
import ChatInterface from '@/components/Chat/ChatInterface';
import Button from '@/components/UI/Button';

export default function Dashboard() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'todos' | 'chat'>('todos');
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    if (!authService.isAuthenticated()) {
      router.push('/login');
      return;
    }

    // Get user info from auth service
    const fetchUser = async () => {
      try {
        const userInfo = await authService.getCurrentUser();
        if (!userInfo) {
          // If we can't get user info, the token might be invalid
          authService.logout();
          router.push('/login');
          return;
        }
        setUser(userInfo);
      } catch (error) {
        console.error('Error fetching user info:', error);
        authService.logout();
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [router]);

  const handleLogout = () => {
    authService.logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-900">Todo Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user.email}</span>
            <Button
              onClick={handleLogout}
              variant="secondary"
            >
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('todos')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'todos'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📝 My Tasks
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'chat'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              🤖 AI Assistant
            </button>
          </nav>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {activeTab === 'todos' && (
          <div className="bg-white shadow rounded-lg p-6">
            <div className="mb-4">
              <h2 className="text-lg font-medium text-gray-900 mb-2">Your Tasks</h2>
              <p className="text-sm text-gray-600">
                Manage your tasks manually or use the AI Assistant tab to manage them with natural language.
              </p>
            </div>
            <TodoList userId={user.id} />
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="space-y-6">
            <div className="bg-white shadow rounded-lg p-6">
              <div className="mb-4">
                <h2 className="text-lg font-medium text-gray-900 mb-2">AI Task Assistant</h2>
                <p className="text-sm text-gray-600">
                  Use natural language to manage your tasks. Try commands like "create a task to buy groceries" 
                  or "show me all my completed tasks".
                </p>
              </div>
              <ChatInterface userId={user.id} />
            </div>
            
            {/* Quick Examples */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-sm font-medium text-blue-900 mb-2">💡 Try these examples:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-blue-800">
                <div>• "Create a task to call mom tomorrow"</div>
                <div>• "Show me all my tasks"</div>
                <div>• "Mark the grocery shopping task as complete"</div>
                <div>• "Update my workout task description"</div>
                <div>• "Delete all completed tasks"</div>
                <div>• "What tasks do I have for today?"</div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}