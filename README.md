# True Download Manager

A modern, feature-rich download manager built with FastAPI and React.

## Features

- Multi-threaded downloads for faster speed
- Media extraction support (YouTube, social media, etc.)
- Real-time download progress via WebSocket
- Beautiful and responsive UI
- Download history and management
- JWT authentication for secure access

## Tech Stack

### Backend
- FastAPI (Python web framework)
- yt-dlp (Media extraction)
- Selenium (Web automation)
- Celery (Background tasks)
- WebSocket (Real-time updates)

### Frontend
- React
- Material-UI
- WebSocket client

## Setup

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```
4. Start the development servers:
   - Backend: `uvicorn main:app --reload`
   - Frontend: `npm start`

## Docker Deployment

Use Docker Compose to run all services:
```bash
docker-compose up
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
