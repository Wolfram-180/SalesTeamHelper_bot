-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: imagerfrobot_dev
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contacts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `email` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `phone` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `comment` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `manager_id` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (16,'gmail','mail@gmail.com','<нет данных>','<нет данных>',0);
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distributor`
--

DROP TABLE IF EXISTS `distributor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `distributor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `contact_distr_id` int DEFAULT '0',
  `contact_froneri_id` int DEFAULT '0',
  `froneri_cont_based_on_mail` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distributor`
--

LOCK TABLES `distributor` WRITE;
/*!40000 ALTER TABLE `distributor` DISABLE KEYS */;
INSERT INTO `distributor` VALUES (1,'Ашан',16,16,16),(2,'Магнит',16,16,16),(3,'Дикси',16,16,16),(4,'Лента',16,16,16),(6,'Окей',16,16,16),(7,'Билла',16,16,16),(8,'Магнолия',16,16,16),(9,'Метро',16,16,16),(14,'Перекресток',16,16,16),(13,'Карусель',16,16,16),(11,'Азбука Вкуса',16,16,16),(12,'Авоська',16,16,16),(15,'Пятерочка',16,16,16),(16,'Розничная точка',16,16,16);
/*!40000 ALTER TABLE `distributor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(45) COLLATE utf32_bin DEFAULT '',
  `street` varchar(45) COLLATE utf32_bin DEFAULT '',
  `bldng` varchar(45) COLLATE utf32_bin DEFAULT '',
  `id_distributor` int DEFAULT '0',
  `id_contact` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `street` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `bldng` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `distributor_id` int DEFAULT '0',
  `telegram_id` int DEFAULT '0',
  `distr_name` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `rep_text` varchar(500) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `phone` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `message4` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `report_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reports_in_process` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=59 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_parts`
--

DROP TABLE IF EXISTS `reports_parts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports_parts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_reports` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `report_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `text` varchar(500) COLLATE utf32_bin DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=63 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_parts`
--

LOCK TABLES `reports_parts` WRITE;
/*!40000 ALTER TABLE `reports_parts` DISABLE KEYS */;
INSERT INTO `reports_parts` VALUES (1,'29','2020-04-01 15:56:49','SKU: Экстрем, да вообще куча всго \n\n Сколько штук: Штук 20-30 \n\n Дополнительное описание: Это все '),(2,'29','2020-04-01 16:03:56','SKU: Да со всеми \n\n Сколько штук: Штук 35 \n\n Дополнительное описание: Неа '));
/*!40000 ALTER TABLE `reports_parts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-11-02 15:53:40
