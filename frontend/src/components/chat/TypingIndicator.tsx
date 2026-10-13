import React from 'react';
import { FaRobot } from 'react-icons/fa';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-start space-x-3 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg animate-fade-in">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
        <FaRobot className="text-white text-sm" />
      </div>
      
      <div className="flex-1">
        <div className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
          AI Assistant is typing
        </div>
        <div className="flex space-x-1">
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
