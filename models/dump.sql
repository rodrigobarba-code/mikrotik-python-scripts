/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.4.3-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: sevensuite
-- ------------------------------------------------------
-- Server version	11.4.3-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `regions`
--

DROP TABLE IF EXISTS `regions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `regions` (
  `region_id` int(11) NOT NULL AUTO_INCREMENT,
  `region_name` varchar(128) NOT NULL,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regions`
--

LOCK TABLES `regions` WRITE;
/*!40000 ALTER TABLE `regions` DISABLE KEYS */;
INSERT INTO `regions` VALUES
(1,'Mexicali'),
(2,'San Luis'),
(3,'Tecate'),
(4,'San Felipe'),
(5,'Obregon'),
(6,'Tijuana'),
(7,'Rosarito'),
(8,'Ensenada'),
(9,'San Diego'),
(10,'Hermosillo');
/*!40000 ALTER TABLE `regions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites` (
  `site_id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_region_id` int(11) NOT NULL,
  `site_name` varchar(128) NOT NULL,
  `site_segment` int(11) NOT NULL,
  PRIMARY KEY (`site_id`),
  KEY `fk_region_id` (`fk_region_id`),
  CONSTRAINT `sites_ibfk_1` FOREIGN KEY (`fk_region_id`) REFERENCES `regions` (`region_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sites`
--

LOCK TABLES `sites` WRITE;
/*!40000 ALTER TABLE `sites` DISABLE KEYS */;
INSERT INTO `sites` VALUES
(1,1,'Robledo',1),
(2,1,'Alamitos',2),
(3,1,'Alfareros',3),
(4,1,'Queretaro',4),
(5,1,'Castellon',5),
(6,1,'Silva',6),
(7,1,'Aeropuerto',7),
(8,1,'Emmsa',8),
(9,2,'Poder Uno',9),
(10,1,'Hidalgo',12),
(11,3,'Rumorosa',13),
(12,1,'Polvora',15),
(13,4,'San Felipe',17),
(14,1,'Saturno',174),
(15,5,'Central',60),
(16,6,'Otay',101),
(17,6,'Fussion',102),
(18,6,'Pacifico',103),
(19,3,'Cerro Bola',105),
(20,6,'Colorado',106),
(21,6,'Cuichillas',107),
(22,7,'Rosarito',108),
(23,7,'Rosartito 2',491),
(24,6,'Vallarta',109),
(25,6,'Oaxaca',492),
(26,6,'Cuahutemoc',118),
(27,6,'Playas',493),
(28,6,'Cosmopolitan',123),
(29,8,'Punta Banda',128),
(30,8,'Cerro Viejo',129),
(31,6,'El Roble',133),
(32,9,'San Diego',140),
(33,10,'Hermosillo',200);
/*!40000 ALTER TABLE `sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `routers`
--

DROP TABLE IF EXISTS `routers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `routers` (
  `router_id` int(11) NOT NULL AUTO_INCREMENT,
  `router_name` varchar(128) NOT NULL,
  `router_description` varchar(256) NOT NULL,
  `router_brand` varchar(128) NOT NULL,
  `router_model` varchar(128) NOT NULL,
  `router_serial` varchar(128) DEFAULT NULL,
  `fk_site_id` int(11) NOT NULL,
  `router_ip` varchar(16) NOT NULL,
  `router_mac` varchar(32) NOT NULL,
  `router_username` varchar(128) NOT NULL,
  `router_password` varchar(128) NOT NULL,
  `allow_scan` int(11) NOT NULL,
  PRIMARY KEY (`router_id`),
  KEY `fk_site_id` (`fk_site_id`),
  CONSTRAINT `routers_ibfk_1` FOREIGN KEY (`fk_site_id`) REFERENCES `sites` (`site_id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `routers`
--

LOCK TABLES `routers` WRITE;
/*!40000 ALTER TABLE `routers` DISABLE KEYS */;
INSERT INTO `routers` VALUES
(1,'Robledo','Mexicali','Mikrotik','CCR1036-8G-2S+','N/S',1,'10.1.4.254','C4:AD:34:6A:53:27','SevenSR7','TxH24_g8zF',1),
(2,'Alamitos','Mexicali','Mikrotik','CCR2116-12G-4S+','N/S',2,'10.2.4.254','78:9A:18:F2:D0:C5','SevenSR7','TxH24_g8zF',1),
(3,'Alfareros','Mexicali','Mikrotik','CCR1036-8G-2S+','N/S',3,'10.3.4.254','DC:2C:6E:7A:D7:1A','SevenSR7','TxH24_g8zF',1),
(4,'Queretaro','Mexicali','Mikrotik','CCR1016-12G','N/S',4,'10.4.4.254','00:0C:42:C7:45:EF','SevenSR7','TxH24_g8zF',1),
(5,'Castellon','Mexicali','Mikrotik','RB4011iGS+','N/S',5,'10.5.4.254','C4:AD:34:33:C3:0E','SevenSR7','TxH24_g8zF',1),
(6,'Silva','Mexicali','Mikrotik','RB3011UiAS','N/S',6,'10.6.4.254','6C:3B:6B:F7:5E:47','SevenSR7','TxH24_g8zF',1),
(7,'Aeropuerto','Mexicali','Mikrotik','CCR1009-8G-1S','N/S',7,'10.7.4.254','E4:8D:8C:3D:72:BA','SevenSR7','TxH24_g8zF',1),
(8,'Emmsa','Mexicali','Mikrotik','RB3011UiAS','N/S',8,'10.8.4.254','74:4D:28:19:D1:00','SevenSR7','TxH24_g8zF',1),
(9,'Poder Uno','San Luis','Mikrotik','CCR1009-7G-1C','N/S',9,'10.9.4.254','64:D1:54:EE:C3:2E','SevenSR7','TxH24_g8zF',1),
(10,'Hidalgo','Mexicali','Mikrotik','RB3011UiAS','N/S',10,'10.12.4.254','6C:3B:6B:F7:74:AA','SevenSR7','TxH24_g8zF',1),
(11,'Rumorosa','Tecate','Mikrotik','RB3011UiAS','N/S',11,'10.13.4.254','CC:2D:E0:CD:26:19','SevenSR7','TxH24_g8zF',1),
(12,'Polvora','Mexicali','Mikrotik','CCR1036-8G-2S+','N/S',12,'10.15.4.254','08:55:31:35:B3:C2','SevenSR7','TxH24_g8zF',1),
(13,'San Felipe','San Felipe','Mikrotik','RB951Ui-2HnD','N/S',13,'10.17.4.254','6C:3B:6B:F7:4E:0C','SevenSR7','TxH24_g8zF',1),
(14,'Saturno','Mexicali','Mikrotik','CCR1009-8G-1S-1S+','N/S',14,'201.174.15.66','6C:3B:6B:1B:CA:94','SevenSR7','TxH24_g8zF',1),
(15,'Central','Obregon','Mikrotik','RB1100AHx2','N/S',15,'10.60.4.254','E4:8D:8C:1F:44:8E','SevenSR7','TxH24_g8zF',1),
(16,'Otay','Tijuana','Mikrotik','CCR1016-12G','N/S',16,'10.101.4.254','E4:8D:8C:1A:EE:7C','SevenSR7','TxH24_g8zF',1),
(17,'Fussion','Tijuana','Mikrotik','CCR1036-8G-2S+','N/S',17,'10.102.4.254','18:FD:74:0D:A7:D2','SevenSR7','TxH24_g8zF',1),
(18,'Pacifico','Tijuana','Mikrotik','RB3011UiAS','N/S',18,'10.103.4.254','6C:3B:6B:5C:A6:25','SevenSR7','TxH24_g8zF',1),
(19,'Cerro Bola','Tecate','Mikrotik','RB3011UiAS','N/S',19,'10.105.4.254','74:4D:28:37:46:D5','SevenSR7','TxH24_g8zF',1),
(20,'Colorado','Tijuana','Mikrotik','CCR1036-8G-2S+','N/S',20,'10.106.4.254','E4:8D:8C:3C:2E:C2','SevenSR7','TxH24_g8zF',1),
(21,'Cuichillas','Tijuana','Mikrotik','RB3011UiAS','N/S',21,'10.107.4.254','6C:3B:6B:7A:E6:E7','SevenSR7','TxH24_g8zF',1),
(22,'Rosarito','Rosarito','Mikrotik','RB4011iGS+','N/S',22,'10.108.4.254','74:4D:28:A6:55:2D','SevenSR7','TxH24_g8zF',1),
(23,'Rosartito 2','Rosarito','Mikrotik','RB3011UiAS','N/S',23,'10.49.0.22','74:4D:28:19:D1:55','SevenSR7','TxH24_g8zF',1),
(24,'Vallarta','Tijuana','Mikrotik','CCR1036-8G-2S+','N/S',24,'10.109.4.254','08:55:31:EB:33:4F','SevenSR7','TxH24_g8zF',1),
(25,'Oaxaca','Tijuana','Mikrotik','CCR1009-7G-1C','N/S',25,'10.49.0.146','64:D1:54:EC:FD:35','SevenSR7','TxH24_g8zF',1),
(26,'Cuahutemoc','Tijuana','Mikrotik','CCR1036-8G-2S+','N/S',26,'10.118.4.254','08:55:31:EB:2D:CA','SevenSR7','TxH24_g8zF',1),
(27,'Playas','Tijuana','Mikrotik','CCR1009-7G-1C-1S+','N/S',27,'10.49.0.21','6C:3B:6B:EF:1F:B4','SevenSR7','TxH24_g8zF',1),
(28,'Cosmopolitan','Tijuana','Mikrotik','CCR1036-12G-4S','N/S',28,'10.123.4.254','E4:8D:8C:31:FF:F8','SevenSR7','TxH24_g8zF',1),
(29,'Punta Banda','Ensenada','Mikrotik','RB1100AHx2','N/S',29,'10.128.4.254','4C:5E:0C:4E:A6:EB','SevenSR7','TxH24_g8zF',1),
(30,'Cerro Viejo','Ensenada','Mikrotik','CCR1016-12G','N/S',30,'10.129.4.254','6C:3B:6B:F4:EC:30','SevenSR7','TxH24_g8zF',1),
(31,'El Roble','Tijuana','Mikrotik','CCR2116-12G-4S+','N/S',31,'10.133.4.254','D4:01:C3:6B:75:DD','SevenSR7','TxH24_g8zF',1),
(32,'San Diego','San Diego','Mikrotik','CCR1009-7G-1C-1S+','N/S',32,'10.140.4.254','6C:3B:6B:EF:1F:BC','SevenSR7','TxH24_g8zF',1),
(33,'Hermosillo','Hermosillo','Mikrotik','RB3011UiAS','N/S',33,'10.200.4.254','6C:3B:6B:EF:74:CC','SevenSR7','TxH24_g8zF',1);
/*!40000 ALTER TABLE `routers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_username` varchar(128) NOT NULL,
  `user_password` varchar(128) NOT NULL,
  `user_name` varchar(128) NOT NULL,
  `user_lastname` varchar(128) NOT NULL,
  `user_privileges` varchar(128) NOT NULL,
  `user_state` int(11) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'sergio','root','Sergio Ivan','Castro Luna','admin',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-11-14  0:58:10
