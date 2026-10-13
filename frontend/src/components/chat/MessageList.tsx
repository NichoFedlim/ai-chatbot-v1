import React, { useRef, useEffect } from 'react';
import { useChat } from '@/contexts/ChatContext';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';
import { FaRobot } from 'react-icons/fa';

const MessageList: React.FC = () => {
  const { messages, isLoading, error } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <div className="w-20 h-20 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center mb-4">
          <FaRobot className="text-4xl text-primary-500" />
        </div>
        <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
          Welcome to AI Chatbot
        </h3>
        <p className="text-gray-500 dark:text-gray-400 max-w-md">
          Start a conversation with the AI assistant. Type your message below to begin.
        </p>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
      
      {isLoading && <TypingIndicator />}
      
      {error && (
        <div className="p-4 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded-lg">
          <p className="text-sm font-medium">Error</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      )}
      
      <div ref={bottomRef} />
    </div>
  );
};

export default MessageList;
