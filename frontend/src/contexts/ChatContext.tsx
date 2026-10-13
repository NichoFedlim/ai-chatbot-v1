import React, { createContext, useContext, useReducer, useCallback } from 'react';
import type { ChatMessage, ChatState } from '@/types';
import { chatService } from '@/services/api';

// Action types
type ChatAction =
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_CONVERSATION_ID'; payload: string }
  | { type: 'CLEAR_MESSAGES' }
  | { type: 'DELETE_MESSAGE'; payload: number }
  | { type: 'LOAD_HISTORY'; payload: ChatMessage[] };

// Initial state
const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  conversationId: null,
};

// Reducer
function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case 'ADD_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, action.payload],
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
      };
    case 'SET_CONVERSATION_ID':
      return {
        ...state,
        conversationId: action.payload,
      };
    case 'CLEAR_MESSAGES':
      return {
        ...state,
        messages: [],
        conversationId: null,
      };
    case 'DELETE_MESSAGE':
      return {
        ...state,
        messages: state.messages.filter(msg => msg.id !== action.payload),
      };
    case 'LOAD_HISTORY':
      return {
        ...state,
        messages: action.payload,
      };
    default:
      return state;
  }
}

// Context interface
interface ChatContextType extends ChatState {
  sendMessage: (message: string) => Promise<void>;
  deleteMessage: (messageId: number) => Promise<void>;
  clearHistory: () => Promise<void>;
  loadHistory: () => Promise<void>;
}

// Create context
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Provider component
export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Send message to AI
  const sendMessage = useCallback(async (message: string) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_ERROR', payload: null });

      // Add user message immediately
      const userMessage: ChatMessage = {
        id: Date.now(), // Temporary ID
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
      };
      dispatch({ type: 'ADD_MESSAGE', payload: userMessage });

      // Get AI response
      const response = await chatService.sendMessage(message, state.conversationId || undefined);
      
      // Update conversation ID
      if (response.conversation_id) {
        dispatch({ type: 'SET_CONVERSATION_ID', payload: response.conversation_id });
      }

      // Add AI response
      const aiMessage: ChatMessage = {
        id: Date.now() + 1, // Temporary ID
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
        model: response.model,
        tokens_used: response.tokens_used,
      };
      dispatch({ type: 'ADD_MESSAGE', payload: aiMessage });

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to send message';
      dispatch({ type: 'SET_ERROR', payload: errorMessage });
      console.error('Error sending message:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  }, [state.conversationId]);

  // Delete message
  const deleteMessage = useCallback(async (messageId: number) => {
    try {
      await chatService.deleteMessage(messageId);
      dispatch({ type: 'DELETE_MESSAGE', payload: messageId });
    } catch (error) {
      console.error('Error deleting message:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to delete message' });
    }
  }, []);

  // Clear history
  const clearHistory = useCallback(async () => {
    try {
      await chatService.clearHistory();
      dispatch({ type: 'CLEAR_MESSAGES' });
    } catch (error) {
      console.error('Error clearing history:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to clear history' });
    }
  }, []);

  // Load history
  const loadHistory = useCallback(async () => {
    try {
      const response = await chatService.getHistory(1, 100);
      dispatch({ type: 'LOAD_HISTORY', payload: response.messages });
    } catch (error) {
      console.error('Error loading history:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to load history' });
    }
  }, []);

  const contextValue: ChatContextType = {
    ...state,
    sendMessage,
    deleteMessage,
    clearHistory,
    loadHistory,
  };

  return (
    <ChatContext.Provider value={contextValue}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use chat context
export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};