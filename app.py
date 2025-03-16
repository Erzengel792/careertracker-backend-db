from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from extension import db, migrate
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Database
db.init_app(app)
migrate.init_app(app, db)

# JWT Config
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour
app.config["JWT_COOKIE_SECURE"] = True 
app.config["JWT_COOKIE_SAMESITE"] = "None"

# Extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": "your_frontend_url", # ✅ ใส่ URL ของ frontend
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Import Blueprints หลังจาก JWTManager ถูกสร้างแล้ว
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.data_routes import data_bp

# Blueprint registration
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(data_bp, url_prefix='/data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
