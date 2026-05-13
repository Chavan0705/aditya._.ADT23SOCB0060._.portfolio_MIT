# 📡 API Documentation

Complete REST API reference for the Comment Moderation & Tracking System.

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, no authentication is required. In production, add JWT tokens.

## Response Format
All responses are in JSON format with the following structure:

**Success:**
```json
{
    "data": {...},
    "status": "success",
    "code": 200
}
```

**Error:**
```json
{
    "error": "Error message",
    "code": 400
}
```

---

## Endpoints

### 1. Analyze Comment

Analyze a comment for toxicity and store in database.

**Endpoint:**
```
POST /api/analyze
```

**Request:**
```json
{
    "text": "Your comment here"
}
```

**Parameters:**
- `text` (string, required): Comment text to analyze (2-2000 characters)

**Response (201 Created):**
```json
{
    "id": 1,
    "original_text": "Your comment here",
    "category": "Safe / Positive",
    "toxicity_score": 0.15,
    "confidence": 0.95,
    "status": "unreviewed",
    "is_toxic": false,
    "created_at": "2024-01-15 10:30:45",
    "badge_color": "green"
}
```

**Status Codes:**
- `201` - Comment analyzed and stored successfully
- `400` - Invalid comment (too short, empty, etc.)
- `500` - Server error

**Example:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is great!"}'
```

**Category Values:**
- `Hate Speech` - Hateful or discriminatory comments
- `Offensive Language` - Contains offensive/rude language
- `Spam` - Promotional or spam content
- `Threat` - Contains threats or violence
- `Harassment` - Harassment or bullying
- `Safe / Positive` - Safe, positive, or neutral comments

---

### 2. Get All Comments

Retrieve comments with optional filtering.

**Endpoint:**
```
GET /api/comments
```

**Query Parameters:**
- `category` (string, optional): Filter by category
- `status` (string, optional): Filter by status (unreviewed, reviewed, approved)
- `is_toxic` (boolean, optional): Filter by toxicity (true/false)
- `search` (string, optional): Search in comment text

**Response:**
```json
[
    {
        "id": 1,
        "original_text": "Comment text",
        "category": "Safe / Positive",
        "toxicity_score": 0.15,
        "confidence": 0.95,
        "status": "unreviewed",
        "is_toxic": false,
        "created_at": "2024-01-15 10:30:45",
        "badge_color": "green"
    },
    ...
]
```

**Examples:**
```bash
# Get all comments
curl http://localhost:5000/api/comments

# Filter by category
curl http://localhost:5000/api/comments?category=Spam

# Filter by status
curl http://localhost:5000/api/comments?status=reviewed

# Search
curl http://localhost:5000/api/comments?search=keyword

# Combine filters
curl http://localhost:5000/api/comments?category=Offensive%20Language&is_toxic=true
```

---

### 3. Get Comment Statistics

Get dashboard statistics and analytics.

**Endpoint:**
```
GET /api/stats
```

**Response:**
```json
{
    "total_comments": 150,
    "toxic_comments": 45,
    "safe_comments": 105,
    "toxic_percentage": 30.0,
    "category_breakdown": {
        "Safe / Positive": 105,
        "Offensive Language": 25,
        "Spam": 12,
        "Hate Speech": 5,
        "Threat": 2,
        "Harassment": 1
    },
    "recent_comments": [
        {
            "id": 150,
            "original_text": "Latest comment",
            ...
        }
    ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/stats
```

---

### 4. Update Comment Status

Mark a comment as reviewed or approved.

**Endpoint:**
```
PATCH /api/comments/{id}/status
```

**Path Parameters:**
- `id` (integer, required): Comment ID

**Request:**
```json
{
    "status": "reviewed"
}
```

**Status Values:**
- `unreviewed` - Not yet reviewed
- `reviewed` - Reviewed by admin
- `approved` - Approved for posting

**Response:**
```json
{
    "id": 1,
    "original_text": "Comment",
    "category": "Safe / Positive",
    "toxicity_score": 0.15,
    "confidence": 0.95,
    "status": "reviewed",
    "is_toxic": false,
    "created_at": "2024-01-15 10:30:45",
    "badge_color": "green"
}
```

**Status Codes:**
- `200` - Status updated successfully
- `400` - Invalid status value
- `404` - Comment not found
- `500` - Server error

**Example:**
```bash
curl -X PATCH http://localhost:5000/api/comments/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"reviewed"}'
```

---

### 5. Delete Comment

Delete a comment from the database.

**Endpoint:**
```
DELETE /api/comments/{id}
```

**Path Parameters:**
- `id` (integer, required): Comment ID

**Response:**
```json
{
    "message": "Comment deleted"
}
```

**Status Codes:**
- `200` - Comment deleted successfully
- `404` - Comment not found
- `500` - Server error

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/comments/1
```

---

### 6. Export as CSV

Download all comments as CSV file.

**Endpoint:**
```
GET /api/export/csv
```

**Response:**
- File download: `comments_export.csv`
- Format: CSV with headers

**CSV Format:**
```
ID,Comment,Category,Toxicity Score,Confidence,Status,Is Toxic,Date & Time
1,Your comment,Safe / Positive,0.15,0.95,unreviewed,False,2024-01-15 10:30:45
```

**Example:**
```bash
curl http://localhost:5000/api/export/csv -o comments.csv
```

---

### 7. Export as PDF

Download all comments as PDF report.

**Endpoint:**
```
GET /api/export/pdf
```

**Response:**
- File download: `comments_export.pdf`
- Format: PDF document

**Includes:**
- Title and export date
- Summary statistics
- Table of first 50 comments

**Example:**
```bash
curl http://localhost:5000/api/export/pdf -o comments.pdf
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Comment must be at least 2 characters"
}
```

### 404 Not Found
```json
{
    "error": "Comment not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Database connection failed"
}
```

---

## Rate Limiting

Currently, there is no rate limiting. For production, implement:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/analyze', methods=['POST'])
@limiter.limit("5 per minute")
def analyze_comment():
    ...
```

---

## Pagination

To add pagination (recommended for large datasets):

```python
@app.route('/api/comments', methods=['GET'])
def get_comments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    comments = Comment.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'data': [c.to_dict() for c in comments.items],
        'total': comments.total,
        'pages': comments.pages,
        'current_page': page
    })
```

---

## Webhooks (Future Feature)

Plan to add webhooks for real-time notifications:

```python
# Webhook event when toxic comment detected
{
    "event": "comment.analyzed",
    "timestamp": "2024-01-15T10:30:45Z",
    "data": {
        "id": 1,
        "category": "Offensive Language",
        "is_toxic": true
    }
}
```

---

## CORS Headers

All responses include CORS headers:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Performance Tips

1. **Use filtering** to reduce payload:
   ```bash
   curl http://localhost:5000/api/comments?status=unreviewed
   ```

2. **Implement pagination** for large datasets:
   ```bash
   curl "http://localhost:5000/api/comments?page=2&per_page=25"
   ```

3. **Cache statistics** (implement in production):
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})
   
   @cache.cached(timeout=300)
   @app.route('/api/stats')
   def get_stats():
       ...
   ```

---

## Code Examples

### Python with Requests

```python
import requests

# Analyze comment
response = requests.post('http://localhost:5000/api/analyze', json={
    'text': 'This is a great post!'
})
result = response.json()
print(f"Category: {result['category']}")

# Get stats
stats = requests.get('http://localhost:5000/api/stats').json()
print(f"Total comments: {stats['total_comments']}")

# Update status
requests.patch(f"http://localhost:5000/api/comments/{result['id']}/status", json={
    'status': 'reviewed'
})
```

### JavaScript/Fetch

```javascript
// Analyze comment
const response = await fetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: 'Great content!' })
});
const result = await response.json();
console.log(result.category);

// Get comments
const comments = await fetch('/api/comments?category=Spam').then(r => r.json());

// Export as PDF
const pdfLink = document.createElement('a');
pdfLink.href = '/api/export/pdf';
pdfLink.download = 'comments.pdf';
pdfLink.click();
```

### cURL Examples

```bash
# Analyze
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Test comment"}'

# Get filtered comments
curl "http://localhost:5000/api/comments?category=Spam&is_toxic=true"

# Update status
curl -X PATCH http://localhost:5000/api/comments/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"approved"}'

# Delete comment
curl -X DELETE http://localhost:5000/api/comments/1

# Export
curl http://localhost:5000/api/export/csv -o export.csv
curl http://localhost:5000/api/export/pdf -o export.pdf
```

---

## Testing the API

### Using Postman
1. Import these endpoints into Postman
2. Set Content-Type to `application/json`
3. Use the examples above

### Using Python unittest
```python
import unittest
from app import app, db

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_analyze(self):
        response = self.client.post('/api/analyze', json={
            'text': 'Test comment'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('category', response.get_json())
```

---

## Version History

- **v1.0** (Current)
  - Comment analysis and storage
  - Statistics and analytics
  - CSV/PDF export
  - Admin features (delete, update status)

---

## Support

For API issues, check:
1. Response status codes
2. Error messages
3. Request format (JSON)
4. Required fields
5. Terminal logs for server errors

---

**Last Updated:** January 2024
