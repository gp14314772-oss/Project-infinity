# Hardware interface modules

class FingerprintScanner:
    """Mock fingerprint scanner interface"""
    
    def __init__(self):
        self.is_connected = False
        self.registered_teachers = {}  # teacher_id -> fingerprint_hash
    
    def connect(self):
        """Connect to fingerprint scanner"""
        self.is_connected = True
        return True
    
    def register_fingerprint(self, teacher_id: str):
        """Register a teacher's fingerprint"""
        if not self.is_connected:
            return False, "Scanner not connected"
        
        # Simulate fingerprint registration
        fingerprint_hash = hashlib.md5(f"fingerprint_{teacher_id}".encode()).hexdigest()
        self.registered_teachers[teacher_id] = fingerprint_hash
        return True, fingerprint_hash
    
    def verify_fingerprint(self, scanned_data: str = None):
        """Verify a fingerprint scan"""
        if not self.is_connected:
            return False, None
        
        # Simulate fingerprint verification
        # In real implementation, this would process actual fingerprint data
        for teacher_id, stored_hash in self.registered_teachers.items():
            # Simulate successful verification for demonstration
            if scanned_data == stored_hash or scanned_data is None:
                return True, teacher_id
        
        return False, None

class CardReader:
    """Mock card reader interface"""
    
    def __init__(self):
        self.is_connected = False
    
    def connect(self):
        """Connect to card reader"""
        self.is_connected = True
        return True
    
    def read_card(self):
        """Read a card ID"""
        if not self.is_connected:
            return None
        
        # Simulate card reading
        # In real implementation, this would read from actual card reader
        return "CARD001"  # Mock card ID

class CameraSystem:
    """Mock camera system for person detection"""
    
    def __init__(self):
        self.is_connected = False
        self.detection_model_loaded = False
    
    def connect(self):
        """Connect to camera"""
        self.is_connected = True
        return True
    
    def load_detection_model(self):
        """Load YOLO model for person detection"""
        if not self.is_connected:
            return False
        
        self.detection_model_loaded = True
        return True
    
    def count_persons(self, save_image_path: str = None):
        """Count number of persons in camera view"""
        if not self.is_connected or not self.detection_model_loaded:
            return 0
        
        # Simulate person detection
        # In real implementation, this would use OpenCV + YOLO
        import random
        detected_count = random.randint(15, 25)  # Simulate 15-25 students detected
        
        if save_image_path:
            # Simulate saving detection image
            with open(save_image_path, 'w') as f:
                f.write(f"Detection image saved at {datetime.datetime.now()}")
        
        return detected_count

# Hardware manager class
class HardwareManager:
    """Manages all hardware components"""
    
    def __init__(self):
        self.fingerprint_scanner = FingerprintScanner()
        self.card_reader = CardReader()
        self.camera_system = CameraSystem()
        self.is_initialized = False
    
    def initialize_hardware(self):
        """Initialize all hardware components"""
        print("Initializing hardware components...")
        
        # Connect fingerprint scanner
        if self.fingerprint_scanner.connect():
            print("✓ Fingerprint scanner connected")
        else:
            print("✗ Failed to connect fingerprint scanner")
            return False
        
        # Connect card reader
        if self.card_reader.connect():
            print("✓ Card reader connected")
        else:
            print("✗ Failed to connect card reader")
            return False
        
        # Connect camera and load model
        if self.camera_system.connect():
            print("✓ Camera connected")
            if self.camera_system.load_detection_model():
                print("✓ Person detection model loaded")
            else:
                print("✗ Failed to load detection model")
                return False
        else:
            print("✗ Failed to connect camera")
            return False
        
        self.is_initialized = True
        print("All hardware components initialized successfully!")
        return True
    
    def register_teacher_fingerprint(self, teacher_id: str):
        """Register teacher fingerprint"""
        return self.fingerprint_scanner.register_fingerprint(teacher_id)
    
    def verify_teacher(self, fingerprint_data: str = None):
        """Verify teacher fingerprint"""
        return self.fingerprint_scanner.verify_fingerprint(fingerprint_data)
    
    def read_student_card(self):
        """Read student card"""
        return self.card_reader.read_card()
    
    def count_students(self, image_path: str = None):
        """Count students using camera"""
        return self.camera_system.count_persons(image_path)

# Initialize hardware manager
hardware_manager = HardwareManager()
hardware_manager.initialize_hardware()

# Register sample teacher fingerprints
print("\nRegistering teacher fingerprints...")
success, fp_data = hardware_manager.register_teacher_fingerprint("T001")
if success:
    print(f"Teacher T001 fingerprint registered: {fp_data[:10]}...")
    
success, fp_data = hardware_manager.register_teacher_fingerprint("T002")
if success:
    print(f"Teacher T002 fingerprint registered: {fp_data[:10]}...")