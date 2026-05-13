#!/usr/bin/env python3
"""
Startup script for Comment Moderation & Tracking System
Handles database initialization and starts the Flask app
"""

import sys
import os
from app import app, init_db

def main():
    """Initialize and run the application"""
    print("\n" + "="*60)
    print("🚀 Comment Moderation & Tracking System")
    print("="*60 + "\n")
    
    # Initialize database
    print("📊 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully\n")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}\n")
        sys.exit(1)
    
    # Check for model files
    print("🤖 Checking ML model files...")
    if os.path.exists('toxic_model.pkl') and os.path.exists('vectorizer.pkl'):
        print("✅ Model files found - Using trained ML model\n")
    else:
        print("⚠️  Model files not found - Running in demo mode\n")
        print("   To use ML predictions, add:")
        print("   - toxic_model.pkl")
        print("   - vectorizer.pkl\n")
    
    # Start Flask app
    print("🌐 Starting Flask development server...")
    print("-"*60)
    print("Dashboard:  http://localhost:5000/")
    print("Analyzer:   http://localhost:5000/analyzer")
    print("-"*60 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error running server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
