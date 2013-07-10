-- phpMyAdmin SQL Dump
-- version 3.5.3
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 09, 2013 at 05:36 PM
-- Server version: 5.6.10
-- PHP Version: 5.3.15

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sweetfeedback`
--

-- --------------------------------------------------------

--
-- Table structure for table `basic_sensor_log`
--

CREATE TABLE IF NOT EXISTS `basic_sensor_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL,
  `light_level` float NOT NULL,
  `temperature` float NOT NULL,
  `sound_level` float NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `device_online`
--

CREATE TABLE IF NOT EXISTS `device_online` (
  `session` char(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `time` int(11) NOT NULL DEFAULT '0',
  `ipaddress` char(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `extended_window_log`
--

CREATE TABLE IF NOT EXISTS `extended_window_log` (
  `ext_win_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `location_id` int(11) NOT NULL,
  `window_id` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ext_win_log_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=82 ;

-- --------------------------------------------------------

--
-- Table structure for table `extended_window_log_index`
--

CREATE TABLE IF NOT EXISTS `extended_window_log_index` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `ext_win_log_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `window_id` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_repository`
--

CREATE TABLE IF NOT EXISTS `feedback_repository` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `feedback_type` char(50) COLLATE utf8_unicode_ci NOT NULL,
  `feedback_description` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `if_get` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `gcm_id`
--

CREATE TABLE IF NOT EXISTS `gcm_id` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gcm_id` text NOT NULL,
  `user_id` varchar(30) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Locations`
--

CREATE TABLE IF NOT EXISTS `Locations` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `coordinate_x` double NOT NULL,
  `coordinate_y` double NOT NULL,
  `floor_level` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Dumping data for table `Locations`
--

INSERT INTO `Locations` (`location_id`, `room_name`, `coordinate_x`, `coordinate_y`, `floor_level`) VALUES
(2, '336', 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE IF NOT EXISTS `members` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(65) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(65) COLLATE utf8_unicode_ci DEFAULT NULL,
  `token` varchar(65) COLLATE utf8_unicode_ci NOT NULL,
  `temperature_threshold` double NOT NULL DEFAULT '0',
  `light_threshold` double NOT NULL DEFAULT '0',
  `micro_threshold` double NOT NULL DEFAULT '0',
  `facebook_id` text CHARACTER SET utf8,
  `gcm_id` text CHARACTER SET utf8,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=18 ;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`user_id`, `account`, `password`, `token`, `temperature_threshold`, `light_threshold`, `micro_threshold`, `facebook_id`, `gcm_id`) VALUES
(17, NULL, NULL, '5b89aa815b6fccb4349543291b7fd0d7', 0, 0, 0, NULL, '1233455'),
(15, NULL, NULL, '202cb962ac59075b964b07152d234b70', 0, 0, 0, NULL, '123'),
(16, NULL, NULL, '1b2de2499e5f93e00a5a90e79a9da4b1', 0, 0, 0, NULL, '1231231231');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE IF NOT EXISTS `notification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `problem_id` int(11) NOT NULL,
  `gcm_id` text CHARACTER SET utf8 NOT NULL,
  `action` int(11) DEFAULT NULL,
  `annoy_level` int(11) DEFAULT NULL,
  `open_timestamp` timestamp NULL DEFAULT NULL,
  `response_timestamp` timestamp NULL DEFAULT NULL,
  `generate_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=39 ;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`id`, `problem_id`, `gcm_id`, `action`, `annoy_level`, `open_timestamp`, `response_timestamp`, `generate_timestamp`) VALUES
(38, 5, '33', NULL, NULL, NULL, NULL, '2013-06-26 03:53:49');

-- --------------------------------------------------------

--
-- Table structure for table `people_presence_log_ext`
--

CREATE TABLE IF NOT EXISTS `people_presence_log_ext` (
  `log_id` int(11) NOT NULL,
  `people_presence` int(11) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `problems`
--

CREATE TABLE IF NOT EXISTS `problems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` int(11) NOT NULL DEFAULT '0',
  `room` int(11) NOT NULL DEFAULT '0',
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `coordinate_x` int(11) DEFAULT NULL,
  `coordinate_y` int(11) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=77 ;

-- --------------------------------------------------------

--
-- Table structure for table `transportation_log`
--

CREATE TABLE IF NOT EXISTS `transportation_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `trip_id` int(11) NOT NULL,
  `label` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `segment` int(11) NOT NULL,
  `point` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `altitude` double NOT NULL,
  `bearing` double NOT NULL,
  `accuracy` double NOT NULL,
  `speed` double NOT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `transportation_status`
--

CREATE TABLE IF NOT EXISTS `transportation_status` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `trip_id` int(11) NOT NULL DEFAULT '0',
  `trans_type` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `walking_percentage` double NOT NULL DEFAULT '0',
  `biking_percentage` double NOT NULL DEFAULT '0',
  `train_percentage` double NOT NULL DEFAULT '0',
  `driving_percentage` double NOT NULL DEFAULT '0',
  `aver_speed` double NOT NULL,
  `max_speed` double NOT NULL,
  `total_distance` double NOT NULL,
  `total_time` double NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `user_desktop_log`
--

CREATE TABLE IF NOT EXISTS `user_desktop_log` (
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `app` varchar(255) NOT NULL,
  `user_id` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user_online`
--

CREATE TABLE IF NOT EXISTS `user_online` (
  `user_id` int(11) NOT NULL,
  `time` int(11) NOT NULL,
  `ipaddr` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wifi_signal`
--

CREATE TABLE IF NOT EXISTS `wifi_signal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` int(11) NOT NULL,
  `signal_level` text CHARACTER SET utf8 NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `wifi_signal`
--

INSERT INTO `wifi_signal` (`id`, `location`, `signal_level`, `timestamp`) VALUES
(1, 1, '{"00:25:c4:7c:a4:98":-51,"00:25:c4:3c:a4:98":-52,"c4:10:8a:94:64:18":-65,"74:ea:3a:a4:fd:3e":-70,"00:24:6c:2d:17:d0":-66,"00:25:c4:3c:91:28":-87,"00:26:5a:c3:f6:ff":-74,"00:24:6c:2d:17:d2":-71,"00:24:6c:2d:17:d1":-65,"00:24:6c:26:89:f1":-78,"00:0d:0b:ef:50:3f":-75,"00:24:6c:26:89:f2":-80,"c0:c5:20:11:a5:b8":-65,"00:0d:0b:4f:6a:fa":-80,"00:22:2d:4d:52:64":-87,"00:25:c4:7c:9c:38":-75,"00:25:c4:bc:91:28":-85,"00:25:c4:bc:a4:98":-52,"58:93:96:29:4d:78":-85,"c4:10:8a:14:64:18":-65,"f8:d1:11:39:27:02":-87,"c0:c5:20:91:a5:b8":-66,"10:bf:48:e7:2a:a8":-74,"00:25:c4:bc:9c:f8":-73,"c4:10:8a:54:64:18":-65,"00:25:c4:7c:9c:f8":-73,"00:18:e7:eb:81:b8":-85,"00:25:c4:bc:9c:38":-76,"d4:9a:20:54:9e:56":-49,"00:25:c4:3c:9c:38":-68,"00:25:c4:7c:a4:f8":-86,"ac:67:06:9c:02:88":-89,"00:25:c4:3c:9c:f8":-73,"c0:c5:20:51:a5:b8":-64,"00:24:a5:da:9e:15":-62,"58:93:96:27:35:28":-86}', '2013-06-26 04:05:51'),
(2, 1, '{"00:25:c4:7c:a4:98":-49,"00:25:c4:3c:a4:98":-50,"c4:10:8a:94:64:18":-67,"74:ea:3a:a4:fd:3e":-68,"00:24:6c:2d:17:d0":-71,"00:25:c4:3c:91:28":-76,"00:26:5a:c3:f6:ff":-70,"00:24:6c:2d:17:d2":-72,"00:24:6c:2d:17:d1":-69,"00:0d:0b:ef:50:3f":-75,"00:24:6c:26:89:f2":-83,"c0:c5:20:11:a5:b8":-67,"ac:67:06:dd:97:78":-86,"58:93:96:69:4d:78":-84,"00:0d:0b:4f:6a:fa":-79,"00:25:c4:7c:9c:38":-52,"00:25:c4:bc:91:28":-75,"00:25:c4:bc:a4:98":-50,"58:93:96:29:4d:78":-81,"c4:10:8a:14:64:18":-66,"c0:c5:20:91:a5:b8":-64,"10:bf:48:e7:2a:a8":-70,"00:25:c4:bc:9c:f8":-72,"c4:10:8a:54:64:18":-64,"00:25:c4:7c:9c:f8":-72,"00:18:e7:eb:81:b8":-87,"20:cf:30:b7:c0:de":-79,"00:25:c4:3c:91:78":-86,"c4:10:8a:54:64:b8":-89,"00:25:c4:bc:9c:38":-52,"d4:9a:20:54:9e:56":-52,"00:25:c4:3c:9c:38":-53,"00:25:c4:3c:9c:f8":-73,"c0:c5:20:51:a5:b8":-63,"58:93:96:67:35:28":-85,"00:24:a5:da:9e:15":-60}', '2013-06-26 04:23:52'),
(3, 1, '{"00:25:c4:7c:a4:98":-49,"00:25:c4:3c:a4:98":-50,"c4:10:8a:94:64:18":-67,"74:ea:3a:a4:fd:3e":-68,"00:24:6c:2d:17:d0":-71,"00:25:c4:3c:91:28":-76,"00:26:5a:c3:f6:ff":-70,"00:24:6c:2d:17:d2":-72,"00:24:6c:2d:17:d1":-69,"00:0d:0b:ef:50:3f":-75,"00:24:6c:26:89:f2":-83,"c0:c5:20:11:a5:b8":-67,"ac:67:06:dd:97:78":-86,"58:93:96:69:4d:78":-84,"00:0d:0b:4f:6a:fa":-79,"00:25:c4:7c:9c:38":-52,"00:25:c4:bc:91:28":-75,"00:25:c4:bc:a4:98":-50,"58:93:96:29:4d:78":-81,"c4:10:8a:14:64:18":-66,"c0:c5:20:91:a5:b8":-64,"10:bf:48:e7:2a:a8":-70,"00:25:c4:bc:9c:f8":-72,"c4:10:8a:54:64:18":-64,"00:25:c4:7c:9c:f8":-72,"00:18:e7:eb:81:b8":-87,"20:cf:30:b7:c0:de":-79,"00:25:c4:3c:91:78":-86,"c4:10:8a:54:64:b8":-89,"00:25:c4:bc:9c:38":-52,"d4:9a:20:54:9e:56":-52,"00:25:c4:3c:9c:38":-53,"00:25:c4:3c:9c:f8":-73,"c0:c5:20:51:a5:b8":-63,"58:93:96:67:35:28":-85,"00:24:a5:da:9e:15":-60}', '2013-06-26 04:35:50');

-- --------------------------------------------------------

--
-- Table structure for table `Windows`
--

CREATE TABLE IF NOT EXISTS `Windows` (
  `window_id` int(11) NOT NULL AUTO_INCREMENT,
  `window_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `coordinate_x` double NOT NULL,
  `coordinate_y` double NOT NULL,
  `floor_level` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`window_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `window_log`
--

CREATE TABLE IF NOT EXISTS `window_log` (
  `log_id` int(11) NOT NULL,
  `window_id` int(11) NOT NULL,
  `state` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `window_state_log_ext`
--

CREATE TABLE IF NOT EXISTS `window_state_log_ext` (
  `log_id` int(11) NOT NULL,
  `window_state` int(11) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `people_presence_log_ext`
--
ALTER TABLE `people_presence_log_ext`
  ADD CONSTRAINT `people_presence_log_ext_ibfk_1` FOREIGN KEY (`log_id`) REFERENCES `basic_sensor_log` (`log_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `window_state_log_ext`
--
ALTER TABLE `window_state_log_ext`
  ADD CONSTRAINT `window_state_log_ext_ibfk_2` FOREIGN KEY (`log_id`) REFERENCES `basic_sensor_log` (`log_id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
