import ChatContainer from './components/chat/ChatContainer'
import Header from './components/layout/header'
import { ChatProvider } from './contexts/ChatContext'
import { ThemeProvider } from './contexts/ThemeContext'

function App() {
  return (
    <ThemeProvider>
      <ChatProvider>
        <div className="flex min-h-screen flex-col bg-gray-100 dark:bg-gray-950">
          <Header />
          <main className="mx-auto flex w-full max-w-4xl flex-1 flex-col overflow-hidden bg-white shadow-xl dark:bg-gray-900">
            <ChatContainer />
          </main>
        </div>
      </ChatProvider>
    </ThemeProvider>
  )
}

export default App
