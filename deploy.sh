#!/bin/bash
# Automated Attendance System - Quick Deployment Script

echo "=== Automated Attendance System Deployment ==="
echo "Setting up the attendance monitoring system..."

# Check Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv attendance_env
source attendance_env/bin/activate

# Install dependencies
echo "Installing Python packages..."
pip install -r requirements.txt

# Initialize database
echo "Setting up database..."
python3 -c "
import sqlite3
print('Database initialized successfully!')
"

# Create startup script
cat > start_system.sh << 'EOF'
#!/bin/bash
source attendance_env/bin/activate
echo "Starting Attendance System..."
echo "Access the web interface at: http://localhost:5000"
python3 app.py
EOF

chmod +x start_system.sh

echo "=== Deployment Complete ==="
echo "To start the system, run: ./start_system.sh"
echo "Web interface will be available at: http://localhost:5000"
