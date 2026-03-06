import MySQLdb

try:
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='9876'
    )
    cursor = conn.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS emp")
    cursor.execute("USE emp")
    
    with open('schema.sql', 'r') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Error: {e}")
    
    conn.commit()
    print("Database setup successful!")
    
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
    print("Please update MYSQL_PASSWORD in config.py with your MySQL root password")
finally:
    if 'conn' in locals():
        conn.close()
