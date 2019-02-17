-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 25, 2018 at 12:31 AM
-- Server version: 5.5.54-0+deb8u1
-- PHP Version: 5.6.29-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `iotdb`
--
CREATE DATABASE IF NOT EXISTS `iotdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `iotdb`;

-- --------------------------------------------------------

--
-- Table structure for table `access_logs`
--

CREATE TABLE IF NOT EXISTS `access_logs` (
`Id` int(11) NOT NULL,
  `RoomId` int(11) NOT NULL,
  `CardId` varchar(45) NOT NULL,
  `Time` datetime NOT NULL,
  `Exit_time` datetime DEFAULT NULL,
  `IsValid` tinyint(4) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `access_logs`
--

INSERT INTO `access_logs` (`Id`, `RoomId`, `CardId`, `Time`, `Exit_time`, `IsValid`) VALUES
(1, 1, '[136, 4, 75, 165, 98]', '2018-12-08 16:13:06', '2018-12-08 16:13:15', 1),
(2, 1, '[136, 4, 75, 165, 98]', '2018-12-08 16:13:57', '2018-12-08 16:14:28', 1),
(3, 1, '[136, 4, 75, 165, 98]', '2018-12-08 16:15:33', '2018-12-08 16:15:36', 1),
(4, 1, '[136, 4, 75, 165, 98]', '2018-12-08 16:15:40', '2018-12-08 16:15:44', 1),
(5, 1, '[136, 4, 75, 165, 98]', '2018-12-08 16:17:38', '2018-12-08 16:17:51', 1),
(6, 1, '[136, 4, 75, 165, 98]', '2018-12-13 13:43:15', '2018-12-13 13:43:26', 1),
(7, 1, '[136, 4, 75, 165, 98]', '2018-12-13 16:58:51', '2018-12-13 16:59:19', 1),
(8, 1, '[136, 4, 75, 165, 98]', '2018-12-14 15:23:20', '2018-12-14 15:23:20', 1),
(9, 1, '[136, 4, 75, 165, 98]', '2018-12-14 15:25:38', '2018-12-14 15:25:42', 1),
(10, 1, '[136, 4, 75, 165, 98]', '2018-12-14 15:25:49', '2018-12-14 15:25:57', 0),
(11, 1, '[136, 4, 75, 165, 98]', '2018-12-14 15:26:14', '2018-12-14 15:26:30', 0),
(12, 1, '[136, 4, 153, 38, 51]', '2018-12-18 14:57:35', NULL, 0),
(13, 1, '[136, 4, 153, 38, 51]', '2018-12-18 15:01:40', NULL, 0),
(14, 1, '[136, 4, 75, 165, 98]', '2018-12-18 15:01:43', NULL, 0),
(15, 1, '[136, 4, 75, 165, 98]', '2018-12-18 15:02:22', '2018-12-18 15:02:25', 1);

-- --------------------------------------------------------

--
-- Table structure for table `access_rights`
--

CREATE TABLE IF NOT EXISTS `access_rights` (
`Id` int(11) NOT NULL,
  `CardId` varchar(45) NOT NULL,
  `RoomId` int(11) NOT NULL,
  `UserId` int(11) NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `access_rights`
--

INSERT INTO `access_rights` (`Id`, `CardId`, `RoomId`, `UserId`) VALUES
(1, '[136, 4, 75, 165, 98]', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `enviro_info`
--

CREATE TABLE IF NOT EXISTS `enviro_info` (
`Id` int(11) NOT NULL,
  `temp` double NOT NULL,
  `humidity` double NOT NULL,
  `time` datetime NOT NULL,
  `roomId` int(11) NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=215 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `enviro_info`
--

INSERT INTO `enviro_info` (`Id`, `temp`, `humidity`, `time`, `roomId`) VALUES
(1, 1, 2, '2018-12-01 13:16:00', 1),
(2, 1, 2, '2018-12-01 13:20:09', 1),
(3, 29, 58, '2018-12-01 13:50:37', 1),
(4, 29, 58, '2018-12-01 13:50:43', 1),
(5, 29, 58, '2018-12-01 13:50:49', 1),
(6, 29, 58, '2018-12-01 13:50:57', 1),
(7, 29, 58, '2018-12-01 13:51:02', 1),
(8, 29, 61, '2018-12-01 13:51:08', 1),
(9, 30, 61, '2018-12-01 13:51:13', 1),
(10, 29, 64, '2018-12-01 13:51:19', 1),
(11, 29, 62, '2018-12-01 13:51:24', 1),
(12, 29, 59, '2018-12-01 13:52:16', 1),
(13, 28, 65, '2018-12-08 09:57:02', 1),
(14, 28, 65, '2018-12-08 09:57:07', 1),
(15, 28, 65, '2018-12-08 09:57:13', 1),
(16, 28, 65, '2018-12-08 09:57:19', 1),
(17, 28, 65, '2018-12-08 09:57:27', 1),
(18, 14, 160, '2018-12-08 09:57:37', 1),
(19, 28, 65, '2018-12-08 09:57:43', 1),
(20, 28, 65, '2018-12-08 09:57:48', 1),
(21, 28, 65, '2018-12-08 09:57:56', 1),
(22, 14, 160, '2018-12-08 09:58:02', 1),
(23, 28, 65, '2018-12-08 09:58:10', 1),
(24, 28, 65, '2018-12-08 09:58:16', 1),
(25, 28, 65, '2018-12-08 09:58:21', 1),
(26, 28, 64, '2018-12-08 09:58:29', 1),
(27, 28, 64, '2018-12-08 09:58:35', 1),
(28, 28, 64, '2018-12-08 09:58:40', 1),
(29, 28, 64, '2018-12-08 09:58:46', 1),
(30, 28, 64, '2018-12-08 09:58:56', 1),
(31, 28, 64, '2018-12-08 09:59:07', 1),
(32, 28, 64, '2018-12-08 09:59:13', 1),
(33, 28, 63, '2018-12-08 09:59:23', 1),
(34, 28, 63, '2018-12-08 09:59:31', 1),
(35, 28, 63, '2018-12-08 09:59:37', 1),
(36, 28, 63, '2018-12-08 09:59:42', 1),
(37, 28, 63, '2018-12-08 09:59:48', 1),
(38, 28, 63, '2018-12-08 09:59:53', 1),
(39, 14, 159, '2018-12-08 10:00:06', 1),
(40, 14, 159, '2018-12-08 10:00:12', 1),
(41, 14, 159, '2018-12-08 10:00:18', 1),
(42, 14, 159, '2018-12-08 10:00:26', 1),
(43, 28, 63, '2018-12-08 10:00:31', 1),
(44, 28, 63, '2018-12-08 10:00:37', 1),
(45, 14, 159, '2018-12-08 10:00:42', 1),
(46, 28, 63, '2018-12-08 10:00:50', 1),
(47, 28, 63, '2018-12-08 10:00:56', 1),
(48, 14, 159, '2018-12-08 10:01:01', 1),
(49, 28, 63, '2018-12-08 10:01:07', 1),
(50, 28, 63, '2018-12-08 10:01:15', 1),
(51, 28, 63, '2018-12-08 10:01:21', 1),
(52, 14, 159, '2018-12-08 10:01:26', 1),
(53, 28, 63, '2018-12-08 10:01:32', 1),
(54, 28, 63, '2018-12-08 10:01:37', 1),
(55, 28, 63, '2018-12-08 10:01:43', 1),
(56, 28, 63, '2018-12-08 10:01:48', 1),
(57, 14, 159, '2018-12-08 10:01:56', 1),
(58, 28, 63, '2018-12-08 10:02:04', 1),
(59, 28, 63, '2018-12-08 10:02:10', 1),
(60, 28, 63, '2018-12-08 10:02:16', 1),
(61, 28, 63, '2018-12-08 10:02:21', 1),
(62, 28, 63, '2018-12-08 10:02:27', 1),
(63, 28, 63, '2018-12-08 10:02:32', 1),
(64, 28, 63, '2018-12-08 10:02:38', 1),
(65, 28, 63, '2018-12-08 10:02:43', 1),
(66, 28, 62, '2018-12-08 10:02:49', 1),
(67, 28, 63, '2018-12-08 10:02:54', 1),
(68, 28, 63, '2018-12-08 10:03:00', 1),
(69, 14, 159, '2018-12-08 10:03:05', 1),
(70, 28, 63, '2018-12-08 10:03:13', 1),
(71, 14, 159, '2018-12-08 10:03:19', 1),
(72, 28, 63, '2018-12-08 10:03:25', 1),
(73, 28, 61, '2018-12-08 10:03:30', 1),
(74, 14, 159, '2018-12-08 10:03:43', 1),
(75, 28, 63, '2018-12-08 10:03:49', 1),
(76, 28, 63, '2018-12-08 10:03:54', 1),
(77, 28, 63, '2018-12-08 10:04:00', 1),
(78, 28, 63, '2018-12-08 10:04:05', 1),
(79, 28, 63, '2018-12-08 10:04:11', 1),
(80, 28, 63, '2018-12-08 10:04:16', 1),
(81, 28, 63, '2018-12-08 10:04:22', 1),
(82, 14, 159, '2018-12-08 10:04:28', 1),
(83, 28, 63, '2018-12-08 10:04:33', 1),
(84, 28, 63, '2018-12-08 10:04:39', 1),
(85, 14, 159, '2018-12-08 10:04:44', 1),
(86, 28, 63, '2018-12-08 10:04:50', 1),
(87, 28, 63, '2018-12-08 10:04:58', 1),
(88, 28, 63, '2018-12-08 10:05:03', 1),
(89, 28, 63, '2018-12-08 10:05:09', 1),
(90, 28, 63, '2018-12-08 10:05:14', 1),
(91, 28, 62, '2018-12-08 10:05:20', 1),
(92, 28, 63, '2018-12-08 10:05:25', 1),
(93, 28, 62, '2018-12-08 10:05:31', 1),
(94, 28, 63, '2018-12-08 10:05:37', 1),
(95, 28, 63, '2018-12-08 10:05:42', 1),
(96, 28, 63, '2018-12-08 10:05:48', 1),
(97, 28, 63, '2018-12-08 10:05:53', 1),
(98, 28, 63, '2018-12-08 10:05:59', 1),
(99, 28, 63, '2018-12-08 10:06:04', 1),
(100, 28, 63, '2018-12-08 10:06:12', 1),
(101, 28, 63, '2018-12-08 10:06:18', 1),
(102, 28, 63, '2018-12-08 10:06:23', 1),
(103, 28, 63, '2018-12-08 10:06:32', 1),
(104, 28, 63, '2018-12-08 10:06:37', 1),
(105, 28, 63, '2018-12-08 10:06:43', 1),
(106, 28, 63, '2018-12-08 10:06:48', 1),
(107, 28, 63, '2018-12-08 10:06:54', 1),
(108, 28, 63, '2018-12-08 10:06:59', 1),
(109, 14, 159, '2018-12-08 10:07:05', 1),
(110, 28, 62, '2018-12-08 10:07:10', 1),
(111, 28, 63, '2018-12-08 10:07:16', 1),
(112, 14, 159, '2018-12-08 10:07:21', 1),
(113, 28, 63, '2018-12-08 10:07:27', 1),
(114, 28, 63, '2018-12-08 10:07:32', 1),
(115, 28, 63, '2018-12-08 10:07:38', 1),
(116, 28, 63, '2018-12-08 10:07:44', 1),
(117, 28, 63, '2018-12-08 10:07:49', 1),
(118, 28, 63, '2018-12-08 10:07:55', 1),
(119, 28, 63, '2018-12-08 10:08:00', 1),
(120, 28, 63, '2018-12-08 10:08:08', 1),
(121, 28, 63, '2018-12-08 10:08:14', 1),
(122, 28, 63, '2018-12-08 10:08:19', 1),
(123, 28, 63, '2018-12-08 10:08:27', 1),
(124, 28, 63, '2018-12-08 10:08:33', 1),
(125, 14, 159, '2018-12-08 10:08:39', 1),
(126, 28, 63, '2018-12-08 10:08:44', 1),
(127, 28, 63, '2018-12-08 10:08:50', 1),
(128, 28, 63, '2018-12-08 10:08:55', 1),
(129, 28, 63, '2018-12-08 10:09:03', 1),
(130, 28, 62, '2018-12-08 10:09:09', 1),
(131, 28, 63, '2018-12-08 10:09:14', 1),
(132, 28, 62, '2018-12-08 10:09:20', 1),
(133, 28, 63, '2018-12-08 10:09:28', 1),
(134, 28, 63, '2018-12-08 10:09:34', 1),
(135, 28, 63, '2018-12-08 10:09:39', 1),
(136, 28, 63, '2018-12-08 10:09:47', 1),
(137, 28, 62, '2018-12-08 10:09:53', 1),
(138, 28, 62, '2018-12-08 10:10:03', 1),
(139, 28, 62, '2018-12-08 10:10:11', 1),
(140, 28, 63, '2018-12-08 10:10:17', 1),
(141, 28, 62, '2018-12-08 10:10:22', 1),
(142, 28, 62, '2018-12-08 10:10:28', 1),
(143, 28, 62, '2018-12-08 10:10:34', 1),
(144, 28, 62, '2018-12-08 10:10:39', 1),
(145, 28, 62, '2018-12-08 10:10:47', 1),
(146, 28, 62, '2018-12-08 10:10:58', 1),
(147, 28, 62, '2018-12-08 10:11:08', 1),
(148, 28, 62, '2018-12-08 10:11:14', 1),
(149, 28, 57, '2018-12-13 13:30:10', 1),
(150, 28, 58, '2018-12-13 13:30:16', 1),
(151, 28, 57, '2018-12-13 13:30:26', 1),
(152, 28, 58, '2018-12-13 13:30:37', 1),
(153, 28, 58, '2018-12-13 13:30:42', 1),
(154, 28, 58, '2018-12-13 13:30:48', 1),
(155, 28, 58, '2018-12-13 13:30:53', 1),
(156, 28, 58, '2018-12-13 13:30:59', 1),
(157, 28, 58, '2018-12-13 13:31:04', 1),
(158, 28, 57, '2018-12-13 13:31:15', 1),
(159, 28, 58, '2018-12-13 13:31:23', 1),
(160, 28, 58, '2018-12-13 13:31:28', 1),
(161, 28, 59, '2018-12-13 13:33:29', 1),
(162, 28, 59, '2018-12-13 13:33:34', 1),
(163, 28, 59, '2018-12-13 13:33:40', 1),
(164, 28, 58, '2018-12-13 13:33:57', 1),
(165, 28, 58, '2018-12-13 13:34:07', 1),
(166, 28, 58, '2018-12-13 13:42:49', 1),
(167, 28, 58, '2018-12-13 13:42:55', 1),
(168, 14, 157, '2018-12-13 13:43:03', 1),
(169, 28, 56, '2018-12-13 13:43:08', 1),
(170, 14, 155, '2018-12-13 13:43:16', 1),
(171, 28, 57, '2018-12-13 13:43:22', 1),
(172, 14, 156, '2018-12-13 13:43:30', 1),
(173, 14, 155, '2018-12-13 13:43:38', 1),
(174, 28, 56, '2018-12-13 13:43:44', 1),
(175, 28, 57, '2018-12-13 13:43:49', 1),
(176, 28, 56, '2018-12-13 13:43:55', 1),
(177, 28, 56, '2018-12-13 13:44:05', 1),
(178, 28, 56, '2018-12-13 13:44:18', 1),
(179, 28, 58, '2018-12-13 13:44:24', 1),
(180, 28, 56, '2018-12-13 13:44:32', 1),
(181, 28, 55, '2018-12-13 13:44:43', 1),
(182, 28, 57, '2018-12-13 13:44:48', 1),
(183, 28, 58, '2018-12-13 13:44:59', 1),
(184, 28, 57, '2018-12-13 13:56:27', 1),
(185, 30, 57, '2018-12-25 00:15:39', 1),
(186, 30, 56, '2018-12-25 00:15:47', 1),
(187, 30, 56, '2018-12-25 00:15:52', 1),
(188, 30, 55, '2018-12-25 00:16:01', 1),
(189, 15, 155, '2018-12-25 00:16:06', 1),
(190, 30, 57, '2018-12-25 00:16:14', 1),
(191, 30, 55, '2018-12-25 00:16:22', 1),
(192, 30, 55, '2018-12-25 00:16:30', 1),
(193, 30, 55, '2018-12-25 00:16:36', 1),
(194, 15, 155, '2018-12-25 00:16:44', 1),
(195, 30, 55, '2018-12-25 00:16:52', 1),
(196, 30, 55, '2018-12-25 00:17:05', 1),
(197, 30, 54, '2018-12-25 00:17:13', 1),
(198, 30, 54, '2018-12-25 00:17:19', 1),
(199, 15, 154, '2018-12-25 00:17:24', 1),
(200, 30, 56, '2018-12-25 00:17:30', 1),
(201, 30, 57, '2018-12-25 00:17:35', 1),
(202, 30, 55, '2018-12-25 00:17:41', 1),
(203, 30, 56, '2018-12-25 00:17:46', 1),
(204, 30, 55, '2018-12-25 00:17:52', 1),
(205, 30, 55, '2018-12-25 00:17:57', 1),
(206, 30, 55, '2018-12-25 00:18:03', 1),
(207, 30, 55, '2018-12-25 00:18:08', 1),
(208, 30, 55, '2018-12-25 00:18:16', 1),
(209, 30, 54, '2018-12-25 00:18:22', 1),
(210, 30, 55, '2018-12-25 00:18:28', 1),
(211, 30, 55, '2018-12-25 00:18:33', 1),
(212, 30, 54, '2018-12-25 00:18:39', 1),
(213, 30, 53, '2018-12-25 00:18:44', 1),
(214, 15, 155, '2018-12-25 00:18:55', 1);

-- --------------------------------------------------------

--
-- Table structure for table `motion_events`
--

CREATE TABLE IF NOT EXISTS `motion_events` (
`Id` int(11) NOT NULL,
  `RoomId` int(11) NOT NULL,
  `Time` datetime NOT NULL,
  `FilePath` varchar(100) NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `motion_events`
--

INSERT INTO `motion_events` (`Id`, `RoomId`, `Time`, `FilePath`) VALUES
(1, 2, '2018-12-13 16:58:40', '/home/pi/labs/CA1/recordings/video0.h264'),
(2, 2, '2018-12-13 16:58:48', '/home/pi/labs/CA1/recordings/video1.h264'),
(3, 2, '2018-12-13 16:59:31', '/home/pi/labs/CA1/recordings/video2.h264'),
(4, 2, '2018-12-13 16:59:39', '/home/pi/labs/CA1/recordings/video3.h264'),
(5, 2, '2018-12-13 18:17:17', '/home/pi/labs/CA1/recordings/video4.mp4'),
(6, 2, '2018-12-13 18:22:49', '/home/pi/labs/CA1/recordings/video5.mp4'),
(7, 2, '2018-12-13 18:22:57', '/home/pi/labs/CA1/recordings/video6.mp4'),
(8, 2, '2018-12-13 18:25:24', '/home/pi/labs/CA1/recordings/video7.mp4'),
(9, 2, '2018-12-13 18:25:32', '/home/pi/labs/CA1/recordings/video8.mp4'),
(10, 2, '2018-12-13 18:28:17', '/home/pi/labs/CA1/recordings/video9.mp4'),
(11, 2, '2018-12-13 18:28:53', '/home/pi/labs/CA1/recordings/video10.mp4'),
(12, 2, '2018-12-13 18:31:39', '/home/pi/labs/CA1/recordings/video11.mp4'),
(13, 2, '2018-12-13 18:32:39', '/home/pi/labs/CA1/recordings/video12.mp4'),
(14, 2, '2018-12-13 18:36:20', '/home/pi/labs/CA1/recordings/video13.mp4'),
(15, 2, '2018-12-13 18:37:13', '/home/pi/labs/CA1/recordings/video14.mp4'),
(16, 2, '2018-12-13 18:38:27', '/home/pi/labs/CA1/recordings/video15.mp4'),
(17, 2, '2018-12-13 18:38:38', '/home/pi/labs/CA1/recordings/video16.mp4'),
(18, 2, '2018-12-13 18:38:56', '/home/pi/labs/CA1/recordings/video17.mp4'),
(19, 2, '2018-12-13 18:39:04', '/home/pi/labs/CA1/recordings/video18.mp4'),
(20, 2, '2018-12-13 18:39:12', '/home/pi/labs/CA1/recordings/video19.mp4'),
(21, 2, '2018-12-13 18:39:20', '/home/pi/labs/CA1/recordings/video20.mp4'),
(22, 2, '2018-12-13 18:39:30', '/home/pi/labs/CA1/recordings/video21.mp4'),
(23, 2, '2018-12-13 18:39:38', '/home/pi/labs/CA1/recordings/video22.mp4'),
(24, 2, '2018-12-14 12:59:59', '/home/pi/labs/CA1/recordings/video23.mp4'),
(25, 2, '2018-12-14 13:00:07', '/home/pi/labs/CA1/recordings/video24.mp4'),
(26, 2, '2018-12-14 13:00:15', '/home/pi/labs/CA1/recordings/video25.mp4'),
(27, 2, '2018-12-14 13:00:24', '/home/pi/labs/CA1/recordings/video26.mp4'),
(28, 2, '2018-12-14 13:00:32', '/home/pi/labs/CA1/recordings/video27.mp4'),
(29, 2, '2018-12-14 13:00:40', '/home/pi/labs/CA1/recordings/video28.mp4'),
(30, 2, '2018-12-14 13:00:51', '/home/pi/labs/CA1/recordings/video29.mp4'),
(31, 2, '2018-12-14 13:00:59', '/home/pi/labs/CA1/recordings/video30.mp4'),
(32, 2, '2018-12-14 13:01:33', '/home/pi/labs/CA1/recordings/video31.mp4'),
(33, 2, '2018-12-14 13:01:44', '/home/pi/labs/CA1/recordings/video32.mp4'),
(34, 2, '2018-12-14 13:01:52', '/home/pi/labs/CA1/recordings/video33.mp4'),
(35, 2, '2018-12-14 13:02:00', '/home/pi/labs/CA1/recordings/video34.mp4'),
(36, 2, '2018-12-14 13:02:27', '/home/pi/labs/CA1/recordings/video35.mp4'),
(37, 2, '2018-12-14 13:02:35', '/home/pi/labs/CA1/recordings/video36.mp4'),
(38, 2, '2018-12-14 13:03:00', '/home/pi/labs/CA1/recordings/video37.mp4'),
(39, 2, '2018-12-14 13:03:21', '/home/pi/labs/CA1/recordings/video38.mp4'),
(40, 2, '2018-12-14 13:03:31', '/home/pi/labs/CA1/recordings/video39.mp4'),
(41, 2, '2018-12-14 13:03:39', '/home/pi/labs/CA1/recordings/video40.mp4'),
(42, 2, '2018-12-14 13:04:28', '/home/pi/labs/CA1/recordings/video41.mp4'),
(43, 2, '2018-12-14 13:04:36', '/home/pi/labs/CA1/recordings/video42.mp4'),
(44, 2, '2018-12-14 13:04:44', '/home/pi/labs/CA1/recordings/video43.mp4'),
(45, 2, '2018-12-14 13:04:52', '/home/pi/labs/CA1/recordings/video44.mp4'),
(46, 2, '2018-12-14 13:22:07', '/home/pi/labs/CA1/recordings/video45.mp4'),
(47, 2, '2018-12-14 13:22:15', '/home/pi/labs/CA1/recordings/video46.mp4'),
(48, 2, '2018-12-14 13:22:23', '/home/pi/labs/CA1/recordings/video47.mp4'),
(49, 2, '2018-12-14 13:23:23', '/home/pi/labs/CA1/recordings/video48.mp4'),
(50, 2, '2018-12-14 13:24:34', '/home/pi/labs/CA1/recordings/video49.mp4'),
(51, 2, '2018-12-14 13:25:15', '/home/pi/labs/CA1/recordings/video50.mp4'),
(52, 2, '2018-12-14 13:25:24', '/home/pi/labs/CA1/recordings/video51.mp4'),
(53, 2, '2018-12-14 13:25:33', '/home/pi/labs/CA1/recordings/video52.mp4'),
(54, 2, '2018-12-14 13:26:59', '/home/pi/labs/CA1/recordings/video53.mp4'),
(55, 2, '2018-12-14 13:27:07', '/home/pi/labs/CA1/recordings/video54.mp4'),
(56, 2, '2018-12-14 15:02:00', '/home/pi/labs/CA1/recordings/video55.mp4'),
(57, 2, '2018-12-14 15:03:02', '/home/pi/labs/CA1/recordings/video56.mp4'),
(58, 2, '2018-12-14 15:03:48', '/home/pi/labs/CA1/recordings/video57.mp4'),
(59, 2, '2018-12-14 15:06:37', '/home/pi/labs/CA1/recordings/video58.mp4'),
(60, 2, '2018-12-14 15:06:45', '/home/pi/labs/CA1/recordings/video59.mp4'),
(61, 2, '2018-12-14 15:06:56', '/home/pi/labs/CA1/recordings/video60.mp4'),
(62, 2, '2018-12-14 15:22:32', '/home/pi/labs/CA1/recordings/video61.mp4'),
(63, 2, '2018-12-14 15:22:41', '/home/pi/labs/CA1/recordings/video62.mp4'),
(64, 2, '2018-12-14 15:22:49', '/home/pi/labs/CA1/recordings/video63.mp4'),
(65, 2, '2018-12-14 15:23:01', '/home/pi/labs/CA1/recordings/video64.mp4'),
(66, 2, '2018-12-14 15:24:29', '/home/pi/labs/CA1/recordings/video65.mp4'),
(67, 2, '2018-12-14 15:24:39', '/home/pi/labs/CA1/recordings/video66.mp4'),
(68, 2, '2018-12-14 15:24:49', '/home/pi/labs/CA1/recordings/video67.mp4'),
(69, 2, '2018-12-14 15:25:45', '/home/pi/labs/CA1/recordings/video68.mp4'),
(70, 2, '2018-12-14 15:26:04', '/home/pi/labs/CA1/recordings/video69.mp4'),
(71, 2, '2018-12-14 15:26:13', '/home/pi/labs/CA1/recordings/video70.mp4'),
(72, 2, '2018-12-18 13:37:38', '/home/pi/labs/CA1/recordings/video71.mp4'),
(73, 2, '2018-12-18 13:37:47', '/home/pi/labs/CA1/recordings/video72.mp4'),
(74, 2, '2018-12-18 13:37:55', '/home/pi/labs/CA1/recordings/video73.mp4'),
(75, 2, '2018-12-18 13:38:08', '/home/pi/labs/CA1/recordings/video74.mp4'),
(76, 2, '2018-12-18 13:38:16', '/home/pi/labs/CA1/recordings/video75.mp4'),
(77, 2, '2018-12-18 13:38:25', '/home/pi/labs/CA1/recordings/video76.mp4'),
(78, 2, '2018-12-18 13:38:51', '/home/pi/labs/CA1/recordings/video77.mp4'),
(79, 1, '2018-12-18 14:57:39', '/home/pi/labs/CA1/recordings/video78.mp4'),
(80, 1, '2018-12-18 15:01:44', '/home/pi/labs/CA1/recordings/video79.mp4'),
(81, 1, '2018-12-18 15:01:52', '/home/pi/labs/CA1/recordings/video80.mp4'),
(82, 1, '2018-12-25 00:16:10', '/home/pi/labs/CA1/recordings/video81.mp4');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE IF NOT EXISTS `rooms` (
`Id` int(11) NOT NULL,
  `RoomName` varchar(45) NOT NULL,
  `IotDeviceName` varchar(45) NOT NULL
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`Id`, `RoomName`, `IotDeviceName`) VALUES
(1, 'Server Room 2', 'raspberrypi-1646322-SohWeeKiat'),
(2, 'Server Room', 'raspberrypi-1646322-SohWeeKiat2');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
`Id` int(11) NOT NULL,
  `Username` varchar(45) NOT NULL,
  `PasswordHash` varchar(100) NOT NULL,
  `LastLogin` datetime DEFAULT NULL,
  `ChatId` int(11) DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Id`, `Username`, `PasswordHash`, `LastLogin`, `ChatId`) VALUES
(1, 'admin', '$2b$12$GGtQBz/I1Km6K6tLEzVLv.eWuquu2ZyMlUL13z8jdQXibTtb5hflW', '2018-12-25 00:10:48', 417815220);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `access_logs`
--
ALTER TABLE `access_logs`
 ADD PRIMARY KEY (`Id`), ADD UNIQUE KEY `Id_UNIQUE` (`Id`);

--
-- Indexes for table `access_rights`
--
ALTER TABLE `access_rights`
 ADD PRIMARY KEY (`Id`), ADD UNIQUE KEY `Id_UNIQUE` (`Id`), ADD UNIQUE KEY `CardId_UNIQUE` (`CardId`), ADD KEY `access_rights_roomId_fk_idx` (`RoomId`), ADD KEY `access_rights_userId_fk_idx` (`UserId`);

--
-- Indexes for table `enviro_info`
--
ALTER TABLE `enviro_info`
 ADD PRIMARY KEY (`Id`), ADD UNIQUE KEY `Id_UNIQUE` (`Id`), ADD KEY `enviro_info_roomId_fk_idx` (`roomId`);

--
-- Indexes for table `motion_events`
--
ALTER TABLE `motion_events`
 ADD PRIMARY KEY (`Id`), ADD UNIQUE KEY `Id_UNIQUE` (`Id`), ADD KEY `motion_event_rooms_fk_idx` (`RoomId`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
 ADD PRIMARY KEY (`Id`), ADD UNIQUE KEY `Id_UNIQUE` (`Id`), ADD UNIQUE KEY `RoomName_UNIQUE` (`RoomName`), ADD UNIQUE KEY `IotDeviceName_UNIQUE` (`IotDeviceName`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
 ADD PRIMARY KEY (`Id`), ADD UNIQUE KEY `Username_UNIQUE` (`Username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `access_logs`
--
ALTER TABLE `access_logs`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `access_rights`
--
ALTER TABLE `access_rights`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `enviro_info`
--
ALTER TABLE `enviro_info`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=215;
--
-- AUTO_INCREMENT for table `motion_events`
--
ALTER TABLE `motion_events`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=83;
--
-- AUTO_INCREMENT for table `rooms`
--
ALTER TABLE `rooms`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
