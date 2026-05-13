# 🚀 Setup & Installation Guide

Complete step-by-step guide to set up and run the Comment Moderation & Tracking System.

## Prerequisites

- **Python 3.8+** (Check: `python --version` or `python3 --version`)
- **pip** (Usually comes with Python)
- **Git** (Optional, for cloning)

## Quick Start (5 minutes)

### 1. Navigate to Project Directory
```bash
cd flask_backend
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Load Sample Data (Optional but Recommended)
```bash
python load_sample_data.py 50
```
This creates 50 sample comments for testing. Adjust the number as needed.

### 5. Run the Application
```bash
python run.py
```

You should see:
```
============================================================
🚀 Comment Moderation & Tracking System
============================================================

📊 Initializing database...
✅ Database initialized successfully

🤖 Checking ML model files...
⚠️  Model files not found - Running in demo mode

🌐 Starting Flask development server...
------------------------------------------------------------
Dashboard:  http://localhost:5000/
Analyzer:   http://localhost:5000/analyzer
------------------------------------------------------------
```

### 6. Access the Application
- **Dashboard**: http://localhost:5000/
- **Analyzer**: http://localhost:5000/analyzer

## Detailed Installation Steps

### Step 1: Environment Setup

#### Option A: Using Command Line

**Windows CMD:**
```bash
cd path\to\flask_backend
python -m venv venv
venv\Scripts\activate
```

**Windows PowerShell:**
```powershell
cd path/to/flask_backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux Terminal:**
```bash
cd path/to/flask_backend
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt when activated.

### Step 2: Install Dependencies

With virtual environment activated:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask 3.0 - Web framework
- SQLAlchemy - ORM and database
- Flask-CORS - Cross-origin support
- joblib - Model loading
- scikit-learn - ML library
- reportlab - PDF generation
- pandas & numpy - Data processing

### Step 3: Set Up Database

The database is automatically initialized when you run the app, but you can also manually initialize:

```bash
python -c "from app import app, init_db; init_db()"
```

This creates `comments.db` with the necessary tables.

### Step 4: (Optional) Add ML Model Files

If you have trained ML models:

1. Place `toxic_model.pkl` in `flask_backend/`
2. Place `vectorizer.pkl` in `flask_backend/`

The app will automatically detect and use them.

### Step 5: Load Sample Data

For testing with pre-populated comments:

```bash
# Load 50 sample comments
python load_sample_data.py 50

# Load 100 sample comments
python load_sample_data.py 100
```

The script creates a realistic mix:
- 70% Safe comments
- 10% Hate Speech
- 10% Offensive Language
- 5% Spam
- 3% Threats
- 2% Harassment

### Step 6: Run the Application

```bash
python run.py
```

Or directly:
```bash
python app.py
```

## Configuration

### Environment Variables

Create a `.env` file in `flask_backend/` directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///comments.db
```

Then load with:
```bash
pip install python-dotenv
```

And in `app.py`, add:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Database Configuration

Edit `app.py` to change database:

**SQLite (default):**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
```

**PostgreSQL:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
```

**MySQL:**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/dbname'
```

## Troubleshooting

### Issue: "No module named 'flask'"

**Solution:**
```bash
# Make sure virtual environment is activated
# (You should see (venv) at the start of your prompt)
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Use a different port
python -c "from app import app; app.run(port=5001)"

# Or kill the process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Issue: Database locked or corrupted

**Solution:**
```bash
# Delete the database file and restart
rm comments.db  # On macOS/Linux
del comments.db  # On Windows

# Then run the app again to recreate it
python run.py
```

### Issue: CORS errors in browser console

**Solution:** The CORS is already configured in `app.py`. If you still have issues, make sure you're accessing via `http://localhost:5000`, not `http://127.0.0.1:5000`.

### Issue: Model files not found error

**Solution:** This is expected! The app runs in demo mode without ML models. This is fine for testing. To use real ML models:
1. Get/train `toxic_model.pkl` and `vectorizer.pkl`
2. Place them in the `flask_backend/` directory
3. Restart the app

### Issue: Cannot access http://localhost:5000

**Possible causes:**
1. App is not running - check terminal
2. Using wrong port - check the output
3. Firewall blocking - allow port 5000
4. Flask not installed - run `pip install -r requirements.txt`

## Testing the System

### Manual Testing

1. **Test Analyzer:**
   - Go to http://localhost:5000/analyzer
   - Enter a comment like "You're an idiot"
   - Click "Analyze Comment"
   - Should show as Offensive Language (Toxic)

2. **Test Dashboard:**
   - Go to http://localhost:5000/
   - Should show statistics
   - Try the search and filter options

3. **Test Exports:**
   - Go to Dashboard
   - Click "Export CSV" or "Export PDF"
   - File should download

### Command Line Testing

Test the API endpoints:

```bash
# Test analyze endpoint
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is great content!"}'

# Get all comments
curl http://localhost:5000/api/comments

# Get statistics
curl http://localhost:5000/api/stats
```

## Performance Optimization

### For Development
```bash
# Run with auto-reload disabled (faster startup)
export FLASK_ENV=development
export FLASK_DEBUG=False
python app.py
```

### For Production
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or with Waitress (Windows)
pip install waitress
waitress-serve --port=5000 app:app
```

## Deactivating Virtual Environment

When you're done working:

```bash
# macOS/Linux/Windows PowerShell
deactivate

# Windows CMD
venv\Scripts\deactivate.bat
```

## Project Structure

```
flask_backend/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── utils.py                  # Utility functions
├── run.py                    # Startup script
├── requirements.txt          # Python dependencies
├── load_sample_data.py       # Sample data generator
├── comments.db              # SQLite database (auto-created)
├── templates/
│   ├── dashboard.html       # Dashboard page
│   └── analyzer.html        # Analyzer page
└── README.md                # Documentation
```

## Next Steps

1. **Explore the Dashboard**
   - Analyze some comments
   - Check the statistics
   - Try the export features

2. **Test the Analyzer**
   - Input various comments
   - Check how they're classified

3. **Configure Your Own**
   - Add custom keywords in `utils.py`
   - Integrate your own ML model
   - Customize the UI

4. **Deploy**
   - See `README.md` for deployment options
   - Consider using Heroku, AWS, or DigitalOcean

## Getting Help

1. Check the error message in the terminal
2. Review the troubleshooting section above
3. Check `README.md` for more documentation
4. Verify all files are in correct locations

## Quick Commands Reference

```bash
# Activate virtual environment
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate              # Windows

# Install dependencies
pip install -r requirements.txt

# Load sample data
python load_sample_data.py 50

# Run the app
python run.py

# Test API
curl http://localhost:5000/api/stats

# Deactivate virtual environment
deactivate
```

---

**Congratulations! You're ready to use the Comment Moderation System! 🎉**
