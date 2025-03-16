from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
from extension import db
from models import User,UserRole,StudentProfile, GraduateProfile
from config import Config
import uuid
from datetime import datetime

data_bp = Blueprint('data', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_to_blob_storage(file):
    filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
    blob_client = blob_service_client.get_blob_client(container="profilepic", blob=filename)
    blob_client.upload_blob(file)
    return blob_client.url


@data_bp.route('/current-user', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # ค้นหา Profile โดยใช้ user_id
    if user.role == UserRole.student:
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
    elif user.role == UserRole.graduate:
        profile = GraduateProfile.query.filter_by(user_id=user.id).first()
    else:
        return jsonify({"status": "error", "message": "User role not assigned."}), 400

    if not profile:
        return jsonify({"status": "error", "message": "Profile not found."}), 404

    # เพิ่มข้อมูล faculty และ major ลงในผลลัพธ์
    result = {
        "full_name": profile.full_name,
        "email": user.email,
        "profile_image": profile.profile_image,
        "faculty": profile.faculty,
        "major": profile.major
    }

    return jsonify(result), 200





@data_bp.route('/student-data', methods=['GET'])
def get_student_data():
    students = StudentProfile.query.all()
    result = [{
        "full_name": student.full_name,
        "faculty": student.faculty,
        "major": student.major,
        "profile_image": student.profile_image if student.profile_image else None,
        "extracurricular_activities": student.extracurricular_activities,
        "academic_projects": student.academic_projects
    } for student in students]

    return jsonify(result), 200


@data_bp.route('/graduate-data', methods=['GET'])
def get_graduate_data():
    graduates = GraduateProfile.query.all()
    result = [{
        "full_name": grad.full_name,
        "faculty": grad.faculty,
        "major": grad.major,
        "profile_image": grad.profile_image if grad.profile_image else None,
        "extracurricular_activities": grad.extracurricular_activities,
        "academic_projects": grad.academic_projects,
        "internship_status": grad.internship_status,
        "internship_company": grad.internship_company,
        "internship_position": grad.internship_position,
        "internship_duration": grad.internship_duration,
        "internship_task": grad.internship_task,
        "internship_experience": grad.internship_experience,
        "career_status": grad.career_status,
        "career_company": grad.career_company,
        "career_position": grad.career_position,
        "date_of_employment": grad.date_of_employment.isoformat() if grad.date_of_employment else None,
        "career_task": grad.career_task,
        "career_experience": grad.career_experience
    } for grad in graduates]

    return jsonify(result), 200


@data_bp.route('/graduates', methods=['GET'])
def get_graduates_by_faculty():
    faculty = request.args.get('faculty')

    if not faculty:
        return jsonify({"status": "error", "message": "Faculty is required"}), 400

    graduates = GraduateProfile.query.filter_by(faculty=faculty).all()

    result = [{
        "full_name": grad.full_name,
        "faculty": grad.faculty,
        "major": grad.major,
        "profile_image": grad.profile_image if grad.profile_image else None,
        "extracurricular_activities": grad.extracurricular_activities,
        "academic_projects": grad.academic_projects,
        "internship_status": grad.internship_status,
        "internship_company": grad.internship_company,
        "internship_position": grad.internship_position,
        "internship_duration": grad.internship_duration,
        "internship_task": grad.internship_task,
        "internship_experience": grad.internship_experience,
        "career_status": grad.career_status,
        "career_company": grad.career_company,
        "career_position": grad.career_position,
        "date_of_employment": grad.date_of_employment.isoformat() if grad.date_of_employment else None,
        "career_task": grad.career_task,
        "career_experience": grad.career_experience
    } for grad in graduates]

    return jsonify(result), 200


@data_bp.route('/faculties', methods=['GET'])
def get_faculties():
    faculties = db.session.query(GraduateProfile.faculty).distinct().all()
    faculties_list = [faculty[0] for faculty in faculties]

    return jsonify(faculties_list), 200

@data_bp.route('/graduates-by-company', methods=['GET'])
def get_graduates_by_company():
    company_name = request.args.get('company', '').strip()

    if not company_name:
        return jsonify({"status": "error", "message": "Company name is required"}), 400

    graduates = GraduateProfile.query.filter_by(career_company=company_name).all()
    results = [{
        "full_name": grad.full_name,
        "faculty": grad.faculty,
        "major": grad.major,
        "profile_image": grad.profile_image if grad.profile_image else None,
        "extracurricular_activities": grad.extracurricular_activities,
        "academic_projects": grad.academic_projects,
        "internship_status": grad.internship_status,
        "internship_company": grad.internship_company,
        "internship_position": grad.internship_position,
        "internship_duration": grad.internship_duration,
        "internship_task": grad.internship_task,
        "internship_experience": grad.internship_experience,
        "career_status": grad.career_status,
        "career_company": grad.career_company,
        "career_position": grad.career_position,
        "date_of_employment": grad.date_of_employment.isoformat() if grad.date_of_employment else None,
        "career_task": grad.career_task,
        "career_experience": grad.career_experience
    } for grad in graduates]

    return jsonify(results), 200

@data_bp.route('/companies', methods=['GET'])
def get_companies():
    try:
        companies = db.session.query(GraduateProfile.career_company).filter(GraduateProfile.career_company.isnot(None)).distinct().all()
        companies_list = [company[0] for company in companies if company[0]]
        return jsonify(companies_list), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/careers', methods=['GET'])
def get_careers():
    try:
        careers = db.session.query(GraduateProfile.career_position).filter(GraduateProfile.career_position.isnot(None)).distinct().all()
        careers_list = [career[0] for career in careers if career[0]]
        return jsonify(careers_list), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@data_bp.route('/graduates-by-career', methods=['GET'])
def get_graduates_by_career():
    career_name = request.args.get('career', '').strip()

    if not career_name:
        return jsonify({"status": "error", "message": "Career name is required"}), 400

    graduates = GraduateProfile.query.filter_by(career_position=career_name).all()
    results = [{
        "full_name": grad.full_name,
        "faculty": grad.faculty,
        "major": grad.major,
        "profile_image": grad.profile_image if grad.profile_image else None,
        "extracurricular_activities": grad.extracurricular_activities,
        "academic_projects": grad.academic_projects,
        "internship_status": grad.internship_status,
        "internship_company": grad.internship_company,
        "internship_position": grad.internship_position,
        "internship_duration": grad.internship_duration,
        "internship_task": grad.internship_task,
        "internship_experience": grad.internship_experience,
        "career_status": grad.career_status,
        "career_company": grad.career_company,
        "career_position": grad.career_position,
        "date_of_employment": grad.date_of_employment.isoformat() if grad.date_of_employment else None,
        "career_task": grad.career_task,
        "career_experience": grad.career_experience
    } for grad in graduates]

    return jsonify(results), 200



@data_bp.route('/student-form', methods=['POST'])
@jwt_required()
def add_student():
    current_user_id = get_jwt_identity()  # ใช้ user_id
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    data = request.form.to_dict()

    if 'profileImage' in request.files:
        image = request.files['profileImage']
        if image and allowed_file(image.filename):
            image_url = upload_to_blob_storage(image)
        else:
            return jsonify({"status": "error", "message": "Invalid image file."}), 400
    else:
        image_url = None

    # แปลงข้อมูลวันที่ให้เป็น date object
    date_of_birth_str = data.get('dateOfBirth', '')
    year_of_enrollment_str = data.get('yearOfEnrollment', '')

    try:
        date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date() if date_of_birth_str else None
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format for dateOfBirth"}), 400

    try:
        year_of_enrollment = datetime.strptime(year_of_enrollment_str, "%Y-%m-%d").date() if year_of_enrollment_str else None
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format for yearOfEnrollment"}), 400

    student = StudentProfile(
        user_id=user.id,  # ใช้ user_id เชื่อมโยงกับ User
        full_name=data.get('full_name'),
        student_id=data.get('studentId'),
        gender=data.get('gender'),
        date_of_birth=date_of_birth,
        email=user.email,  # ใช้ email จาก User
        phone_number=data.get('phoneNumber'),
        faculty=data.get('faculty'),
        major=data.get('major'),
        year_of_enrollment=year_of_enrollment,
        current_academic_year=data.get('currentAcademicYear'),
        extracurricular_activities=data.get('extracurricularActivities'),
        academic_projects=data.get('academicProjects'),
        profile_image=image_url
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"status": "success", "message": "Student profile created successfully"}), 201




@data_bp.route('/graduate-form', methods=['POST'])
@jwt_required()
def add_graduate():
    current_user_id = get_jwt_identity()  # ใช้ user_id
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    data = request.form.to_dict()

    if 'profileImage' in request.files:
        image = request.files['profileImage']
        if image and allowed_file(image.filename):
            image_url = upload_to_blob_storage(image)
        else:
            return jsonify({"status": "error", "message": "Invalid file type"}), 400
    else:
        image_url = None

    # แปลงข้อมูลวันที่ให้เป็น date object
    date_of_birth_str = data.get('dateOfBirth', '')
    year_of_enrollment_str = data.get('yearOfEnrollment', '')
    date_of_employment_str = data.get('dateOfEmployment', '')

    try:
        date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date() if date_of_birth_str else None
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format for dateOfBirth"}), 400

    try:
        year_of_enrollment = datetime.strptime(year_of_enrollment_str, "%Y-%m-%d").date() if year_of_enrollment_str else None
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format for yearOfEnrollment"}), 400

    try:
        date_of_employment = datetime.strptime(date_of_employment_str, "%Y-%m-%d").date() if date_of_employment_str else None
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid date format for dateOfEmployment"}), 400

    graduate = GraduateProfile(
        user_id=user.id,  # ใช้ user_id เชื่อมโยงกับ User
        full_name=data.get('full_name'),  # ใช้ full_name ที่ถูกส่งมาจาก Frontend
        student_id=data.get('studentId'),
        gender=data.get('gender'),
        date_of_birth=date_of_birth,
        email=user.email,  # ใช้ email จาก User
        phone_number=data.get('phoneNumber'),
        faculty=data.get('faculty'),
        major=data.get('major'),
        year_of_enrollment=year_of_enrollment,
        current_academic_year=data.get('currentAcademicYear'),
        extracurricular_activities=data.get('extracurricularActivities'),
        academic_projects=data.get('academicProjects'),
        profile_image=image_url,

        # เช็คสถานะ Internship ก่อนบันทึกข้อมูล
        internship_status=data.get('internshipStatus'),
        internship_company=data.get('internshipCompany') if data.get('internshipStatus') == "completed" else None,
        internship_position=data.get('internshipPosition') if data.get('internshipStatus') == "completed" else None,
        internship_duration=data.get('internshipDuration') if data.get('internshipStatus') == "completed" else None,
        internship_task=data.get('internshipTask') if data.get('internshipStatus') == "completed" else None,
        internship_experience=data.get('internshipExperience') if data.get('internshipStatus') == "completed" else None,

        # เช็คสถานะ Career ก่อนบันทึกข้อมูล
        career_status=data.get('careerStatus'),
        career_company=data.get('careerCompany') if data.get('careerStatus') == "employed" else None,
        career_position=data.get('careerPosition') if data.get('careerStatus') == "employed" else None,
        date_of_employment=date_of_employment,
        career_task=data.get('careerTask') if data.get('careerStatus') == "employed" else None,
        career_experience=data.get('careerExperience') if data.get('careerStatus') == "employed" else None
    )

    db.session.add(graduate)
    db.session.commit()

    return jsonify({"status": "success", "message": "Graduate profile created successfully"}), 201


