# Installation & Troubleshooting Guide

## Quick Start (3 Steps)

### Option 1: Automatic Setup (Linux/Mac)
```bash
cd flask_backend
bash setup.sh
```

### Option 2: Automatic Setup (Windows)
```bash
cd flask_backend
setup.bat
```

### Option 3: Manual Setup
```bash
# Step 1: Navigate to project
cd flask_backend

# Step 2: Create and activate virtual environment
python -m venv venv

# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Load sample data (optional)
python load_sample_data.py 50

# Step 5: Run the application
python run.py
```

Then open your browser to:
- Dashboard: **http://localhost:5000/**
- Analyzer: **http://localhost:5000/analyzer**

## System Requirements

- Python 3.8 or higher
- 100MB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for CDN resources)

## What Gets Created

When you first run the app:

```
flask_backend/
├── venv/                    # Virtual environment (created by setup)
├── comments.db              # SQLite database (auto-created)
├── logs/                    # Application logs (auto-created)
└── ...
```

The database is automatically created with all necessary tables on first run.

## Troubleshooting

### Issue 1: "Python not found" or "python3 not found"
**Solution:**
- Check if Python is installed: `python --version`
- If not installed, download from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### Issue 2: "ModuleNotFoundError" when running app
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue 3: Port 5000 already in use
**Solution:**
- Option A: Stop the other application using port 5000
- Option B: Change port in `config.py` (line with `PORT = 5000`)
- Option C: Use a different port:
```bash
export FLASK_PORT=5001
python run.py
```

### Issue 4: "Address already in use" error
**Solution:**
```bash
# Linux/Mac: Find and kill the process
lsof -i :5000
kill -9 <PID>

# Windows: Find and kill the process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue 5: Database locked error
**Solution:**
```bash
# Stop the running Flask server (Ctrl+C)
# Delete the old database
rm comments.db  # Linux/Mac
del comments.db # Windows

# Restart the app - new database will be created
python run.py
```

### Issue 6: Dashboard/Analyzer page shows blank or 404
**Solution:**
- Make sure Flask server is running (you should see "Running on http://localhost:5000")
- Try refreshing the page (Ctrl+R or Cmd+R)
- Check the terminal for error messages
- Try accessing: http://localhost:5000/ (without https)

### Issue 7: Charts not showing on dashboard
**Solution:**
- This is usually due to slow network loading Chart.js library
- Wait a few seconds and refresh the page
- If persistent, check internet connection
- Check browser console for errors (F12 → Console tab)

### Issue 8: Sample data not loading
**Solution:**
```bash
# This is optional - you can skip it
# Or manually load after Flask is running:
python load_sample_data.py 100
```

## Running in Production

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```bash
docker build -t moderation-system .
docker run -p 5000:5000 moderation-system
```

### On Heroku
```bash
heroku create your-app-name
git push heroku main
heroku open
```

## Verification Checklist

After setup, verify everything works:

- [ ] Flask server starts without errors
- [ ] Dashboard loads at http://localhost:5000/
- [ ] Analyzer loads at http://localhost:5000/analyzer
- [ ] Can submit a comment and get analysis
- [ ] Dashboard shows statistics
- [ ] Can view comment history
- [ ] Export buttons work (CSV/PDF)

## Common Port Issues

If port 5000 is already in use:

```bash
# Find what's using port 5000
# Linux/Mac:
lsof -i :5000

# Windows:
netstat -ano | findstr :5000

# Kill the process (if safe to do so)
# Linux/Mac:
kill -9 <PID>

# Windows:
taskkill /PID <PID> /F
```

Then restart Flask:
```bash
python run.py
```

## Getting Help

1. Check the relevant documentation:
   - `START_HERE.md` - Quick navigation
   - `QUICK_START.md` - 5-minute setup
   - `README.md` - Feature guide
   - `API.md` - API documentation

2. Check the Flask server terminal output for error messages

3. Check browser console (F12 → Console) for JavaScript errors

4. Verify all dependencies are installed:
```bash
pip list | grep -E "Flask|SQLAlchemy|scikit-learn"
```

## First Run Checklist

- [x] Python 3.8+ installed
- [x] Virtual environment created
- [x] Dependencies installed
- [x] Sample data loaded (optional)
- [x] Flask server started
- [x] Dashboard accessible at http://localhost:5000/
- [x] Analyzer accessible at http://localhost:5000/analyzer

## Performance Tips

- First load may be slower (JavaScript/CSS caching)
- Subsequent page loads will be faster
- For better performance, close other browser tabs
- Clear browser cache if seeing old data

## Next Steps

1. Explore the dashboard at http://localhost:5000/
2. Try analyzing comments at http://localhost:5000/analyzer
3. Read `API.md` to understand the API
4. Customize the system for your needs

## Support Resources

- **Quick Start:** `QUICK_START.md` (5 minutes)
- **Full Setup:** `SETUP.md` (detailed guide)
- **Features:** `README.md` (complete guide)
- **API:** `API.md` (endpoints & examples)
- **Architecture:** `PROJECT_OVERVIEW.md` (technical details)

---

**Need help?** Check the documentation files in the flask_backend directory!
