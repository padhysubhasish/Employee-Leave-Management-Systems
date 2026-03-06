# Leave Management System

A Flask-based web application for managing employee leave requests with role-based access for employees and managers.

## Features

- User authentication (Login/Register)
- Employee dashboard for leave requests
- Manager dashboard for approving/rejecting leaves
- Leave history tracking
- MySQL database backend

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

### 1. Clone or Navigate to Project Directory

```bash
cd c:\Users\priya\OneDrive\Desktop\code\Employee
```

### 2. Install Python Dependencies

```bash
pip install -r leave_management_system/requirements.txt
```

### 3. Configure MySQL Database

1. Start your MySQL server
2. Update the MySQL password in `leave_management_system/config.py`:
   ```python
   MYSQL_PASSWORD = 'your_mysql_password'
   ```

### 4. Setup Database

Run the database setup script:

```bash
cd leave_management_system
python setup_db.py
```

This will create the `leave_management` database and required tables.

## Running the Application

### Start the Flask Server

```bash
cd leave_management_system
python app.py
```

The application will start on `http://localhost:5000`

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

### For Employees:
1. Register a new account
2. Login with your credentials
3. Submit leave requests
4. View leave history

### For Managers:
1. Login with manager credentials
2. View pending leave requests
3. Approve or reject employee leaves
4. Monitor team leave status

## Project Structure

```
Employee/
└── leave_management_system/
    ├── routes/              # Route handlers
    │   ├── auth.py         # Authentication routes
    │   ├── employee.py     # Employee routes
    │   └── manager.py      # Manager routes
    ├── static/             # Static files
    │   ├── css/
    │   └── js/
    ├── templates/          # HTML templates
    ├── app.py             # Main application
    ├── config.py          # Configuration
    ├── database.py        # Database initialization
    ├── models.py          # Data models
    ├── setup_db.py        # Database setup script
    └── requirements.txt   # Python dependencies
```

## Configuration

Edit `leave_management_system/config.py` to customize:
- Secret key
- MySQL host
- MySQL user
- MySQL password
- Database name

## Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Verify credentials in `config.py`
- Check if port 3306 is not blocked

### Module Not Found Error
```bash
pip install -r leave_management_system/requirements.txt
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Security Notes

- Change `SECRET_KEY` in production
- Never commit passwords to version control
- Use environment variables for sensitive data

## License

This project is for educational purposes.
