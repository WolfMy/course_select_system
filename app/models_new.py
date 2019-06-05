from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login

@login.user_loader
def load_user(Num):
    if len(Num) == 8:
        return Student.query.get(int(Num))
    elif len(Num) == 4:
        return Teacher.query.get(int(Num))
    elif len(Num) == 3:
        return Manager.query.get(int(Num))
    else:
        pass

class Dept(db.Model):
    # 学院
    DeptNum = db.Column(db.String(4), primary_key=True)
    DeptName = db.Column(db.String(10), nullable=False)
    DeptChairman = db.Column(db.String(10), nullable=False)
    DeptTel = db.Column(db.String(11))
    DeptDesc = db.Column(db.Text)
    Teachers = db.relationship('Teacher', backref='dept', lazy='dynamic')
    Majors = db.relationship('Major', backref='dept', lazy='dynamic')
    Courses = db.relationship('Course', backref='dept', lazy='dynamic')

class Major(db.Model):
    # 专业
    MajorNum = db.Column(db.String(6), primary_key=True)
    DeptNum = db.Column(db.String(4), db.ForeignKey('dept.DeptNum'), nullable=False)
    MajorName = db.Column(db.String(10), nullable=False)
    MajorAssistant = db.Column(db.String(10), nullable=False)
    MajorTel = db.Column(db.String(11))
    MajorDesc = db.Column(db.Text)
    Students = db.relationship('Student', backref='major', lazy='dynamic')
    TrainingProgram = db.Column(db.String(7))

class Course_select_table(db.Model):
    __tablename__ = "course_select_table"
    StudentNum = db.Column(db.String(8), db.ForeignKey('student.StudentNum'), primary_key=True, nullable=False)
    CourseNum = db.Column(db.String(10), db.ForeignKey('course.CourseNum'), primary_key=True, nullable=False)
    TeacherNum = db.Column(db.String(8), db.ForeignKey('teacher.TeacherNum'), primary_key=True, nullable=False)
    Grade = db.Column(db.Integer)

    def __init__(self, StudentNum, CourseNum, TeacherNum):
        self.StudentNum = StudentNum
        self.CourseNum = CourseNum
        self.TeacherNum = TeacherNum
        
    def input_grade(self, grade):   
        self.Grade = grade

class Course_Teacher(db.Model):
    __tablename__ = "course_teacher"
    CourseNum = db.Column(db.String(8), db.ForeignKey('course.CourseNum'), primary_key=True, nullable=False)
    TeacherNum = db.Column(db.String(10), db.ForeignKey('teacher.TeacherNum'), primary_key=True, nullable=False)
    #Time = db.Column(db.Text)
    CourseCapacity = db.Column(db.Integer, nullable=False)

    def __init__(self, CourseNum, TeacherNum, CourseCapacity):
        self.CourseNum = CourseNum
        self.TeacherNum = TeacherNum
        self.CourseCapacity = CourseCapacity

class Teacher(UserMixin, db.Model):
    # 教师
    TeacherNum = db.Column(db.String(8), primary_key=True)
    DeptNum = db.Column(db.String(4), db.ForeignKey('dept.DeptNum'), nullable=False)
    TeacherName = db.Column(db.String(10), nullable=False)
    TeacherSex = db.Column(db.String(2), nullable=False)
    TeacherInyear = db.Column(db.String(4), nullable=False)
    TeacherTitle = db.Column(db.String(10))
    TeacherPassword = db.Column(db.Text, nullable=False)
    Students = db.relationship('Student', secondary='course_select_table', backref='teacher', lazy='dynamic')
    Courses = db.relationship('Course', secondary='course_teacher', backref='teacher', lazy='dynamic')

    def __init__(self, TeacherNum, DeptNum, TeacherName, TeacherSex, TeacherInyear, TeacherTitle):
        self.TeacherNum = TeacherNum
        self.DeptNum = DeptNum
        self.TeacherName = TeacherName
        self.TeacherSex = TeacherSex
        self.TeacherInyear = TeacherInyear
        self.TeacherTitle = TeacherTitle
        self.set_password('admin')

    # override
    def get_id(self):
        return self.TeacherNum
    def set_password(self, password):
        self.TeacherPassword = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.TeacherPassword, password)

class Student(UserMixin, db.Model):
    # 学生
    StudentNum = db.Column(db.String(8), primary_key=True)
    MajorNum = db.Column(db.String(16), db.ForeignKey('major.MajorNum'), nullable=False)
    StudentName = db.Column(db.String(10), nullable=False)
    StudentSex = db.Column(db.String(10), nullable=False)
    StudentInyear = db.Column(db.String(4), nullable=False)
    StudengtPassword = db.Column(db.Text, nullable=False)
    Courses = db.relationship('Course', secondary='course_select_table', backref='student', lazy='dynamic')

    def __init__(self, StudentNum, MajorNum, StudentName, StudentSex, StudentInyear):
        self.StudentNum = StudentNum
        self.MajorNum = MajorNum
        self.StudentName = StudentName
        self.StudentSex = StudentSex
        self.StudentInyear = StudentInyear
        self.set_password('admin')

    # override
    def get_id(self):
        return self.StudentNum
    def set_password(self, password):
        self.StudengtPassword = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.StudengtPassword, password)
    def drop_course(self, CourseNum):
        course_drop = [course for course in self.Courses if course.CourseNum==CourseNum][0]
        self.Courses.remove(course_drop)

class Course(db.Model):
    # 课程
    CourseNum = db.Column(db.String(8), primary_key=True)
    CourseName = db.Column(db.String(10), nullable=False)
    CourseCredit = db.Column(db.Integer, nullable=False)
    CourseTime = db.Column(db.Integer, nullable=False)
    CourseDesc = db.Column(db.Text)
    Teachers = db.relationship('Teacher', secondary='course_teacher', backref='course', lazy='dynamic') 
    DeptNum = db.Column(db.String(4), db.ForeignKey('dept.DeptNum'), nullable=False)

    def __init__(self, CourseNum, CourseName, CourseCredit, CourseTime, DeptNum, CourseDesc):
        self.CourseNum = CourseNum
        self.CourseName = CourseName
        self.CourseCredit = CourseCredit
        self.CourseTime = CourseTime
        self.DeptNum = DeptNum
        self.CourseDesc = CourseDesc
       

class Manager(UserMixin, db.Model):
    # 管理员
    ManagerNum = db.Column(db.String(8), primary_key=True)
    ManagerName = db.Column(db.String(10), nullable=False)
    ManagerSex = db.Column(db.String(2), nullable=False)
    ManagerBirthday = db.Column(db.DateTime)
    ManagerPassword = db.Column(db.Text, nullable=False)
    ManagerPermission = db.Column(db.Integer, nullable=False)

    # override
    def get_id(self):
        return self.ManagerNum
    def set_password(self, password):
        self.ManagerPassword = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.ManagerPassword, password)

class TrainingProgram(db.Model):
    # 培养计划
    TPNumber = db.Column(db.String(7), primary_key=True)