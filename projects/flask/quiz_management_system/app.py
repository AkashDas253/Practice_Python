import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
from functools import wraps
from models import db, User, Quiz, Question, Option, Attempt, Response

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- UTILITIES ---

def get_remaining_seconds(attempt):
    quiz = Quiz.query.get(attempt.quiz_id)
    
    if not quiz or quiz.time_limit == 0:
        return None
    
    if not attempt.started_at:
        return quiz.time_limit * 60

    elapsed = (datetime.utcnow() - attempt.started_at).total_seconds()
    remaining = (quiz.time_limit * 60) - elapsed
    
    return max(0, int(remaining))

def calculate_grade(attempt_id):
    responses = Response.query.filter_by(attempt_id=attempt_id).all()
    if not responses:
        return 0.0

    quiz_id = Attempt.query.get(attempt_id).quiz_id
    total_q = Question.query.filter_by(quiz_id=quiz_id).count()
    correct = 0

    for resp in responses:
        opt = Option.query.get(resp.option_id)
        if opt and opt.is_correct:
            correct += 1
            
    return round((correct / total_q) * 100, 2)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User.query.get(session.get('user_id'))
        if not user or user.role != 'admin':
            return "Access Denied", 403
        return f(*args, **kwargs)
    return decorated_function

# --- AUTH ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth.html')

    action = request.form.get('action') 
    username = request.form.get('username')
    password = request.form.get('password')

    if action == 'register':
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 400
        
        user = User(username=username, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
    else:
        user = User.query.filter_by(username=username).first()
        if not (user and user.check_password(password)):
            return jsonify({"error": "Invalid username or password"}), 401

    session.update({'user_id': user.id, 'username': user.username})
    
    target = url_for('admin_dashboard') if user.role == 'admin' else url_for('gallery')
    return jsonify({"redirect": target})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ADMIN ---

@app.route('/admin/create-quiz', methods=['GET', 'POST'])
@admin_required
def create_quiz():
    if request.method == 'POST':
        data = request.json
        try:
            quiz = Quiz(
                title=data.get('title'),
                description=data.get('description'),
                time_limit=int(data.get('time_limit', 10)),
                max_attempts=int(data.get('max_attempts', 3))
            )
            db.session.add(quiz)
            db.session.commit()

            for q_info in data.get('questions', []):
                if q_info.get('type') == 'reuse':
                    orig = Question.query.get(q_info.get('id'))
                    if orig:
                        new_q = Question(quiz_id=quiz.id, text=orig.text)
                        db.session.add(new_q)
                        db.session.commit()
                        for o in orig.options:
                            db.session.add(Option(question_id=new_q.id, text=o.text, is_correct=o.is_correct))
                else:
                    new_q = Question(quiz_id=quiz.id, text=q_info.get('text'))
                    db.session.add(new_q)
                    db.session.commit()
                    for o_info in q_info.get('options', []):
                        if o_info.get('text'):
                            db.session.add(Option(question_id=new_q.id, text=o_info['text'], is_correct=bool(o_info.get('is_correct'))))
            
            db.session.commit()
            return jsonify({"status": "success", "redirect": url_for('gallery')})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 400
            
    return render_template('admin_create.html', question_bank=Question.query.all())

@app.route('/admin/quiz/<int:quiz_id>/stats')
@admin_required
def quiz_stats(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    attempts = Attempt.query.filter_by(quiz_id=quiz_id, status='completed').all()
    
    scores = [a.score for a in attempts] if attempts else [0]
    results = db.session.query(
        User.username, 
        db.func.max(Attempt.score).label('best_score'),
        db.func.count(Attempt.id).label('attempt_count')
    ).join(Attempt).filter(Attempt.quiz_id == quiz_id, Attempt.status == 'completed')\
     .group_by(User.id).all()

    return render_template('admin_stats.html', 
                           quiz=quiz, 
                           avg=round(sum(scores)/len(scores), 2) if attempts else 0, 
                           high=max(scores), 
                           participants=len(set(a.user_id for a in attempts)),
                           results=results)

# --- CORE APP ---

@app.route('/')
def index():
    uid = session.get('user_id')
    if not uid: return redirect(url_for('login'))
    
    user = User.query.get(uid)
    if not user:
        session.clear()
        return redirect(url_for('login'))

    if user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    uid = session.get('user_id')
    user = User.query.get(uid)
    
    if user.role == 'admin': return redirect(url_for('admin_dashboard'))

    quiz_data = []
    for q in Quiz.query.all():
        active = Attempt.query.filter_by(user_id=uid, quiz_id=q.id, status='started').first()
        quiz_data.append({
            'info': q,
            'completed': Attempt.query.filter_by(user_id=uid, quiz_id=q.id, status='completed').count(),
            'active_id': active.id if active else None
        })
    return render_template('gallery.html', quizzes=quiz_data, user=user)

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    quizzes = Quiz.query.all()
    stats = {
        'total_students': User.query.filter_by(role='student').count(),
        'total_attempts': Attempt.query.count()
    }
    return render_template('admin_dashboard.html', quizzes=quizzes, stats=stats)

@app.route('/quiz/<int:quiz_id>/start')
def start_quiz(quiz_id):
    uid = session.get('user_id')
    if not uid: return redirect(url_for('login'))

    user = User.query.get(uid)
    if not user:
        session.clear()
        return redirect(url_for('login'))

    if user.role == 'admin':
        return redirect(url_for('admin_dashboard'))

    active = Attempt.query.filter_by(user_id=uid, quiz_id=quiz_id, status='started').first()
    if active: 
        return redirect(url_for('quiz_engine_view', attempt_id=active.id))

    quiz = Quiz.query.get_or_404(quiz_id)
    done_count = Attempt.query.filter_by(user_id=uid, quiz_id=quiz_id, status='completed').count()
    
    if quiz.max_attempts > 0 and done_count >= quiz.max_attempts: 
        return "No attempts left. You have reached the maximum limit.", 403

    attempt = Attempt(
        user_id=uid, 
        quiz_id=quiz_id, 
        attempt_number=done_count + 1, 
        status='started',
        started_at=datetime.utcnow() 
    )
    
    db.session.add(attempt)
    db.session.commit()
    
    return redirect(url_for('quiz_engine_view', attempt_id=attempt.id))

@app.route('/attempt/<int:attempt_id>')
def quiz_engine_view(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    if attempt.user_id != session.get('user_id') or attempt.status == 'completed':
        return redirect(url_for('gallery'))
    return render_template('engine.html', attempt=attempt, quiz=Quiz.query.get(attempt.quiz_id), remaining_time=get_remaining_seconds(attempt))

# --- API ---

@app.route('/api/attempt/<int:attempt_id>/questions')
def api_get_questions(attempt_id):
    attempt = Attempt.query.get(attempt_id)
    resps = {r.question_id: r.option_id for r in Response.query.filter_by(attempt_id=attempt_id).all()}
    
    data = []
    for q in Quiz.query.get(attempt.quiz_id).questions:
        data.append({
            "id": q.id, "text": q.text,
            "options": [{"id": o.id, "text": o.text} for o in q.options],
            "selected_option": resps.get(q.id)
        })
    return jsonify(data)

@app.route('/api/sync', methods=['POST'])
def api_sync_response():
    data = request.json
    attempt = Attempt.query.get(data['attempt_id'])
    if attempt.status != 'started': return jsonify({"error": "Closed"}), 403

    resp = Response.query.filter_by(attempt_id=attempt.id, question_id=data['question_id']).first()
    if resp:
        resp.option_id = data['option_id']
    else:
        db.session.add(Response(attempt_id=attempt.id, question_id=data['question_id'], option_id=data['option_id']))
    db.session.commit()
    return jsonify({"status": "synced"})

@app.route('/api/attempt/<int:attempt_id>/submit', methods=['POST'])
def api_submit(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    attempt.score = calculate_grade(attempt_id)
    attempt.status, attempt.completed_at = 'completed', datetime.utcnow()
    db.session.commit()
    return jsonify({"score": attempt.score, "redirect": "/"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)