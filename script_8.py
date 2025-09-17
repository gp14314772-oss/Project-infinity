# Create requirements file and installation/setup instructions

requirements_content = '''# Automated Attendance & Monitoring System - Requirements

# Core Python packages
Flask==2.3.3
opencv-python==4.8.1.78
numpy==1.24.3
sqlite3  # Built-in with Python

# For fingerprint scanner integration (when using real hardware)
# pyfingerprint==1.5

# For additional functionality
requests==2.31.0
Pillow==10.0.1

# For YOLO object detection (optional - for advanced person detection)
# ultralytics==8.0.200

# Development and testing
pytest==7.4.3
pytest-flask==1.2.0

# For production deployment
gunicorn==21.2.0
'''

setup_instructions = '''# Automated Attendance & Monitoring System
## Setup and Installation Instructions

### Prerequisites
- Python 3.8 or higher
- Raspberry Pi 4/5 (for hardware deployment)
- USB Fingerprint Scanner
- USB Card Reader
- USB Webcam

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd attendance-system
   
   # Or extract downloaded files
   unzip attendance-system.zip
   cd attendance-system
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python3 -c "from attendance_core import create_database; create_database()"
   ```

5. **Run the Application**
   ```bash
   # For development
   python3 app.py
   
   # For production
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

6. **Access the Web Interface**
   - Open browser and go to: `http://localhost:5000`
   - Or for network access: `http://YOUR_IP:5000`

### Hardware Setup (For Physical Deployment)

1. **Connect Hardware Components**
   - USB Fingerprint Scanner → Raspberry Pi USB port
   - USB Card Reader → Raspberry Pi USB port  
   - USB Webcam → Raspberry Pi USB port

2. **Configure Hardware Permissions**
   ```bash
   # Add user to required groups
   sudo usermod -a -G dialout,video $USER
   
   # Set up udev rules for hardware access
   sudo nano /etc/udev/rules.d/99-attendance-hardware.rules
   ```

3. **Install Hardware-Specific Libraries**
   ```bash
   # For fingerprint scanner
   pip install pyfingerprint
   
   # For advanced camera features
   pip install ultralytics
   ```

### File Structure
```
attendance-system/
├── app.py                 # Flask web application
├── attendance_core.py     # Core system logic
├── hardware_manager.py    # Hardware interface
├── attendance_system.db   # SQLite database
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   └── session_detail.html
├── static/              # Static assets
│   ├── css/style.css
│   └── js/app.js
└── README.md           # This file
```

### Configuration

1. **Database Configuration**
   - Default: SQLite database (`attendance_system.db`)
   - For production: Consider PostgreSQL or MySQL

2. **Hardware Configuration**
   - Edit hardware settings in `hardware_manager.py`
   - Adjust detection thresholds as needed

3. **Security Configuration**
   - Change default Flask secret key
   - Set up proper authentication for production
   - Configure firewall rules

### Usage

1. **Starting a Session**
   - Teacher scans fingerprint
   - System creates new session
   - Students scan ID cards
   - Camera verifies student count

2. **Ending a Session**
   - Teacher scans fingerprint again
   - System generates attendance report
   - Data saved to database

3. **Viewing Reports**
   - Access web dashboard
   - View session details
   - Export attendance data

### Troubleshooting

1. **Hardware Issues**
   - Check USB connections
   - Verify device permissions
   - Test hardware individually

2. **Software Issues**
   - Check Python version compatibility
   - Verify all dependencies installed
   - Check database permissions

3. **Network Issues**
   - Verify port 5000 is open
   - Check firewall settings
   - Test local vs network access

### Support and Maintenance

- Regular database backups
- Monitor system logs
- Update dependencies periodically
- Test hardware components regularly

For technical support, refer to the project documentation or contact the development team.
'''

# Create additional template files
teachers_template = '''{% extends "base.html" %}

{% block title %}Teachers Management{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1><i class="fas fa-chalkboard-teacher"></i> Teachers Management</h1>
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addTeacherModal">
                <i class="fas fa-plus"></i> Add Teacher
            </button>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">Registered Teachers</h5>
            </div>
            <div class="card-body">
                {% if teachers %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Teacher ID</th>
                                <th>Name</th>
                                <th>Fingerprint Status</th>
                                <th>Registration Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for teacher in teachers %}
                            <tr>
                                <td><code>{{ teacher[1] }}</code></td>
                                <td>{{ teacher[2] }}</td>
                                <td>
                                    {% if teacher[3] %}
                                    <span class="badge bg-success">Registered</span>
                                    {% else %}
                                    <span class="badge bg-warning">Pending</span>
                                    {% endif %}
                                </td>
                                <td>{{ teacher[4] }}</td>
                                <td>
                                    <button class="btn btn-sm btn-outline-secondary">
                                        <i class="fas fa-edit"></i> Edit
                                    </button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="text-center py-4">
                    <i class="fas fa-user-plus fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No teachers registered yet.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

sessions_template = '''{% extends "base.html" %}

{% block title %}Sessions History{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="mb-4">
            <i class="fas fa-calendar-alt"></i> Sessions History
        </h1>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">All Sessions</h5>
            </div>
            <div class="card-body">
                {% if sessions %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Session ID</th>
                                <th>Teacher</th>
                                <th>Class</th>
                                <th>Subject</th>
                                <th>Start Time</th>
                                <th>End Time</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for session in sessions %}
                            <tr>
                                <td><code>{{ session[1][:8] }}...</code></td>
                                <td>{{ session[-1] }}</td>
                                <td><span class="badge bg-secondary">{{ session[3] }}</span></td>
                                <td>{{ session[4] }}</td>
                                <td>{{ session[5] }}</td>
                                <td>{{ session[6] if session[6] else 'In Progress' }}</td>
                                <td>
                                    {% if session[7] == 'active' %}
                                    <span class="badge bg-warning">Active</span>
                                    {% else %}
                                    <span class="badge bg-success">Completed</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <a href="{{ url_for('session_detail', session_id=session[1]) }}" 
                                       class="btn btn-sm btn-outline-primary">
                                        <i class="fas fa-eye"></i> View
                                    </a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="text-center py-4">
                    <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No sessions found.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

# Save files
with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

with open('README.md', 'w') as f:
    f.write(setup_instructions)

with open('templates/teachers.html', 'w') as f:
    f.write(teachers_template)

with open('templates/sessions.html', 'w') as f:
    f.write(sessions_template)

print("Additional files created:")
print("- requirements.txt")
print("- README.md")
print("- templates/teachers.html") 
print("- templates/sessions.html")