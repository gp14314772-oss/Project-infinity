// Automated Attendance & Monitoring System JavaScript

class AttendanceSystem {
    constructor() {
        this.data = {
            teachers: [
                {"id": "T001", "name": "Dr. Smith", "fingerprintRegistered": true},
                {"id": "T002", "name": "Prof. Johnson", "fingerprintRegistered": true},
                {"id": "T003", "name": "Ms. Davis", "fingerprintRegistered": false}
            ],
            students: [
                {"id": "S001", "name": "Alice Brown", "cardId": "CARD001", "class": "10A"},
                {"id": "S002", "name": "Bob Wilson", "cardId": "CARD002", "class": "10A"},
                {"id": "S003", "name": "Charlie Davis", "cardId": "CARD003", "class": "10A"},
                {"id": "S004", "name": "Diana Miller", "cardId": "CARD004", "class": "10B"},
                {"id": "S005", "name": "Eva Martinez", "cardId": "CARD005", "class": "10A"},
                {"id": "S006", "name": "Frank Anderson", "cardId": "CARD006", "class": "10B"},
                {"id": "S007", "name": "Grace Lee", "cardId": "CARD007", "class": "10A"},
                {"id": "S008", "name": "Henry Chen", "cardId": "CARD008", "class": "10B"}
            ],
            sampleSessions: [
                {
                    "sessionId": "SES001",
                    "teacherId": "T001",
                    "teacherName": "Dr. Smith",
                    "class": "10A",
                    "subject": "Mathematics",
                    "startTime": "2025-09-17 09:00:00",
                    "endTime": "2025-09-17 09:45:00",
                    "status": "completed",
                    "attendanceCount": 6,
                    "cameraDetected": 6,
                    "discrepancy": 0
                },
                {
                    "sessionId": "SES002", 
                    "teacherId": "T002",
                    "teacherName": "Prof. Johnson",
                    "class": "10B",
                    "subject": "Science",
                    "startTime": "2025-09-17 10:00:00",
                    "endTime": "2025-09-17 10:45:00",
                    "status": "completed",
                    "attendanceCount": 5,
                    "cameraDetected": 7,
                    "discrepancy": 2
                }
            ]
        };

        this.currentSession = {
            sessionId: null,
            teacher: null,
            class: null,
            subject: null,
            startTime: null,
            endTime: null,
            presentStudents: [],
            cardsScanned: 0,
            cameraDetected: 0
        };

        this.availableStudents = [];
        this.init();
    }

    init() {
        this.initializeElements();
        this.setupEventListeners();
        this.updateDashboard();
        this.populateRecentSessions();
        this.populateTeacherSelect();
    }

    initializeElements() {
        // Dashboard elements
        this.totalTeachersEl = document.getElementById('total-teachers');
        this.totalStudentsEl = document.getElementById('total-students');
        this.totalSessionsEl = document.getElementById('total-sessions');
        this.activeStatusEl = document.getElementById('active-status');
        
        // Modal elements
        this.modal = document.getElementById('session-modal');
        this.modalOverlay = document.getElementById('modal-overlay');
        this.closeModalBtn = document.getElementById('close-modal');
        
        // Session workflow elements
        this.startSessionBtn = document.getElementById('start-session-btn');
        this.teacherSelect = document.getElementById('teacher-select');
        this.verifyFingerprintBtn = document.getElementById('verify-fingerprint');
        this.authLoadingEl = document.getElementById('auth-loading');
        
        // Session setup elements
        this.classSelect = document.getElementById('class-select');
        this.subjectInput = document.getElementById('subject-input');
        this.setupCompleteBtn = document.getElementById('setup-complete');
        
        // Attendance elements
        this.cardsScannedEl = document.getElementById('cards-scanned');
        this.presentCountEl = document.getElementById('present-count');
        this.simulateCardScanBtn = document.getElementById('simulate-card-scan');
        this.verifyCameraBtn = document.getElementById('verify-camera');
        this.presentStudentsEl = document.getElementById('present-students');
        
        // Verification elements
        this.finalCardsCountEl = document.getElementById('final-cards-count');
        this.cameraDetectedCountEl = document.getElementById('camera-detected-count');
        this.discrepancyCountEl = document.getElementById('discrepancy-count');
        this.endSessionBtn = document.getElementById('end-session-btn');
        
        // Report elements
        this.reportSessionIdEl = document.getElementById('report-session-id');
        this.reportTeacherEl = document.getElementById('report-teacher');
        this.reportClassEl = document.getElementById('report-class');
        this.reportSubjectEl = document.getElementById('report-subject');
        this.reportDurationEl = document.getElementById('report-duration');
        this.reportAttendanceEl = document.getElementById('report-attendance');
        this.reportVerificationEl = document.getElementById('report-verification');
        this.finishSessionBtn = document.getElementById('finish-session');
    }

    setupEventListeners() {
        // Main session button
        if (this.startSessionBtn) {
            this.startSessionBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.openSessionModal();
            });
        }

        // Modal close events
        if (this.closeModalBtn) {
            this.closeModalBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.closeSessionModal();
            });
        }

        if (this.modalOverlay) {
            this.modalOverlay.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.closeSessionModal();
            });
        }
        
        // Workflow event listeners
        if (this.teacherSelect) {
            this.teacherSelect.addEventListener('change', () => this.onTeacherSelect());
        }

        if (this.verifyFingerprintBtn) {
            this.verifyFingerprintBtn.addEventListener('click', () => this.verifyFingerprint());
        }

        if (this.setupCompleteBtn) {
            this.setupCompleteBtn.addEventListener('click', () => this.completeSessionSetup());
        }
        
        if (this.simulateCardScanBtn) {
            this.simulateCardScanBtn.addEventListener('click', () => this.simulateCardScan());
        }

        if (this.verifyCameraBtn) {
            this.verifyCameraBtn.addEventListener('click', () => this.performCameraVerification());
        }

        if (this.endSessionBtn) {
            this.endSessionBtn.addEventListener('click', () => this.endSession());
        }

        if (this.finishSessionBtn) {
            this.finishSessionBtn.addEventListener('click', () => this.finishAndReturn());
        }

        // ESC key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal && !this.modal.classList.contains('hidden')) {
                this.closeSessionModal();
            }
        });
    }

    updateDashboard() {
        if (this.totalTeachersEl) this.totalTeachersEl.textContent = this.data.teachers.length;
        if (this.totalStudentsEl) this.totalStudentsEl.textContent = this.data.students.length;
        if (this.totalSessionsEl) this.totalSessionsEl.textContent = this.data.sampleSessions.length;
        if (this.activeStatusEl) this.activeStatusEl.textContent = this.currentSession.sessionId ? 'Active' : 'Inactive';
    }

    populateRecentSessions() {
        const tbody = document.getElementById('sessions-tbody');
        if (!tbody) return;
        
        tbody.innerHTML = '';

        this.data.sampleSessions.forEach(session => {
            const row = document.createElement('tr');
            const statusClass = session.discrepancy === 0 ? 'status--success' : 'status--warning';
            const statusText = session.discrepancy === 0 ? 'Verified' : `${session.discrepancy} Discrepancy`;
            
            row.innerHTML = `
                <td>${session.sessionId}</td>
                <td>${session.teacherName}</td>
                <td>${session.class}</td>
                <td>${session.subject}</td>
                <td>${session.attendanceCount}</td>
                <td><span class="status ${statusClass}">${statusText}</span></td>
            `;
            tbody.appendChild(row);
        });
    }

    populateTeacherSelect() {
        if (!this.teacherSelect) return;
        
        this.teacherSelect.innerHTML = '<option value="">Choose a teacher...</option>';
        this.data.teachers.forEach(teacher => {
            const option = document.createElement('option');
            option.value = teacher.id;
            option.textContent = teacher.name;
            option.dataset.fingerprintRegistered = teacher.fingerprintRegistered;
            this.teacherSelect.appendChild(option);
        });
    }

    openSessionModal() {
        console.log('Opening session modal...');
        if (!this.modal) {
            console.error('Modal element not found');
            return;
        }
        
        // Reset session state
        this.resetSession();
        
        // Show modal
        this.modal.classList.remove('hidden');
        this.modal.style.display = 'flex';
        
        // Show first step
        this.showStep(1);
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        console.log('Modal opened successfully');
    }

    closeSessionModal() {
        console.log('Closing session modal...');
        if (!this.modal) return;
        
        this.modal.classList.add('hidden');
        this.modal.style.display = 'none';
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        // Reset session
        this.resetSession();
        
        console.log('Modal closed successfully');
    }

    resetSession() {
        this.currentSession = {
            sessionId: null,
            teacher: null,
            class: null,
            subject: null,
            startTime: null,
            endTime: null,
            presentStudents: [],
            cardsScanned: 0,
            cameraDetected: 0
        };
        
        this.availableStudents = [];
        
        // Reset form elements
        if (this.teacherSelect) this.teacherSelect.value = '';
        if (this.subjectInput) this.subjectInput.value = '';
        if (this.verifyFingerprintBtn) this.verifyFingerprintBtn.disabled = true;
        if (this.authLoadingEl) this.authLoadingEl.classList.add('hidden');
        if (this.presentStudentsEl) this.presentStudentsEl.innerHTML = '';
        
        this.updateAttendanceDisplay();
    }

    showStep(stepNumber) {
        console.log(`Showing step ${stepNumber}`);
        
        // Hide all steps
        for (let i = 1; i <= 5; i++) {
            const step = document.getElementById(`step-${i}`);
            if (step) {
                step.classList.add('hidden');
                step.classList.remove('active');
            }
        }
        
        // Show target step
        const targetStep = document.getElementById(`step-${stepNumber}`);
        if (targetStep) {
            targetStep.classList.remove('hidden');
            targetStep.classList.add('active');
            console.log(`Step ${stepNumber} is now visible`);
        } else {
            console.error(`Step ${stepNumber} element not found`);
        }
    }

    onTeacherSelect() {
        if (!this.teacherSelect) return;
        
        const selectedOption = this.teacherSelect.selectedOptions[0];
        if (selectedOption && selectedOption.value) {
            const fingerprintRegistered = selectedOption.dataset.fingerprintRegistered === 'true';
            if (this.verifyFingerprintBtn) {
                this.verifyFingerprintBtn.disabled = !fingerprintRegistered;
            }
            
            if (!fingerprintRegistered) {
                alert('This teacher does not have fingerprint registered. Please contact administrator.');
            }
        } else {
            if (this.verifyFingerprintBtn) this.verifyFingerprintBtn.disabled = true;
        }
    }

    verifyFingerprint() {
        if (!this.authLoadingEl || !this.verifyFingerprintBtn) return;
        
        this.authLoadingEl.classList.remove('hidden');
        this.verifyFingerprintBtn.disabled = true;
        
        // Simulate fingerprint verification delay
        setTimeout(() => {
            const selectedTeacher = this.data.teachers.find(t => t.id === this.teacherSelect.value);
            this.currentSession.teacher = selectedTeacher;
            this.currentSession.sessionId = this.generateSessionId();
            this.currentSession.startTime = new Date();
            
            this.authLoadingEl.classList.add('hidden');
            this.showStep(2);
        }, 2000);
    }

    completeSessionSetup() {
        if (!this.subjectInput || !this.subjectInput.value.trim()) {
            alert('Please enter a subject for the session.');
            return;
        }

        this.currentSession.class = this.classSelect ? this.classSelect.value : '10A';
        this.currentSession.subject = this.subjectInput.value.trim();
        
        // Filter students for the selected class
        this.availableStudents = this.data.students.filter(s => s.class === this.currentSession.class);
        
        this.showStep(3);
        this.updateAttendanceDisplay();
    }

    simulateCardScan() {
        if (this.availableStudents.length === 0) {
            alert('No students available for this class.');
            return;
        }

        // Get students not yet present
        const notPresentStudents = this.availableStudents.filter(
            student => !this.currentSession.presentStudents.find(p => p.id === student.id)
        );

        if (notPresentStudents.length === 0) {
            alert('All students in this class are already marked present.');
            return;
        }

        // Randomly select a student
        const randomStudent = notPresentStudents[Math.floor(Math.random() * notPresentStudents.length)];
        this.currentSession.presentStudents.push(randomStudent);
        this.currentSession.cardsScanned++;

        this.updateAttendanceDisplay();
        this.addStudentChip(randomStudent);
    }

    updateAttendanceDisplay() {
        if (this.cardsScannedEl) this.cardsScannedEl.textContent = this.currentSession.cardsScanned;
        if (this.presentCountEl) this.presentCountEl.textContent = this.currentSession.presentStudents.length;
    }

    addStudentChip(student) {
        if (!this.presentStudentsEl) return;
        
        const chip = document.createElement('div');
        chip.className = 'student-chip';
        chip.textContent = student.name;
        this.presentStudentsEl.appendChild(chip);
    }

    performCameraVerification() {
        // Simulate camera detection with some randomness
        const actualCount = this.currentSession.cardsScanned;
        const variation = Math.floor(Math.random() * 3) - 1; // -1, 0, or 1
        this.currentSession.cameraDetected = Math.max(0, actualCount + variation);

        if (this.finalCardsCountEl) this.finalCardsCountEl.textContent = this.currentSession.cardsScanned;
        if (this.cameraDetectedCountEl) this.cameraDetectedCountEl.textContent = this.currentSession.cameraDetected;
        
        const discrepancy = Math.abs(this.currentSession.cameraDetected - this.currentSession.cardsScanned);
        if (this.discrepancyCountEl) {
            this.discrepancyCountEl.textContent = discrepancy;
            
            // Apply status styling
            if (discrepancy === 0) {
                this.discrepancyCountEl.className = 'value status status--match';
            } else {
                this.discrepancyCountEl.className = 'value status status--discrepancy';
            }
        }

        this.showStep(4);
    }

    endSession() {
        this.currentSession.endTime = new Date();
        this.generateSessionReport();
        this.showStep(5);
    }

    generateSessionReport() {
        const duration = this.calculateDuration(this.currentSession.startTime, this.currentSession.endTime);
        const discrepancy = Math.abs(this.currentSession.cameraDetected - this.currentSession.cardsScanned);
        
        if (this.reportSessionIdEl) this.reportSessionIdEl.textContent = this.currentSession.sessionId;
        if (this.reportTeacherEl) this.reportTeacherEl.textContent = this.currentSession.teacher.name;
        if (this.reportClassEl) this.reportClassEl.textContent = this.currentSession.class;
        if (this.reportSubjectEl) this.reportSubjectEl.textContent = this.currentSession.subject;
        if (this.reportDurationEl) this.reportDurationEl.textContent = duration;
        if (this.reportAttendanceEl) this.reportAttendanceEl.textContent = this.currentSession.presentStudents.length;
        
        if (this.reportVerificationEl) {
            if (discrepancy === 0) {
                this.reportVerificationEl.textContent = 'Verified';
                this.reportVerificationEl.className = 'status status--success';
            } else {
                this.reportVerificationEl.textContent = `${discrepancy} Discrepancy Found`;
                this.reportVerificationEl.className = 'status status--warning';
            }
        }
    }

    calculateDuration(startTime, endTime) {
        const diff = endTime - startTime;
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minutes`;
    }

    generateSessionId() {
        const timestamp = Date.now().toString().slice(-6);
        return `SES${timestamp}`;
    }

    finishAndReturn() {
        // Add the completed session to the sample sessions
        const newSession = {
            sessionId: this.currentSession.sessionId,
            teacherId: this.currentSession.teacher.id,
            teacherName: this.currentSession.teacher.name,
            class: this.currentSession.class,
            subject: this.currentSession.subject,
            startTime: this.formatDateTime(this.currentSession.startTime),
            endTime: this.formatDateTime(this.currentSession.endTime),
            status: 'completed',
            attendanceCount: this.currentSession.presentStudents.length,
            cameraDetected: this.currentSession.cameraDetected,
            discrepancy: Math.abs(this.currentSession.cameraDetected - this.currentSession.cardsScanned)
        };

        // Add to beginning of array for most recent first
        this.data.sampleSessions.unshift(newSession);
        
        // Close modal and update dashboard
        this.closeSessionModal();
        this.updateDashboard();
        this.populateRecentSessions();
        
        // Show success message
        alert('Session completed successfully! Check the recent sessions table for details.');
    }

    formatDateTime(date) {
        return date.toISOString().slice(0, 19).replace('T', ' ');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing Attendance System...');
    new AttendanceSystem();
});