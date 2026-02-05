'use client';

import { useState, useRef, useEffect } from 'react';
import Button from '../UI/Button';
import Input from '../UI/Input';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  actions_taken?: Array<{
    tool: string;
    result: any;
    status: string;
  }>;
}

interface ChatInterfaceProps {
  userId: string;
}

export default function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      const token = localStorage.getItem('access_token');

      const response = await fetch(`${apiUrl}/api/v1/users/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: inputMessage,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Set conversation ID if this is the first message
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: data.timestamp,
        actions_taken: data.actions_taken
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatActionResult = (action: any) => {
    if (action.tool === 'list_tasks' && action.result.tasks) {
      return `Found ${action.result.count} tasks`;
    } else if (action.tool === 'add_task' && action.result.title) {
      return `Created task: "${action.result.title}"`;
    } else if (action.tool === 'update_task' && action.result.title) {
      return `Updated task: "${action.result.title}"`;
    } else if (action.tool === 'complete_task' && action.result.title) {
      return `Marked "${action.result.title}" as ${action.result.is_completed ? 'completed' : 'incomplete'}`;
    } else if (action.tool === 'delete_task' && action.result.message) {
      return action.result.message;
    }
    return `Executed ${action.tool}`;
  };

  return (
    <div className="flex flex-col h-96 bg-white border rounded-lg shadow-sm">
      {/* Header */}
      <div className="px-4 py-3 border-b bg-gray-50 rounded-t-lg">
        <h3 className="text-lg font-medium text-gray-900">AI Task Assistant</h3>
        <p className="text-sm text-gray-500">
          Ask me to create, update, complete, or delete your tasks using natural language!
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 py-8">
            <p className="mb-2">👋 Hi! I'm your AI task assistant.</p>
            <p className="text-sm">Try saying things like:</p>
            <ul className="text-sm mt-2 space-y-1">
              <li>"Create a task to buy groceries"</li>
              <li>"Show me all my tasks"</li>
              <li>"Mark the grocery task as complete"</li>
              <li>"Delete the completed tasks"</li>
            </ul>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <p className="text-sm">{message.content}</p>
              
              {/* Show actions taken by the AI */}
              {message.actions_taken && message.actions_taken.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-200">
                  <p className="text-xs text-gray-600 mb-1">Actions taken:</p>
                  {message.actions_taken.map((action, index) => (
                    <div key={index} className="text-xs text-gray-600">
                      ✓ {formatActionResult(action)}
                    </div>
                  ))}
                </div>
              )}
              
              <p className="text-xs mt-1 opacity-70">
                {new Date(message.timestamp * 1000).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 max-w-xs lg:max-w-md px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                <span className="text-sm">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="px-4 py-3 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here... (e.g., 'Create a task to call mom')"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={isLoading}
          />
          <Button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-4 py-2"
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}