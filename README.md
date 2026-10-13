# AI Chatbot - Full-Stack Application

A production-ready AI chatbot with FastAPI backend and React frontend. Features OpenAI GPT integration, SQLite persistence, and a modern responsive UI.
Made by Nicholas Fedlim. With help from DeepSeek AI.

## Features

### Backend
- ✅ RESTful API with FastAPI
- ✅ OpenAI GPT-3.5/GPT-4 integration
- ✅ SQLite database for persistent storage
- ✅ Rate limiting
- ✅ Comprehensive error handling
- ✅ Request logging
- ✅ Environment-based configuration
- ✅ Swagger/OpenAPI documentation
- ✅ Unit tests

### Frontend
- ✅ Modern React with TypeScript
- ✅ Tailwind CSS for styling
- ✅ Dark/light mode toggle
- ✅ Markdown rendering
- ✅ Real-time chat interface
- ✅ Auto-scrolling
- ✅ Typing indicator
- ✅ Message deletion
- ✅ Keyboard shortcuts
- ✅ Responsive design
- ✅ Accessibility features

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- OpenAI API key (optional, fallback available)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Edit .env and add your OpenAI API key (or leave empty for fallback mode)
6. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The API will be available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/api/docs`

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Run development server:
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`

## API Documentation
### POST /api/chat
Send a message to the AI and get a response.

Request:
```json
{
  "message": "Hello, how are you?",
  "conversation_id": "optional-conversation-id"
}
```

Response:
```json
{
  "message": "I'm doing well, thank you! How can I help you today?",
  "conversation_id": "generated-conversation-id",
  "timestamp": "2024-01-01T12:00:00Z",
  "model": "gpt-3.5-turbo",
  "tokens_used": 45,
  "latency_ms": 1234
}
```

### GET /api/history
Retrieve chat history.

Parameters:
- page (optional, default: 1)
- page_size (optional, default: 50)

Response:
```json
{
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Hello",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ],
  "total_count": 1,
  "page": 1,
  "page_size": 50
}
```

### DELETE /api/history/{message_id}
Delete a specific message.

### POST /api/clear
Clear all chat history.

## Configuration
Backend Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | `""` |
| `OPENAI_MODEL` | OpenAI model | `gpt-3.5-turbo` |
| `OPENAI_MAX_TOKENS` | Max tokens in response | `500` |
| `OPENAI_TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `DATABASE_URL` | SQLite database URL | `sqlite:///./chatbot.db` |
| `RATE_LIMIT_PER_MINUTE` | API rate limit | `30` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `localhost:3000,5173` |

### Testing
Run backend tests:
```bash
cd backend
pytest tests/
```

## Project Structure
```text
ai-chatbot/
├── backend/
│   ├── app/
│   │   ├── routers/      # API route handlers
│   │   ├── services/     # Business logic
│   │   ├── middleware/   # Custom middleware
│   │   ├── models.py     # Database models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI app
│   └── tests/            # Test files
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── contexts/     # Context providers
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript types
│   └── public/           # Static assets
└── README.md
```

### Performance Optimization
- Database indexing for faster queries
- Response caching for repeated queries
- Pagination for large histories
- Debounced input handling
- Lazy loading for non-critical components
- Minified production builds

### Security Features
- Rate limiting to prevent abuse
- Input validation and sanitization
- CORS configuration
- Environment variable management
- Error handling without sensitive data exposure
- SQL injection prevention via ORM

### Accessibility
- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- Sufficient color contrast
- Focus indicators
- Reduced motion support

### License
MIT

## Setup Instructions

1. **Clone and setup backend:**
```bash
# Create project directory
mkdir ai-chatbot
cd ai-chatbot

# Setup backend
mkdir backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Edit .env with your API key
uvicorn app.main:app --reload
```
2. Setup frontend (new terminal):

```bash
cd ai-chatbot/frontend
npm install
cp .env.example .env
npm run dev
```

3. Access the application:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/api/docs`

The chatbot will work immediately with the fallback mode even without an API key, but for the best experience, add your OpenAI API key to the backend .env file.
