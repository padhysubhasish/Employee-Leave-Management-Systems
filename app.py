from flask import Flask
from config import Config
from database import init_db
from routes.auth import auth_bp
from routes.employee import employee_bp
from routes.manager import manager_bp

app = Flask(__name__)
app.config.from_object(Config)

init_db(app)

app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(manager_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
