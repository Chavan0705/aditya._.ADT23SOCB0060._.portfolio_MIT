"""
Comment Moderation & Tracking System
Flask Backend with SQLAlchemy and ML-based Toxic Comment Detection
"""

from flask import Flask, request, jsonify, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import numpy as np
import os
from io import BytesIO, StringIO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

# Initialize Flask App
app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# ==================== DATABASE MODELS ====================
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    toxicity_score = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='unreviewed')  # unreviewed, reviewed, approved
    is_toxic = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'original_text': self.original_text,
            'category': self.category,
            'toxicity_score': round(self.toxicity_score, 2),
            'confidence': round(self.confidence, 2),
            'status': self.status,
            'is_toxic': self.is_toxic,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'badge_color': self.get_badge_color()
        }
    
    def get_badge_color(self):
        if self.category == 'Hate Speech':
            return 'red'
        elif self.category == 'Offensive Language':
            return 'orange'
        elif self.category == 'Threat':
            return 'red'
        elif self.category == 'Harassment':
            return 'orange'
        elif self.category == 'Spam':
            return 'yellow'
        else:
            return 'green'

# ==================== CLASSIFICATION LOGIC ====================
TOXIC_KEYWORDS = {
    'hate_speech': ['racist', 'bigot', 'discrimination', 'ethnicity'],
    'offensive': ['stupid', 'dumb', 'idiot', 'fool', 'crap', 'damn'],
    'spam': ['buy now', 'click here', 'free money', 'limited offer', 'act now'],
    'threat': ['kill', 'die', 'hurt', 'violence', 'destroy'],
    'harassment': ['loser', 'pathetic', 'worthless', 'shame'],
}

def categorize_comment(text, toxicity_score):
    """
    Map model prediction and keywords to 6 categories
    """
    text_lower = text.lower()
    
    # Check for specific category keywords
    for category, keywords in TOXIC_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            if category == 'hate_speech':
                return 'Hate Speech', 0.85
            elif category == 'offensive':
                return 'Offensive Language', 0.75
            elif category == 'spam':
                return 'Spam', 0.70
            elif category == 'threat':
                return 'Threat', 0.90
            elif category == 'harassment':
                return 'Harassment', 0.80
    
    # Use toxicity score for categorization
    if toxicity_score < 0.3:
        return 'Safe / Positive', 0.95
    elif toxicity_score < 0.5:
        return 'Spam', 0.60
    elif toxicity_score < 0.7:
        return 'Offensive Language', toxicity_score
    else:
        return 'Threat', toxicity_score

def predict_toxicity(text):
    """
    Generate toxicity prediction
    Uses keyword matching and random simulation for demo
    """
    # Demo prediction based on keywords
    text_lower = text.lower()
    
    # Count toxic keywords
    toxic_count = 0
    for keywords in TOXIC_KEYWORDS.values():
        toxic_count += sum(1 for keyword in keywords if keyword in text_lower)
    
    # Return score based on keywords, with some randomness for demo
    if toxic_count > 0:
        return min(0.95, 0.6 + (toxic_count * 0.15))
    else:
        return np.random.uniform(0.1, 0.4)

# ==================== API ROUTES ====================

@app.route('/api/analyze', methods=['POST'])
def analyze_comment():
    """Analyze a comment and store in database"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
            
        text = data.get('text', '').strip()
        
        if not text or len(text) < 2:
            return jsonify({'error': 'Comment must be at least 2 characters'}), 400
        
        # Get toxicity prediction
        toxicity_score = predict_toxicity(text)
        category, confidence = categorize_comment(text, toxicity_score)
        is_toxic = toxicity_score > 0.5
        
        # Store in database
        comment = Comment(
            original_text=text,
            category=category,
            toxicity_score=toxicity_score,
            confidence=confidence,
            is_toxic=is_toxic
        )
        db.session.add(comment)
        db.session.commit()
        
        return jsonify(comment.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments', methods=['GET'])
def get_comments():
    """Get all comments with optional filtering"""
    try:
        category = request.args.get('category')
        status = request.args.get('status')
        is_toxic = request.args.get('is_toxic')
        search = request.args.get('search')
        
        query = Comment.query
        
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)
        if is_toxic:
            query = query.filter_by(is_toxic=is_toxic.lower() == 'true')
        if search:
            query = query.filter(Comment.original_text.ilike(f'%{search}%'))
        
        comments = query.order_by(Comment.created_at.desc()).all()
        return jsonify([c.to_dict() for c in comments]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment"""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<int:comment_id>/status', methods=['PATCH'])
def update_comment_status(comment_id):
    """Update comment status"""
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify({'error': 'Comment not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
            
        new_status = data.get('status')
        
        if new_status not in ['unreviewed', 'reviewed', 'approved']:
            return jsonify({'error': 'Invalid status'}), 400
        
        comment.status = new_status
        db.session.commit()
        return jsonify(comment.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        total_comments = Comment.query.count()
        toxic_comments = Comment.query.filter_by(is_toxic=True).count()
        safe_comments = total_comments - toxic_comments
        
        # Category breakdown
        categories = db.session.query(
            Comment.category, 
            db.func.count(Comment.id)
        ).group_by(Comment.category).all()
        
        category_data = {cat: count for cat, count in categories}
        
        # Recent comments
        recent = Comment.query.order_by(Comment.created_at.desc()).limit(10).all()
        
        stats = {
            'total_comments': total_comments,
            'toxic_comments': toxic_comments,
            'safe_comments': safe_comments,
            'toxic_percentage': round((toxic_comments / total_comments * 100) if total_comments > 0 else 0, 2),
            'category_breakdown': category_data,
            'recent_comments': [c.to_dict() for c in recent]
        }
        
        return jsonify(stats), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export comments as CSV"""
    try:
        comments = Comment.query.all()
        
        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow(['ID', 'Comment', 'Category', 'Toxicity Score', 'Confidence', 'Status', 'Is Toxic', 'Date & Time'])
        
        # Data
        for comment in comments:
            writer.writerow([
                comment.id,
                comment.original_text,
                comment.category,
                f"{comment.toxicity_score:.2f}",
                f"{comment.confidence:.2f}",
                comment.status,
                'Yes' if comment.is_toxic else 'No',
                comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        # Convert to bytes
        output.seek(0)
        csv_bytes = BytesIO(output.getvalue().encode('utf-8'))
        
        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name='comments_export.csv'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    """Export comments as PDF"""
    try:
        comments = Comment.query.all()
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30
        )
        elements.append(Paragraph("Comment Moderation Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Stats
        total = len(comments)
        toxic = sum(1 for c in comments if c.is_toxic)
        safe = total - toxic
        
        stats_text = f"Total Comments: {total} | Toxic: {toxic} | Safe: {safe}"
        elements.append(Paragraph(stats_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Table
        data = [['ID', 'Comment', 'Category', 'Score', 'Status']]
        for comment in comments[:50]:  # Limit to 50 for PDF
            comment_text = comment.original_text[:50] + '...' if len(comment.original_text) > 50 else comment.original_text
            data.append([
                str(comment.id),
                comment_text,
                comment.category,
                f"{comment.toxicity_score:.2f}",
                comment.status
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='comments_export.pdf'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Serve the dashboard"""
    return render_template('dashboard.html')

@app.route('/analyzer', methods=['GET'])
def analyzer():
    """Serve the analyzer page"""
    return render_template('analyzer.html')

# ==================== DATABASE INITIALIZATION ====================
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
