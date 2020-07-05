from app import app
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models_new import Student, Teacher, Manager, Course, Course_select_table, Course_Teacher, Major, Dept
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

@app.route('/voluntary_selection')
@login_required
def voluntary_selection():
    return render_template('student/voluntary_selection.html')