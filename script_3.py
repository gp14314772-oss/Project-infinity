# Main attendance session workflow

class AttendanceSessionManager:
    """Manages the complete attendance session workflow"""
    
    def __init__(self, attendance_system, hardware_manager):
        self.attendance_system = attendance_system
        self.hardware_manager = hardware_manager
        self.current_session = None
        self.session_active = False
    
    def start_attendance_session(self, class_name: str, subject: str):
        """Start a new attendance session"""
        if self.session_active:
            return False, "Another session is already active"
        
        print("\n" + "="*50)
        print("STARTING ATTENDANCE SESSION")
        print("="*50)
        
        # Step 1: Teacher fingerprint verification
        print("Step 1: Teacher verification required...")
        print("Please scan your fingerprint...")
        
        # Simulate fingerprint scan (in real implementation, this would wait for actual scan)
        success, teacher_id = self.hardware_manager.verify_teacher()
        
        if not success:
            print("✗ Teacher verification failed!")
            return False, "Teacher verification failed"
        
        print(f"✓ Teacher verified: {teacher_id}")
        
        # Step 2: Start session in database
        session_id = self.attendance_system.start_session(teacher_id, class_name, subject)
        self.current_session = session_id
        self.session_active = True
        
        print(f"✓ Session started with ID: {session_id}")
        print(f"Class: {class_name}")
        print(f"Subject: {subject}")
        print(f"Start time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nStudents can now scan their ID cards to mark attendance.")
        
        return True, session_id
    
    def process_student_attendance(self, num_students: int = 3):
        """Process student card scans for attendance"""
        if not self.session_active:
            return False, "No active session"
        
        print("\n" + "-"*40)
        print("STUDENT ATTENDANCE PHASE")
        print("-"*40)
        
        attendance_count = 0
        sample_cards = ["CARD001", "CARD002", "CARD003", "CARD004"]
        
        for i in range(min(num_students, len(sample_cards))):
            print(f"\nStudent {i+1} scanning card...")
            
            # Simulate card scan
            card_id = sample_cards[i]
            success, message = self.attendance_system.mark_attendance(self.current_session, card_id)
            
            if success:
                print(f"✓ Attendance marked for card: {card_id}")
                attendance_count += 1
            else:
                print(f"✗ Failed to mark attendance: {message}")
        
        print(f"\nTotal students marked present: {attendance_count}")
        return True, attendance_count
    
    def perform_camera_verification(self):
        """Perform camera-based verification"""
        if not self.session_active:
            return False, "No active session"
        
        print("\n" + "-"*40)
        print("CAMERA VERIFICATION PHASE")
        print("-"*40)
        
        print("Camera scanning classroom...")
        
        # Get camera count
        detected_count = self.hardware_manager.count_students(f"session_{self.current_session}_verification.jpg")
        
        # Log verification
        discrepancy = self.attendance_system.log_camera_verification(
            self.current_session, 
            detected_count,
            f"session_{self.current_session}_verification.jpg"
        )
        
        print(f"Camera detected: {detected_count} students")
        print(f"Card scans recorded: {detected_count - discrepancy} students")
        
        if discrepancy == 0:
            print("✓ Perfect match! No proxy attendance detected.")
        elif discrepancy > 0:
            print(f"⚠ WARNING: {discrepancy} discrepancy detected!")
            print("Possible proxy attendance or students without cards.")
        
        return True, discrepancy
    
    def end_attendance_session(self):
        """End the current attendance session"""
        if not self.session_active:
            return False, "No active session"
        
        print("\n" + "-"*40)
        print("ENDING ATTENDANCE SESSION")
        print("-"*40)
        
        # Teacher fingerprint verification to end session
        print("Teacher verification required to end session...")
        success, teacher_id = self.hardware_manager.verify_teacher()
        
        if not success:
            print("✗ Teacher verification failed! Session remains active.")
            return False, "Teacher verification failed"
        
        # End session
        self.attendance_system.end_session(self.current_session)
        
        print(f"✓ Session ended by teacher: {teacher_id}")
        print(f"End time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Generate session report
        report = self.attendance_system.get_session_report(self.current_session)
        self.print_session_report(report)
        
        self.session_active = False
        self.current_session = None
        
        return True, "Session ended successfully"
    
    def print_session_report(self, report):
        """Print formatted session report"""
        if not report:
            print("No report data available")
            return
        
        print("\n" + "="*50)
        print("SESSION ATTENDANCE REPORT")
        print("="*50)
        
        session = report['session']
        print(f"Session ID: {session[1]}")
        print(f"Teacher: {session[-1]} ({session[2]})")
        print(f"Class: {session[3]}")
        print(f"Subject: {session[4]}")
        print(f"Start Time: {session[5]}")
        print(f"End Time: {session[6]}")
        print(f"Status: {session[7]}")
        
        print(f"\nAttendance Summary:")
        print(f"Total Present: {report['total_present']}")
        
        if report['attendance_records']:
            print(f"\nStudent List:")
            for record in report['attendance_records']:
                print(f"- {record[7]} (ID: {record[2]}) - Scanned at: {record[3]}")
        
        if report['camera_verification']:
            camera_log = report['camera_verification']
            print(f"\nCamera Verification:")
            print(f"Detected Count: {camera_log[2]}")
            print(f"Card Scan Count: {camera_log[3]}")
            discrepancy = abs(camera_log[2] - camera_log[3])
            if discrepancy == 0:
                print("✓ Verification Status: PASSED (No discrepancy)")
            else:
                print(f"⚠ Verification Status: WARNING ({discrepancy} discrepancy)")

# Initialize session manager
session_manager = AttendanceSessionManager(attendance_system, hardware_manager)
print("Attendance Session Manager initialized successfully!")