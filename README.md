[TOC]

> 展示网站: <https://120.27.192.52:4070>
>
> 首先用管理员账户登陆（帐号admin，密码admin）
>
> 创建自己的8位学号，默认密码admin。
>
> 再用自己学号登陆选课系统进行体验。

##一、Python_Flask的初始化（Bootstrap框架、SQLalchemy的ORM框架、数据库迁移工具）

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from .config import Config

# create and configure the app
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import view, models_new
```



##二、选课系统关系模型的定义

在基础的属性定义外，还定义了各类之间的一对多关系，多对多关系，包括：

- 学院：教师 = 1:n
- 学院：专业 = 1:n
- 学院：课程 = 1:n
- 专业：学生 = 1:n
- 教师：课程 = m:n
- 学生：课程 = m:n

在教师与课程的多对多关系中，额外建立一张表，用于存储老师开设课程的具体属性：上课时间、课程容量等。

在教师、课程、学生这个三方多对多关系中，额外建立一张结联表。 

```python
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
```



## 三、登陆、登出模块

登陆验证时，首先从学生表中查找输入的学号，若无，再从教师表中去查找。管理员采用单独的登陆界面，用于区分。

密码验证采用flask的加盐哈希加密算法，无SQL注入风险，保证用户的信息安全。

在此基础上，添加了"记住我"的登陆选项。

![image-20190611213905119](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611213905119.png)

```python
@app.route('/login', methods=('GET', 'POST'))
def login():
    if isinstance(current_user._get_current_object(), Manager):
        logout_user()
    if current_user.is_authenticated:
        if isinstance(current_user._get_current_object(), Student):
            return redirect(url_for('student_index'))
        elif isinstance(current_user._get_current_object(), Teacher):
            return redirect(url_for('teacher_index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember')
        remember = [True if remember=='on' else False][0]
        error = None
        is_student = 1
        user = Student.query.filter_by(StudentNum=username).first()
        # 判断是否为学生
        if not user:
            # 若不是，则选取老师
            is_student = 0
            user = Teacher.query.filter_by(TeacherNum=username).first()
        if not user:
            error = '学号不存在！'
        elif not user.check_password(password):
            error = '密码错误！'
        
        if error is None:
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            if is_student:
                return redirect(url_for('student_index'))
            else:
                return redirect(url_for('teacher_index'))
        flash(error)
    return render_template('login.html')

@app.route('/admin', methods=('GET', 'POST'))
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Manager.query.filter_by(ManagerNum=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password!')
            return redirect(url_for('admin'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('manager'))
    return render_template('admin.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```



## 四、学生界面的功能简述

1. 信息查询：学生个人信息（可修改密码）、专业信息、学院信息

2. 查询已选课程信息，更换已选课程授课教师，退课

3. 查询所有开设课程的信息

4. 查询已选课程的成绩

   ![image-20190611214328463](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214328463.png)

   ![image-20190611214216601](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214216601.png)

   ![image-20190611214238123](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214238123.png)

   ![image-20190611214255516](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214255516.png)

```python
@app.route('/student_index')
@login_required
def student_index():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('student/student.html')
    else:
        logout_user()

@app.route('/student_info/<int:change>', methods=['GET','POST'])
@app.route('/student_info', defaults={'change':0}, methods=['GET','POST'])
@login_required
def student_info(change):
    if request.method == 'POST':
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        new_password2 = request.form['newpassword2']
        if not new_password==new_password2:
            flash('两次密码输入不一致！')
        elif not current_user.check_password(old_password):
            flash('原密码输入错误！')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('student_info'))
    return render_template('student/student_info.html', change=change)

  @app.route('/course_select_table', methods=['GET',])
@login_required
def course_select_table():
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        tables = []
        for Course_ in Courses:
            course_select_table = Course_select_table.query.filter_by(StudentNum=current_user.StudentNum,CourseNum=Course_.CourseNum).first()
            teacher = Teacher.query.filter_by(TeacherNum=course_select_table.TeacherNum).first()
            table = {
                'CourseNum':Course_.CourseNum,
                'CourseName':Course_.CourseName,
                'CourseCredit':Course_.CourseCredit,
                'CourseTime':Course_.CourseTime,
                'CourseDept':teacher.dept.DeptName,
                'TeacherName':teacher.TeacherName,
            }
            tables.append(table)
        return render_template('student/course_select_table.html', tables=tables)

@app.route('/course_teachers/<CourseNum>', methods=['GET',])
@login_required
def course_teachers(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        course_teachers = Course_Teacher.query.filter_by(CourseNum=CourseNum).all()
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        tables = []
        for course_teacher in course_teachers:
            course_select_table = Course_select_table.query.filter_by(CourseNum=CourseNum, TeacherNum=course_teacher.TeacherNum).all()
            teacher = Teacher.query.filter_by(TeacherNum=course_teacher.TeacherNum).first()
            table = {
                'CourseNum':course_teacher.CourseNum,
                'TeacherNum':course_teacher.TeacherNum,
                'CourseName':course.CourseName,
                'TeacherName':teacher.TeacherName,
                'Time':'TODO',
                'CourseCapacity':course_teacher.CourseCapacity,
                'CourseStudents':len(course_select_table),
            }
            tables.append(table)
        return render_template('student/course_teachers.html', tables=tables)

@app.route('/course', methods=['GET',])
@login_required
def course():
    if isinstance(current_user._get_current_object(), Student):
        all_courses = Course.query.all()
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        tables = []
        for course in all_courses:
            table = {
                'CourseNum':course.CourseNum,
                'CourseName':course.CourseName,
                'CourseCredit':course.CourseCredit,
                'CourseTime':course.CourseTime,
                'CourseDept':course.dept.DeptName
            }
            tables.append(table)
        return render_template('student/course.html', tables=tables, course_selected=course_selected)

@app.route('/course_drop/<CourseNum>', methods=['GET',])
@login_required
def course_drop(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        if not CourseNum in course_selected:
            flash('您未选择该门课程！')
        else:
            current_user.drop_course(CourseNum)
            db.session.commit()
            flash('您已成功退选该门课程。')
        return redirect(url_for('course_select_table'))

@app.route('/course_select/<CourseNum>/<TeacherNum>', methods=['GET',])
@login_required
def course_select(CourseNum, TeacherNum):
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        if  CourseNum in course_selected:
            flash('错误：您已选课程中存在该门课程！')
        else:
            course_select = Course_select_table(current_user.StudentNum, CourseNum, TeacherNum)
            db.session.add(course_select)
            db.session.commit()
            flash('您已成功选择该门课程。')
        return redirect(url_for('course'))

@app.route('/course_change/<CourseNum>', methods=['GET',])
@login_required
def course_change(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        current_user.drop_course(CourseNum)
        db.session.commit()
        return redirect(url_for('course_teachers', CourseNum=CourseNum))

@app.route('/grade_query', methods=['GET',])
@login_required
def grade_query():
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        tables = []
        for Course_ in Courses:
            course = Course.query.filter_by(CourseNum=Course_.CourseNum).first()
            course_select_table = Course_select_table.query.filter_by(StudentNum=current_user.StudentNum, CourseNum=Course_.CourseNum).first()
            teacher = Teacher.query.filter_by(TeacherNum=course_select_table.TeacherNum).first()
            table = {
                'CourseNum':Course_.CourseNum,
                'CourseName':course.CourseName,
                'CourseCredit':course.CourseCredit,
                'CourseTime':course.CourseTime,
                'CourseDept':teacher.dept.DeptName,
                'TeacherName':teacher.TeacherName,
                'Grade':course_select_table.Grade,
            }
            tables.append(table)
        return render_template('student/grade_query.html', tables=tables)

@app.route('/major_info', methods=['GET',])
@login_required
def major_info():
    return render_template('student/major_info.html')

@app.route('/dept_info', methods=['GET',])
@login_required
def dept_info():
    return render_template('student/dept_info.html')
```



## 五、教师界面功能简述

1. 信息查询：教师个人信息（可修改密码）

2. 查看学生选此教师开设课程的详情，包括各个学生的个人信息，以及已选学生人数等

3. 为此教师开设课程中的学生，录入此门课程的成绩，支持录入后修改成绩的功能

   ![image-20190611214409671](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214409671.png)

   ![image-20190611214434016](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214434016.png)

   ![image-20190611214444999](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214444999.png)

```python
@app.route('/teacher_index')
@login_required
def teacher_index():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('teacher/teacher.html')
    else:
        logout_user()

@app.route('/teacher_info/<int:change>', methods=['GET','POST'])
@app.route('/teacher_info', defaults={'change':0}, methods=['GET','POST'])
@login_required
def teacher_info(change):
    if request.method == 'POST':
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        new_password2 = request.form['newpassword2']
        if not new_password==new_password2:
            flash('两次密码输入不一致！')
        elif not current_user.check_password(old_password):
            flash('原密码输入错误！')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('teacher_info'))
    return render_template('teacher/teacher_info.html', change=change)
  
 @app.route('/course_select_detail')
@login_required
def course_select_detail():
    if isinstance(current_user._get_current_object(), Teacher):
        courses = current_user.Courses
        course_tables = []
        for course in courses:
            course_select_tables = Course_select_table.query.filter_by(CourseNum=course.CourseNum, TeacherNum=current_user.TeacherNum).all()
            course_info = {
                'CourseNum':course.CourseNum,
                'CourseName':course.CourseName,
                'CourseStudents':len(course_select_tables),
            }
            tables = []
            for course_select_table in course_select_tables:
                student = Student.query.filter_by(StudentNum=course_select_table.StudentNum).first()
                table = {
                    'StudentNum':student.StudentNum,
                    'StudentName':student.StudentName,
                    'StudentSex':student.StudentSex,
                    'DeptName':student.major.dept.DeptName,
                    'MajorName':student.major.MajorName,
                }
                tables.append(table)
            course_tables.append([course_info,tables])
        return render_template('teacher/course_select_detail.html', course_tables=course_tables)

@app.route('/course_grade_input/<CourseNum>', methods=['GET', 'POST'])
@app.route('/course_grade_input', defaults={'CourseNum':0})
@login_required
def course_grade_input(CourseNum):
    if isinstance(current_user._get_current_object(), Teacher):
        if request.method == 'POST':
            course = Course.query.filter_by(CourseNum=CourseNum).first()
            course_select_tables = Course_select_table.query.filter_by(CourseNum=course.CourseNum, TeacherNum=current_user.TeacherNum).all()                            
            for course_select_table in course_select_tables:
                student = Student.query.filter_by(StudentNum=course_select_table.StudentNum).first()
                if not course_select_table.Grade:
                    grade = request.form[student.StudentNum]
                    course_select_table.input_grade(grade)
            db.session.commit()
            flash('成绩录入成功！')
            return redirect(url_for('course_grade_input'))
        else:
            courses = current_user.Courses
            course_tables = []
            for course in courses:
                flag = 0
                course_select_tables = Course_select_table.query.filter_by(CourseNum=course.CourseNum, TeacherNum=current_user.TeacherNum).all()                
                course_info = {
                    'CourseNum':course.CourseNum,
                    'CourseName':course.CourseName,
                    'CourseStudents':len(course_select_tables),
                }
                tables = []
                for course_select_table in course_select_tables:
                    student = Student.query.filter_by(StudentNum=course_select_table.StudentNum).first()
                    table = {
                        'StudentNum':student.StudentNum,
                        'StudentName':student.StudentName,
                        'StudentSex':student.StudentSex,
                        'DeptName':student.major.dept.DeptName,
                        'MajorName':student.major.MajorName,
                        'Grade':course_select_table.Grade
                    }
                    if not table['Grade']:
                        flag = 1
                    tables.append(table)
                course_tables.append([course_info, tables, flag])
        return render_template('teacher/course_grade_input.html', course_tables=course_tables)

@app.route('/grade_set_zero/<CourseNum>/<StudentNum>')
def grade_set_zero(CourseNum, StudentNum):
    if isinstance(current_user._get_current_object(), Teacher):
        course_select_table = Course_select_table.query.filter_by(StudentNum=StudentNum, CourseNum=CourseNum).first()
        course_select_table.input_grade(None)
        db.session.commit()
        return redirect(url_for('course_grade_input'))
```



## 六、管理员界面简述

1. 学生管理：
   - 录入学生：先检测学生表中是否存在学号冲突的学生，若无则插入此学生信息。
   - 删除学生：先查询出此学生所有已选课程，系统将其全部退选后，再删除此学生。

2. 教师管理：
   - 录入教师：同"录入学生"。

3. 课程管理：
   - 创建课程
   - 教师开设课程
   - 删除课程

4. 学生选课管理：
   - 手动签课
   - 手动退课
   - 修改课程容量
   - 删除此开设课程

![image-20190611214508267](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214508267.png)

![image-20190611214535166](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214535166.png)

![image-20190611214543382](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214543382.png)

![image-20190611214552924](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214552924.png)

![image-20190611214617197](/Users/mouyu/Library/Application Support/typora-user-images/image-20190611214617197.png)

```python
@app.route('/manager')
@login_required
def manager():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('admin/manager.html')
    else:
        logout_user()
        return redirect(url_for('admin'))
   
@app.route('/student_manage', methods=['GET', 'POST'])
@login_required
def student_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'majors': [major.MajorName for major in Major.query.all()]
        }
        students = Student.query.order_by(Student.MajorNum).all()
        return render_template('admin/student_manage.html', info=info, students=students)

@app.route('/add_student', methods=['POST',])
@login_required
def add_student():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            StudentNum = request.form['StudentNum']
            MajorName = request.form['MajorName']
            MajorNum = Major.query.filter_by(MajorName=MajorName).first().MajorNum
            StudentName = request.form['StudentName']
            StudentSex = request.form['StudentSex']
            StudentInyear = request.form['StudentInyear']
            if not Student.query.filter_by(StudentNum=StudentNum).first():
                student = Student(StudentNum, MajorNum, StudentName, StudentSex, StudentInyear)
                db.session.add(student)
                db.session.commit()
                flash('录入学生信息成功！')
            else:
                flash('学号%s已存在！'%(StudentNum))
        return redirect(url_for('student_manage'))

@app.route('/delete_student/<StudentNum>', methods=['GET', 'POST'])
@login_required
def delete_student(StudentNum):
    if isinstance(current_user._get_current_object(), Manager):
        delete_stu = Student.query.filter_by(StudentNum=StudentNum).first()
        # 先删除选课表中信息
        course_tables = Course_select_table.query.filter_by(StudentNum=StudentNum).all()
        for course_table in course_tables:
            db.session.delete(course_table)
        db.session.commit()
        db.session.delete(delete_stu)
        db.session.commit()
        flash('删除学生成功！')
        return redirect(url_for('student_manage'))

@app.route('/teacher_manage', methods=['GET', 'POST'])
@login_required
def teacher_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'depts': [dept.DeptName for dept in Dept.query.all()]
        }
        teachers = Teacher.query.order_by(Teacher.DeptNum).all()
        return render_template('admin/teacher_manage.html', info=info, teachers=teachers)

@app.route('/add_teacher', methods=['POST',])
@login_required
def add_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            TeacherNum = request.form['TeacherNum']
            DeptName = request.form['DeptName']
            DeptNum = Dept.query.filter_by(DeptName=DeptName).first().DeptNum
            TeacherName = request.form['TeacherName']
            TeacherSex = request.form['TeacherSex']
            TeacherTitle = request.form['TeacherTitle']
            TeacherInyear = request.form['TeacherInyear']
            if not Teacher.query.filter_by(TeacherNum=TeacherNum).first():
                teacher = Teacher(TeacherNum, DeptNum, TeacherName, TeacherSex, TeacherInyear, TeacherTitle)
                db.session.add(teacher)
                db.session.commit()
                flash('录入教师信息成功！')
            else:
                flash('工号%s已存在!'%(TeacherNum))
        return redirect(url_for('teacher_manage'))

@app.route('/course_manage', methods=['GET', 'POST'])
@login_required
def course_manage():
    if isinstance(current_user._get_current_object(), Manager):
        info = {
            'depts':[dept.DeptName for dept in Dept.query.all()],
            'courses':[course.CourseName for course in Course.query.all()],
            'teachers':[teacher.TeacherName for teacher in Teacher.query.all()],
        }
        courses = Course.query.order_by(Course.CourseNum).all()
    return render_template('admin/course_manage.html', info=info, courses=courses)

@app.route('/add_course', methods=['POST',])
@login_required
def add_course():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseName = request.form['CourseName']
            CourseNum = request.form['CourseNum']
            DeptName = request.form['DeptName']
            DeptNum = Dept.query.filter_by(DeptName=DeptName).first().DeptNum
            CourseCredit = request.form['CourseCredit']
            CourseTime = request.form['CourseTime']
            CourseDesc = request.form['CourseDesc']
            if not Course.query.filter_by(CourseNum=CourseNum).first():
                course = Course(CourseNum, CourseName, CourseCredit, CourseTime, DeptNum, CourseDesc)
                db.session.add(course)
                db.session.commit()
                flash('创建课程成功！')
            else:
                flash('课程号"%s"重复，请修改课程号！'%(CourseNum))
        return redirect(url_for('course_manage'))

@app.route('/add_course_teacher', methods=['POST',])
@login_required
def add_course_teacher():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseName = request.form['CourseName']
            CourseNum = Course.query.filter_by(CourseName=CourseName).first().CourseNum
            TeacherName = request.form['TeacherName']
            TeacherNum = Teacher.query.filter_by(TeacherName=TeacherName).first().TeacherNum
            CourseCapacity = request.form['CourseCapacity']
            if not Course_Teacher.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).first():
                course_teacher = Course_Teacher(CourseNum, TeacherNum, CourseCapacity)
                db.session.add(course_teacher)
                db.session.commit()
                flash('开设课程成功！')
            else:
                flash('%s老师已开设"%s"课程，请勿重复添加！'%(TeacherName, CourseName))
        return redirect(url_for('course_manage'))

@app.route('/course_delete/<CourseNum>')
@login_required
def course_delete(CourseNum):
    if isinstance(current_user._get_current_object(), Manager):
        # 先删除选课信息
        course_select_tables = Course_select_table.query.filter_by(CourseNum=CourseNum).all()
        for course_select_table in course_select_tables:
            db.session.delete(course_select_table)
        db.session.commit()
        flash('删除学生选课信息成功！')
        # 再删除课程与老师的对应表
        course_teachers = Course_Teacher.query.filter_by(CourseNum=CourseNum).all()
        for course_teacher in course_teachers:
            db.session.delete(course_teacher)
        db.session.commit()
        flash('删除教师开设课程成功！')
        # 最后删除课程
        course = Course.query.filter_by(CourseNum=CourseNum).first()
        db.session.delete(course)
        db.session.commit()
        flash('删除课程成功！')
    return redirect(url_for('course_manage'))

@app.route('/course_select_manage', methods=['GET', 'POST'])
@login_required
def course_select_manage():
    if isinstance(current_user._get_current_object(), Manager):
        course_teachers = Course_Teacher.query.order_by(Course_Teacher.CourseNum).all()
        tables = []
        for course_teacher in course_teachers:
            course = Course.query.filter_by(CourseNum=course_teacher.CourseNum).first()
            teacher = Teacher.query.filter_by(TeacherNum=course_teacher.TeacherNum).first()
            course_select_tables = Course_select_table.query.filter_by(CourseNum=course.CourseNum, TeacherNum=teacher.TeacherNum).all()                
            table = {
                'CourseNum':course.CourseNum,
                'CourseName':course.CourseName,
                'TeacherNum':teacher.TeacherNum,
                'TeacherName':teacher.TeacherName,
                'CourseCapacity':course_teacher.CourseCapacity,
                'CourseStudents':len(course_select_tables),
            }
            tables.append(table)
    return render_template('admin/course_select_manage.html', tables=tables)

@app.route('/course_teacher_delete/<CourseNum>/<TeacherNum>')
@login_required
def course_teacher_delete(CourseNum, TeacherNum):
    if isinstance(current_user._get_current_object(), Manager):
        # 先删除选课信息
        course_select_tables = Course_select_table.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).all()
        for course_select_table in course_select_tables:
            db.session.delete(course_select_table)
        db.session.commit()
        flash('删除学生选课信息成功！')
        # 再删除课程与老师的对应表
        course_teacher = Course_Teacher.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).first()
        db.session.delete(course_teacher)
        db.session.commit()
        flash('删除教师开设课程成功！')
    return redirect(url_for('course_select_manage'))

@app.route('/add_course_select', methods=['POST',])
@login_required
def add_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            TeacherNum = request.form['TeacherNum']
            StudentNum = request.form['StudentNum']
            if not Course_select_table.query.filter_by(CourseNum=CourseNum,StudentNum=StudentNum).first():
                course_select_table = Course_select_table(StudentNum, CourseNum, TeacherNum)
                db.session.add(course_select_table)
                db.session.commit()
                flash('手动签课成功！')
            else:
                flash('手动签课失败！该学生已选择该门课程！')
    return redirect(url_for('course_select_manage'))

@app.route('/drop_course_select', methods=['POST',])
@login_required
def drop_course_select():
    if isinstance(current_user._get_current_object(), Manager):
        if request.method == 'POST':
            CourseNum = request.form['CourseNum']
            TeacherNum = request.form['TeacherNum']
            StudentNum = request.form['StudentNum']
            course_select_table = Course_select_table.query.filter_by(CourseNum=CourseNum,TeacherNum=TeacherNum,StudentNum=StudentNum).first()
            if course_select_table:
                db.session.delete(course_select_table)
                db.session.commit()
                flash('手动退课成功！')
            else:
                flash('手动退课失败！学生(%s)未选择教师(%s)的课程(%s)'%(StudentNum,TeacherNum,CourseNum))
    return redirect(url_for('course_select_manage'))

@app.route('/change_course_capacity/<CourseNum>/<TeacherNum>/<add_or_sub>', methods=['GET',])
@login_required
def change_course_capacity(CourseNum, TeacherNum, add_or_sub):
    if isinstance(current_user._get_current_object(), Manager):
        course_teacher = Course_Teacher.query.filter_by(CourseNum=CourseNum, TeacherNum=TeacherNum).first()
        if add_or_sub == 'add':
            course_teacher.CourseCapacity += 10
            flash('课程容量扩容10人！')
        elif add_or_sub == 'sub':
            course_teacher.CourseCapacity -= 10
            flash('课程容量缩容10人！')
        db.session.commit()
    return redirect(url_for('course_select_manage'))
```