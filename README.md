# Vitta Setu

Vitta Setu is a production-ready, SaaS-style UPI Payment Bridge built with Python Flask and Clean Architecture principles. It bridges merchant websites with UPI applications by creating secure temporary payment sessions.

## Features
- **Clean Architecture:** Strict separation between Routes, Services, Repositories, and Models.
- **Merchant Dashboard:** Comprehensive analytics, API key management, and transaction history.
- **Payment Experience:** Premium glassmorphism UI, 10-minute animated countdown timer.
- **Desktop Synchronization:** Real-time Server-Sent Events (SSE) synchronization between desktop QR and mobile scanners.
- **Reliable Webhooks:** HMAC-SHA256 signed callbacks with exponential backoff delivery retries.
- **API Playground:** Built-in interactive documentation and testing suite with multi-language code examples.
- **Enterprise Security:** API Key authentication, idempotency, rate limiting, and strictly versioned API endpoints.

## Deployment

The application is containerized and ready for production deployment using Docker Compose.

1. Create a `.env` file from `.env.example` and update the `SECRET_KEY`.
2. Build and start the stack:
   ```bash
   docker-compose up -d --build
   ```
3. The Nginx reverse proxy ensures SSE endpoints work smoothly by disabling proxy buffering for `/payment/stream`.

## Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
python run.py
```

## Architecture Layers
- `app/routes/`: Controllers handling HTTP requests.
- `app/services/`: Core business logic (Payments, Auth, Callbacks).
- `app/repositories/`: Data access abstraction over SQLAlchemy.
- `app/models/`: Database schema definitions.
