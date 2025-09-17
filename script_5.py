# Create Flask web application for the dashboard

flask_app_code = '''
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import datetime
import uuid
from typing import Dict, List

app = Flask(__name__)

class WebAttendanceSystem:
    def __init__(self, db_path='attendance_system.db'):
        self.db_path = db_path
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_all_teachers(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers ORDER BY name")
        teachers = cursor.fetchall()
        conn.close()
        return teachers
    
    def get_all_students(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY class_name, name")
        students = cursor.fetchall()
        conn.close()
        return students
    
    def get_recent_sessions(self, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, t.name as teacher_name 
            FROM sessions s 
            JOIN teachers t ON s.teacher_id = t.teacher_id 
            ORDER BY s.created_at DESC 
            LIMIT ?
        """, (limit,))
        sessions = cursor.fetchall()
        conn.close()
        return sessions
    
    def get_session_details(self, session_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get session info
        cursor.execute("""
            SELECT s.*, t.name as teacher_name 
            FROM sessions s 
            JOIN teachers t ON s.teacher_id = t.teacher_id 
            WHERE s.session_id = ?
        """, (session_id,))
        session = cursor.fetchone()
        
        # Get attendance records
        cursor.execute("""
            SELECT a.*, st.name as student_name, st.class_name
            FROM attendance a
            JOIN students st ON a.student_id = st.student_id
            WHERE a.session_id = ?
            ORDER BY a.card_scan_time
        """, (session_id,))
        attendance = cursor.fetchall()
        
        # Get camera verification
        cursor.execute("""
            SELECT * FROM camera_logs 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (session_id,))
        camera_log = cursor.fetchone()
        
        conn.close()
        return session, attendance, camera_log

# Initialize web system
web_system = WebAttendanceSystem()

@app.route('/')
def dashboard():
    """Main dashboard"""
    teachers = web_system.get_all_teachers()
    students = web_system.get_all_students()
    recent_sessions = web_system.get_recent_sessions()
    
    stats = {
        'total_teachers': len(teachers),
        'total_students': len(students),
        'recent_sessions': len(recent_sessions)
    }
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_sessions=recent_sessions)

@app.route('/teachers')
def teachers():
    """Teachers management page"""
    teachers = web_system.get_all_teachers()
    return render_template('teachers.html', teachers=teachers)

@app.route('/students')
def students():
    """Students management page"""
    students = web_system.get_all_students()
    return render_template('students.html', students=students)

@app.route('/sessions')
def sessions():
    """Sessions history page"""
    sessions = web_system.get_recent_sessions(50)
    return render_template('sessions.html', sessions=sessions)

@app.route('/session/<session_id>')
def session_detail(session_id):
    """Session detail page"""
    session, attendance, camera_log = web_system.get_session_details(session_id)
    
    if not session:
        return "Session not found", 404
    
    # Calculate stats
    total_present = len(attendance)
    discrepancy = 0
    if camera_log:
        discrepancy = abs(camera_log[2] - camera_log[3])
    
    return render_template('session_detail.html',
                         session=session,
                         attendance=attendance,
                         camera_log=camera_log,
                         total_present=total_present,
                         discrepancy=discrepancy)

@app.route('/api/add_teacher', methods=['POST'])
def add_teacher():
    """API endpoint to add teacher"""
    data = request.json
    teacher_id = data.get('teacher_id')
    name = data.get('name')
    
    if not teacher_id or not name:
        return jsonify({'success': False, 'error': 'Missing required fields'})
    
    # Add teacher logic here
    return jsonify({'success': True, 'message': 'Teacher added successfully'})

@app.route('/api/add_student', methods=['POST'])
def add_student():
    """API endpoint to add student"""
    data = request.json
    student_id = data.get('student_id')
    name = data.get('name')
    card_id = data.get('card_id')
    class_name = data.get('class_name')
    
    if not all([student_id, name, card_id, class_name]):
        return jsonify({'success': False, 'error': 'Missing required fields'})
    
    # Add student logic here
    return jsonify({'success': True, 'message': 'Student added successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

# Save Flask application
with open('app.py', 'w') as f:
    f.write(flask_app_code)

print("Flask web application created: app.py")