import axios from 'axios';
import type { AxiosError, AxiosInstance } from 'axios';
import type { ChatRequest, ChatResponse, HistoryResponse } from '@/types';

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens if needed (not required for single-user app)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle different error types
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      console.error('API Error:', { status, data });
      
      if (status === 429) {
        throw new Error('Rate limit exceeded. Please wait before sending more messages.');
      } else if (status >= 500) {
        throw new Error('Server error. Please try again later.');
      }
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
      throw new Error('Network error. Please check your connection.');
    }
    
    throw error;
  }
);

// API service functions
export const chatService = {
  // Send message and get AI response
  async sendMessage(message: string, conversationId?: string): Promise<ChatResponse> {
    try {
      const request: ChatRequest = {
        message,
        conversation_id: conversationId,
      };
      
      const response = await api.post<ChatResponse>('/api/chat', request);
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  // Get chat history
  async getHistory(page: number = 1, pageSize: number = 100): Promise<HistoryResponse> {
    try {
      const response = await api.get<HistoryResponse>('/api/history', {
        params: { page, page_size: pageSize },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching history:', error);
      throw error;
    }
  },

  // Delete specific message
  async deleteMessage(messageId: number): Promise<void> {
    try {
      await api.delete(`/api/history/${messageId}`);
    } catch (error) {
      console.error('Error deleting message:', error);
      throw error;
    }
  },

  // Clear all history
  async clearHistory(): Promise<void> {
    try {
      await api.post('/api/clear');
    } catch (error) {
      console.error('Error clearing history:', error);
      throw error;
    }
  },
};

export default api;