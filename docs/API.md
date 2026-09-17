# API Documentation

## Overview

The MiPortafolio API provides RESTful endpoints for portfolio management, document processing, and agent interactions.

**Base URL**: `http://localhost:8000/api/v1`

## Authentication

Currently using simple API key authentication (development phase).

```bash
# Include in request headers
Authorization: Bearer YOUR_API_KEY
```

## Core Endpoints

### Portfolio Management

#### Get Portfolio
```http
GET /portfolio
Authorization: Bearer {api_key}

Response:
{
  "id": "string",
  "title": "string",
  "description": "string",
  "projects": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "technologies": ["string"],
      "url": "string",
      "type": "featured" | "secondary"
    }
  ],
  "metadata": {
    "createdAt": "ISO8601",
    "updatedAt": "ISO8601"
  }
}
```

#### Update Portfolio
```http
PUT /portfolio
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "title": "string",
  "description": "string",
  "projects": [...]
}

Response: 200 OK
```

### Documents

#### Upload Document
```http
POST /documents/upload
Authorization: Bearer {api_key}
Content-Type: multipart/form-data

Parameters:
- file: File (required)
- type: "resume" | "certificate" | "project" (optional)

Response:
{
  "id": "string",
  "name": "string",
  "type": "string",
  "url": "string",
  "uploadedAt": "ISO8601"
}
```

#### Get Documents
```http
GET /documents
Authorization: Bearer {api_key}

Query Parameters:
- type: string (optional)
- limit: number (default: 20)
- offset: number (default: 0)

Response:
{
  "documents": [...],
  "total": number,
  "limit": number,
  "offset": number
}
```

#### Delete Document
```http
DELETE /documents/{id}
Authorization: Bearer {api_key}

Response: 204 No Content
```

### Agent Interactions

#### Submit Task
```http
POST /agent/tasks
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "type": "analyze_portfolio" | "generate_content" | "process_document",
  "parameters": {
    "key": "value"
  },
  "priority": 1 - 10 (optional, default: 5)
}

Response:
{
  "taskId": "string",
  "status": "pending",
  "createdAt": "ISO8601"
}
```

#### Get Task Status
```http
GET /agent/tasks/{taskId}
Authorization: Bearer {api_key}

Response:
{
  "taskId": "string",
  "status": "pending" | "processing" | "completed" | "failed",
  "progress": 0-100,
  "result": {...},
  "error": "string" (if failed),
  "createdAt": "ISO8601",
  "completedAt": "ISO8601" (if completed)
}
```

#### Get Task Results
```http
GET /agent/tasks/{taskId}/result
Authorization: Bearer {api_key}

Response:
{
  "taskId": "string",
  "result": {...},
  "metadata": {...}
}
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {...},
    "timestamp": "ISO8601"
  }
}
```

### Common Error Codes

| Code | Status | Description |
|------|--------|-------------|
| `INVALID_REQUEST` | 400 | Request validation failed |
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

## Rate Limiting

- **Requests per minute**: 60
- **Requests per hour**: 1000

Headers included in response:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1693478400
```

## Pagination

List endpoints support pagination:

```bash
GET /documents?limit=20&offset=0

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 150,
    "hasMore": true,
    "nextOffset": 20
  }
}
```

## Filtering & Sorting

```bash
# Filtering
GET /documents?type=resume&status=active

# Sorting
GET /projects?sort=createdAt:desc&sort=title:asc

# Combining
GET /documents?type=certificate&sort=uploadedAt:desc&limit=10
```

## Webhooks (Future)

Subscribe to events for real-time updates:

```http
POST /webhooks/subscribe
Authorization: Bearer {api_key}
Content-Type: application/json

{
  "event": "task.completed" | "document.uploaded" | "portfolio.updated",
  "url": "https://your-domain.com/webhook",
  "active": true
}
```

## API Client Libraries

### JavaScript/TypeScript
```typescript
import { PortfolioClient } from '@mportafolio/api-client';

const client = new PortfolioClient({
  baseURL: 'http://localhost:8000/api/v1',
  apiKey: process.env.API_KEY
});

// Usage
const portfolio = await client.portfolio.get();
const documents = await client.documents.list({ type: 'resume' });
const task = await client.agent.submitTask({
  type: 'analyze_portfolio',
  parameters: { format: 'json' }
});
```

### Python
```python
from mportafolio.client import PortfolioClient

client = PortfolioClient(
    base_url="http://localhost:8000/api/v1",
    api_key=os.getenv("API_KEY")
)

# Usage
portfolio = client.portfolio.get()
documents = client.documents.list(type="resume")
task = client.agent.submit_task(
    type="analyze_portfolio",
    parameters={"format": "json"}
)
```

## Health Check

```http
GET /health

Response:
{
  "status": "healthy",
  "version": "2.0.0",
  "services": {
    "database": "healthy",
    "agent": "healthy"
  }
}
```

## Versioning

API versions are indicated in the URL path:
- Current: `/api/v1`
- Deprecated versions remain available for 6 months

## Support & Issues

- **API Issues**: [GitHub Issues](https://github.com/Harp-Andres/MiPortafolio/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/Harp-Andres/MiPortafolio/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/Harp-Andres/MiPortafolio/wiki)

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for API version history and breaking changes.
