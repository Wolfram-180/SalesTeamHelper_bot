CREATE DATABASE `imagerfrobot_dev` /*!40100 DEFAULT CHARACTER SET utf32 COLLATE utf32_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `contacts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `email` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `phone` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `comment` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `manager_id` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;

CREATE TABLE `distributor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  `contact_distr_id` int DEFAULT '0',
  `contact_froneri_id` int DEFAULT '0',
  `froneri_cont_based_on_mail` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;

CREATE TABLE `locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(45) COLLATE utf32_bin DEFAULT '',
  `street` varchar(45) COLLATE utf32_bin DEFAULT '',
  `bldng` varchar(45) COLLATE utf32_bin DEFAULT '',
  `id_distributor` int DEFAULT '0',
  `id_contact` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;

CREATE TABLE `reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `street` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `bldng` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `distributor_id` int DEFAULT '0',
  `telegram_id` int DEFAULT '0',
  `distr_name` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `rep_text` varchar(500) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `message3` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `message4` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `report_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `reports_in_process` varchar(200) COLLATE utf32_bin DEFAULT '<нет данных>',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;

CREATE TABLE `reports_parts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_reports` varchar(200) CHARACTER SET utf32 COLLATE utf32_bin DEFAULT '<нет данных>',
  `report_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `text` varchar(500) COLLATE utf32_bin DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf32 COLLATE=utf32_bin;

