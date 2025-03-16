import enum
from datetime import datetime
from extension import db

class UserRole(enum.Enum):
    unassigned = "unassigned"
    student = "student"
    graduate = "graduate"
    admin = "admin"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.unassigned)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    student_profile = db.relationship('StudentProfile', backref='users', uselist=False)
    graduate_profile = db.relationship('GraduateProfile', backref='users', uselist=False)

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    faculty = db.Column(db.String(100))
    major = db.Column(db.String(100))
    year_of_enrollment = db.Column(db.Date)
    current_academic_year = db.Column(db.String(20))
    extracurricular_activities = db.Column(db.Text)
    academic_projects = db.Column(db.Text)
    profile_image = db.Column(db.String(255))

class GraduateProfile(db.Model):
    __tablename__ = 'graduate_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    faculty = db.Column(db.String(100))
    major = db.Column(db.String(100))
    year_of_enrollment = db.Column(db.Date)
    current_academic_year = db.Column(db.String(20))
    extracurricular_activities = db.Column(db.Text)
    academic_projects = db.Column(db.Text)
    profile_image = db.Column(db.String(255))

    internship_status = db.Column(db.String(20))
    internship_company = db.Column(db.String(100))
    internship_position = db.Column(db.String(100))
    internship_duration = db.Column(db.String(50))
    internship_task = db.Column(db.Text)
    internship_experience = db.Column(db.Text)

    career_status = db.Column(db.String(20))
    career_company = db.Column(db.String(100))
    career_position = db.Column(db.String(100))
    date_of_employment = db.Column(db.Date)
    career_task = db.Column(db.Text)
    career_experience = db.Column(db.Text)

class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    degree = db.Column(db.String(100))
    institution = db.Column(db.String(255))
    major = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

class CareerRecord(db.Model):
    __tablename__ = 'career_records'

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
