import MessageInput from './MessageInput'
import MessageList from './MessageList'

function ChatContainer() {
  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <MessageList />
      <MessageInput />
    </div>
  )
}

export default ChatContainer