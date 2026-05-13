#!/usr/bin/env python3
"""
Script to load sample comments into the database for testing and demonstration
Usage: python load_sample_data.py [count]
Example: python load_sample_data.py 50
"""

import sys
import random
from datetime import datetime, timedelta
from app import app, db, Comment
from utils import CommentAnalyzer, DataGenerator

# Sample comments for better testing
SAMPLE_COMMENTS = {
    'hate_speech': [
        "This is racist garbage, we don't want your kind here.",
        "All members of that ethnicity are criminals, it's scientifically proven.",
        "Discrimination is justified against these people.",
    ],
    'offensive_language': [
        "This is absolutely stupid and idiotic.",
        "You're a dumb fool, this content sucks.",
        "What a bunch of crap, this is terrible.",
    ],
    'spam': [
        "Buy now at my store, click here for free money!",
        "Limited offer just for you! Act now before it's gone!",
        "Visit my website at sketchy-link.com for amazing deals!",
    ],
    'threat': [
        "I'm going to hurt you for what you said.",
        "You deserve to die, someone should kill you.",
        "I'm going to bomb this place, mark my words.",
    ],
    'harassment': [
        "You're a worthless loser and a complete waste of space.",
        "You're pathetic and deserve all the shame coming to you.",
        "Everyone agrees you're garbage and not welcome here.",
    ],
    'safe': [
        "This article is really informative and helpful!",
        "Great job on this project, very well done!",
        "I really appreciated the thoughtful discussion here.",
        "This made my day, thank you for sharing!",
        "Excellent explanation, I learned so much.",
        "Best thing I've read in a long time!",
        "Very inspiring and motivating content.",
        "Great quality work, keep it up!",
    ]
}

def load_sample_data(count=50):
    """Load sample comments into database"""
    print(f"\n📥 Loading {count} sample comments into database...\n")
    
    with app.app_context():
        try:
            # Clear existing comments (optional)
            # Comment.query.delete()
            # db.session.commit()
            
            created_count = 0
            now = datetime.utcnow()
            
            # Distribution: 70% safe, 10% each of 5 toxic categories
            distribution = {
                'safe': int(count * 0.7),
                'hate_speech': int(count * 0.1),
                'offensive_language': int(count * 0.1),
                'spam': int(count * 0.05),
                'threat': int(count * 0.03),
                'harassment': int(count * 0.02),
            }
            
            # Load comments for each category
            for category, num_comments in distribution.items():
                comments_list = SAMPLE_COMMENTS.get(category, [])
                
                for i in range(num_comments):
                    # Get random comment or generate variation
                    if comments_list:
                        text = random.choice(comments_list)
                    else:
                        text = f"Sample {category} comment {i+1}"
                    
                    # Add some variation
                    if i % 3 == 0:
                        text = text + " " + random.choice(["Really!", "Seriously!", "I mean it!", "No joke!", "100% true!"])
                    
                    # Calculate toxicity
                    if category == 'safe':
                        toxicity = random.uniform(0.1, 0.3)
                        confidence = random.uniform(0.85, 0.99)
                    elif category == 'offensive_language':
                        toxicity = random.uniform(0.55, 0.75)
                        confidence = random.uniform(0.7, 0.9)
                    elif category == 'spam':
                        toxicity = random.uniform(0.45, 0.65)
                        confidence = random.uniform(0.65, 0.85)
                    elif category == 'threat':
                        toxicity = random.uniform(0.8, 0.99)
                        confidence = random.uniform(0.85, 0.99)
                    elif category == 'harassment':
                        toxicity = random.uniform(0.65, 0.85)
                        confidence = random.uniform(0.75, 0.95)
                    else:  # hate_speech
                        toxicity = random.uniform(0.75, 0.99)
                        confidence = random.uniform(0.8, 0.98)
                    
                    # Map to category name
                    category_map = {
                        'safe': 'Safe / Positive',
                        'hate_speech': 'Hate Speech',
                        'offensive_language': 'Offensive Language',
                        'spam': 'Spam',
                        'threat': 'Threat',
                        'harassment': 'Harassment',
                    }
                    
                    # Create comment with random timestamp (last 30 days)
                    days_ago = random.randint(0, 30)
                    hours_ago = random.randint(0, 24)
                    created_at = now - timedelta(days=days_ago, hours=hours_ago)
                    
                    # Create comment object
                    comment = Comment(
                        original_text=text,
                        category=category_map[category],
                        toxicity_score=toxicity,
                        confidence=confidence,
                        is_toxic=toxicity > 0.5,
                        created_at=created_at,
                        status=random.choice(['unreviewed', 'reviewed', 'approved'])
                    )
                    
                    db.session.add(comment)
                    created_count += 1
                    
                    if created_count % 10 == 0:
                        print(f"   ✓ {created_count} comments processed...")
            
            # Commit all at once
            db.session.commit()
            print(f"\n✅ Successfully loaded {created_count} sample comments!\n")
            
            # Print summary
            total = Comment.query.count()
            toxic = Comment.query.filter_by(is_toxic=True).count()
            safe = total - toxic
            
            print("📊 Database Summary:")
            print(f"   Total Comments: {total}")
            print(f"   Toxic: {toxic} ({toxic/total*100:.1f}%)")
            print(f"   Safe: {safe} ({safe/total*100:.1f}%)")
            print()
            
            # Category breakdown
            categories = db.session.query(
                Comment.category,
                db.func.count(Comment.id)
            ).group_by(Comment.category).all()
            
            print("📈 Category Breakdown:")
            for cat, count in sorted(categories, key=lambda x: x[1], reverse=True):
                print(f"   {cat}: {count}")
            print()
            
        except Exception as e:
            print(f"❌ Error loading sample data: {e}")
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    # Get count from command line argument
    count = 50
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print(f"Invalid count: {sys.argv[1]}")
            print("Usage: python load_sample_data.py [count]")
            sys.exit(1)
    
    load_sample_data(count)
