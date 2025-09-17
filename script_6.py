# Create HTML templates for the web interface

# Create templates directory structure
import os
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Base template
base_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Automated Attendance System{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('dashboard') }}">
                <i class="fas fa-users"></i> Attendance System
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('dashboard') }}">
                            <i class="fas fa-home"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('teachers') }}">
                            <i class="fas fa-chalkboard-teacher"></i> Teachers
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('students') }}">
                            <i class="fas fa-user-graduate"></i> Students
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('sessions') }}">
                            <i class="fas fa-calendar-alt"></i> Sessions
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>'''

# Dashboard template
dashboard_template = '''{% extends "base.html" %}

{% block title %}Dashboard - Attendance System{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="mb-4">
            <i class="fas fa-tachometer-alt"></i> Dashboard
        </h1>
    </div>
</div>

<div class="row mb-4">
    <div class="col-md-4">
        <div class="card bg-primary text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ stats.total_teachers }}</h4>
                        <p class="mb-0">Total Teachers</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-chalkboard-teacher fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-success text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ stats.total_students }}</h4>
                        <p class="mb-0">Total Students</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-user-graduate fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-info text-white">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h4>{{ stats.recent_sessions }}</h4>
                        <p class="mb-0">Recent Sessions</p>
                    </div>
                    <div class="align-self-center">
                        <i class="fas fa-calendar-alt fa-2x"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-clock"></i> Recent Sessions
                </h5>
            </div>
            <div class="card-body">
                {% if recent_sessions %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Session ID</th>
                                <th>Teacher</th>
                                <th>Class</th>
                                <th>Subject</th>
                                <th>Start Time</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for session in recent_sessions %}
                            <tr>
                                <td><code>{{ session[1][:8] }}...</code></td>
                                <td>{{ session[-1] }}</td>
                                <td><span class="badge bg-secondary">{{ session[3] }}</span></td>
                                <td>{{ session[4] }}</td>
                                <td>{{ session[5] }}</td>
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
                    <p class="text-muted">No recent sessions found.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

# Session detail template
session_detail_template = '''{% extends "base.html" %}

{% block title %}Session Details - {{ session[1][:8] }}{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>
                <i class="fas fa-calendar-alt"></i> Session Details
            </h1>
            <a href="{{ url_for('sessions') }}" class="btn btn-secondary">
                <i class="fas fa-arrow-left"></i> Back to Sessions
            </a>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-info-circle"></i> Session Information
                </h5>
            </div>
            <div class="card-body">
                <table class="table table-borderless">
                    <tr>
                        <th width="200">Session ID:</th>
                        <td><code>{{ session[1] }}</code></td>
                    </tr>
                    <tr>
                        <th>Teacher:</th>
                        <td>{{ session[-1] }} ({{ session[2] }})</td>
                    </tr>
                    <tr>
                        <th>Class:</th>
                        <td><span class="badge bg-secondary">{{ session[3] }}</span></td>
                    </tr>
                    <tr>
                        <th>Subject:</th>
                        <td>{{ session[4] }}</td>
                    </tr>
                    <tr>
                        <th>Start Time:</th>
                        <td>{{ session[5] }}</td>
                    </tr>
                    <tr>
                        <th>End Time:</th>
                        <td>{{ session[6] if session[6] else 'In Progress' }}</td>
                    </tr>
                    <tr>
                        <th>Status:</th>
                        <td>
                            {% if session[7] == 'active' %}
                            <span class="badge bg-warning">Active</span>
                            {% else %}
                            <span class="badge bg-success">Completed</span>
                            {% endif %}
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-chart-bar"></i> Verification Status
                </h5>
            </div>
            <div class="card-body text-center">
                {% if camera_log %}
                <div class="mb-3">
                    <h3 class="text-primary">{{ camera_log[2] }}</h3>
                    <p class="text-muted mb-0">Camera Detected</p>
                </div>
                <div class="mb-3">
                    <h3 class="text-info">{{ camera_log[3] }}</h3>
                    <p class="text-muted mb-0">Card Scans</p>
                </div>
                <div class="mb-3">
                    {% if discrepancy == 0 %}
                    <span class="badge bg-success fs-6">
                        <i class="fas fa-check"></i> Verified
                    </span>
                    {% else %}
                    <span class="badge bg-warning fs-6">
                        <i class="fas fa-exclamation-triangle"></i> {{ discrepancy }} Discrepancy
                    </span>
                    {% endif %}
                </div>
                {% else %}
                <p class="text-muted">No verification data available</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="card-title mb-0">
                    <i class="fas fa-users"></i> Attendance Records ({{ total_present }} Present)
                </h5>
            </div>
            <div class="card-body">
                {% if attendance %}
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Student Name</th>
                                <th>Student ID</th>
                                <th>Class</th>
                                <th>Card Scan Time</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for record in attendance %}
                            <tr>
                                <td>{{ loop.index }}</td>
                                <td>{{ record[7] }}</td>
                                <td><code>{{ record[2] }}</code></td>
                                <td><span class="badge bg-secondary">{{ record[8] }}</span></td>
                                <td>{{ record[3] }}</td>
                                <td><span class="badge bg-success">Present</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <div class="text-center py-4">
                    <i class="fas fa-user-times fa-3x text-muted mb-3"></i>
                    <p class="text-muted">No attendance records found for this session.</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

# Save templates
with open('templates/base.html', 'w') as f:
    f.write(base_template)

with open('templates/dashboard.html', 'w') as f:
    f.write(dashboard_template)

with open('templates/session_detail.html', 'w') as f:
    f.write(session_detail_template)

print("HTML templates created:")
print("- templates/base.html")
print("- templates/dashboard.html") 
print("- templates/session_detail.html")