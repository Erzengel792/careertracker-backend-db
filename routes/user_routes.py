from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extension import db
from models import User, UserRole, StudentProfile, GraduateProfile

user_bp = Blueprint('user', __name__)

@user_bp.route('/set-account-type', methods=['POST'])
@jwt_required()
def set_account_type():
    data = request.get_json()
    current_user_id = int(get_jwt_identity())

    account_type = data.get('account_type')
    accept_policy = data.get('accept_policy')

    if not account_type or account_type not in ["student", "graduate"]:
        return jsonify({"status": "error", "message": "Invalid account type provided."}), 400

    if accept_policy is not True:
        return jsonify({"status": "error", "message": "You must accept the privacy policy."}), 400

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    # ✅ แปลง account_type ให้ตรงกับ UserRole
    user.role = UserRole[account_type]
    db.session.commit()

    # ✅ เช็คว่ามี Profile หรือยัง
    if user.role == UserRole.student:
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
        redirect_url = "/student-form" if not profile else "/dashboard"
    elif user.role == UserRole.graduate:
        profile = GraduateProfile.query.filter_by(user_id=user.id).first()
        redirect_url = "/graduate-form" if not profile else "/dashboard"

    return jsonify({
        "status": "success",
        "message": "Account type updated successfully.",
        "redirect": redirect_url
    }), 200

@user_bp.route('/check-account-type', methods=['GET'])
@jwt_required()
def check_account_type():
    current_user_id = int(get_jwt_identity())

    # ✅ ค้นหา user โดยใช้ user_id
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    # ✅ ถ้ายังเป็น `unassigned` แสดงว่ายังไม่ได้เลือก role → ส่ง Redirect ไป `/select-role`
    if user.role == UserRole.unassigned:
        return jsonify({
            "status": "success",
            "has_account_type": False,
            "message": "Account type not set",
            "redirect": "/select-role"
        }), 200

    # ✅ เช็คว่ามี `Profile` หรือยัง
    profile = None
    if user.role == UserRole.student:
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
    elif user.role == UserRole.graduate:
        profile = GraduateProfile.query.filter_by(user_id=user.id).first()

    # ✅ ถ้าไม่มี Profile ให้ Redirect ไปยังหน้ากรอกข้อมูล
    if not profile:
        redirect_url = "/student-form" if user.role == UserRole.student else "/graduate-form"
    else:
        redirect_url = "/dashboard"

    return jsonify({
        "status": "success",
        "has_account_type": True,
        "account_type": user.role.value,
        "redirect": redirect_url
    }), 200


