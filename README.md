# MyOKR - Goal Management System

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A modern, comprehensive OKR (Objectives and Key Results) management system built with Flask. Track, manage, and analyze your organization's goals with beautiful visualizations and intuitive interfaces.

## 🚀 Live Demo

**🌐 [https://myokr-goal-management.vercel.app/](https://myokr-goal-management.vercel.app/)**

### Demo Login Credentials
- **Admin**: `admin@example.com` / `admin123`
- **Team Lead**: `john.doe@example.com` / `password123`
- **Developer**: `jane.smith@example.com` / `password123`

## ✨ Features

### 🎯 **Core OKR Management**
- Create & edit objectives with measurable key results
- Real-time progress tracking and calculations
- Status management (Active, Completed, Paused, Cancelled, Archived)
- Priority levels and team assignment
- Due date tracking and overdue monitoring

### 📊 **Advanced Analytics Dashboard**
- Interactive charts and real-time metrics
- Team performance comparison and rankings
- Timeline analysis and trend visualization
- Export capabilities and printable reports
- Executive summary reports with recommendations

### 👥 **User & Team Management**
- Role-based access control (Admin, Team Lead, User)
- Organization → Department → Team hierarchy
- User permissions and granular access control

### 🔧 **Technical Features**
- Responsive design (Bootstrap 5)
- Modern UI with custom styling
- SQLite database with Flask-SQLAlchemy
- Secure authentication with password hashing
- Form validation and CSRF protection

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Setup
```bash
# Clone the repository
git clone https://github.com/sharda1100/myokr-goal-management.git
cd myokr-goal-management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py

# Run the application
python run.py
```

Visit `http://localhost:5000` to access the application.

## 📁 Project Structure

```
myokr-goal-management/
├── app/
│   ├── forms/          # WTForms for user input
│   ├── models/         # SQLAlchemy database models
│   ├── routes/         # Flask route handlers
│   ├── static/         # CSS, JS, and images
│   └── templates/      # Jinja2 HTML templates
├── instance/           # SQLite database
├── config.py          # Application configuration
├── run.py             # Development server
├── wsgi.py            # Production WSGI entry point
├── init_db.py         # Database initialization
└── requirements.txt   # Python dependencies
```

## 🚀 Deployment

The application is deployed on Vercel and configured for serverless deployment.

### Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## 📊 Key Metrics

- **5 Sample OKRs** with different statuses and priorities
- **Multiple Teams** across Engineering, Marketing, and Sales
- **Real-time Analytics** with interactive charts
- **Role-based Access** for different user types
- **Responsive Design** for all devices

## 🔒 Security

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- SQL injection prevention with SQLAlchemy ORM
- XSS protection with Jinja2 auto-escaping
- Secure session management

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Sharda Kumari**
- GitHub: [@sharda1100](https://github.com/sharda1100)
- Repository: [myokr-goal-management](https://github.com/sharda1100/myokr-goal-management)

---

**Built with ❤️ using Flask, Bootstrap, and Chart.js**
