# Demonstrate complete attendance session workflow

print("DEMONSTRATING COMPLETE ATTENDANCE SESSION WORKFLOW")
print("="*60)

# Start a session
success, session_id = session_manager.start_attendance_session("10A", "Mathematics")

if success:
    # Process student attendance
    success, count = session_manager.process_student_attendance(3)
    
    if success:
        # Perform camera verification
        success, discrepancy = session_manager.perform_camera_verification()
        
        if success:
            # End the session
            success, message = session_manager.end_attendance_session()
            
            if success:
                print(f"\n✓ Complete session workflow executed successfully!")
            else:
                print(f"\n✗ Failed to end session: {message}")