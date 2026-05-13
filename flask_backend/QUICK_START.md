# ⚡ Quick Start Guide

Get the Comment Moderation System running in **5 minutes**.

## 📦 What You Have

A complete, production-ready Flask application with:
- **Dashboard** - Real-time analytics and comment management
- **Analyzer** - Comment classification and toxicity detection
- **REST API** - 7 endpoints for full CRUD operations
- **Database** - SQLite with auto-initialization
- **Export** - CSV and PDF download functionality

## 🚀 Start Here (5 Steps)

### Step 1️⃣: Navigate to Project
```bash
cd flask_backend
```

### Step 2️⃣: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**You should see `(venv)` at the start of your terminal prompt.**

### Step 3️⃣: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4️⃣: Load Sample Data (Optional but Recommended)
```bash
python load_sample_data.py 50
```

Creates 50 test comments with realistic data distribution.

### Step 5️⃣: Run the App
```bash
python run.py
```

You should see:
```
🚀 Comment Moderation & Tracking System
📊 Initializing database...
✅ Database initialized successfully
🌐 Starting Flask development server...
Dashboard:  http://localhost:5000/
Analyzer:   http://localhost:5000/analyzer
```

## 🌐 Access the App

Open your browser and visit:

- **Dashboard**: [http://localhost:5000/](http://localhost:5000/)
- **Analyzer**: [http://localhost:5000/analyzer](http://localhost:5000/analyzer)

## 📚 Full Documentation

| File | Purpose |
|------|---------|
| **SETUP.md** | Detailed installation & troubleshooting |
| **README.md** | Complete feature guide & usage |
| **API.md** | REST API endpoint documentation |
| **PROJECT_OVERVIEW.md** | Architecture & design overview |

## 🎯 What to Try First

### 1. Test the Analyzer
1. Go to http://localhost:5000/analyzer
2. Enter: "You're an idiot"
3. Click "Analyze Comment"
4. See it classified as "Offensive Language" (Toxic)

### 2. Explore the Dashboard
1. Go to http://localhost:5000/
2. View statistics and recent comments
3. Try the search and filter features
4. Click "Export CSV" to download data

### 3. Load More Data
```bash
python load_sample_data.py 100
```

Adds 100 more sample comments for realistic testing.

## 💡 Key Features to Explore

✅ **Real-time Dashboard**
- Statistics cards with live counts
- Interactive charts (pie & bar)
- Recent comments table
- Color-coded status badges

✅ **Comment Analyzer**
- Instant toxicity detection
- 6-category classification
- Confidence percentage
- Timestamp tracking

✅ **Admin Controls**
- Search by comment text
- Filter by category (6 types)
- Filter by status (3 states)
- Mark comments as reviewed/approved
- Delete inappropriate content

✅ **Data Export**
- Download as CSV (all data)
- Generate PDF reports (first 50 comments)
- Includes full metadata

## 🔗 API Quick Test

```bash
# Test analyze endpoint
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is awesome!"}'

# Get all comments
curl http://localhost:5000/api/comments

# Get statistics
curl http://localhost:5000/api/stats
```

## 🎨 Design Preview

The application features:
- 🌙 **Dark glassmorphism theme**
- 📊 **Interactive charts** with Chart.js
- 🎯 **Color-coded badges** (Red=Toxic, Green=Safe, Yellow=Warning, Orange=Offensive)
- 📱 **Responsive design** (Desktop, Tablet, Mobile)
- ✨ **Smooth animations** and transitions

## ⚙️ Configuration

### Change Port
```bash
# Edit run.py and change:
app.run(port=5001)  # Instead of 5000
```

### Use Different Database
In `app.py`, change:
```python
# SQLite (default)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'

# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
```

### Add ML Models
1. Get `toxic_model.pkl` and `vectorizer.pkl`
2. Place in `flask_backend/` directory
3. Restart the app
4. System will automatically use them

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Use a different port
python -c "from app import app; app.run(port=5001)"
```

### Module Not Found Error
```bash
# Make sure virtual environment is activated
# You should see (venv) in your terminal prompt
pip install -r requirements.txt
```

### Database Issues
```bash
# Delete and recreate database
rm comments.db  # or del comments.db on Windows
python run.py   # Recreates it automatically
```

## 📋 File Structure

```
flask_backend/
├── app.py              # Main Flask application
├── run.py              # Startup script
├── requirements.txt    # Dependencies
├── load_sample_data.py # Data generator
├── utils.py            # Helper functions
├── config.py           # Configuration
├── comments.db         # Database (auto-created)
├── templates/
│   ├── dashboard.html  # Main dashboard
│   └── analyzer.html   # Comment analyzer
└── Docs/
    ├── README.md       # Full documentation
    ├── SETUP.md        # Setup guide
    ├── API.md          # API reference
    └── PROJECT_OVERVIEW.md
```

## 🚀 Next Steps

### Short-term
- [ ] Explore the dashboard features
- [ ] Test the analyzer with various comments
- [ ] Load sample data and view analytics
- [ ] Export data as CSV/PDF

### Medium-term
- [ ] Integrate with your own ML model
- [ ] Customize categories and keywords
- [ ] Set up email notifications
- [ ] Add user authentication

### Long-term
- [ ] Deploy to production (Heroku, AWS, etc.)
- [ ] Add database backups
- [ ] Implement rate limiting
- [ ] Scale with multiple workers
- [ ] Add advanced analytics

## 📞 Support Resources

1. **Error in Terminal?**
   - Read the error message carefully
   - Check SETUP.md troubleshooting section
   - Verify all dependencies are installed

2. **How do I use the API?**
   - See API.md for complete endpoint docs
   - Use curl or Postman to test
   - JavaScript examples included

3. **Want to customize?**
   - Edit TOXIC_KEYWORDS in utils.py
   - Modify category colors in HTML templates
   - Change database in app.py

## 🎓 Learning Path

1. **Beginner**: Use the dashboard, try analyzing comments
2. **Intermediate**: Read API.md, test endpoints with curl
3. **Advanced**: Modify app.py, integrate custom ML model
4. **Expert**: Deploy to production, optimize for scale

## ✨ Pro Tips

💡 **Auto-refresh Dashboard**
- Dashboard auto-refreshes every 30 seconds
- See new comments in real-time

💡 **Quick Filters**
- Use the search box to find comments instantly
- Combine multiple filters for precision

💡 **Status Tracking**
- Mark comments as reviewed to track moderation progress
- Status dropdown is inline for quick access

💡 **Data Export**
- Export before deleting important comments
- PDF includes summary statistics

💡 **Demo Mode**
- Works without ML models installed
- Perfect for presentations and testing

## 🎉 Ready?

```bash
python run.py
```

Open http://localhost:5000/ and start moderating!

---

**Questions?** Check the documentation files listed above.

**Ready to deploy?** See README.md for deployment options.

**Happy moderating! 🚀**
