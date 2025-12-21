from app import app, db
from models import User, Quiz, Question, Option

def seed_data():
    with app.app_context():
        db.create_all()
        
        # 1. Admin Account
        if not User.query.filter_by(username='admin1').first():
            admin = User(username='admin1', role='admin')
            admin.set_password('admin-pass') 
            db.session.add(admin)

        # 2. Student Account
        if not User.query.filter_by(username='student1').first():
            student = User(username='student1', role='student')
            student.set_password('password123') 
            db.session.add(student)

        # 3. Sample Quiz Content
        if not Quiz.query.filter_by(title='JavaScript Basics').first():
            quiz = Quiz(
                title='JavaScript Basics',
                description='Test your knowledge of Vanilla JS concepts.',
                time_limit=5, 
                max_attempts=3
            )
            db.session.add(quiz)
            db.session.commit() 
            
            q1 = Question(quiz_id=quiz.id, text='Which keyword creates a constant?')
            db.session.add(q1)
            db.session.commit()
            
            db.session.add_all([
                Option(question_id=q1.id, text='var', is_correct=False),
                Option(question_id=q1.id, text='let', is_correct=False),
                Option(question_id=q1.id, text='const', is_correct=True),
                Option(question_id=q1.id, text='final', is_correct=False)
            ])
        
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()