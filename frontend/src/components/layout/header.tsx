import React from 'react';
import { FaRobot, FaTrash, FaPlus, FaMoon, FaSun } from 'react-icons/fa';
import { useTheme } from '@/contexts/ThemeContext';
import { useChat } from '@/contexts/ChatContext';

const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();
  const { clearHistory } = useChat();

  const handleClearHistory = async () => {
    if (window.confirm('Clear all chat history? This action cannot be undone.')) {
      await clearHistory();
    }
  };

  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-full bg-primary-500 flex items-center justify-center">
            <FaRobot className="text-white text-xl" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 dark:text-white">
              AI Chatbot
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Your AI assistant
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => window.location.reload()}
            className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title="New Chat"
          >
            <FaPlus />
          </button>
          
          <button
            onClick={handleClearHistory}
            className="p-2 text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title="Clear History"
          >
            <FaTrash />
          </button>
          
          <button
            onClick={toggleTheme}
            className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <FaMoon /> : <FaSun />}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;