-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: localhost    Database: studentHelperDB
-- ------------------------------------------------------
-- Server version	8.0.20-0ubuntu0.19.10.1

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

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add post',7,'add_post'),(26,'Can change post',7,'change_post'),(27,'Can delete post',7,'delete_post'),(28,'Can view post',7,'view_post'),(29,'Can add goals',8,'add_goals'),(30,'Can change goals',8,'change_goals'),(31,'Can delete goals',8,'delete_goals'),(32,'Can view goals',8,'view_goals'),(33,'Can add course',9,'add_course'),(34,'Can change course',9,'change_course'),(35,'Can delete course',9,'delete_course'),(36,'Can view course',9,'view_course'),(37,'Can add rules',10,'add_rules'),(38,'Can change rules',10,'change_rules'),(39,'Can delete rules',10,'delete_rules'),(40,'Can view rules',10,'view_rules'),(41,'Can add description',11,'add_description'),(42,'Can change description',11,'change_description'),(43,'Can delete description',11,'delete_description'),(44,'Can view description',11,'view_description'),(45,'Can add prediction',12,'add_prediction'),(46,'Can change prediction',12,'change_prediction'),(47,'Can delete prediction',12,'delete_prediction'),(48,'Can view prediction',12,'view_prediction'),(49,'Can add files',13,'add_files'),(50,'Can change files',13,'change_files'),(51,'Can delete files',13,'delete_files'),(52,'Can view files',13,'view_files'),(53,'Can add teacher',14,'add_teacher'),(54,'Can change teacher',14,'change_teacher'),(55,'Can delete teacher',14,'delete_teacher'),(56,'Can view teacher',14,'view_teacher'),(57,'Can add events',15,'add_events'),(58,'Can change events',15,'change_events'),(59,'Can delete events',15,'delete_events'),(60,'Can view events',15,'view_events');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$216000$NAhpX6XUxCX3$4Knugp0qKoYyyqmf+39ZZXXiPiZIjCbAbHguZkAgHYY=',NULL,0,'john','','','jlennon@beatles.com',0,1,'2020-11-14 14:09:37.234418');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(9,'studentHelper','course'),(11,'studentHelper','description'),(15,'studentHelper','events'),(13,'studentHelper','files'),(8,'studentHelper','goals'),(7,'studentHelper','post'),(12,'studentHelper','prediction'),(10,'studentHelper','rules'),(14,'studentHelper','teacher');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-11-14 14:00:29.399848'),(2,'auth','0001_initial','2020-11-14 14:00:36.666842'),(3,'admin','0001_initial','2020-11-14 14:01:06.626598'),(4,'admin','0002_logentry_remove_auto_add','2020-11-14 14:01:11.919109'),(5,'admin','0003_logentry_add_action_flag_choices','2020-11-14 14:01:12.066708'),(6,'contenttypes','0002_remove_content_type_name','2020-11-14 14:01:20.428666'),(7,'auth','0002_alter_permission_name_max_length','2020-11-14 14:01:29.567062'),(8,'auth','0003_alter_user_email_max_length','2020-11-14 14:01:33.580877'),(9,'auth','0004_alter_user_username_opts','2020-11-14 14:01:34.438118'),(10,'auth','0005_alter_user_last_login_null','2020-11-14 14:01:38.509298'),(11,'auth','0006_require_contenttypes_0002','2020-11-14 14:01:38.660111'),(12,'auth','0007_alter_validators_add_error_messages','2020-11-14 14:01:38.842576'),(13,'auth','0008_alter_user_username_max_length','2020-11-14 14:01:44.870540'),(14,'auth','0009_alter_user_last_name_max_length','2020-11-14 14:01:50.056606'),(15,'auth','0010_alter_group_name_max_length','2020-11-14 14:01:51.898066'),(16,'auth','0011_update_proxy_permissions','2020-11-14 14:01:52.702768'),(17,'auth','0012_alter_user_first_name_max_length','2020-11-14 14:02:02.563374'),(18,'sessions','0001_initial','2020-11-14 14:02:04.597979'),(19,'studentHelper','0001_initial','2020-11-14 14:02:07.830884'),(20,'studentHelper','0002_auto_20201114_1420','2020-11-14 14:23:14.509673');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_course`
--

DROP TABLE IF EXISTS `studentHelper_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ECTS` int NOT NULL,
  `name` varchar(30) NOT NULL,
  `type` varchar(1) NOT NULL,
  `client_id_id` int NOT NULL,
  `teacher_id_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studentHelper_course_teacher_id_id_96997163_fk_studentHe` (`teacher_id_id`),
  KEY `studentHelper_course_client_id_id_a6dae177_fk_auth_user_id` (`client_id_id`),
  CONSTRAINT `studentHelper_course_client_id_id_a6dae177_fk_auth_user_id` FOREIGN KEY (`client_id_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `studentHelper_course_teacher_id_id_96997163_fk_studentHe` FOREIGN KEY (`teacher_id_id`) REFERENCES `studentHelper_teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_course`
--

LOCK TABLES `studentHelper_course` WRITE;
/*!40000 ALTER TABLE `studentHelper_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_description`
--

DROP TABLE IF EXISTS `studentHelper_description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_description` (
  `event_id_id` int NOT NULL,
  `course` tinyint(1) NOT NULL,
  `description` varchar(128) NOT NULL,
  PRIMARY KEY (`event_id_id`),
  CONSTRAINT `studentHelper_descri_event_id_id_e65860cf_fk_studentHe` FOREIGN KEY (`event_id_id`) REFERENCES `studentHelper_events` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_description`
--

LOCK TABLES `studentHelper_description` WRITE;
/*!40000 ALTER TABLE `studentHelper_description` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_description` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_events`
--

DROP TABLE IF EXISTS `studentHelper_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `period_type` varchar(7) NOT NULL,
  `client_id_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studentHelper_events_client_id_id_6650fdeb_fk_auth_user_id` (`client_id_id`),
  CONSTRAINT `studentHelper_events_client_id_id_6650fdeb_fk_auth_user_id` FOREIGN KEY (`client_id_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_events`
--

LOCK TABLES `studentHelper_events` WRITE;
/*!40000 ALTER TABLE `studentHelper_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_files`
--

DROP TABLE IF EXISTS `studentHelper_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_path` varchar(30) NOT NULL,
  `description` varchar(64) NOT NULL,
  `course_id_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studentHelper_files_course_id_id_8e0f7b2a_fk_studentHe` (`course_id_id`),
  CONSTRAINT `studentHelper_files_course_id_id_8e0f7b2a_fk_studentHe` FOREIGN KEY (`course_id_id`) REFERENCES `studentHelper_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_files`
--

LOCK TABLES `studentHelper_files` WRITE;
/*!40000 ALTER TABLE `studentHelper_files` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_goals`
--

DROP TABLE IF EXISTS `studentHelper_goals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_goals` (
  `id` int NOT NULL AUTO_INCREMENT,
  `end_date` date NOT NULL,
  `type` varchar(1) NOT NULL,
  `description` varchar(128) NOT NULL,
  `course_id_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studentHelper_goals_course_id_id_728af238_fk_studentHe` (`course_id_id`),
  CONSTRAINT `studentHelper_goals_course_id_id_728af238_fk_studentHe` FOREIGN KEY (`course_id_id`) REFERENCES `studentHelper_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_goals`
--

LOCK TABLES `studentHelper_goals` WRITE;
/*!40000 ALTER TABLE `studentHelper_goals` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_goals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_prediction`
--

DROP TABLE IF EXISTS `studentHelper_prediction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_prediction` (
  `id` int NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `pred_time` time(6) NOT NULL,
  `actual_time` time(6) NOT NULL,
  `course_id_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `studentHelper_predic_course_id_id_80138ad6_fk_studentHe` (`course_id_id`),
  CONSTRAINT `studentHelper_predic_course_id_id_80138ad6_fk_studentHe` FOREIGN KEY (`course_id_id`) REFERENCES `studentHelper_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_prediction`
--

LOCK TABLES `studentHelper_prediction` WRITE;
/*!40000 ALTER TABLE `studentHelper_prediction` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_prediction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_rules`
--

DROP TABLE IF EXISTS `studentHelper_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_rules` (
  `course_id_id` int NOT NULL,
  `group` tinyint(1) NOT NULL,
  `lab_elements` int NOT NULL,
  `exer_elements` int NOT NULL,
  `lect_elements` int NOT NULL,
  `lab_weight` int NOT NULL,
  `exer_weight` int NOT NULL,
  `lect_weight` int NOT NULL,
  `formula` varchar(30) NOT NULL,
  PRIMARY KEY (`course_id_id`),
  CONSTRAINT `studentHelper_rules_course_id_id_fd9ea872_fk_studentHe` FOREIGN KEY (`course_id_id`) REFERENCES `studentHelper_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_rules`
--

LOCK TABLES `studentHelper_rules` WRITE;
/*!40000 ALTER TABLE `studentHelper_rules` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentHelper_teacher`
--

DROP TABLE IF EXISTS `studentHelper_teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentHelper_teacher` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `surname` varchar(30) NOT NULL,
  `title` varchar(30) NOT NULL,
  `webpage` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentHelper_teacher`
--

LOCK TABLES `studentHelper_teacher` WRITE;
/*!40000 ALTER TABLE `studentHelper_teacher` DISABLE KEYS */;
/*!40000 ALTER TABLE `studentHelper_teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-14 15:28:26
