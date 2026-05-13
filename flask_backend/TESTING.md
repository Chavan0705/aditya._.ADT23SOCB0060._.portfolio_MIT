# Testing & Verification Guide

## Quick Test (2 Minutes)

### Step 1: Start the Application
```bash
cd flask_backend
python run.py
```

You should see:
```
[v0] Initializing database...
[v0] Database initialized successfully
[v0] Sample data loaded with 50 comments
[v0] Flask application starting...
 * Running on http://localhost:5000
```

### Step 2: Test Dashboard
Open browser to: **http://localhost:5000/**

You should see:
- Page title: "Comment Moderation Dashboard"
- Statistics cards at the top
- Interactive pie chart
- Interactive bar chart
- Comments table with data
- Search and filter options

### Step 3: Test Analyzer
Open browser to: **http://localhost:5000/analyzer**

You should see:
- Input field for comments
- Character counter
- Analyze button
- Result display area

Try submitting a comment like: "This is a great product!"

You should get:
- Prediction category (Safe, Offensive, etc.)
- Toxicity status (Non-toxic/Toxic)
- Confidence percentage
- Timestamp

## Feature Testing Checklist

### Dashboard Features
- [ ] Page loads without errors
- [ ] Statistics cards display correctly
- [ ] Pie chart displays and is interactive
- [ ] Bar chart displays and is interactive
- [ ] Comments table shows all comments
- [ ] Search box filters comments by text
- [ ] Category filter works
- [ ] Status filter works
- [ ] Toxicity filter works
- [ ] Mark as reviewed button works
- [ ] Delete button works
- [ ] CSV export downloads file
- [ ] PDF export downloads file
- [ ] Auto-refresh works (every 30 seconds)

### Analyzer Features
- [ ] Page loads without errors
- [ ] Can type in comment field
- [ ] Character counter updates
- [ ] Analyze button is clickable
- [ ] Results display correctly
- [ ] Category prediction is shown
- [ ] Confidence percentage is shown
- [ ] Toxic/Non-toxic badge displays
- [ ] Timestamp is recorded
- [ ] Link to dashboard works

### API Endpoints

Test each endpoint manually:

#### 1. Analyze Comment
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"comment":"This is a test comment"}'
```

Expected response:
```json
{
  "id": 51,
  "comment": "This is a test comment",
  "category": "Safe",
  "toxicity_score": 0.05,
  "confidence": 0.95,
  "is_toxic": false,
  "status": "unreviewed",
  "timestamp": "2026-05-14 10:30:45"
}
```

#### 2. Get All Comments
```bash
curl http://localhost:5000/api/comments
```

Expected response: Array of comments with metadata

#### 3. Get Statistics
```bash
curl http://localhost:5000/api/stats
```

Expected response:
```json
{
  "total_comments": 51,
  "toxic_count": 5,
  "safe_count": 46,
  "categories": {
    "Safe": 46,
    "Offensive": 3,
    "Spam": 1,
    "Hate Speech": 1,
    "Threat": 0,
    "Harassment": 0
  },
  "average_confidence": 0.92
}
```

#### 4. Update Comment Status
```bash
curl -X PATCH http://localhost:5000/api/comments/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"reviewed"}'
```

#### 5. Delete Comment
```bash
curl -X DELETE http://localhost:5000/api/comments/1
```

#### 6. Export as CSV
```bash
curl http://localhost:5000/api/export/csv > comments.csv
```

#### 7. Export as PDF
```bash
curl http://localhost:5000/api/export/pdf > comments.pdf
```

## Browser Console Testing

1. Open browser DevTools (F12 or Cmd+Option+I)
2. Go to Console tab
3. Check for any JavaScript errors (red text)
4. Should see minimal logging

Common errors to watch for:
- CORS errors (shouldn't see these)
- 404 errors (shouldn't see these)
- Network errors (check internet connection)

## Performance Testing

### Load Time Test
```bash
# Check dashboard load time
curl -w "Time: %{time_total}s\n" -o /dev/null http://localhost:5000/

# Check API response time
curl -w "Time: %{time_total}s\n" -o /dev/null http://localhost:5000/api/stats
```

Expected times:
- Dashboard: < 2 seconds
- API: < 100ms

### Database Query Test
The system should handle 100+ comments without slowdown.

To test:
```bash
# Load more sample data
python load_sample_data.py 500

# Then check dashboard - should still be responsive
```

## Data Persistence Testing

### Test 1: Data Survives Restart
1. Add 5 comments via analyzer
2. Stop Flask (Ctrl+C)
3. Start Flask again
4. Check if comments still appear in dashboard

Expected: Comments should persist

### Test 2: Database File
```bash
# Check database file exists
ls -la comments.db

# Database should be several KB in size
# Should contain all comments
```

## Error Handling Testing

### Test 1: Invalid Input
Submit empty comment - should show validation message

### Test 2: Large Comment
Submit very long comment (5000+ characters) - should handle gracefully

### Test 3: Special Characters
Submit comment with special characters: `"<script>alert('xss')</script>"` - should not execute

### Test 4: Server Error Recovery
1. Stop Flask server (Ctrl+C)
2. Try accessing dashboard - should show connection error
3. Restart Flask
4. Dashboard should work again

## Mobile Responsiveness Testing

1. Open dashboard on mobile device or use browser DevTools device emulator
2. Test on different screen sizes:
   - Mobile (375px width)
   - Tablet (768px width)
   - Desktop (1024px+ width)

Expected: UI should be fully responsive and usable

## Security Testing

### Test 1: XSS Prevention
Submit comment: `<img src=x onerror="alert('xss')">`
- Should NOT execute JavaScript
- Should display as plain text

### Test 2: SQL Injection Prevention
Submit comment: `'; DROP TABLE comments; --`
- Should NOT delete table
- Should treat as normal comment

### Test 3: CORS
JavaScript from another domain trying to access API:
- Should work (CORS enabled)
- But only for safe operations

## Automated Test Script

Create `test_app.py`:
```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test if server is running"""
    try:
        response = requests.get(BASE_URL)
        print(f"✓ Server is running (Status: {response.status_code})")
        return True
    except:
        print("✗ Server is not running")
        return False

def test_api_analyze():
    """Test analyze endpoint"""
    data = {"comment": "Test comment"}
    response = requests.post(f"{BASE_URL}/api/analyze", json=data)
    if response.status_code == 200:
        print(f"✓ Analyze endpoint works")
        return True
    else:
        print(f"✗ Analyze endpoint failed (Status: {response.status_code})")
        return False

def test_api_stats():
    """Test stats endpoint"""
    response = requests.get(f"{BASE_URL}/api/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Stats endpoint works (Total comments: {data['total_comments']})")
        return True
    else:
        print(f"✗ Stats endpoint failed")
        return False

def test_api_comments():
    """Test comments endpoint"""
    response = requests.get(f"{BASE_URL}/api/comments")
    if response.status_code == 200:
        print(f"✓ Comments endpoint works")
        return True
    else:
        print(f"✗ Comments endpoint failed")
        return False

if __name__ == "__main__":
    print("Testing Comment Moderation System...")
    print("=" * 40)
    
    test_health()
    test_api_analyze()
    test_api_stats()
    test_api_comments()
    
    print("=" * 40)
    print("Testing complete!")
```

Run with:
```bash
pip install requests
python test_app.py
```

## Final Verification

Before considering the app ready:

- [x] App starts without errors
- [x] Dashboard loads and displays data
- [x] Analyzer works and analyzes comments
- [x] All API endpoints respond
- [x] Database stores data persistently
- [x] Export functions work
- [x] No console errors
- [x] Responsive design works
- [x] Charts display correctly
- [x] Security issues handled

## What to Check if Something Breaks

1. **Flask won't start:**
   - Check Python version: `python --version`
   - Check dependencies: `pip list`
   - Reinstall: `pip install -r requirements.txt`

2. **Dashboard shows 404:**
   - Check Flask is running
   - Check URL is http://localhost:5000/ (not https)
   - Check no port conflict

3. **No data showing:**
   - Load sample data: `python load_sample_data.py 50`
   - Check database: `ls comments.db`

4. **Charts not showing:**
   - Refresh page
   - Check internet connection
   - Check browser console

5. **API not responding:**
   - Check Flask is running
   - Check for error messages in terminal
   - Try restarting Flask

## Success Criteria

Your installation is successful when:

✓ Flask starts without errors  
✓ Dashboard loads with data  
✓ Analyzer analyzes comments  
✓ Charts display correctly  
✓ All buttons work  
✓ Export downloads files  
✓ No console errors  

---

For more help, check the documentation files!
