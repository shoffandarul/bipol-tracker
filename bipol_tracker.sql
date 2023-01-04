-- MariaDB dump 10.19  Distrib 10.4.24-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: bipol_tracker
-- ------------------------------------------------------
-- Server version	10.4.24-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bipol`
--

DROP TABLE IF EXISTS `bipol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bipol` (
  `id_bipol` int(11) NOT NULL AUTO_INCREMENT,
  `plat_nomor` varchar(12) NOT NULL,
  `id_driver` int(11) NOT NULL,
  PRIMARY KEY (`id_bipol`),
  UNIQUE KEY `plat_nomor` (`plat_nomor`),
  KEY `id_driver` (`id_driver`) USING BTREE,
  CONSTRAINT `bipol_ibfk_1` FOREIGN KEY (`id_driver`) REFERENCES `driver` (`id_driver`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bipol`
--

LOCK TABLES `bipol` WRITE;
/*!40000 ALTER TABLE `bipol` DISABLE KEYS */;
INSERT INTO `bipol` VALUES (1,'B 2301 PNJ',2),(2,'B 2302 JNP',4),(3,'B 2303 NJP',5),(4,'B 2304 PJN',3),(5,'B 2305 JPN',1);
/*!40000 ALTER TABLE `bipol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driver`
--

DROP TABLE IF EXISTS `driver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `driver` (
  `id_driver` int(11) NOT NULL AUTO_INCREMENT,
  `nama` text NOT NULL,
  `username` varchar(12) NOT NULL,
  `password` varchar(12) NOT NULL,
  PRIMARY KEY (`id_driver`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driver`
--

LOCK TABLES `driver` WRITE;
/*!40000 ALTER TABLE `driver` DISABLE KEYS */;
INSERT INTO `driver` VALUES (1,'Burhan','burhand','123'),(2,'Ogah','ogahh','123'),(3,'Abdul','abdull','123'),(4,'Ijal','ijall','123'),(5,'Mamat','mamat','123');
/*!40000 ALTER TABLE `driver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jadwal`
--

DROP TABLE IF EXISTS `jadwal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jadwal` (
  `id_jadwal` int(11) NOT NULL AUTO_INCREMENT,
  `id_bipol` int(11) NOT NULL,
  `hari` varchar(6) NOT NULL,
  `waktu` time NOT NULL,
  `halte` text NOT NULL,
  PRIMARY KEY (`id_jadwal`),
  KEY `id_bipol` (`id_bipol`),
  CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`id_bipol`) REFERENCES `bipol` (`id_bipol`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jadwal`
--

LOCK TABLES `jadwal` WRITE;
/*!40000 ALTER TABLE `jadwal` DISABLE KEYS */;
INSERT INTO `jadwal` VALUES (1,1,'Senin','07:00:00','PNJ'),(2,1,'Senin','07:10:00','Pondok Cina'),(3,1,'Senin','07:20:00','Stasiun UI'),(4,1,'Senin','07:30:00','Pondok Cina'),(5,1,'Senin','07:40:00','PNJ'),(6,1,'Senin','07:50:00','Pondok Cina'),(7,1,'Senin','08:00:00','Stasiun UI'),(8,2,'Senin','07:05:00','PNJ'),(9,2,'Senin','07:15:00','Pondok Cina'),(10,2,'Senin','07:25:00','Stasiun UI'),(11,2,'Senin','07:35:00','Pondok Cina'),(12,2,'Senin','07:45:00','PNJ'),(13,2,'Senin','07:55:00','Pondok Cina'),(14,2,'Senin','08:05:00','Stasiun UI'),(15,3,'Senin','07:10:00','PNJ'),(16,3,'Senin','07:20:00','Pondok Cina'),(17,3,'Senin','07:30:00','Stasiun UI'),(18,3,'Senin','07:40:00','Pondok Cina'),(19,3,'Senin','07:50:00','PNJ'),(20,3,'Senin','08:00:00','Pondok Cina'),(21,3,'Senin','08:10:00','Stasiun UI'),(22,4,'Senin','07:20:00','PNJ'),(23,4,'Senin','07:30:00','Pondok Cina'),(24,4,'Senin','07:40:00','Stasiun UI'),(25,4,'Senin','07:50:00','Pondok Cina'),(26,4,'Senin','08:00:00','PNJ'),(27,4,'Senin','08:10:00','Pondok Cina'),(28,4,'Senin','08:20:00','Stasiun UI'),(29,5,'Senin','07:25:00','PNJ'),(30,5,'Senin','07:35:00','Pondok Cina'),(31,5,'Senin','07:45:00','Stasiun UI'),(32,5,'Senin','07:55:00','Pondok Cina'),(33,5,'Senin','08:05:00','PNJ'),(34,5,'Senin','08:15:00','Pondok Cina'),(35,5,'Senin','08:25:00','Stasiun UI');
/*!40000 ALTER TABLE `jadwal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posisi`
--

DROP TABLE IF EXISTS `posisi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posisi` (
  `id_bipol` int(11) NOT NULL,
  `posisi` text NOT NULL,
  `waktu` time NOT NULL,
  `kapasitas` varchar(8) NOT NULL,
  PRIMARY KEY (`id_bipol`) USING BTREE,
  CONSTRAINT `posisi_ibfk_1` FOREIGN KEY (`id_bipol`) REFERENCES `bipol` (`id_bipol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posisi`
--

LOCK TABLES `posisi` WRITE;
/*!40000 ALTER TABLE `posisi` DISABLE KEYS */;
INSERT INTO `posisi` VALUES (1,'Stasiun UI','08:20:00','Tersedia'),(2,'Pondok Cina','08:15:00','Tersedia'),(3,'Pondok Cina','08:20:00','Tersedia'),(4,'PNJ','08:15:00','Tersedia'),(5,'PNJ','08:20:00','Tersedia');
/*!40000 ALTER TABLE `posisi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-04  9:44:12
