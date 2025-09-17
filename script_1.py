# Core classes for the attendance system

import datetime
import hashlib
import json
import uuid
from typing import List, Dict, Optional
import sqlite3

class AttendanceSystem:
    def __init__(self, db_path='attendance_system.db'):
        self.db_path = db_path
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def add_teacher(self, teacher_id: str, name: str, fingerprint_data: bytes = None):
        """Add a new teacher to the system"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO teachers (teacher_id, name, fingerprint_template) VALUES (?, ?, ?)",
                (teacher_id, name, fingerprint_data)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_student(self, student_id: str, name: str, card_id: str, class_name: str):
        """Add a new student to the system"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO students (student_id, name, card_id, class_name) VALUES (?, ?, ?, ?)",
                (student_id, name, card_id, class_name)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def start_session(self, teacher_id: str, class_name: str, subject: str):
        """Start a new attendance session"""
        session_id = str(uuid.uuid4())
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO sessions (session_id, teacher_id, class_name, subject, start_time) VALUES (?, ?, ?, ?, ?)",
            (session_id, teacher_id, class_name, subject, datetime.datetime.now())
        )
        conn.commit()
        conn.close()
        return session_id
    
    def end_session(self, session_id: str):
        """End an attendance session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE sessions SET end_time = ?, status = 'completed' WHERE session_id = ?",
            (datetime.datetime.now(), session_id)
        )
        conn.commit()
        conn.close()
    
    def mark_attendance(self, session_id: str, card_id: str):
        """Mark attendance using card scan"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get student ID from card ID
        cursor.execute("SELECT student_id FROM students WHERE card_id = ?", (card_id,))
        student_result = cursor.fetchone()
        
        if not student_result:
            conn.close()
            return False, "Student not found"
        
        student_id = student_result[0]
        
        # Check if already marked
        cursor.execute(
            "SELECT id FROM attendance WHERE session_id = ? AND student_id = ?",
            (session_id, student_id)
        )
        
        if cursor.fetchone():
            conn.close()
            return False, "Already marked present"
        
        # Mark attendance
        cursor.execute(
            "INSERT INTO attendance (session_id, student_id, card_scan_time) VALUES (?, ?, ?)",
            (session_id, student_id, datetime.datetime.now())
        )
        conn.commit()
        conn.close()
        return True, "Attendance marked successfully"
    
    def log_camera_verification(self, session_id: str, detected_count: int, image_path: str = None):
        """Log camera detection results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current card scan count
        cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE session_id = ?",
            (session_id,)
        )
        card_scan_count = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO camera_logs (session_id, detected_count, card_scan_count, image_path) VALUES (?, ?, ?, ?)",
            (session_id, detected_count, card_scan_count, image_path)
        )
        conn.commit()
        conn.close()
        
        return abs(detected_count - card_scan_count)  # Return discrepancy
    
    def get_session_report(self, session_id: str):
        """Generate attendance report for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get session details
        cursor.execute("""
            SELECT s.*, t.name as teacher_name 
            FROM sessions s 
            JOIN teachers t ON s.teacher_id = t.teacher_id 
            WHERE s.session_id = ?
        """, (session_id,))
        session = cursor.fetchone()
        
        if not session:
            conn.close()
            return None
        
        # Get attendance records
        cursor.execute("""
            SELECT a.*, st.name as student_name, st.class_name
            FROM attendance a
            JOIN students st ON a.student_id = st.student_id
            WHERE a.session_id = ?
        """, (session_id,))
        attendance_records = cursor.fetchall()
        
        # Get camera logs
        cursor.execute(
            "SELECT * FROM camera_logs WHERE session_id = ? ORDER BY timestamp DESC LIMIT 1",
            (session_id,)
        )
        camera_log = cursor.fetchone()
        
        conn.close()
        
        return {
            'session': session,
            'attendance_records': attendance_records,
            'camera_verification': camera_log,
            'total_present': len(attendance_records)
        }

# Initialize the system
attendance_system = AttendanceSystem()

# Add some sample data
print("Adding sample teachers...")
attendance_system.add_teacher("T001", "Dr. Smith")
attendance_system.add_teacher("T002", "Prof. Johnson")

print("Adding sample students...")
attendance_system.add_student("S001", "Alice Brown", "CARD001", "10A")
attendance_system.add_student("S002", "Bob Wilson", "CARD002", "10A")
attendance_system.add_student("S003", "Charlie Davis", "CARD003", "10A")
attendance_system.add_student("S004", "Diana Miller", "CARD004", "10B")

print("Sample data added successfully!")