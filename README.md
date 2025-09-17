# Automated Attendance & Monitoring System
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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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
