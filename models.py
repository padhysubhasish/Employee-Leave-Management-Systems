from werkzeug.security import generate_password_hash, check_password_hash
from database import mysql

class User:
    @staticmethod
    def create(name, email, password, role, department):
        hashed_password = generate_password_hash(password)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role, department, vacation_balance, sick_balance) VALUES (%s, %s, %s, %s, %s, 20, 10)",
            (name, email, hashed_password, role, department)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    @staticmethod
    def find_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        return dict(user) if user else None

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def get_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return dict(user) if user else None

    @staticmethod
    def update_balance(user_id, vacation_balance, sick_balance):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE users SET vacation_balance = %s, sick_balance = %s WHERE id = %s",
            (vacation_balance, sick_balance, user_id)
        )
        mysql.connection.commit()
        cursor.close()

class Leave:
    @staticmethod
    def create(user_id, leave_type, start_date, end_date, reason):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO leaves (user_id, leave_type, start_date, end_date, reason, status) VALUES (%s, %s, %s, %s, %s, 'pending')",
            (user_id, leave_type, start_date, end_date, reason)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    @staticmethod
    def get_by_user(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM leaves WHERE user_id = %s ORDER BY submitted_at DESC", (user_id,))
        leaves = cursor.fetchall()
        cursor.close()
        return [dict(leave) for leave in leaves]

    @staticmethod
    def get_all_pending():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT l.*, u.name, u.email, u.department 
            FROM leaves l 
            JOIN users u ON l.user_id = u.id 
            WHERE l.status = 'pending' 
            ORDER BY l.submitted_at DESC
        """)
        leaves = cursor.fetchall()
        cursor.close()
        return [dict(leave) for leave in leaves]

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT l.*, u.name, u.email, u.department 
            FROM leaves l 
            JOIN users u ON l.user_id = u.id 
            ORDER BY l.submitted_at DESC
        """)
        leaves = cursor.fetchall()
        cursor.close()
        return [dict(leave) for leave in leaves]

    @staticmethod
    def update_status(leave_id, status, comment):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE leaves SET status = %s, manager_comment = %s WHERE id = %s",
            (status, comment, leave_id)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_id(leave_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM leaves WHERE id = %s", (leave_id,))
        leave = cursor.fetchone()
        cursor.close()
        return dict(leave) if leave else None

    @staticmethod
    def get_approved_leaves():
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT l.*, u.name 
            FROM leaves l 
            JOIN users u ON l.user_id = u.id 
            WHERE l.status = 'approved' 
            ORDER BY l.start_date
        """)
        leaves = cursor.fetchall()
        cursor.close()
        return [dict(leave) for leave in leaves]
