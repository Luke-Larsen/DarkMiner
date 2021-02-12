SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `Work` (
  `Name` varchar(255) NOT NULL,
  `Version` int(11) NOT NULL,
  `CPU` varchar(255) NOT NULL,
  `Active` int(11) NOT NULL,
  `Mining` int(11) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `TotalMinedTime` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
COMMIT;
