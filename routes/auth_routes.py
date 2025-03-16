from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from extension import db
from models import User, UserRole, StudentProfile, GraduateProfile
from datetime import datetime
bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email', '').strip().lower()  # ✅ Trim & lowercase email
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    # ✅ ตรวจสอบความยาว Password (ควรมีอย่างน้อย 6 ตัวอักษร)
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long."}), 400

    # ✅ ตรวจสอบว่า Email ซ้ำหรือไม่
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User with given email already exists."}), 400

    # ✅ Hash Password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # ✅ สร้าง User ใหม่ (กำหนด role เป็น unassigned)
    new_user = User(
        email=email,
        password_hash=hashed_password,
        role=UserRole.unassigned  # ยังไม่ได้เลือก role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully.",
        "user_id": new_user.id  # ✅ คืนค่า user_id ให้ Frontend
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    # ✅ ตรวจสอบ email โดยใช้ lowercase
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials."}), 401

    # ✅ อัปเดต last_login ให้ใช้ datetime.utcnow()
    user.last_login = datetime.utcnow()
    db.session.commit()

    # ✅ ใช้ user.id เป็น identity ใน JWT
    access_token = create_access_token(identity=str(user.id))

    response = jsonify({
        "message": "Login successful.",
        "token": access_token,
        "user_id": user.id,  # ✅ คืน user_id ให้ frontend ใช้ต่อ
        "role": user.role.value  # ✅ คืน role ให้ frontend ใช้
    })

    response.headers["X-Content-Type-Options"] = "nosniff"
    return response, 200
