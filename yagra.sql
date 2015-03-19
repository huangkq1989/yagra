-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: yagra
-- ------------------------------------------------------
-- Server version	5.1.73-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `yagra`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `yagra` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `yagra`;

--
-- Table structure for table `access_control`
--

DROP TABLE IF EXISTS `access_control`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `access_control` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `last_time` double DEFAULT '0',
  `allowance` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `access_control`
--

LOCK TABLES `access_control` WRITE;
/*!40000 ALTER TABLE `access_control` DISABLE KEYS */;
/*!40000 ALTER TABLE `access_control` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` char(32) COLLATE utf8_unicode_ci NOT NULL,
  `salt` char(32) COLLATE utf8_unicode_ci NOT NULL,
  `avatar_key` char(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `avatar_url` char(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `register_on` datetime DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `avatar_key` (`avatar_key`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (7,'huangkq','huangkq@foxmail.com','òýÏtœK¤?D«Zæ„–Eþ4öXxB|&£OÃÃ]','D’RÎ*É²Ò‚³Æ¬èjÔ×tµËWïÎ³–†´Û_','3a201a64275d381416d76205679426d6','000/000/0007.jpg','2015-03-19 22:26:07',1),(2,'huangkq123','huangkangquan1989@163.com','|™Þ/šh:­r#©(£C,Ýiw•[Y`ºåªB','Ýf%¥ÿ‹	ÇŠ¡$º°‘?¹©áÕn]?Òú¡è‹b','a23bf19576d064ef52ef79dca9e7c573','000/000/0002.jpg','2015-03-19 11:29:23',1),(3,'yagra_admin','yagra_admin@163.com','öT*5ÖQ-?ñu¾nvñ‚3ËŒùyü,8Œc{/§^','ü0*‘ðø«ÐN\0ŠÚè£ÿÊí˜HÄa/ßˆõÒn­u?','eda31c99d48062be48529a5cbf2fd654','000/000/0003.jpg','2015-03-19 16:40:44',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-19 22:47:08
