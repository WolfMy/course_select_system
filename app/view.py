from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models_new import Student, Teacher, Manager, Course, Course_select_table, Major
from app.forms import EditProfileForm
from app import db


@app.route('/')
def index():
    return render_template('index.html')

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
            login_user(user)
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

@app.route('/student_index')
@login_required
def student_index():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('system/student.html')
    else:
        logout_user()
    
@app.route('/teacher_index')
@login_required
def teacher_index():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('system/teacher.html')
    else:
        logout_user()

@app.route('/manager')
@login_required
def manager():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('system/manager.html')
    else:
        logout_user()
        return redirect(url_for('admin'))

@app.route('/student_info', methods=['GET','POST'])
@login_required
def student_info():
    form = EditProfileForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        new_password2 = form.new_password2.data
        if not new_password==new_password2:
            flash('两次密码输入不一致！')
        elif not current_user.check_password(old_password):
            flash('原密码输入错误！')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('student_info'))
    return render_template('system/student_info.html', form=form)

@app.route('/teacher_info', methods=['GET','POST'])
@login_required
def teacher_info():
    form = EditProfileForm()
    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        new_password2 = form.new_password2.data
        if not new_password==new_password2:
            flash('两次密码输入不一致！')
        elif not current_user.check_password(old_password):
            flash('原密码输入错误！')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Your changes have been saved.')
        return redirect(url_for('teacher_info'))
    return render_template('system/teacher_info.html', form=form)

@app.route('/course_select_table', methods=['GET',])
@login_required
def course_select_table():
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        tables = []
        for Course_ in Courses:
            course = Course.query.filter_by(CourseNum=Course_.CourseNum).first()
            teacher = Teacher.query.filter_by(CourseNum=Course_.CourseNum).first()
            table = {
                'CourseNum':Course_.CourseNum,
                'CourseName':course.CourseName,
                'CourseCredit':course.CourseCredit,
                'CourseTime':course.CourseTime,
                'TeacherName':teacher.TeacherName,
            }
            tables.append(table)
        return render_template('system/course_select_table.html', tables=tables)

@app.route('/course', methods=['GET',])
@login_required
def course():
    if isinstance(current_user._get_current_object(), Student):
        all_courses = Course.query.all()
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        tables = []
        for course in all_courses:
            if not course.CourseNum in course_selected:
                teacher = Teacher.query.filter_by(CourseNum=course.CourseNum).first()
                table = {
                    'CourseNum':course.CourseNum,
                    'CourseName':course.CourseName,
                    'CourseCredit':course.CourseCredit,
                    'CourseTime':course.CourseTime,
                    'TeacherName':teacher.TeacherName,
                }
                tables.append(table)
        return render_template('system/course.html', tables=tables)

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

@app.route('/course_select/<CourseNum>', methods=['GET',])
@login_required
def course_select(CourseNum):
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        course_selected = [Course_.CourseNum for Course_ in Courses]
        if  CourseNum in course_selected:
            flash('错误：您已选课程中存在该门课程！')
        else:
            course = Course.query.filter_by(CourseNum=CourseNum).first()
            current_user.select_course(course)
            db.session.commit()
            flash('您已成功选择该门课程。')
        return redirect(url_for('course_select_table'))

@app.route('/major_info', methods=['GET',])
@login_required
def major_info():
    return render_template('system/major_info.html')

@app.route('/dept_info', methods=['GET',])
@login_required
def dept_info():
    return render_template('system/dept_info.html')

@app.route('/course_select_detail/<int:grade_input>')
@app.route('/course_select_detail', defaults={'grade_input':0})
@login_required
def course_select_detail(grade_input):
    if isinstance(current_user._get_current_object(), Teacher):
        course = Course.query.filter_by(CourseNum=current_user.CourseNum).first()
        Students = course.student
        course_info = {
            'CourseNum':course.CourseNum,
            'CourseName':course.CourseName,
            'CourseStudents':len(Students),
        }
        tables = []
        for Student in Students:
            major = Major.query.filter_by(MajorNum=Student.MajorNum).first()
            dept = major.dept
            table = {
                'StudentNum':Student.StudentNum,
                'StudentName':Student.StudentName,
                'StudentSex':Student.StudentSex,
                'DeptName':dept.DeptName,
                'MajorName':major.MajorName
            }
            tables.append(table)
        if not grade_input:
            return render_template('system/course_select_detail.html', tables=tables, course_info=course_info)
        else:
            # TODO: 添加成绩显示功能
            for table in tables:
                course_select_table = Course_select_table.query.filter_by(StudentNum=table['StudentNum'], CourseNum=course_info['CourseNum']).first()
                table['grade'] = course_select_table.Grade
            return render_template('system/course_select_detail.html', tables=tables, course_info=course_info, grade_input=grade_input)

@app.route('/course_grade_input', methods=['GET', 'POST'])
@login_required
def course_grade_input():
    if isinstance(current_user._get_current_object(), Teacher):
        if request.method == 'POST':
            course = Course.query.filter_by(CourseNum=current_user.CourseNum).first()
            Students = course.student
            for Student in Students:
                grade = request.form[Student.StudentNum]
                course_select_table = Course_select_table.query.filter_by(StudentNum=Student.StudentNum, CourseNum=course.CourseNum).first()
                course_select_table.input_grade(grade)
            db.session.commit()
            flash('成绩录入成功！')
            return redirect(url_for('course_select_detail', grade_input=1))

@app.route('/grade_query', methods=['GET',])
@login_required
def grade_query():
    if isinstance(current_user._get_current_object(), Student):
        Courses = current_user.Courses
        tables = []
        for Course_ in Courses:
            course = Course.query.filter_by(CourseNum=Course_.CourseNum).first()
            teacher = Teacher.query.filter_by(CourseNum=Course_.CourseNum).first()
            course_select_table = Course_select_table.query.filter_by(StudentNum=current_user.StudentNum, CourseNum=course.CourseNum).first()
            table = {
                'CourseNum':Course_.CourseNum,
                'CourseName':course.CourseName,
                'CourseCredit':course.CourseCredit,
                'CourseTime':course.CourseTime,
                'TeacherName':teacher.TeacherName,
                'Grade':course_select_table.Grade,
            }
            tables.append(table)
        return render_template('system/grade_query.html', tables=tables)