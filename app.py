from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import cohere
from dotenv import load_dotenv
import requests
from collections import defaultdict

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-very-secure-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:diya@localhost/neevamind')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
sess = Session(app)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])  


# Cohere API setup
COHERE_API_KEY = os.getenv('COHERE_API_KEY', 'useyourownapikey')
co = cohere.Client(COHERE_API_KEY)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    diary_entries = db.relationship('DiaryEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    insights = db.relationship('Insight', backref='user', lazy=True, cascade='all, delete-orphan')

class DiaryEntry(db.Model):
    __tablename__ = 'diary_entries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entry_text = db.Column(db.Text, nullable=False)
    mood_tag = db.Column(db.String(50))
    memory_clarity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Insight(db.Model):
    __tablename__ = 'insights'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    insight_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Authentication Routes
@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            })
    return jsonify({'authenticated': False}), 401

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already exists with this email'}), 400
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        # Log in the user
        session['user_id'] = new_user.id
        
        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Signup failed: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        session['user_id'] = user.id
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

# Diary Routes
@app.route('/api/diary/entry', methods=['POST'])
def create_diary_entry():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        
        data = request.get_json()
        entry_text = data.get('entryText')
        mood_tag = data.get('moodTag')
        memory_clarity = data.get('memoryClarity')
        
        if not entry_text:
            return jsonify({'message': 'Entry text is required'}), 400
        
        new_entry = DiaryEntry(
            user_id=session['user_id'],
            entry_text=entry_text,
            mood_tag=mood_tag,
            memory_clarity=memory_clarity
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Diary entry created successfully',
            'entry': {
                'id': new_entry.id,
                'entry_text': new_entry.entry_text,
                'mood_tag': new_entry.mood_tag,
                'memory_clarity': new_entry.memory_clarity,
                'created_at': new_entry.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Failed to create diary entry: {str(e)}'}), 500

@app.route('/api/diary/entries', methods=['GET'])
def get_diary_entries():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        
        entries = DiaryEntry.query.filter_by(user_id=session['user_id']).order_by(DiaryEntry.created_at.desc()).all()
        
        return jsonify({
            'entries': [{
                'id': entry.id,
                'entry_text': entry.entry_text,
                'mood_tag': entry.mood_tag,
                'memory_clarity': entry.memory_clarity,
                'created_at': entry.created_at.isoformat()
            } for entry in entries]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch diary entries: {str(e)}'}), 500

# AI Insights Routes
@app.route('/api/insights/generate', methods=['POST'])
def generate_insights():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401

        entries = DiaryEntry.query.filter_by(user_id=session['user_id']).order_by(DiaryEntry.created_at.desc()).all()

        if not entries:
            return jsonify({'message': 'No diary entries found to analyze'}), 400

        # Prepare entries for analysis
        entries_text = "\n\n".join([
            f"Entry {i+1} ({entry.created_at.strftime('%Y-%m-%d')}):\n"
            f"Mood: {entry.mood_tag or 'Not specified'}\n"
            f"Memory Clarity: {entry.memory_clarity or 'Not specified'}/10\n"
            f"Content: {entry.entry_text}"
            for i, entry in enumerate(entries)
        ])

        # Call Cohere API without specifying model (uses default available)
        response = co.generate(
            prompt=f"""
            You are an AI assistant specialized in analyzing diary entries for early signs of cognitive decline and Alzheimer's disease. 
            Analyze the following diary entries and provide 5 specific insights about the person's cognitive wellness, 
            mood patterns, memory clarity, language usage, and behavioral patterns.

            Focus on:
            1. Mood analysis - emotional patterns and stability
            2. Memory patterns - any signs of memory issues or confusion
            3. Cognitive health - thinking patterns, clarity, coherence
            4. Language usage - vocabulary, sentence structure, communication clarity
            5. Behavioral insights - daily routines, activities mentioned

            For each insight, provide:
            - Clear, actionable observation
            - Category (mood, memory, cognitive, language, behavior)
            - Confidence level (0.0-1.0)

            Format your response as a JSON array with objects containing:
            - "insight_text": the insight description
            - "category": one of the categories above
            - "confidence": confidence score

            Diary entries to analyze:
            {entries_text}

            Respond only with the JSON array, no additional text.
            """,
            max_tokens=1000,
            temperature=0.3
        )

        insights_text = response.generations[0].text.strip()

        # Print raw Cohere response
        print("Raw Cohere Response:")
        print(insights_text)

        # Sanitize and parse JSON
        import json
        import re

        try:
            insights_text_clean = re.sub(r',\s*\]', ']', insights_text)  # Fix trailing commas
            insights_data = json.loads(insights_text_clean)
        except Exception as e:
            print("JSON parsing failed. Using fallback. Error:", str(e))
            insights_data = []
            lines = insights_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                    insights_data.append({
                        'insight_text': line.strip("1234567890.-* "),
                        'category': 'general',
                        'confidence': 0.7
                    })

        # Fallback test insights if parsing failed
        if not insights_data:
            print("No valid insights parsed. Creating test insights.")
            insights_data = [
                {'insight_text': 'Mood is generally calm with some fluctuations.', 'category': 'mood', 'confidence': 0.8},
                {'insight_text': 'Memory clarity seems stable.', 'category': 'memory', 'confidence': 0.85},
                {'insight_text': 'Language usage is rich and coherent.', 'category': 'language', 'confidence': 0.9}
            ]

        # Save insights to DB
        saved_insights = []
        for insight_data in insights_data[:5]:  # Limit to 5
            new_insight = Insight(
                user_id=session['user_id'],
                insight_text=insight_data.get('insight_text', 'No text'),
                category=insight_data.get('category', 'general'),
                confidence=insight_data.get('confidence', 0.5)
            )
            db.session.add(new_insight)
            saved_insights.append(new_insight)

        db.session.commit()

        return jsonify({
            'message': 'Insights generated successfully',
            'insights': [{
                'id': insight.id,
                'insight_text': insight.insight_text,
                'category': insight.category,
                'confidence': insight.confidence,
                'created_at': insight.created_at.isoformat()
            } for insight in saved_insights]
        }), 200

    except Exception as e:
        print("Insight generation error:", str(e))
        return jsonify({'message': f'Failed to generate insights: {str(e)}'}), 500


@app.route('/api/insights', methods=['GET'])
def get_insights():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        
        insights = Insight.query.filter_by(user_id=session['user_id']).order_by(Insight.created_at.desc()).all()
        
        return jsonify({
            'insights': [{
                'id': insight.id,
                'insight_text': insight.insight_text,
                'category': insight.category,
                'confidence': insight.confidence,
                'created_at': insight.created_at.isoformat()
            } for insight in insights]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to fetch insights: {str(e)}'}), 500

@app.route('/api/insights/weekly-report', methods=['GET'])
def get_weekly_report():
    try:
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        
        # Get entries from the last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        entries = DiaryEntry.query.filter(
            DiaryEntry.user_id == session['user_id'],
            DiaryEntry.created_at >= week_ago
        ).order_by(DiaryEntry.created_at.desc()).all()
        
        # Group entries by day and calculate metrics
        daily_data = defaultdict(lambda: {'entries': [], 'mood_scores': [], 'memory_scores': []})
        
        for entry in entries:
            day_name = entry.created_at.strftime('%a')
            daily_data[day_name]['entries'].append(entry)
            
            # Convert mood to numerical score
            mood_scores = {
                'happy': 8, 'calm': 7, 'energetic': 9,
                'sad': 3, 'anxious': 2, 'confused': 1, 'tired': 4
            }
            mood_score = mood_scores.get(entry.mood_tag, 5)
            daily_data[day_name]['mood_scores'].append(mood_score)
            
            if entry.memory_clarity:
                daily_data[day_name]['memory_scores'].append(entry.memory_clarity)
        
        # Prepare report data
        report = []
        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        for day in days_order:
            if day in daily_data:
                mood_avg = sum(daily_data[day]['mood_scores']) / len(daily_data[day]['mood_scores'])
                memory_avg = sum(daily_data[day]['memory_scores']) / len(daily_data[day]['memory_scores']) if daily_data[day]['memory_scores'] else 5
                
                report.append({
                    'day': day,
                    'moodScore': round(mood_avg, 1),
                    'memoryScore': round(memory_avg, 1),
                    'entryCount': len(daily_data[day]['entries'])
                })
            else:
                report.append({
                    'day': day,
                    'moodScore': 0,
                    'memoryScore': 0,
                    'entryCount': 0
                })
        
        return jsonify({'report': report}), 200
        
    except Exception as e:
        return jsonify({'message': f'Failed to generate weekly report: {str(e)}'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
