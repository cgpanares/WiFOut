-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 07, 2018 at 07:52 PM
-- Server version: 10.1.28-MariaDB
-- PHP Version: 7.1.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wifout`
--

-- --------------------------------------------------------

--
-- Table structure for table `allowed`
--

CREATE TABLE `allowed` (
  `allowed_ID` int(10) NOT NULL,
  `allowedDate` date NOT NULL,
  `bssidMAC` varchar(100) NOT NULL,
  `channelNum` varchar(100) NOT NULL,
  `nameSSID` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `blocked`
--

CREATE TABLE `blocked` (
  `blocked_ID` int(10) NOT NULL,
  `blockedDate` date NOT NULL,
  `bssidMACB` varchar(100) NOT NULL,
  `channelNumB` varchar(100) NOT NULL,
  `nameSSIDB` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `credentials`
--

CREATE TABLE `credentials` (
  `admin_ID` int(10) NOT NULL,
  `userName` varchar(100) NOT NULL,
  `passWord` varchar(1000) NOT NULL,
  `email` varchar(100) NOT NULL,
  `tracking` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `credentials`
--

INSERT INTO `credentials` (`admin_ID`, `userName`, `passWord`, `email`, `tracking`) VALUES
(2, 'wifoutadmin', 'pbkdf2:sha256:50000$Bg1NLfCd$34c143af9a6b9fbde356745722f4efd281bda8707629abf7181461d6505bd118', 'ragnamon@yahoo.com', '/');

-- --------------------------------------------------------

--
-- Table structure for table `DailyCount`
--

CREATE TABLE `DailyCount` (
  `dataD_ID` int(100) NOT NULL,
  `dateDaily` varchar(1000) NOT NULL,
  `monthAndYear` varchar(1000) NOT NULL,
  `AllowedD` varchar(1000) NOT NULL,
  `BlockedD` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `MonthlyCount`
--

CREATE TABLE `MonthlyCount` (
  `dataM_ID` int(100) NOT NULL,
  `dateMonthly` varchar(1000) NOT NULL,
  `yearOfMonth` varchar(1000) NOT NULL,
  `AllowedM` varchar(1000) NOT NULL,
  `BlockedM` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_ID` int(200) NOT NULL,
  `dateOfProcess` date NOT NULL,
  `yearOfProcess` varchar(1000) NOT NULL,
  `monthOfProcess` varchar(1000) NOT NULL,
  `dayOfProcess` varchar(1000) NOT NULL,
  `weekNofProcess` varchar(1000) NOT NULL,
  `timeOfProcess` varchar(1000) NOT NULL,
  `bssidMACR` varchar(1000) NOT NULL,
  `ssidNameR` varchar(1000) NOT NULL,
  `channelR` varchar(1000) NOT NULL,
  `StatusR` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tempChannel`
--

CREATE TABLE `tempChannel` (
  `channel_ID` int(100) NOT NULL,
  `channelNumb` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tempChannel`
--

INSERT INTO `tempChannel` (`channel_ID`, `channelNumb`) VALUES
(0, '1');

-- --------------------------------------------------------

--
-- Table structure for table `tempDate`
--

CREATE TABLE `tempDate` (
  `date_ID` int(100) NOT NULL,
  `monthRecordfromR` varchar(1000) NOT NULL,
  `yearRecordfromR` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `WeeklyCount`
--

CREATE TABLE `WeeklyCount` (
  `dataW_ID` int(100) NOT NULL,
  `dateWeekly` varchar(1000) NOT NULL,
  `yearOfWeek` varchar(1000) NOT NULL,
  `AllowedW` varchar(1000) NOT NULL,
  `BlockedW` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `YearlyCount`
--

CREATE TABLE `YearlyCount` (
  `dataY_ID` int(100) NOT NULL,
  `dateYearly` varchar(1000) NOT NULL,
  `AllowedY` varchar(1000) NOT NULL,
  `BlockedY` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `allowed`
--
ALTER TABLE `allowed`
  ADD PRIMARY KEY (`allowed_ID`);

--
-- Indexes for table `blocked`
--
ALTER TABLE `blocked`
  ADD PRIMARY KEY (`blocked_ID`);

--
-- Indexes for table `credentials`
--
ALTER TABLE `credentials`
  ADD PRIMARY KEY (`admin_ID`);

--
-- Indexes for table `DailyCount`
--
ALTER TABLE `DailyCount`
  ADD PRIMARY KEY (`dataD_ID`);

--
-- Indexes for table `MonthlyCount`
--
ALTER TABLE `MonthlyCount`
  ADD PRIMARY KEY (`dataM_ID`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_ID`);

--
-- Indexes for table `tempChannel`
--
ALTER TABLE `tempChannel`
  ADD PRIMARY KEY (`channel_ID`);

--
-- Indexes for table `tempDate`
--
ALTER TABLE `tempDate`
  ADD PRIMARY KEY (`date_ID`);

--
-- Indexes for table `WeeklyCount`
--
ALTER TABLE `WeeklyCount`
  ADD PRIMARY KEY (`dataW_ID`);

--
-- Indexes for table `YearlyCount`
--
ALTER TABLE `YearlyCount`
  ADD PRIMARY KEY (`dataY_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `allowed`
--
ALTER TABLE `allowed`
  MODIFY `allowed_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `blocked`
--
ALTER TABLE `blocked`
  MODIFY `blocked_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=98;

--
-- AUTO_INCREMENT for table `credentials`
--
ALTER TABLE `credentials`
  MODIFY `admin_ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `DailyCount`
--
ALTER TABLE `DailyCount`
  MODIFY `dataD_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `MonthlyCount`
--
ALTER TABLE `MonthlyCount`
  MODIFY `dataM_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `report_ID` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `tempDate`
--
ALTER TABLE `tempDate`
  MODIFY `date_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `WeeklyCount`
--
ALTER TABLE `WeeklyCount`
  MODIFY `dataW_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `YearlyCount`
--
ALTER TABLE `YearlyCount`
  MODIFY `dataY_ID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
