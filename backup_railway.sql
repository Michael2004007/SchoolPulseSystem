-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: railway
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `alumno`
--

DROP TABLE IF EXISTS `alumno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alumno` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `curso` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alumno`
--

LOCK TABLES `alumno` WRITE;
/*!40000 ALTER TABLE `alumno` DISABLE KEYS */;
INSERT INTO `alumno` VALUES (1,'OSCAR','DOS SANTOS','4'),(2,'MILENE ','FERRARI','3'),(3,'Oscar','Dos Santos','4 A'),(4,'Mikaela','Dos Santos','4 A'),(5,'Ivan','Dario','4 A');
/*!40000 ALTER TABLE `alumno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cobro`
--

DROP TABLE IF EXISTS `cobro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cobro` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pulsera_id` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_cobro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `pulsera_id` (`pulsera_id`),
  CONSTRAINT `cobro_ibfk_1` FOREIGN KEY (`pulsera_id`) REFERENCES `pulsera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobro`
--

LOCK TABLES `cobro` WRITE;
/*!40000 ALTER TABLE `cobro` DISABLE KEYS */;
INSERT INTO `cobro` VALUES (1,7,20000.00,'2026-04-26 14:26:53'),(2,8,20000.00,'2026-04-26 14:27:04');
/*!40000 ALTER TABLE `cobro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pulsera`
--

DROP TABLE IF EXISTS `pulsera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pulsera` (
  `id` int NOT NULL,
  `estado` enum('disponible','repartida','pagada') DEFAULT 'disponible',
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pulsera`
--

LOCK TABLES `pulsera` WRITE;
/*!40000 ALTER TABLE `pulsera` DISABLE KEYS */;
INSERT INTO `pulsera` VALUES (1,'repartida','2026-04-26 14:25:36'),(2,'repartida','2026-04-26 14:25:36'),(3,'repartida','2026-04-26 14:25:36'),(4,'repartida','2026-04-26 14:25:36'),(5,'repartida','2026-04-26 14:25:36'),(6,'repartida','2026-04-26 14:25:36'),(7,'pagada','2026-04-26 14:25:36'),(8,'pagada','2026-04-26 14:25:36'),(9,'repartida','2026-04-26 14:25:36'),(10,'repartida','2026-04-26 14:25:36'),(11,'repartida','2026-04-26 14:58:49'),(12,'repartida','2026-04-26 14:58:49'),(13,'repartida','2026-04-26 14:58:49'),(14,'repartida','2026-04-26 14:58:49'),(15,'repartida','2026-04-26 14:58:49'),(16,'repartida','2026-04-26 14:58:49'),(17,'repartida','2026-04-26 14:58:49'),(18,'repartida','2026-04-26 14:58:49'),(19,'repartida','2026-04-26 14:58:49'),(20,'repartida','2026-04-26 14:58:49'),(21,'disponible','2026-04-26 14:58:49'),(22,'disponible','2026-04-26 14:58:49'),(23,'disponible','2026-04-26 14:58:49'),(24,'disponible','2026-04-26 14:58:49'),(25,'disponible','2026-04-26 14:58:49'),(26,'disponible','2026-04-26 14:58:49'),(27,'disponible','2026-04-26 14:58:49'),(28,'disponible','2026-04-26 14:58:49'),(29,'disponible','2026-04-26 14:58:49'),(30,'disponible','2026-04-26 14:58:49'),(31,'disponible','2026-04-26 14:58:49'),(32,'disponible','2026-04-26 14:58:49'),(33,'disponible','2026-04-26 14:58:49'),(34,'disponible','2026-04-26 14:58:49'),(35,'disponible','2026-04-26 14:58:49'),(36,'disponible','2026-04-26 14:58:49'),(37,'disponible','2026-04-26 14:58:49'),(38,'disponible','2026-04-26 14:58:49'),(39,'disponible','2026-04-26 14:58:49'),(40,'disponible','2026-04-26 14:58:49'),(41,'disponible','2026-04-26 14:58:49'),(42,'disponible','2026-04-26 14:58:49'),(43,'disponible','2026-04-26 14:58:49'),(44,'disponible','2026-04-26 14:58:49'),(45,'disponible','2026-04-26 14:58:49'),(46,'disponible','2026-04-26 14:58:49'),(47,'disponible','2026-04-26 14:58:49'),(48,'disponible','2026-04-26 14:58:49'),(49,'disponible','2026-04-26 14:58:49'),(50,'disponible','2026-04-26 14:58:49');
/*!40000 ALTER TABLE `pulsera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reparto`
--

DROP TABLE IF EXISTS `reparto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reparto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `alumno_id` int NOT NULL,
  `pulsera_id` int NOT NULL,
  `fecha_reparto` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `alumno_id` (`alumno_id`),
  KEY `pulsera_id` (`pulsera_id`),
  CONSTRAINT `reparto_ibfk_1` FOREIGN KEY (`alumno_id`) REFERENCES `alumno` (`id`),
  CONSTRAINT `reparto_ibfk_2` FOREIGN KEY (`pulsera_id`) REFERENCES `pulsera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reparto`
--

LOCK TABLES `reparto` WRITE;
/*!40000 ALTER TABLE `reparto` DISABLE KEYS */;
INSERT INTO `reparto` VALUES (1,1,1,'2026-04-26 14:25:54'),(2,1,2,'2026-04-26 14:25:54'),(3,1,3,'2026-04-26 14:25:54'),(4,1,4,'2026-04-26 14:25:54'),(5,1,5,'2026-04-26 14:25:54'),(6,2,6,'2026-04-26 14:26:09'),(7,2,7,'2026-04-26 14:26:09'),(8,2,8,'2026-04-26 14:26:09'),(9,2,9,'2026-04-26 14:26:09'),(10,2,10,'2026-04-26 14:26:09'),(11,3,11,'2026-04-26 14:59:34'),(12,3,12,'2026-04-26 14:59:34'),(13,3,13,'2026-04-26 14:59:34'),(14,3,14,'2026-04-26 14:59:34'),(15,3,15,'2026-04-26 14:59:34'),(16,4,17,'2026-04-26 15:00:02'),(17,4,18,'2026-04-26 15:00:02'),(18,4,19,'2026-04-26 15:00:02'),(19,4,20,'2026-04-26 15:00:02'),(20,5,16,'2026-04-26 15:03:34');
/*!40000 ALTER TABLE `reparto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` varchar(20) DEFAULT 'admin',
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Oscar','Oscar123','admin','Administrador'),(2,'Milene','123456','porton','Milene');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-26 17:41:29
