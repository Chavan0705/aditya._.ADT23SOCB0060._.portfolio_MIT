"""
Utility functions for Comment Moderation System
"""

import re
from datetime import datetime, timedelta
import random

class CommentAnalyzer:
    """Utility class for comment analysis"""
    
    TOXIC_KEYWORDS = {
        'hate_speech': ['racist', 'bigot', 'discrimination', 'ethnicity', 'slur'],
        'offensive': ['stupid', 'dumb', 'idiot', 'fool', 'crap', 'damn', 'sucks'],
        'spam': ['buy now', 'click here', 'free money', 'limited offer', 'act now', 'visit link'],
        'threat': ['kill', 'die', 'hurt', 'violence', 'destroy', 'punch', 'bomb'],
        'harassment': ['loser', 'pathetic', 'worthless', 'shame', 'garbage', 'waste'],
    }
    
    CATEGORY_MAP = {
        'hate_speech': 'Hate Speech',
        'offensive': 'Offensive Language',
        'spam': 'Spam',
        'threat': 'Threat',
        'harassment': 'Harassment',
    }
    
    @staticmethod
    def clean_text(text):
        """Clean and normalize comment text"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def extract_keywords(text, keywords_dict):
        """Extract matched keywords from text"""
        text_lower = text.lower()
        matched = []
        
        for category, keywords in keywords_dict.items():
            for keyword in keywords:
                if keyword in text_lower:
                    matched.append((category, keyword))
        
        return matched
    
    @staticmethod
    def calculate_toxicity(text, model=None, vectorizer=None):
        """
        Calculate toxicity score
        Falls back to keyword matching if model unavailable
        """
        text_clean = CommentAnalyzer.clean_text(text)
        
        # Try ML model first
        if model and vectorizer:
            try:
                vectorized = vectorizer.transform([text_clean])
                prediction = model.predict(vectorized)[0]
                probability = model.predict_proba(vectorized)[0]
                return probability[1] if len(probability) > 1 else prediction
            except Exception as e:
                print(f"Model prediction error: {e}")
        
        # Fallback to keyword matching
        matches = CommentAnalyzer.extract_keywords(text_clean, CommentAnalyzer.TOXIC_KEYWORDS)
        if not matches:
            return random.uniform(0.1, 0.3)  # Safe
        elif len(matches) == 1:
            return random.uniform(0.4, 0.6)  # Suspicious
        else:
            return random.uniform(0.6, 0.9)  # Likely toxic
    
    @staticmethod
    def categorize_comment(text, toxicity_score):
        """
        Categorize comment based on keywords and toxicity score
        Returns (category, confidence)
        """
        text_lower = text.lower()
        
        # Check for specific category keywords
        for category, keywords in CommentAnalyzer.TOXIC_KEYWORDS.items():
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


class DataGenerator:
    """Generate sample comments for testing"""
    
    SAFE_COMMENTS = [
        "Great article! Very informative and well written.",
        "I really enjoyed this content. Thanks for sharing!",
        "This is exactly what I needed. Appreciate it!",
        "Excellent work! Keep it up.",
        "Love the quality of this post.",
        "Very helpful and insightful discussion.",
        "Best thing I've read today!",
        "Thank you for the detailed explanation.",
    ]
    
    TOXIC_COMMENTS = [
        "This is complete trash, you're an idiot.",
        "I hate this, it's the worst thing ever.",
        "Kill yourself, nobody likes you.",
        "You're a worthless loser, garbage person.",
        "Go die in a fire, terrorist scum.",
        "This is spam, buy now at my fake link.",
        "Racist garbage, discrimination at its finest.",
        "You deserve to be hurt for this.",
    ]
    
    @staticmethod
    def generate_random_comments(count=10):
        """Generate random mix of safe and toxic comments"""
        comments = []
        for _ in range(count):
            if random.random() < 0.3:  # 30% toxic
                comment = random.choice(DataGenerator.TOXIC_COMMENTS)
            else:  # 70% safe
                comment = random.choice(DataGenerator.SAFE_COMMENTS)
            comments.append(comment)
        return comments


class DateHelper:
    """Date and time utility functions"""
    
    @staticmethod
    def now():
        """Get current datetime"""
        return datetime.utcnow()
    
    @staticmethod
    def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
        """Format datetime object"""
        if isinstance(dt, str):
            return dt
        return dt.strftime(format_str)
    
    @staticmethod
    def get_relative_time(dt):
        """Get relative time (e.g., '2 hours ago')"""
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        
        diff = datetime.utcnow() - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"
    
    @staticmethod
    def get_date_range(days=7):
        """Get date range for the last N days"""
        end = datetime.utcnow()
        start = end - timedelta(days=days)
        return start, end


class StatsCalculator:
    """Calculate statistics from comments"""
    
    @staticmethod
    def calculate_stats(comments):
        """Calculate comprehensive statistics"""
        total = len(comments)
        toxic = sum(1 for c in comments if c.get('is_toxic', False))
        safe = total - toxic
        
        categories = {}
        for comment in comments:
            cat = comment.get('category', 'Unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total': total,
            'toxic': toxic,
            'safe': safe,
            'toxic_percentage': (toxic / total * 100) if total > 0 else 0,
            'categories': categories,
            'avg_toxicity_score': sum(c.get('toxicity_score', 0) for c in comments) / total if total > 0 else 0
        }
    
    @staticmethod
    def get_category_trends(comments, days=7):
        """Get category trends over time"""
        trends = {}
        now = datetime.utcnow()
        cutoff = now - timedelta(days=days)
        
        for comment in comments:
            created = comment.get('created_at')
            if isinstance(created, str):
                created = datetime.fromisoformat(created)
            
            if created >= cutoff:
                cat = comment.get('category', 'Unknown')
                trends[cat] = trends.get(cat, 0) + 1
        
        return trends


class ExportHelper:
    """Helper functions for data export"""
    
    @staticmethod
    def format_for_csv(comments):
        """Format comments for CSV export"""
        lines = ['ID,Comment,Category,Toxicity Score,Confidence,Status,Is Toxic,Date & Time']
        
        for comment in comments:
            line = f'{comment.get("id", "")},' \
                   f'"{comment.get("original_text", "").replace(chr(34), chr(34)*2)}",' \
                   f'{comment.get("category", "")},' \
                   f'{comment.get("toxicity_score", "")},' \
                   f'{comment.get("confidence", "")},' \
                   f'{comment.get("status", "")},' \
                   f'{comment.get("is_toxic", "")},' \
                   f'{comment.get("created_at", "")}'
            lines.append(line)
        
        return '\n'.join(lines)
    
    @staticmethod
    def get_summary_stats(comments):
        """Get summary statistics for export"""
        total = len(comments)
        toxic = sum(1 for c in comments if c.get('is_toxic', False))
        safe = total - toxic
        
        return {
            'total_comments': total,
            'toxic_comments': toxic,
            'safe_comments': safe,
            'toxic_percentage': (toxic / total * 100) if total > 0 else 0,
            'export_date': DateHelper.format_datetime(DateHelper.now()),
        }
