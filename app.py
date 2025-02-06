from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

# PostgreSQL Database Configuration (Update with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/taskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email Configuration (Update with your SMTP credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

# Initialize Database and Mail
db = SQLAlchemy(app)
mail = Mail(app)

# Define Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    assignee = db.Column(db.String(100), nullable=False)

# Create Database Tables
with app.app_context():
    db.create_all()

# Function to send email notification
def send_email_notification(assignee_email, task_title, task_due_date):
    try:
        msg = Message(
            subject="New Task Assigned",
            recipients=[assignee_email],
            body=f"You have been assigned a new task: '{task_title}'\nDue Date: {task_due_date}\n\nPlease check your task list for more details."
        )
        mail.send(msg)
    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# POST Route to Create a New Task
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    # Validate request data
    required_fields = ['title', 'description', 'due_date', 'priority', 'status', 'assignee']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    # Create a new task
    new_task = Task(
        title=data['title'],
        description=data['description'],
        due_date=due_date,
        priority=data['priority'],
        status=data['status'],
        assignee=data['assignee']
    )

    db.session.add(new_task)
    db.session.commit()

@app.route('/models/tornado-mode', methods=['GET'])
def tornado_mode():
    """Fetch only urgent tasks."""
    urgent_tasks = Task.query.filter(Task.completed == False).all()
    urgent_tasks = [task for task in urgent_tasks if task.is_urgent()]

    return jsonify([{
        'id': task.id,
        'title': task.title,
        'due_date': task.due_date.isoformat(),
        'priority': task.priority
    } for task in urgent_tasks])


    # Send email notification
    send_email_notification(data['assignee'], data['title'], data['due_date'])

    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "due_date": new_task.due_date.isoformat(),
        "priority": new_task.priority,
        "status": new_task.status,
        "assignee": new_task.assignee
    }), 201  # 201 Created

if __name__ == '__main__':
    app.run(debug=True)
