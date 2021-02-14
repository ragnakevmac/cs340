-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 11, 2021 at 02:41 AM
-- Server version: 10.4.17-MariaDB-log
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_macandok`
--

-- --------------------------------------------------------

--
-- Table structure for table `Passengers`
--

DROP TABLE IF EXISTS `Passengers`;
CREATE TABLE `Passengers` (
  `passenger_id` int(11) NOT NULL PRIMARY KEY auto_increment,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `occupation` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `Trainlines`
--

DROP TABLE IF EXISTS `Trainlines`;
CREATE TABLE `Trainlines` (
  `trainline_id` int(11) NOT NULL PRIMARY KEY auto_increment,
  `trainline_company` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `Commuter_Passes`
--

DROP TABLE IF EXISTS `Commuter_Passes`;
CREATE TABLE `Commuter_Passes` (
  `commuter_pass_id` int(11) NOT NULL PRIMARY KEY auto_increment,
  `cost` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,

	passenger_id int, 
	FOREIGN KEY (passenger_id) REFERENCES Passengers (passenger_id)
	ON UPDATE CASCADE ON DELETE CASCADE,

	trainline_id int NOT NULL,
	FOREIGN KEY (trainline_id) REFERENCES Trainlines (trainline_id)
	ON UPDATE CASCADE ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `Prefectures`
--

DROP TABLE IF EXISTS `Prefectures`;
CREATE TABLE `Prefectures` (
  `prefecture_id` int(11) NOT NULL PRIMARY KEY auto_increment,
  `prefecture_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `Stations`
--

DROP TABLE IF EXISTS `Stations`;
CREATE TABLE `Stations` (
  `station_id` int(11) NOT NULL PRIMARY KEY auto_increment,
  `station_name` varchar(255) NOT NULL,

	prefecture_id int NOT NULL,
	FOREIGN KEY (prefecture_id) REFERENCES Prefectures (prefecture_id)
	ON UPDATE CASCADE ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `Trainlines_and_Stations`
--

DROP TABLE IF EXISTS `Trainlines_and_Stations`;
CREATE TABLE `Trainlines_and_Stations` (
  `trainline_and_station_id` int(11) NOT NULL PRIMARY KEY auto_increment,

	trainline_id int,
	FOREIGN KEY (trainline_id) REFERENCES Trainlines (trainline_id)
	ON UPDATE CASCADE ON DELETE CASCADE,

	station_id int,
	FOREIGN KEY (station_id) REFERENCES Stations (station_id)
	ON UPDATE CASCADE ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8;








--
-- Dumping data for table `Trainlines`
--

INSERT INTO `Trainlines` (`trainline_company`) VALUES
('Yamanote Line'),
('Hibiya Line'),
('Ginza Line'),
('Yokosuka Line'),
('Tokaido Line'),
('Nambu Line'),
('Narita Line'),
('Negishi Line'),
('Ito Line'),
('Ome Line'),
('Yokohama Line'),
('Shonan-Shinjuku Line');


--
-- Dumping data for table `Prefectures`
--

INSERT INTO `Prefectures` (`prefecture_name`) VALUES
('Tokyo Prefecture'),
('Kanagawa Prefecture'),
('Chiba Prefecture'),
('Saitama Prefecture'),
('Gunma Prefecture'),
('Tochigi Prefecture'),
('Ibaraki Prefecture');


--
-- Dumping data for table `Stations`
--

INSERT INTO `Stations` (`station_name`, `prefecture_id`) VALUES
('Maihama Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Chiba Prefecture')),
('Shinjuku Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture')),
('Yokohama Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Kanagawa Prefecture')),
('Ikebukuro Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture')),
('Tokyo Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture')),
('Shinagawa Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Kanagawa Prefecture')),
('Shibuya Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture')),
('Shimbashi Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture')),
('Omiya Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Saitama Prefecture')),
('Akihabara Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture')),
('Kita-Senju Station', (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = 'Tokyo Prefecture'));


--
-- Dumping data for table `Passengers`
--

INSERT INTO `Passengers` (`first_name`, `last_name`, `birthdate`, `occupation`, `email`) VALUES
('John', 'Smith', '2020-03-20', 'student', 'john_smith@gmail.com'),
('Pedro', 'Varo', '2020-02-20', 'student', 'pedro_varo@gmail.com'),
('Kevin', 'Macandog', '2020-01-20', 'student', 'Kevin_Macandog@gmail.com'),
('Risa', 'Oribe', '2020-01-20', 'student', 'Risa_Oribe@gmail.com'),
("Hiro", "Honda", "1994-4-10", "Office Worker", "taru@pmail.com"),
("Yasu", "Yamanoto", "1987-9-11", "Chef", "hiro@pmail.com"),
("Pancho", "Villa", "1985-3-11", "Handyman", "pancho@pmail.com"),
("Mario", "Bross", "1970-1-1", "Comedian", "mario@pmail.com");


--
-- Dumping data for table `Commuter_Passes`
--

INSERT INTO `Commuter_Passes` (`cost`, `start_date`, `end_date`, `passenger_id`, `trainline_id`) VALUES
('100.00', '2020-10-01', '2021-11-11', (SELECT passenger_id FROM Passengers WHERE first_name = "Risa" AND last_name = "Oribe"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yamanote Line")),
('90.00', '2021-01-11', '2021-05-25', (SELECT passenger_id FROM Passengers WHERE first_name = "Risa" AND last_name = "Oribe"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Ginza Line")),
('150.00', '2021-01-20', '2021-04-20', (SELECT passenger_id FROM Passengers WHERE first_name = "Risa" AND last_name = "Oribe"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Hibiya Line")),
('0.00', '2021-02-11', '2031-02-11', NULL, (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yamanote Line")),
('0.00', '2021-02-11', '2031-02-11', NULL, (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Ginza Line")),
('0.00', '2021-02-11', '2021-02-11', NULL, (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Hibiya Line")),
('132.00', "2021-02-10", "2021-06-10", (SELECT passenger_id FROM Passengers WHERE first_name = "Hiro" AND last_name = "Honda"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yokohama Line")),
('66.00', "2021-02-12", "2021-04-12", (SELECT passenger_id FROM Passengers WHERE first_name = "Yasu" AND last_name = "Yamanoto"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yamanote Line")),
('33.00', "2021-02-20", "2021-03-20", (SELECT passenger_id FROM Passengers WHERE first_name = "Pancho" AND last_name = "Villa"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Ome Line")),
('198.00', "2021-02-25", "2021-08-25", (SELECT passenger_id FROM Passengers WHERE first_name = "Mario" AND last_name = "Bross"), (SELECT trainline_id FROM Trainlines WHERE trainline_company = "Shonan-Shinjuku Line"));


--
-- Dumping data for table `Trainlines_and_Stations`
--

INSERT INTO Trainlines_and_Stations (trainline_id, station_id) VALUES 
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yamanote Line"),
(SELECT station_id FROM Stations WHERE station_name = "Tokyo Station")),
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yokosuka Line"),
(SELECT station_id FROM Stations WHERE station_name = "Yokohama Station")),
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Narita Line"),
(SELECT station_id FROM Stations WHERE station_name = "Shinagawa Station")),
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Shonan-Shinjuku Line"),
(SELECT station_id FROM Stations WHERE station_name = "Shimbashi Station"));












/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
