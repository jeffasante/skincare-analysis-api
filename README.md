# Skincare Analysis API

A FastAPI-based backend service for mobile image upload and skincare analysis simulation.

## Table of Contents

- [Features](#features)
- [How to Run the Service](#how-to-run-the-service)
- [Available Endpoints](#available-endpoints)
- [Example Usage](#example-usage)
- [Design Decisions & Assumptions](#design-decisions--assumptions)
- [Production Improvements](#production-improvements)

## Features

- Image upload with validation (JPEG/PNG, max 5MB)
- Mock skincare analysis with structured responses
- Comprehensive error handling
- Clean separation of concerns
- API key authentication (bonus feature)
- Request logging (bonus feature)
- Docker support (bonus feature)

## How to Run the Service

### Option 1: Local Setup

**Prerequisites:**

- Python 3.8+
- pip
- libmagic (for file type validation)
  - macOS: `brew install libmagic`
  - Ubuntu/Debian: `sudo apt-get install libmagic1`
  - Windows: Install python-magic-bin instead

**Installation Steps:**

```bash
# Navigate to project directory
cd skincare-analysis-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Option 2: Docker (Recommended)

Docker includes all dependencies and provides a consistent environment.

```bash
# Build the image
docker build -t skincare-api .

# Run the container
docker run -d -p 8000:8000 --name skincare-api-container skincare-api

# View logs
docker logs -f skincare-api-container

# Stop the container
docker stop skincare-api-container

# Remove the container
docker rm skincare-api-container
```

## Available Endpoints

### API Documentation

Once running, interactive API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Authentication

All endpoints (except `/health` and documentation endpoints) require an API key in the request header:

```
X-API-Key: dev-api-key-12345
```

For production environments, set a custom API key using the `API_KEY` environment variable.

### Endpoint Details

#### 1. Health Check

```http
GET /health
```

**Purpose:** Verify service is running and responsive.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2026-01-05T10:30:00Z"
}
```

#### 2. Upload Image

```http
POST /upload
Content-Type: multipart/form-data
X-API-Key: dev-api-key-12345
```

**Purpose:** Upload an image for analysis.

**Parameters:**

- `file`: Image file (JPEG or PNG, max 5MB)

**Validation:**

- File type checked by extension and content (magic numbers)
- File size enforced (5MB maximum)
- Invalid uploads return meaningful error messages

**Success Response (200):**

```json
{
  "image_id": "abc123def456",
  "filename": "my_photo.jpg",
  "size": 2048576,
  "uploaded_at": "2026-01-05T10:30:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid file type or size exceeded
- `401 Unauthorized`: Missing or invalid API key
- `500 Internal Server Error`: Server error during upload

#### 3. Analyze Image

```http
POST /analyze
Content-Type: application/json
X-API-Key: dev-api-key-12345
```

**Purpose:** Perform mock analysis on a previously uploaded image.

**Request Body:**

```json
{
  "image_id": "abc123def456"
}
```

**Success Response (200):**

```json
{
  "image_id": "abc123def456",
  "skin_type": "Combination",
  "issues": ["Hyperpigmentation", "Fine Lines"],
  "confidence": 0.87,
  "recommendations": [
    "Use vitamin C serum for hyperpigmentation",
    "Apply retinol for fine lines"
  ],
  "analyzed_at": "2026-01-05T10:31:00Z"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid image_id format
- `404 Not Found`: Image ID not found
- `401 Unauthorized`: Missing or invalid API key
- `500 Internal Server Error`: Server error during analysis

## Example Usage

### Using cURL

```bash
# Health check (no API key required)
curl http://localhost:8000/health

# Upload an image
curl -X POST "http://localhost:8000/upload" \
  -H "X-API-Key: dev-api-key-12345" \
  -F "file=@/path/to/your/image.jpg"

# Analyze the image (use image_id from upload response)
curl -X POST "http://localhost:8000/analyze" \
  -H "X-API-Key: dev-api-key-12345" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "abc123def456"}'
```

### Using Python

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "dev-api-key-12345"
headers = {"X-API-Key": API_KEY}

# Upload image
with open("photo.jpg", "rb") as f:
    response = requests.post(
        f"{API_URL}/upload",
        headers=headers,
        files={"file": f}
    )
    data = response.json()
    image_id = data["image_id"]
    print(f"Uploaded: {image_id}")

# Analyze image
response = requests.post(
    f"{API_URL}/analyze",
    headers=headers,
    json={"image_id": image_id}
)
result = response.json()
print(f"Skin Type: {result['skin_type']}")
print(f"Issues: {', '.join(result['issues'])}")
print(f"Confidence: {result['confidence']}")
```

### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Click on an endpoint (e.g., POST /upload)
3. Click "Try it out"
4. Add the API key in the "X-API-Key" field: `dev-api-key-12345`
5. Upload a file or provide request body
6. Click "Execute"

## Design Decisions & Assumptions

### Current Implementation

**1. Local File Storage**

- Images stored on the filesystem in `uploads/` directory
- Simple implementation with no external dependencies
- File names use UUID (first 16 characters) to prevent collisions
- Suitable for development, testing, and demonstration

**2. Mock Analysis Logic**

- Deterministic results based on image dimensions
- Simulates realistic AI analysis patterns
- Returns skin type, issues (1-3), confidence scores (0.75-0.95), and recommendations
- No actual ML model required for this demonstration

**3. Simple API Key Authentication**

- Header-based authentication: `X-API-Key`
- Default key for development: `dev-api-key-12345`
- Configurable via environment variable for production
- Sufficient for demonstration and early development

**4. Multi-Layer Validation**

- **Extension validation**: Checks file extension against whitelist
- **Size validation**: Enforces 5MB maximum file size
- **Content validation**: Uses magic numbers to verify actual file type
- Prevents malicious uploads and provides clear error messages

**5. Error Handling**

- Meaningful HTTP status codes
- Descriptive error messages in responses
- Comprehensive logging for debugging
- Graceful failure with cleanup (e.g., removing invalid uploaded files)

**6. Separation of Concerns**

- **Routes**: HTTP request/response handling
- **Services**: Business logic and data operations
- **Utils**: Reusable validation and helper functions
- **Config**: Centralized configuration management

### Key Assumptions

1. **Single-tenant use**: No user management or multi-tenancy required
2. **Synchronous processing**: Analysis returns immediately (no job queue needed for mock logic)
3. **No persistent database**: File metadata not stored beyond API responses
4. **Development environment**: Default API key acceptable for demo purposes
5. **Image retention**: Uploaded images persist indefinitely (no automatic cleanup)
6. **Network**: API runs on trusted network or behind additional security layers

## Production Improvements

If this were a production system, the following enhancements would be necessary:

#### 1. Storage

- Cloud storage (AWS S3, GCS, Azure Blob)
- CDN for image delivery
- Automatic cleanup of old images
- Image optimization and compression

#### 2. Database

- PostgreSQL or MongoDB for metadata
- Track upload history and analysis results
- Enable querying and analytics
- User association and history

#### 3. Real AI Integration

- TensorFlow/PyTorch model integration
- Async processing queue (Celery, Redis Queue)
- GPU support for inference
- Model versioning and A/B testing

#### 4. Security

- JWT-based authentication
- Rate limiting per user/IP
- Image sanitization and virus scanning
- HTTPS only
- Input validation with schema enforcement
- CORS configuration for specific origins

#### 5. Observability

- Structured logging (JSON format)
- Metrics collection (Prometheus)
- Distributed tracing (OpenTelemetry)
- Error tracking (Sentry)
- Performance monitoring

#### 6. Performance

- Redis caching for analysis results
- Image preprocessing pipeline
- Database connection pooling
- Horizontal scaling with load balancer
- Async/await optimization

#### 7. Testing

- Unit tests (pytest)
- Integration tests
- Load testing (Locust, k6)
- CI/CD pipeline (GitHub Actions)
- Code coverage reporting

#### 8. API Design

- Versioning (`/v1/upload`, `/v2/upload`)
- Pagination for list endpoints
- Filtering and sorting options
- Backward compatibility strategy
- API deprecation notices

#### 9. Compliance

- GDPR compliance (data retention, right to deletion)
- HIPAA if medical (encryption at rest/transit, audit logs)
- Terms of service acceptance tracking
- Privacy policy enforcement

#### 10. Infrastructure

- Kubernetes deployment
- Auto-scaling configuration
- Health checks and readiness probes
- Blue-green deployment
- Disaster recovery plan

## Environment Variables

```bash
# API Configuration
API_KEY=your-secret-api-key-here
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880  # 5MB in bytes

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## Troubleshooting

**Issue**: "File not found" error on analyze

- **Solution**: Ensure the image_id from upload response is used correctly

**Issue**: "Invalid file type"

- **Solution**: Only JPEG and PNG files are accepted. Check file extension and content.

**Issue**: "File too large"

- **Solution**: Images must be under 5MB. Compress before uploading.

**Issue**: "Unauthorized"

- **Solution**: Include `X-API-Key` header with correct API key.

**Issue**: python-magic not working on macOS

- **Solution**: Install libmagic: `brew install libmagic`

## Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (if implemented)
pytest

# Format code
black app/

# Type checking
mypy app/

# Lint code
flake8 app/
```

## Technical Stack

- **Framework**: FastAPI 0.109.0
- **Server**: Uvicorn 0.25.0
- **File Handling**: python-multipart, python-magic
- **Image Processing**: Pillow 10.2.0
- **Validation**: Pydantic 2.5.3
- **Containerization**: Docker

## License

MIT License - feel free to use this code as needed.

---

**Submission Notes:**

- Development time: Approximately 4 hours
- All core requirements implemented
- All bonus features included (API key auth, logging, Docker)
- Production-ready architecture with clear upgrade path
- Ready for mobile application integration
