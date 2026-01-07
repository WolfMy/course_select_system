> 按照“安装与运行指南”中的步骤进行操作，即可在本地运行选课系统。
>
> 首先用管理员账户登陆（帐号000，密码admin）
>
> 创建自己的8位学号，默认密码admin。
>
> 再用自己学号登陆选课系统进行体验。

## 一、安装与运行指南（Bootstrap框架、SQLalchemy的ORM框架、数据库迁移工具）

### 1. 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（macOS/Linux）
source venv/bin/activate

# 激活虚拟环境（Windows）
# venv\Scripts\activate
```

### 2. 安装项目依赖
```bash
pip install -r requirements.txt
```

### 3. 数据库准备
应用使用MySQL数据库，配置如下：
- 用户名：root
- 密码：root
- 数据库名：course_select_system
- 端口：3306

#### 创建数据库并导入初始数据
```bash
# 登录MySQL（需要输入密码）
mysql -u root -p

# 在MySQL命令行中执行以下操作
CREATE DATABASE course_select_system CHARACTER SET utf8;
EXIT;

# 导入SQL脚本
mysql -u root -p course_select_system < course_select_system.sql
```

### 4. 数据库迁移（如果需要）
```bash
# 初始化数据库迁移（如果尚未初始化）
flask db init

# 执行数据库迁移
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. 运行应用
```bash
# 直接运行Python文件
python main.py
```

应用将在 <http://0.0.0.0:4070> 上运行。

### 注意事项
1. 确保MySQL服务正在运行
2. 根据您的环境，可能需要修改 `app/config.py` 中的数据库连接信息
3. 如果需要启用调试模式，可以修改 `main.py` 中的debug参数为True


## 二、选课系统关系模型的定义

在基础的属性定义外，还定义了各类之间的一对多关系，多对多关系，包括：

- 学院：教师 = 1:n
- 学院：专业 = 1:n
- 学院：课程 = 1:n
- 专业：学生 = 1:n
- 教师：课程 = m:n
- 学生：课程 = m:n

在教师与课程的多对多关系中，额外建立一张表，用于存储老师开设课程的具体属性：上课时间、课程容量等。

在教师、课程、学生这个三方多对多关系中，额外建立一张结联表。 


## 三、登陆、登出模块

登陆验证时，首先从学生表中查找输入的学号，若无，再从教师表中去查找。管理员采用单独的登陆界面，用于区分。

密码验证采用flask的加盐哈希加密算法，无SQL注入风险，保证用户的信息安全。

在此基础上，添加了"记住我"的登陆选项。

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/Login.png)


## 四、学生界面的功能简述

1. 信息查询：学生个人信息（可修改密码）、专业信息、学院信息

2. 查询已选课程信息，更换已选课程授课教师，退课

3. 查询所有开设课程的信息

4. 查询已选课程的成绩

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/Student.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/SelectedCourse.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/AllCourse.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/GradeInquiry.png)


## 五、教师界面功能简述

1. 信息查询：教师个人信息（可修改密码）

2. 查看学生选此教师开设课程的详情，包括各个学生的个人信息，以及已选学生人数等

3. 为此教师开设课程中的学生，录入此门课程的成绩，支持录入后修改成绩的功能

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/Teacher.png)
   
   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/TeacherCourse.png)
   
   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/GradeInput.png)


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

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/StuManage.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/TeacherManage.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/CourseManage.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/CourseManage2.png)

   ![image](https://github.com/WolfMy/course_select_system/blob/master/image/SelectManage.png)
   
