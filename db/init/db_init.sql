--
-- Table structure for table `pf_roles`
--

DROP TABLE IF EXISTS `pf_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pf_roles` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(60) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `default` tinyint(1) NOT NULL DEFAULT 0,
  `can_delete` tinyint(1) NOT NULL DEFAULT 1,
  `login_destination` varchar(255) NOT NULL DEFAULT '/',
  `default_context` varchar(255) DEFAULT 'content',
  `deleted` int(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pf_roles`
--

LOCK TABLES `pf_roles` WRITE;
/*!40000 ALTER TABLE `pf_roles` DISABLE KEYS */;
INSERT INTO `pf_roles` VALUES
(1,'Maintain','Has full control over every aspect of the site.',0,0,'/','',0),
(21,'User','This is the default user with access to login.',1,0,'/','',0),
(31,'Admin','For System Admin Account',0,0,'/','',0);
/*!40000 ALTER TABLE `pf_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bpf_system_config`
--

DROP TABLE IF EXISTS `pf_system_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pf_system_config` (
  `name` varchar(50) NOT NULL,
  `value` varchar(1024) DEFAULT NULL,
  `option` varchar(1000) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pf_users`
--

DROP TABLE IF EXISTS `pf_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pf_users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `role_id` tinyint(1) NOT NULL DEFAULT 4,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `username` varchar(50) NOT NULL DEFAULT '',
  `displayname` varchar(50) NOT NULL DEFAULT '',
  `password_hash` char(60) NOT NULL,
  `last_login` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_ip` varchar(45) NOT NULL DEFAULT '',
  `description` varchar(100) DEFAULT NULL,
  `wrong_count` tinyint(1) NOT NULL DEFAULT 0,
  `password_overdue` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `password_reset` tinyint(1) DEFAULT 0,
  `locked` tinyint(1) NOT NULL DEFAULT 0,
  `banned` tinyint(1) NOT NULL DEFAULT 0,
  `deleted` tinyint(1) NOT NULL DEFAULT 0,
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_displayname` (`displayname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

