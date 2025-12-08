# Hybrid Analyzer API

A FastAPI backend for text analysis using HuggingFace zero-shot classification and Google Gemini for summarization and tone detection.

## Features

- **Authentication**: JWT-based authentication with HTTP-only cookies
- **Text Classification**: Zero-shot classification using HuggingFace BART-MNLI
- **Summarization**: Contextual text summarization using Google Gemini
- **Tone Analysis**: Automatic tone detection (positif/neutre/negatif)
- **Latency Metrics**: Detailed execution time tracking for all API calls

## Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- HuggingFace Inference API
- Google Gemini API

## Installation

### 1. Clone and setup virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Install dependencies

```bash
pip install -r app/requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the `backend` directory:

```env
# Database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=hybrid_analyzer

# JWT Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# API Keys
HF_TOKEN=hf_your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create new user account |
| POST | `/auth/login` | Login and receive JWT cookie |
| GET | `/auth/me` | Get current user info (requires auth) |
| POST | `/auth/logout` | Clear authentication cookie |

### Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze/` | Analyze text (requires auth) |
| GET | `/analyze/health` | Health check |

## Usage

### Register a new user

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}' \
  -c cookies.txt
```

### Analyze text

```bash
curl -X POST "http://localhost:8000/analyze/" \
  -H "Content-Type: application/json" \
  -d '{"text": "The new smartphone features an advanced AI chip with 50% faster performance."}' \
  -b cookies.txt
```

### Response format

```json
{
  "category": "technology",
  "hf_scores": {
    "technology": 0.9234,
    "business": 0.0421,
    "science": 0.0198
  },
  "summary": "The article discusses a new smartphone with advanced AI capabilities...",
  "tone": "positif",
  "meta": {
    "hf_latency_ms": 456,
    "gemini_latency_ms": 892,
    "total_execution_ms": 1348
  }
}
```

## Project Structure

```
backend/
├── app/
│   ├── config.py              # Environment configuration
│   ├── main.py                # FastAPI application entry point
│   ├── database/
│   │   ├── base.py            # SQLAlchemy Base
│   │   └── connection.py      # Database connection
│   ├── models/
│   │   └── user.py            # User model
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── analyze.py         # Analysis endpoint
│   │   └── db_check.py        # Database health check
│   ├── schemas/
│   │   ├── user_schema.py     # User Pydantic schemas
│   │   └── analyze_schema.py  # Analysis Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── huggingface_service.py  # HuggingFace API client
│   │   └── gemini_service.py  # Gemini API client
│   └── utils/
│       └── security.py        # Password hashing and JWT
├── .env                       # Environment variables
├── .env.example               # Environment template
└── requirements.txt           # Python dependencies
```

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API returns structured error responses:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad request (validation error) |
| 401 | Unauthorized (invalid/missing JWT) |
| 503 | Service unavailable (AI API error) |

## Rate Limits

Note that Gemini API has rate limits on the free tier. If you encounter 429 errors, wait approximately 30-60 seconds before retrying.

## License

MIT
