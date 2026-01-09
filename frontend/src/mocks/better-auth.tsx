// Mock implementation of better-auth for building purposes
import React from 'react';

interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
}

interface SessionData {
  user: User;
}

interface SessionResult {
  data?: SessionData | null;
  status: 'authenticated' | 'unauthenticated' | 'loading';
}

// Mock components and functions to match the expected interface
export const BetterAuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <>{children}</>;
};

export const useSession = (): SessionResult => {
  return { data: null, status: 'unauthenticated' };
};

export const signIn = async (provider: string, credentials?: any) => {
  // Mock sign in function
  return {
    error: null,
    user: {
      id: '',
      email: '',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    },
    session: { token: '' }
  };
};

export const signOut = async (options?: any) => {
  // Mock sign out function
  return {};
};