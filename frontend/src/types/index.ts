// Type definitions for the chat application

export interface ChatMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  is_deleted?: boolean;
  model?: string;
  tokens_used?: number;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  timestamp: string;
  model: string;
  tokens_used?: number;
  latency_ms?: number;
}

export interface HistoryResponse {
  messages: ChatMessage[];
  total_count: number;
  page: number;
  page_size: number;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
  status_code: number;
}

export type Theme = 'light' | 'dark';

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  conversationId: string | null;
}