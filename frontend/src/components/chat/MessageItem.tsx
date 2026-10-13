import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { format } from 'date-fns';
import { FaUser, FaRobot, FaTrash, FaCopy, FaCheck } from 'react-icons/fa';
import clsx from 'clsx';
import type { ChatMessage } from '@/types';
import { useChat } from '@/contexts/ChatContext';

interface MessageItemProps {
  message: ChatMessage;
}

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const { deleteMessage } = useChat();
  const [copied, setCopied] = useState(false);

  const isUser = message.role === 'user';

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Delete this message?')) {
      await deleteMessage(message.id);
    }
  };

  return (
    <div
      className={clsx(
        'group flex items-start space-x-3 p-4 rounded-lg transition-all duration-200 animate-fade-in',
        isUser ? 'bg-primary-50 dark:bg-primary-900/20' : 'bg-gray-50 dark:bg-gray-800'
      )}
    >
      {/* Avatar */}
      <div
        className={clsx(
          'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
          isUser ? 'bg-primary-500' : 'bg-green-500'
        )}
      >
        {isUser ? (
          <FaUser className="text-white text-sm" />
        ) : (
          <FaRobot className="text-white text-sm" />
        )}
      </div>

      {/* Message content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-1">
          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
            {isUser ? 'You' : 'AI Assistant'}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {format(new Date(message.timestamp), 'HH:mm')}
          </span>
        </div>

        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>

        {message.model && (
          <div className="mt-2 text-xs text-gray-400 dark:text-gray-500">
            Model: {message.model}
            {message.tokens_used && ` • ${message.tokens_used} tokens`}
          </div>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="flex space-x-1">
          <button
            onClick={handleCopy}
            className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
            title="Copy message"
          >
            {copied ? <FaCheck className="text-green-500" /> : <FaCopy />}
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400 transition-colors"
            title="Delete message"
          >
            <FaTrash />
          </button>
        </div>
      </div>
    </div>
  );
};

export default MessageItem;
