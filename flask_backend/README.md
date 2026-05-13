# Comment Moderation & Tracking System

A professional, feature-rich comment moderation system built with Flask, SQLAlchemy, and modern ML-based toxic comment detection. Includes a beautiful glassmorphic dashboard, analytics, and admin features.

## 🎯 Features

### Core Moderation Capabilities
- **ML-based Toxicity Detection**: Uses trained toxic comment classification model
- **Smart Categorization**: Auto-classifies comments into 6 categories:
  - Hate Speech
  - Offensive Language
  - Spam
  - Threat
  - Harassment
  - Safe / Positive

### Database & Storage
- **SQLite Database**: Stores all analyzed comments with metadata
- **Comment Tracking**: Records original text, category, toxicity score, confidence, timestamp
- **Status Management**: Track comment review status (unreviewed, reviewed, approved)

### Dashboard Features
- **Real-time Statistics**: Total comments, toxic vs safe breakdown, percentage metrics
- **Interactive Charts**: 
  - Pie chart for toxicity distribution
  - Bar chart for category breakdown
- **Comment Table**: Recent comments with color-coded badges, sortable and filterable
- **Export Functionality**: Download comments as CSV or PDF reports
- **Admin Controls**: Delete comments, mark as reviewed, filter by status

### UI/UX Design
- **Glassmorphism Theme**: Modern dark theme with frosted glass effect
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Animated Cards**: Smooth hover effects and transitions
- **Color-Coded Badges**:
  - 🔴 Red → Toxic/Threats
  - 🟢 Green → Safe/Positive
  - 🟡 Yellow → Spam
  - 🟠 Orange → Offensive/Harassment

### Admin Features
- **Search & Filter**: Search by comment text, filter by category or status
- **Batch Operations**: Delete and mark comments as reviewed
- **Status Tracking**: Monitor which comments have been reviewed
- **Analytics**: View trends and patterns in comment data

## 📋 Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLAlchemy + SQLite
- **ML Model**: scikit-learn (pretrained)
- **Export**: ReportLab (PDF generation)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Charts**: Chart.js
- **CORS**: Flask-CORS for cross-origin requests

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Step 1: Clone/Navigate to Project
```bash
cd flask_backend
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Add ML Model Files (If Available)
Place your trained model files in the root directory:
- `toxic_model.pkl` - Trained classification model
- `vectorizer.pkl` - Text vectorizer (TF-IDF)

> **Note**: If model files are not available, the system runs in demo mode with random predictions. This is useful for testing the UI without ML dependencies.

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 6: Access the Application
- **Dashboard**: http://localhost:5000/
- **Analyzer**: http://localhost:5000/analyzer

## 📖 Usage Guide

### Analyzing Comments
1. Go to the **Analyzer** page
2. Enter a comment in the textarea
3. Click **"Analyze Comment"**
4. View the results:
   - Category classification
   - Toxicity score (0-100%)
   - Confidence percentage
   - Timestamp of analysis
5. Result is automatically saved to the database

### Viewing Dashboard
1. Go to the **Dashboard**
2. View real-time statistics:
   - Total comments analyzed
   - Toxic vs Safe breakdown
   - Category distribution chart
   - Recent comments table
3. Use search and filters to find specific comments
4. Click on status dropdown to mark comments as reviewed/approved
5. Click "Delete" to remove a comment

### Exporting Data
1. From the dashboard, click **"Export CSV"** or **"Export PDF"**
2. File will download with complete comment history
3. CSV includes: ID, Comment, Category, Scores, Status, Timestamp
4. PDF includes: Summary stats + First 50 comments

## 🔌 API Endpoints

### Analysis
```
POST /api/analyze
Content-Type: application/json

Request:
{
    "text": "Comment text to analyze"
}

Response:
{
    "id": 1,
    "original_text": "...",
    "category": "Safe / Positive",
    "toxicity_score": 0.15,
    "confidence": 0.95,
    "status": "unreviewed",
    "is_toxic": false,
    "created_at": "2024-01-15 10:30:45",
    "badge_color": "green"
}
```

### Get Comments
```
GET /api/comments?category=Spam&status=unreviewed&search=keyword
Response: Array of comment objects
```

### Get Statistics
```
GET /api/stats
Response: {
    "total_comments": 150,
    "toxic_comments": 45,
    "safe_comments": 105,
    "toxic_percentage": 30.0,
    "category_breakdown": {...},
    "recent_comments": [...]
}
```

### Update Comment Status
```
PATCH /api/comments/{id}/status
Content-Type: application/json

Request:
{
    "status": "reviewed"
}
```

### Delete Comment
```
DELETE /api/comments/{id}
```

### Export Data
```
GET /api/export/csv
GET /api/export/pdf
```

## 🎨 Color Scheme

- **Primary**: Blue (#3b82f6) - Accent and interactive elements
- **Secondary**: Purple (#8b5cf6) - Gradients and highlights
- **Background**: Dark Blue (#0f172a, #1e293b) - Main background
- **Text**: Light Gray (#e2e8f0) - Primary text
- **Danger**: Red (#ef4444) - Toxic/alerts
- **Success**: Green (#22c55e) - Safe comments
- **Warning**: Yellow (#eab308) - Spam
- **Info**: Orange (#f97316) - Offensive

## 🔒 Security Features

- **Input Validation**: Comment length validation
- **SQL Injection Protection**: SQLAlchemy parameterized queries
- **CORS Configuration**: Restricted cross-origin requests
- **Error Handling**: Proper error responses and logging
- **Database**: Local SQLite (can be migrated to PostgreSQL)

## 📊 Database Schema

```sql
CREATE TABLE comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    toxicity_score FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'unreviewed',
    is_toxic BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚦 Demo Mode

If ML model files are not available:
- System generates random predictions (0.2-0.8 range)
- Uses keyword matching for categorization
- Full UI/UX functionality works as expected
- Perfect for testing and demonstrations

## 🔄 Auto-Refresh

The dashboard automatically refreshes data every 30 seconds to show new comments in real-time.

## 🛠️ Customization

### Add Custom Keywords
Edit the `TOXIC_KEYWORDS` dictionary in `app.py`:
```python
TOXIC_KEYWORDS = {
    'your_category': ['keyword1', 'keyword2'],
}
```

### Change Categories
Modify the `categorize_comment()` function to add/remove categories.

### Customize Colors
Edit the CSS variables in the HTML templates:
- Update badge colors in `.badge-*` classes
- Modify background gradients in the `<style>` section

### Database Migration
To use PostgreSQL instead of SQLite:
```python
# In app.py, change:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db'
```

## 📈 Performance Considerations

- **Database Indexing**: Consider adding indexes on `created_at`, `category`, `status`
- **Pagination**: Implement pagination for large datasets
- **Caching**: Use Redis for frequently accessed stats
- **Batch Operations**: Add batch delete/update endpoints

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
python app.py --port 5001
```

### Model Files Not Found
- System will run in demo mode with random predictions
- Download pre-trained models from scikit-learn or train your own

### Database Locked
- Delete `comments.db` to reset the database
- Ensure only one instance of the app is running

### CORS Issues
- Flask-CORS is configured to allow all origins
- Restrict to specific domains in production

## 📝 Logging

All errors are logged to console. For production, implement proper logging:
```python
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

## 🚀 Deployment

### Heroku
```bash
# Add Procfile
web: python app.py

# Deploy
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues, questions, or feature requests, refer to the API documentation above or contact support.

---

**Built with ❤️ for professional content moderation**
