-- MySQL dump 10.13  Distrib 9.5.0, for macos26.1 (arm64)
--
-- Host: localhost    Database: course_select_system
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '97374f78-eb8b-11f0-b54c-d5d5ade16141:1-166';

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('ddcf6d407079');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `CourseNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `CourseName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `CourseCredit` int NOT NULL,
  `CourseTime` int NOT NULL,
  `CourseDesc` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci,
  `DeptNum` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`CourseNum`),
  KEY `DeptNum` (`DeptNum`),
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`DeptNum`) REFERENCES `dept` (`deptnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES ('1','数据库原理',3,48,'','1'),('10','审计学',3,48,'高等数学简介','9'),('11','毛概',3,48,'毛概简介','10'),('12','市场营销学',3,48,'市场营销学简介','7'),('14','线性代数',3,48,'线性代数简介','8'),('15','形式与政策',3,48,'形式与政策简介','10'),('2','计算机组成原理',3,48,'计算机组成原理简介','1'),('20','电路与电子学',3,48,'','4'),('3','Linux系统',3,48,'Linux系统简介','1'),('4','数据库课程设计',3,48,'数据库课程设计简介','1'),('5','密码学',2,32,'','2'),('6','数据结构(甲)',3,48,'数据结构','2'),('7','编译原理',3,48,'编译原理简介','1'),('9','数学分析',3,48,'数学分析简介','8');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_select_table`
--

DROP TABLE IF EXISTS `course_select_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_select_table` (
  `StudentNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `CourseNum` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TeacherNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `Grade` int DEFAULT NULL,
  PRIMARY KEY (`StudentNum`,`CourseNum`,`TeacherNum`),
  KEY `CourseNum` (`CourseNum`),
  KEY `TeacherNum` (`TeacherNum`),
  CONSTRAINT `course_select_table_ibfk_1` FOREIGN KEY (`CourseNum`) REFERENCES `course` (`CourseNum`),
  CONSTRAINT `course_select_table_ibfk_2` FOREIGN KEY (`StudentNum`) REFERENCES `student` (`studentnum`),
  CONSTRAINT `course_select_table_ibfk_3` FOREIGN KEY (`TeacherNum`) REFERENCES `teacher` (`teachernum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_select_table`
--

LOCK TABLES `course_select_table` WRITE;
/*!40000 ALTER TABLE `course_select_table` DISABLE KEYS */;
INSERT INTO `course_select_table` VALUES ('17262229','14','2002',NULL),('17272224','1','0001',100),('17272224','2','0002',NULL),('17272224','20','0038',NULL),('17272224','4','0001',99),('17282224','12','2001',NULL);
/*!40000 ALTER TABLE `course_select_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_teacher`
--

DROP TABLE IF EXISTS `course_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_teacher` (
  `CourseNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TeacherNum` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `CourseCapacity` int NOT NULL,
  PRIMARY KEY (`CourseNum`,`TeacherNum`),
  KEY `TeacherNum` (`TeacherNum`),
  CONSTRAINT `course_teacher_ibfk_1` FOREIGN KEY (`CourseNum`) REFERENCES `course` (`CourseNum`),
  CONSTRAINT `course_teacher_ibfk_2` FOREIGN KEY (`TeacherNum`) REFERENCES `teacher` (`teachernum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_teacher`
--

LOCK TABLES `course_teacher` WRITE;
/*!40000 ALTER TABLE `course_teacher` DISABLE KEYS */;
INSERT INTO `course_teacher` VALUES ('1','0001',11),('10','0001',20),('11','0038',80),('12','2001',30),('14','2002',25),('15','2001',80),('2','0002',30),('2','0004',10),('20','0038',48),('3','0003',20),('4','0001',15),('5','1001',10),('6','1002',5),('7','0005',50),('9','2000',40);
/*!40000 ALTER TABLE `course_teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dept`
--

DROP TABLE IF EXISTS `dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dept` (
  `DeptNum` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `DeptName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `DeptChairman` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `DeptTel` varchar(11) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `DeptDesc` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci,
  PRIMARY KEY (`DeptNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dept`
--

LOCK TABLES `dept` WRITE;
/*!40000 ALTER TABLE `dept` DISABLE KEYS */;
INSERT INTO `dept` VALUES ('1','计算机学院','计算机学院党委书记',NULL,'计算机学院简介'),('10','马克思主义学院','马院党委书记',NULL,'马院简介'),('2','网络空间安全学院','网安学院党委书记',NULL,'网络空间安全学院简介'),('3','机械工程学院','王主任','13711111111','学院全日制在校大学生千余人，研究生近百人。现设有机械工程、工业设计和环境科学与工程3个系，下设机械设计制造及其自动化、车辆工程、工业设计、环境工程和环境科学5个本科专业，并拥有机械电子工程、机械制造及其自动化、机械设计及理论、精密仪器与机械4个二级学科硕士学位点，形成了学科方向稳定、培养体系完整的本科生、研究生人才培养体系。\n 学院设有机械电子工程、机械制造及其自动化、机械设计与车辆工程、工业设计、环境科学与工程等5个研究所，拥有实力雄厚的教学科研队伍。学院学术带头人为李教授、张教授、王教授和刘教授四位博士生导师。\n 学院在机电装备技术、特种加工、测控技术等领域，特色明显。完成了一系列国家计划项目，国家、省部级基金项目和横向科研项目，一批成果获得国家和省部级科技进步奖，并拥有一批国家发明专利。在研的国家自然科学基金6项，其中国家自然科学基金重点项目1项。'),('4','电子信息学院','李书记','137222222','电子信息学院是我校历史最悠久的学院之一，也是学校重点建设发展的学院。历经30余年的发展，已形成学士、硕士和博士完整的培养体系。作为国内具有较高知名度的工科学院，多个研究领域在国内外具有较强的影响力。'),('5','通信工程学院','张院长','13777333333','通信工程学院是学校重点建设的学院之一，历经30多年发展，已形成学士、硕士和博士完整的培养体系。\n 学院现有“通信工程”、“信息对抗技术”、“信息工程”3个本科专业以及一个中外合作办学项目“通信工程”。通信工程专业是国家重点专业、浙江省优势专业和卓越工程师教育培养计划试点专业，信息对抗技术专业是全省唯一武器类专业。拥有信息与通信工程一级学科工学硕士学位授予权和电子与通信工程领域工程硕士学位授予权。信息与通信工程一级硕士学位点包含信号与信息处理、通信与信息系统、信息安全3个二级学科硕士点。自主设置目录外二级学科智能信息处理与系统博士点。拥有1个浙江省一流学科（B类）、1个国防特色学科和1个原信息产业部重点学科。'),('6','自动化学院','王院长','13777444444','杭州电子科技大学自动化学院成立于2000年，其前身是1985年成立的机器人研究室和1994年成立的自动化系，是学校最富活力、发展最快的学院之一。学院现设置有2个本科专业：自动化(国防特色重点专业、卓越工程师培养计划专业、省重点及优势专业)、电气工程及其自动化(省重点及优势专业)；在校本科生及研究生2000余人。'),('7','管理学院','李院长','13777766666','学院的发展可追溯至1956年学校前身杭州航空工业财经学校的成立，1980年杭州电子工业学院成立时管理工程系为独立建制，1995年组建工商管理学院，2000年，成立管理学院。当前，学院依托学校电子信息特色与优势，致力于建设成为信息化特色明显、国际化水平一流的高水平学院，成为我国特别是浙江省信息化管理人才培养、信息化管理创新研究和社会服务的重要基地。'),('8','理学院','张院长','13777777777','理学院以数学、物理两大学科为基础，依托学校电子信息优势，重基础，强特色，坚持走理工交叉融合的学科发展道路。现拥有信息与计算科学、数学与应用数学、应用物理学、光电信息科学与工程、应用统计学等五个本科专业，另有与经济学院合办的金融学（数学与应用数学复合）专业，其中信息与计算科学专业为浙江省“十二五”优势专业。现有系统优化与智能计算二级博士点（自主设置），数学、物理学和统计学（与经济学院联合）等三个一级学科硕士点。数学学科为浙江省“十二五”一级重点学科、浙江省“十三五”一流学科（A类）和学校博士单位建设支撑学科，物理学科为校一流学科（A类）。学院设有数学系、物理系，基础数学研究所、应用数学研究所、计算数学研究所、运筹与控制研究所、能源研究所和光电子物理与技术研究所'),('9','会计学院','会计学院党委书记',NULL,'会计学院简介');
/*!40000 ALTER TABLE `dept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `major`
--

DROP TABLE IF EXISTS `major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `major` (
  `MajorNum` varchar(6) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `DeptNum` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `MajorName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `MajorAssistant` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `MajorTel` varchar(11) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `MajorDesc` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci,
  `TrainingProgram` varchar(7) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`MajorNum`),
  KEY `DeptNum` (`DeptNum`),
  CONSTRAINT `major_ibfk_1` FOREIGN KEY (`DeptNum`) REFERENCES `dept` (`DeptNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `major`
--

LOCK TABLES `major` WRITE;
/*!40000 ALTER TABLE `major` DISABLE KEYS */;
INSERT INTO `major` VALUES ('1','1','计算机科学与技术','张助理',NULL,'计算机科学与技术简介','1'),('10','1','计算机科学与技术','李助理','14988658658','计算机科学与技术','10'),('11','1','软件工程','王助理','14777989686','软件工程','11'),('12','1','软件工程卓越工程师','刘助理','16999856635','软件工程卓越工程师','12'),('13','1','物联网工程','陈助理','1447524456','物联网工程','13'),('14','7','人力资源管理专业','周助理','14424744585','无','14'),('15','7','电子商务专业','FV','19981144457','无','15'),('16','7','工商管理专业','VS','4556686','无','16'),('17','8','光电信息科学与工程','JUGG','6456456','无','17'),('18','8','数学与应用数学','AM','565334','无','18'),('19','3','车辆工程','赵助理','13466863628','车辆工程','19'),('2','2','网络工程','钱助理',NULL,'网络工程简介','2'),('20','3','海洋工程与技术','孙助理','14574212463','海洋工程与技术','20'),('3','4','电子科学与技术','周助理','15585324632','电子科学与技术','3'),('4','4','电子信息工程','吴助理','18898909876','电子信息工程','4'),('5','5','通信工程','郑助理','18815612398','通信工程','5'),('6','5','信息对抗技术','杨助理','14256998659','信息对抗技术','6'),('7','6','电气工程及其自动化','黄助理','19877545681','电气工程及其自动化','7'),('8','6','自动化专业','赵助理','13646244512','自动化专业','8'),('9','6','自动化（卓越）','钱助理','12545525568','自动化（卓越）','9');
/*!40000 ALTER TABLE `major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manager`
--

DROP TABLE IF EXISTS `manager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manager` (
  `ManagerNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `ManagerName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `ManagerSex` varchar(2) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `ManagerBirthday` datetime DEFAULT NULL,
  `ManagerPassword` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `ManagerPermission` int NOT NULL,
  PRIMARY KEY (`ManagerNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manager`
--

LOCK TABLES `manager` WRITE;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` VALUES ('000','管理员','男',NULL,'pbkdf2:sha256:50000$Kd1BWslr$3235dda29fc6980052b036ccff257c2f62a5653260ecd61225916fd8b2844720',1);
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `StudentNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `MajorNum` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `StudentName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `StudentSex` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `StudentInyear` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `StudentPassword` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`StudentNum`),
  KEY `MajorNum` (`MajorNum`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`MajorNum`) REFERENCES `major` (`MajorNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('12345678','1','王明','男','2026','pbkdf2:sha256:600000$KgQHLnQQDoQe31OP$f90cca7f08b9b5a657a91013bceef38014cef72e12c5c14e200be1adc4366195'),('17262229','5','李明','男','2017','pbkdf2:sha256:150000$J125habF$a8e79022bf66ab52467660edf84dbaab60d843b9f75e2a3c9ce15581eb24d862'),('17272224','1','张伟','男','2017','pbkdf2:sha256:150000$cpVX6sre$a50066924e9d647237ee4489c59c29a4674d69cc81910028d74d98cff395249b'),('17272225','2','王芳','男','2017','pbkdf2:sha256:150000$JsNLA406$46b9a76895d17825ead245f5401393c54a8bd770bbadcc9445c6446abf3f51ff'),('17272227','2','刘洋','男','2017','pbkdf2:sha256:150000$fE2he8Sq$e311d730f648be3df26a0634f240af7909d6b9e03fe94e4837b71e38abe469ef'),('17282224','16','陈静','女','2017','pbkdf2:sha256:150000$JK1MBBsP$733f34e4ef9d11dd0a5b12d4f836b83e66ddd17711012477376b121d80dbf9b3');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `TeacherNum` varchar(8) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `DeptNum` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TeacherName` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TeacherSex` varchar(2) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TeacherInyear` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `TeacherTitle` varchar(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `TeacherPassword` text CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`TeacherNum`),
  KEY `DeptNum` (`DeptNum`),
  CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`DeptNum`) REFERENCES `dept` (`DeptNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('0001','1','刘老师','女','1999','教授','pbkdf2:sha256:150000$yjfNLX6V$7f1425dad325dc5d24a67769cb144829a47d5ada96f11f68d685bedcf02ad275'),('0002','1','王老师','女','1997','教授','pbkdf2:sha256:150000$lfocOIrq$c08ef4894bda14e7e947b77f4f939d9b2c44be2eaed2c79d434bf50a59dda10b'),('0003','1','李老师','男','2010','副教授','pbkdf2:sha256:150000$BRKZvQ1X$bb52920ef91c622dcdf3ad152f0d2d93b4543577a776addbf2aef11422f0f449'),('0004','1','陈老师','男','1998','副教授','pbkdf2:sha256:150000$jwqThKCt$83bed964ea9996c057a31eda1dd742b708b5e868f5a9adf473794a0ea826de18'),('0005','1','杨老师','男','1999','教授','pbkdf2:sha256:150000$k2zgGaXD$03c5c82263874603415d5b190a4b83a2e0437cfa57ddea4af05726df6a7868f1'),('0038','4','黄老师','男','1999','副教授','pbkdf2:sha256:150000$3j3Df9Bj$ca389d9c07a3a0aa90ffb209f131e9dbc09e3ba7331e7b5d68c2bb028f3f2304'),('1001','2','周老师','男','2000','教授','pbkdf2:sha256:150000$qKcrEw4M$e1fb31fefb289f8aa3514377b98ea1d68b7ac3746a71f2e8474a7da2dd267aa1'),('1002','2','吴老师','男','2001','副教授','pbkdf2:sha256:150000$jwqThKCt$83bed964ea9996c057a31eda1dd742b708b5e868f5a9adf473794a0ea826de18'),('2000','5','郑老师','男','2000','教授','pbkdf2:sha256:150000$76KVi5v6$fb3a174d22738f863c8ca1677ce37d2085284b2c537c5198fa44990cfaf7709a'),('2001','7','徐老师','女','1999','副教授','pbkdf2:sha256:150000$yqHyPP7S$1e03c77b6564052c351a8fb1aea2bc45784749568823ea8aa2484ea530eb1026'),('2002','8','孙老师','男','1999','教授','pbkdf2:sha256:150000$Yk18mr5E$f185ba64d82644fed19a4f8d55552154e52486320a3c7604a15e028e4f4920ff');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `training_program`
--

DROP TABLE IF EXISTS `training_program`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `training_program` (
  `TPNumber` varchar(7) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`TPNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `training_program`
--

LOCK TABLES `training_program` WRITE;
/*!40000 ALTER TABLE `training_program` DISABLE KEYS */;
INSERT INTO `training_program` VALUES ('1'),('10'),('11'),('12'),('13'),('14'),('15'),('16'),('17'),('18'),('19'),('2'),('3'),('4'),('5'),('6'),('7'),('8'),('9');
/*!40000 ALTER TABLE `training_program` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-10 22:27:52
