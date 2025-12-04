.  # 项目根目录
├── app  # 应用主目录，包含前后端代码
│   ├── __init__.py  # 后端：应用初始化文件
│   ├── config.py  # 后端：配置文件
│   ├── forms.py  # 后端：表单定义
│   ├── models_new.py  # 后端：数据模型定义(新版本)
│   ├── models.py  # 后端：数据模型定义
│   ├── static  # 前端：静态资源文件
│   ├── templates  # 前端：HTML模板文件
│   │   ├── admin # 前端：管理员页面模板
│   │   │   ├── course_manage.html
│   │   │   ├── course_select_manage.html
│   │   │   ├── manager.html
│   │   │   ├── student_manage.html
│   │   │   └── teacher_manage.html
│   │   ├── admin.html
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── student # 前端：学生页面模板
│   │   │   ├── course_select_table.html
│   │   │   ├── course_teachers.html
│   │   │   ├── course.html
│   │   │   ├── dept_info.html
│   │   │   ├── grade_query.html
│   │   │   ├── major_info.html
│   │   │   ├── student_info.html
│   │   │   ├── student.html
│   │   │   └── voluntary_selection.html
│   │   └── teacher # 前端：教师页面模板
│   │       ├── course_grade_input.html
│   │       ├── course_select_detail.html
│   │       ├── teacher_info.html
│   │       └── teacher.html
│   └── view.py  # 后端：视图函数，处理HTTP请求
├── course_select_system.sql  # 数据库：SQL脚本文件
├── main.py  # 应用入口文件
├── migrations  # 后端：数据库迁移相关文件
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── ddcf6d407079_.py
├── README.md # 项目说明文档
├── requirements.txt  # 项目依赖列表
└── tree.md # 项目目录结构说明文档
