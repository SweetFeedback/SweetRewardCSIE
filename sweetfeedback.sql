-- phpMyAdmin SQL Dump
-- version 3.5.3
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 26, 2013 at 12:15 PM
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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=335068 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=281 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE IF NOT EXISTS `members` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(65) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(65) COLLATE utf8_unicode_ci NOT NULL,
  `token` varchar(65) COLLATE utf8_unicode_ci NOT NULL,
  `temperature_threshold` double NOT NULL DEFAULT '0',
  `light_threshold` double NOT NULL DEFAULT '0',
  `micro_threshold` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=6 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=12873 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

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
