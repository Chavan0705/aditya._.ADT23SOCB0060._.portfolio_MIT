# START HERE - Quick Navigation Guide

Welcome to the Comment Moderation & Tracking System! This guide will help you get started quickly.

## What Is This?

A professional web application for:
- Analyzing comments for toxic content
- Detecting 6 categories of problematic text
- Managing and tracking comment history
- Exporting data for reporting
- Real-time analytics and dashboards

## Quick Start (3 Steps - 2 Minutes)

### On Linux/Mac:
```bash
cd flask_backend
bash setup.sh
```

### On Windows:
```bash
cd flask_backend
setup.bat
```

### Manual Setup (All Platforms):
```bash
cd flask_backend
python -m venv venv
source venv/bin/activate              # Windows: venv\Scripts\activate
pip install -r requirements.txt
python load_sample_data.py 50         # Optional
python run.py
```

Then open your browser to:
- **Dashboard:** http://localhost:5000/
- **Analyzer:** http://localhost:5000/analyzer

## Choose Your Path

### I Just Want to Try It Out
→ Follow **Quick Start** above, then go to TESTING.md

### I Need Detailed Setup Instructions
→ Read **INSTALLATION_GUIDE.md**

### I Want to Understand the Features
→ Read **README.md**

### I Need to Integrate with My Code
→ Read **API.md**

### I Want to Understand the Architecture
→ Read **PROJECT_OVERVIEW.md**

### Something Isn't Working
→ Read **INSTALLATION_GUIDE.md** (Troubleshooting section)

### I Want to Test the System
→ Read **TESTING.md**

## File Guide

```
flask_backend/
│
├── INSTALLATION_GUIDE.md    ← Setup, troubleshooting, production deployment
├── TESTING.md               ← How to test the application
├── QUICK_START.md           ← 5-minute quick start
├── README.md                ← Complete feature guide
├── API.md                   ← API endpoints with examples
├── PROJECT_OVERVIEW.md      ← Architecture & design details
├── SETUP.md                 ← Detailed setup guide
│
├── setup.sh                 ← Run this on Linux/Mac
├── setup.bat                ← Run this on Windows
├── run.py                   ← Start the application
│
├── app.py                   ← Flask backend
├── utils.py                 ← Utility functions
├── config.py                ← Configuration
├── requirements.txt         ← Python dependencies
│
├── templates/
│   ├── dashboard.html       ← Analytics dashboard
│   └── analyzer.html        ← Comment analyzer
│
└── load_sample_data.py      ← Load demo data
```

## What's Available

### Routes (URLs)

| URL | Purpose |
|-----|---------|
| http://localhost:5000/ | Main dashboard with analytics |
| http://localhost:5000/analyzer | Comment analyzer interface |

### API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| POST | /api/analyze | Analyze a comment |
| GET | /api/comments | Get all comments |
| GET | /api/stats | Get statistics |
| PATCH | /api/comments/{id}/status | Update comment status |
| DELETE | /api/comments/{id} | Delete a comment |
| GET | /api/export/csv | Export as CSV |
| GET | /api/export/pdf | Export as PDF |

Full details in **API.md**

## Key Features

✓ ML-based toxicity detection  
✓ 6-category classification  
✓ Real-time dashboard  
✓ Interactive charts  
✓ Search & filter  
✓ CSV/PDF export  
✓ Admin controls  
✓ Responsive design  

See **README.md** for complete feature list.

## Common First Steps

1. **Run the app**
   ```bash
   python run.py
   ```
   Then visit http://localhost:5000/

2. **Analyze a comment**
   Go to http://localhost:5000/analyzer and type something

3. **Check the dashboard**
   Go to http://localhost:5000/ to see statistics

4. **Export data**
   Click CSV or PDF export button on dashboard

5. **Try the API**
   See **API.md** for code examples

## Troubleshooting

### App won't start?
→ Read "INSTALLATION_GUIDE.md" - Troubleshooting section

### Pages showing blank?
→ Check "TESTING.md" - Troubleshooting section

### API not working?
→ Check "API.md" for endpoint details

### Questions about features?
→ Read "README.md"

## System Requirements

- Python 3.8+
- 100MB disk space
- Modern web browser
- Internet connection (for charts library)

## Next Steps

1. **Get it running:** Follow Quick Start above
2. **Learn the features:** Read README.md
3. **Test everything:** Read TESTING.md
4. **Integrate with code:** Read API.md
5. **Deploy:** Read INSTALLATION_GUIDE.md - Production section

## Documentation Index

| Document | Purpose | Read Time |
|----------|---------|-----------|
| START_HERE.md | This file - navigation | 3 min |
| QUICK_START.md | 5-minute setup | 5 min |
| INSTALLATION_GUIDE.md | Complete setup & troubleshooting | 10 min |
| README.md | All features & how to use | 15 min |
| API.md | API reference with examples | 20 min |
| PROJECT_OVERVIEW.md | Architecture & technical details | 15 min |
| TESTING.md | How to test the system | 10 min |

## Getting Help

1. **Setup issues?** → INSTALLATION_GUIDE.md
2. **How do I use it?** → README.md
3. **How do I integrate?** → API.md
4. **It's broken?** → TESTING.md or INSTALLATION_GUIDE.md
5. **How does it work?** → PROJECT_OVERVIEW.md

## Summary

The system is:
- **Easy to setup** - One command on Linux/Mac, one on Windows
- **Well documented** - 7 comprehensive guides
- **Production ready** - Tested, secure, scalable
- **Fully featured** - Everything you requested + bonus features

To get started:
1. Run setup.sh (Mac/Linux) or setup.bat (Windows)
2. Visit http://localhost:5000/
3. Read the relevant guide for your needs

---

**Ready? Let's go!**

Choose one:
- Just want to try it? → Run `python run.py` and visit http://localhost:5000/
- Need help setting up? → Read INSTALLATION_GUIDE.md
- Want to learn everything? → Read README.md
- Need to integrate? → Read API.md

---

Questions? Check the relevant documentation file in this directory!
