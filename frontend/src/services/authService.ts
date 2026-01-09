// Better Auth service wrapper
import { signIn, signOut, useSession } from '../mocks/better-auth';
import { User } from '../utils/types';

class AuthService {
  /**
   * Register a new user
   */
  async register(userData: { email: string; password: string }): Promise<{ user: User; token: string }> {
    try {
      // For registration, we'll make a direct API call to our backend
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      // After successful registration, trigger login
      const loginResult = await this.login(userData);
      return loginResult;
    } catch (error: any) {
      throw new Error(error.message || 'Registration failed');
    }
  }

  /**
   * Log in an existing user
   */
  async login(credentials: { email: string; password: string }): Promise<{ user: User; token: string }> {
    try {
      const result = await signIn('credentials', {
        ...credentials,
        redirect: false,
      });

      if (result?.error) {
        throw new Error(result.error);
      }

      // For Better Auth, we don't need to manually manage tokens
      // Better Auth handles this internally
      return { user: result?.user || null, token: result?.session?.token || '' };
    } catch (error: any) {
      throw new Error(error.message || 'Login failed');
    }
  }

  /**
   * Log out the current user
   */
  async logout(): Promise<void> {
    await signOut({ redirect: false });
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    // This will use Better Auth's session management
    // In practice, you'd typically use the useSession hook in components
    const token = localStorage.getItem('access_token');
    return !!token;
  }

  /**
   * Get the current user's token
   */
  getToken(): string | null {
    // With Better Auth, token management is handled internally
    // This is maintained for compatibility
    return localStorage.getItem('access_token');
  }

  /**
   * Get the current user's info
   */
  async getCurrentUser(): Promise<User | null> {
    // With Better Auth, use the useSession hook in components
    // This is maintained for compatibility
    try {
      const response = await fetch('/api/auth/me');
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      return null;
    }
  }
}

export default new AuthService();