# True Download Manager


A modern, efficient download manager built with FastAPI and React.

## Project Structure

```
true-download-manager/
│
├── backend/                   # FastAPI & Python backend
├── frontend/                  # React frontend code
├── docker-compose.yml         # Docker Compose configuration for all services
├── README.md                  # Project documentation
└── .gitignore                 # Files/directories to exclude from Git
```

## Features

Multi-threaded downloads for faster speed
Media extraction support (YouTube, social media, etc.)
Real-time download progress via WebSocket
Beautiful and responsive UI
Download history and management
JWT authentication for secure access
=======
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
- PostgreSQL (Database)
- Redis (Message broker)

### Frontend
- React (JavaScript library)
- Material-UI (Component library)
- WebSocket (Real-time updates)

### Desktop Wrapper
- Electron (Cross-platform desktop application framework)

## Prerequisites

- Docker (for backend and database services)
- Node.js & npm/yarn (for frontend and Electron development)
- Python 3.x (for backend development)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/true-download-manager.git
   cd true-download-manager
   ```

2. Start the application:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs


## License

MIT License
=======
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
