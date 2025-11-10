-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: vcms
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `Action` varchar(50) DEFAULT NULL,
  `TableName` varchar(50) DEFAULT NULL,
  `RecordID` int DEFAULT NULL,
  `LogDetails` text,
  `Timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`LogID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,'DELETE','REPO',10,'Repo deleted: Name=Deleting a repo, OwnerID=6','2025-11-06 09:33:33'),(2,'DELETE','REPO',12,'Repo deleted: Name=Dbms demo, OwnerID=6','2025-11-10 09:09:24'),(3,'DELETE','REPO',9,'Repo deleted: Name=DBMS miniproject, OwnerID=6','2025-11-10 16:55:27'),(4,'DELETE','REPO',8,'Repo deleted: Name=ChatApp, OwnerID=5','2025-11-10 18:38:55');
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branch` (
  `BID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `CreatedOn` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreatedBy` int NOT NULL,
  `RID` int NOT NULL,
  `Status` varchar(50) DEFAULT 'Active',
  `CommitCount` int DEFAULT '0',
  PRIMARY KEY (`BID`),
  KEY `CreatedBy` (`CreatedBy`),
  KEY `RID` (`RID`),
  CONSTRAINT `branch_ibfk_1` FOREIGN KEY (`CreatedBy`) REFERENCES `user` (`UID`) ON DELETE CASCADE,
  CONSTRAINT `branch_ibfk_2` FOREIGN KEY (`RID`) REFERENCES `repo` (`RID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES (1,'main','2025-10-03 19:55:07',1,1,'Active',2),(2,'feature/add-caching','2025-10-03 19:55:07',1,1,'Active',1),(3,'main','2025-10-03 19:55:07',1,2,'Active',1),(4,'develop','2025-10-03 19:55:07',2,2,'Active',1),(5,'main','2025-10-03 19:55:07',2,3,'Active',1),(6,'main','2025-10-03 19:55:07',3,4,'Active',1),(7,'main','2025-10-03 19:55:07',1,5,'Active',1),(8,'main','2025-10-03 19:55:07',4,6,'Active',1),(9,'main','2025-10-03 19:55:07',2,7,'Active',1),(10,'feature/payment-gateway','2025-10-03 19:55:07',4,7,'Active',1),(15,'main','2025-11-06 09:35:50',7,11,'Active',0),(17,'feature/login','2025-11-10 18:30:29',2,1,'Active',0);
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch_files`
--

DROP TABLE IF EXISTS `branch_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branch_files` (
  `BID` int NOT NULL,
  `FID` int NOT NULL,
  PRIMARY KEY (`BID`,`FID`),
  KEY `FID` (`FID`),
  CONSTRAINT `branch_files_ibfk_1` FOREIGN KEY (`BID`) REFERENCES `branch` (`BID`) ON DELETE CASCADE,
  CONSTRAINT `branch_files_ibfk_2` FOREIGN KEY (`FID`) REFERENCES `file` (`FID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch_files`
--

LOCK TABLES `branch_files` WRITE;
/*!40000 ALTER TABLE `branch_files` DISABLE KEYS */;
INSERT INTO `branch_files` VALUES (1,1),(2,1),(17,1),(1,2),(2,2),(17,2),(1,3),(2,3),(3,3),(4,3),(5,3),(17,3),(3,4),(4,4),(4,5),(5,6),(6,7),(6,8),(7,9),(8,10),(9,11),(10,11),(2,13);
/*!40000 ALTER TABLE `branch_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `can_have`
--

DROP TABLE IF EXISTS `can_have`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `can_have` (
  `RID` int NOT NULL,
  `BID` int NOT NULL,
  `CID` int NOT NULL,
  `Message` text,
  PRIMARY KEY (`RID`,`BID`,`CID`),
  KEY `BID` (`BID`),
  KEY `CID` (`CID`),
  CONSTRAINT `can_have_ibfk_1` FOREIGN KEY (`RID`) REFERENCES `repo` (`RID`) ON DELETE CASCADE,
  CONSTRAINT `can_have_ibfk_2` FOREIGN KEY (`BID`) REFERENCES `branch` (`BID`) ON DELETE CASCADE,
  CONSTRAINT `can_have_ibfk_3` FOREIGN KEY (`CID`) REFERENCES `commit` (`CID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `can_have`
--

LOCK TABLES `can_have` WRITE;
/*!40000 ALTER TABLE `can_have` DISABLE KEYS */;
INSERT INTO `can_have` VALUES (1,1,1,'Initial commit: Setup web server structure'),(1,1,2,'Add request handler logic'),(1,2,12,'Add caching layer implementation'),(2,3,3,'Initial commit for mobile app'),(2,4,4,'Add task data model'),(3,5,5,'Initial commit for data analyzer'),(4,6,6,'Initial commit for game engine'),(5,7,7,'Initial commit for blog'),(6,8,8,'Initial commit for learning platform'),(7,9,9,'Initial commit for e-commerce site'),(7,10,10,'Add payment gateway integration');
/*!40000 ALTER TABLE `can_have` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `can_modify`
--

DROP TABLE IF EXISTS `can_modify`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `can_modify` (
  `RID` int NOT NULL,
  `CID` int NOT NULL,
  PRIMARY KEY (`RID`,`CID`),
  KEY `CID` (`CID`),
  CONSTRAINT `can_modify_ibfk_1` FOREIGN KEY (`RID`) REFERENCES `repo` (`RID`) ON DELETE CASCADE,
  CONSTRAINT `can_modify_ibfk_2` FOREIGN KEY (`CID`) REFERENCES `commit` (`CID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `can_modify`
--

LOCK TABLES `can_modify` WRITE;
/*!40000 ALTER TABLE `can_modify` DISABLE KEYS */;
INSERT INTO `can_modify` VALUES (1,1),(1,2),(2,3),(2,4),(3,5),(4,6),(5,7),(6,8),(7,9),(7,10),(1,12);
/*!40000 ALTER TABLE `can_modify` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commit`
--

DROP TABLE IF EXISTS `commit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commit` (
  `CID` int NOT NULL AUTO_INCREMENT,
  `Message` text,
  `CommitTime` time NOT NULL,
  `CommitDate` date NOT NULL,
  `BID` int NOT NULL,
  `UID` int NOT NULL,
  PRIMARY KEY (`CID`),
  KEY `BID` (`BID`),
  KEY `UID` (`UID`),
  CONSTRAINT `commit_ibfk_1` FOREIGN KEY (`BID`) REFERENCES `branch` (`BID`) ON DELETE CASCADE,
  CONSTRAINT `commit_ibfk_2` FOREIGN KEY (`UID`) REFERENCES `user` (`UID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commit`
--

LOCK TABLES `commit` WRITE;
/*!40000 ALTER TABLE `commit` DISABLE KEYS */;
INSERT INTO `commit` VALUES (1,'Initial commit: Setup web server structure','10:00:00','2024-01-11',1,1),(2,'Add request handler logic','11:30:00','2024-01-12',1,1),(3,'Initial commit for mobile app','14:00:00','2024-02-20',3,1),(4,'Add task data model','15:00:00','2024-02-21',4,2),(5,'Initial commit for data analyzer','16:00:00','2024-03-25',5,2),(6,'Initial commit for game engine','18:00:00','2024-04-10',6,3),(7,'Initial commit for blog','10:00:00','2024-05-15',7,1),(8,'Initial commit for learning platform','11:00:00','2024-06-01',8,4),(9,'Initial commit for e-commerce site','14:00:00','2024-06-10',9,2),(10,'Add payment gateway integration','17:00:00','2024-06-12',10,4),(12,'Add caching layer implementation','09:00:00','2024-01-15',2,1),(13,'Add user authentication','10:30:00','2025-10-08',3,1),(16,'This is a test commit to fire the trigger','18:32:08','2025-11-10',1,3);
/*!40000 ALTER TABLE `commit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `file` (
  `FID` int NOT NULL AUTO_INCREMENT,
  `FileName` varchar(255) NOT NULL,
  `FilePath` text NOT NULL,
  `FileSize` int DEFAULT NULL,
  `FileType` varchar(50) DEFAULT NULL,
  `CreatedBy` int NOT NULL,
  `CreatedOn` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`FID`),
  KEY `CreatedBy` (`CreatedBy`),
  CONSTRAINT `file_ibfk_1` FOREIGN KEY (`CreatedBy`) REFERENCES `user` (`UID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file`
--

LOCK TABLES `file` WRITE;
/*!40000 ALTER TABLE `file` DISABLE KEYS */;
INSERT INTO `file` VALUES (1,'server.py','/src/server.py',5120,'Python',1,'2025-10-03 19:55:18'),(2,'handler.py','/src/handler.py',2048,'Python',1,'2025-10-03 19:55:18'),(3,'README.md','/README.md',1024,'Markdown',1,'2025-10-03 19:55:18'),(4,'main.dart','/lib/main.dart',8192,'Dart',1,'2025-10-03 19:55:18'),(5,'task_model.dart','/lib/models/task.dart',1536,'Dart',2,'2025-10-03 19:55:18'),(6,'parser.py','/scripts/parser.py',4096,'Python',2,'2025-10-03 19:55:18'),(7,'main.cpp','/src/main.cpp',10240,'C++',3,'2025-10-03 19:55:18'),(8,'player.h','/include/player.h',2048,'C++',3,'2025-10-03 19:55:18'),(9,'index.html','/public/index.html',3072,'HTML',1,'2025-10-03 19:55:18'),(10,'api.js','/src/api.js',6144,'JavaScript',4,'2025-10-03 19:55:18'),(11,'checkout.js','/src/checkout.js',4096,'JavaScript',2,'2025-10-03 19:55:18'),(12,'server.js','/server.js',3584,'JavaScript',5,'2025-10-03 19:55:18'),(13,'cache.py','/src/cache.py',1800,'Python',1,'2025-10-03 19:55:18');
/*!40000 ALTER TABLE `file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repo`
--

DROP TABLE IF EXISTS `repo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repo` (
  `RID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Description` text,
  `Visibility` enum('Public','Private') NOT NULL DEFAULT 'Public',
  `CreatedOn` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `OwnerID` int NOT NULL,
  PRIMARY KEY (`RID`),
  KEY `OwnerID` (`OwnerID`),
  CONSTRAINT `repo_ibfk_1` FOREIGN KEY (`OwnerID`) REFERENCES `user` (`UID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repo`
--

LOCK TABLES `repo` WRITE;
/*!40000 ALTER TABLE `repo` DISABLE KEYS */;
INSERT INTO `repo` VALUES (1,'WebServer','A multi-threaded web server in Python.','Public','2025-10-03 19:54:54',1),(2,'MobileApp','A cross-platform mobile application for task management.','Private','2025-10-03 19:54:54',1),(3,'DataAnalyzer','Scripts for parsing and analyzing large datasets.','Public','2025-10-03 19:54:54',2),(4,'GameEngine','A simple 2D game engine built with C++.','Public','2025-10-03 19:54:54',3),(5,'PersonalBlog','Source code for my personal blog website.','Public','2025-10-03 19:54:54',1),(6,'LearningPlatform','An online platform for interactive courses.','Private','2025-10-03 19:54:54',4),(7,'ECommerceSite','A full-featured e-commerce website backend.','Private','2025-10-03 19:54:54',2),(11,'trying to delete this also ','','Public','2025-11-06 09:35:50',7);
/*!40000 ALTER TABLE `repo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `ReqID` int NOT NULL AUTO_INCREMENT,
  `RequestType` varchar(50) DEFAULT NULL,
  `Status` varchar(50) DEFAULT 'Open',
  `CreatedOn` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreatedBy` int NOT NULL,
  `ClosedOn` datetime DEFAULT NULL,
  `RID` int NOT NULL,
  PRIMARY KEY (`ReqID`),
  KEY `CreatedBy` (`CreatedBy`),
  KEY `RID` (`RID`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`CreatedBy`) REFERENCES `user` (`UID`) ON DELETE CASCADE,
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`RID`) REFERENCES `repo` (`RID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (1,'Pull','Open','2025-10-03 19:56:54',2,NULL,2),(2,'Pull','Closed','2025-10-03 19:56:54',4,NULL,7),(3,'Pull','Open','2025-10-03 19:56:54',1,NULL,1);
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `UID` int NOT NULL AUTO_INCREMENT,
  `Fname` varchar(100) NOT NULL,
  `Lname` varchar(100) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `Phoneno` varchar(20) DEFAULT NULL,
  `DateJoined` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Vipul','Bohra','hashed_password_1','111-222-3333','2024-01-10 09:00:00'),(2,'Sumit','Nair','hashed_password_2','222-333-4444','2024-02-15 11:30:00'),(3,'Vishnu','L','hashed_password_3','333-444-5555','2024-03-20 14:00:00'),(4,'Sohil','N','hashed_password_4','444-555-6666','2024-04-05 16:45:00'),(5,'YatharthAA','Aarush','hashed_password_5','555-666-7777','2024-05-12 18:20:00'),(6,'Vipul','Bohra','a8ac1586c3b935fec79d09395cd24faaa7cb4f1aa954db8b1d7e6944920cf954','+917795213241','2025-11-05 14:10:35'),(7,'Sumit Santhosh','Nair','720baa820ff71219c479005c903b140e23010b09c4e5a1a07e6377fad1438a3a','+91 81528 73333','2025-11-06 09:35:11');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_email`
--

DROP TABLE IF EXISTS `user_email`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_email` (
  `UID` int NOT NULL,
  `Email` varchar(255) NOT NULL,
  PRIMARY KEY (`UID`,`Email`),
  CONSTRAINT `user_email_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `user` (`UID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_email`
--

LOCK TABLES `user_email` WRITE;
/*!40000 ALTER TABLE `user_email` DISABLE KEYS */;
INSERT INTO `user_email` VALUES (1,'vbohra@work.com'),(1,'vipul.b@example.com'),(2,'sumit.n@example.com'),(3,'vishnu.l@example.com'),(4,'sohil.n@example.com'),(5,'yatharth.a@example.com'),(6,'bohravipul05@gmail.com'),(7,'sumitnair731@gmail.com');
/*!40000 ALTER TABLE `user_email` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-10 18:55:30
