from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models_new import Student, Teacher, Manager, Course, Course_select_table, Course_Teacher, Major
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

@app.route('/student_index')
@login_required
def student_index():
    if isinstance(current_user._get_current_object(), Student):
        return render_template('student/student.html')
    else:
        logout_user()
    
@app.route('/teacher_index')
@login_required
def teacher_index():
    if isinstance(current_user._get_current_object(), Teacher):
        return render_template('teacher/teacher.html')
    else:
        logout_user()

@app.route('/manager')
@login_required
def manager():
    if isinstance(current_user._get_current_object(), Manager):
        return render_template('admin/manager.html')
    else:
        logout_user()
        return redirect(url_for('admin'))

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
                'CourseDept':course.Teachers[0].dept.DeptName,
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

@app.route('/student_manage', methods=['GET', 'POST'])
@login_required
def student_manage():
    return render_template('admin/student_manage.html')

@app.route('/teacher_manage', methods=['GET', 'POST'])
@login_required
def teacher_manage():
    return render_template('admin/teacher_manage.html')

@app.route('/course_manage', methods=['GET', 'POST'])
@login_required
def course_manage():
    return render_template('admin/course_manage.html')

@app.route('/course_select_manage', methods=['GET', 'POST'])
@login_required
def course_select_manage():
    return render_template('admin/course_select_manage.html')