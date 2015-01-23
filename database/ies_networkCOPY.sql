-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Temps de generació: 23-01-2015 a les 09:49:56
-- Versió del servidor: 5.5.40
-- Versió de PHP : 5.3.10-1ubuntu3.15

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de dades: `ies_network`
--

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_apinetworkdevice`
--

CREATE TABLE IF NOT EXISTS `aules_apinetworkdevice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,
  `comment` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `ip` char(15) COLLATE utf8_spanish2_ci NOT NULL,
  `admin` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `password` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `network_type` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=3 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_classroom`
--

CREATE TABLE IF NOT EXISTS `aules_classroom` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,
  `comment` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `firewall_rule_id` int(11) DEFAULT NULL,
  `mac_filter` tinyint(1) NOT NULL,
  `network_device_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `aules_classroom_3840d93c` (`firewall_rule_id`),
  KEY `aules_classroom_82a1e427` (`network_device_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=9 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_computer`
--

CREATE TABLE IF NOT EXISTS `aules_computer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classroom_id` int(11) NOT NULL,
  `model_id` int(11) NOT NULL,
  `identifier` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `mac` varchar(17) COLLATE utf8_spanish2_ci NOT NULL,
  `comment` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `buying_date` date DEFAULT NULL,
  `serial` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `aules_computer_c0578458` (`classroom_id`),
  KEY `aules_computer_aff30766` (`model_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=88 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_firewallrule`
--

CREATE TABLE IF NOT EXISTS `aules_firewallrule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `network_device_id` int(11) NOT NULL,
  `dst_ip_list_id` int(11) NOT NULL,
  `comment` varchar(255) COLLATE utf8_spanish2_ci NOT NULL,
  `action` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `redirect_url` varchar(200) COLLATE utf8_spanish2_ci NOT NULL,
  `src_address` char(39) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `src_netmask` int(11) NOT NULL,
  `src_mac_address` varchar(17) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `aules_firewallrule_82a1e427` (`network_device_id`),
  KEY `aules_firewallrule_de18a513` (`dst_ip_list_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_pcmodel`
--

CREATE TABLE IF NOT EXISTS `aules_pcmodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `motherboard` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,
  `ram` int(11) NOT NULL,
  `hdd` int(11) NOT NULL,
  `cpu` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `architecture` int(11) NOT NULL,
  `cpu_virtualization` int(11) NOT NULL,
  `comment` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=8 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_urllist`
--

CREATE TABLE IF NOT EXISTS `aules_urllist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8_spanish2_ci NOT NULL,
  `comment` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=6 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_urllistitem`
--

CREATE TABLE IF NOT EXISTS `aules_urllistitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `url` varchar(200) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `ip_address` char(39) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `netmask` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=13 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `aules_urllist_url_list_items`
--

CREATE TABLE IF NOT EXISTS `aules_urllist_url_list_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `urllist_id` int(11) NOT NULL,
  `urllistitem_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `urllist_id` (`urllist_id`,`urllistitem_id`),
  KEY `aules_urllist_url_list_items_e8f10834` (`urllist_id`),
  KEY `aules_urllist_url_list_items_83df9dd1` (`urllistitem_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=47 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `auth_group`
--

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_spanish2_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `auth_group_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `auth_permission`
--

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=46 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `auth_user`
--

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) COLLATE utf8_spanish2_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_spanish2_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8_spanish2_ci NOT NULL,
  `email` varchar(75) COLLATE utf8_spanish2_ci NOT NULL,
  `password` varchar(128) COLLATE utf8_spanish2_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=18 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `auth_user_groups`
--

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `auth_user_user_permissions`
--

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=85 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `django_admin_log`
--

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext COLLATE utf8_spanish2_ci,
  `object_repr` varchar(200) COLLATE utf8_spanish2_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_spanish2_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=272 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `app_label` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=16 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8_spanish2_ci NOT NULL,
  `session_data` longtext COLLATE utf8_spanish2_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de la taula `django_site`
--

CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) COLLATE utf8_spanish2_ci NOT NULL,
  `name` varchar(50) COLLATE utf8_spanish2_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Estructura de la taula `proxylog_proxyentry`
--

CREATE TABLE IF NOT EXISTS `proxylog_proxyentry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_date` datetime NOT NULL,
  `ip_src` char(39) COLLATE utf8_spanish2_ci NOT NULL,
  `ip_dst` char(39) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `domain_destination` varchar(255) COLLATE utf8_spanish2_ci NOT NULL,
  `path` varchar(255) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `action` varchar(10) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `cache` varchar(10) COLLATE utf8_spanish2_ci DEFAULT NULL,
  `computer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci AUTO_INCREMENT=9889390 ;

--
-- Restriccions per taules bolcades
--

--
-- Restriccions per la taula `aules_classroom`
--
ALTER TABLE `aules_classroom`
  ADD CONSTRAINT `firewall_rule_id_refs_id_46ce88d1` FOREIGN KEY (`firewall_rule_id`) REFERENCES `aules_firewallrule` (`id`),
  ADD CONSTRAINT `network_device_id_refs_id_b633f415` FOREIGN KEY (`network_device_id`) REFERENCES `aules_apinetworkdevice` (`id`);

--
-- Restriccions per la taula `aules_computer`
--
ALTER TABLE `aules_computer`
  ADD CONSTRAINT `classroom_id_refs_id_2166af58` FOREIGN KEY (`classroom_id`) REFERENCES `aules_classroom` (`id`),
  ADD CONSTRAINT `model_id_refs_id_5fea8a01` FOREIGN KEY (`model_id`) REFERENCES `aules_pcmodel` (`id`);

--
-- Restriccions per la taula `aules_firewallrule`
--
ALTER TABLE `aules_firewallrule`
  ADD CONSTRAINT `dst_ip_list_id_refs_id_b3cbdfff` FOREIGN KEY (`dst_ip_list_id`) REFERENCES `aules_urllist` (`id`),
  ADD CONSTRAINT `network_device_id_refs_id_5ac2f5cf` FOREIGN KEY (`network_device_id`) REFERENCES `aules_apinetworkdevice` (`id`);

--
-- Restriccions per la taula `aules_urllist_url_list_items`
--
ALTER TABLE `aules_urllist_url_list_items`
  ADD CONSTRAINT `urllistitem_id_refs_id_3aa62ef5` FOREIGN KEY (`urllistitem_id`) REFERENCES `aules_urllistitem` (`id`),
  ADD CONSTRAINT `urllist_id_refs_id_8c492110` FOREIGN KEY (`urllist_id`) REFERENCES `aules_urllist` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
