-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.4.8-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- k8sti 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `k8sti` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `k8sti`;

-- 테이블 k8sti.project 구조 내보내기
CREATE TABLE IF NOT EXISTS `project` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `url` text NOT NULL,
  `branch` text DEFAULT NULL,
  `token` text DEFAULT NULL,
  `k8s_url` text NOT NULL,
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`pid`),
  KEY `uid` (`uid`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- 테이블 데이터 k8sti.project:~3 rows (대략적) 내보내기
DELETE FROM `project`;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` (`pid`, `title`, `url`, `branch`, `token`, `k8s_url`, `uid`) VALUES
	(1, 'test1', 'test1_url', 'test1', 'test1', 'test1_k8s', 1),
	(2, 'test2', 'test2_url', 'test2', 'test2', 'test2_k8s', 1),
	(3, 'test3', 'test3_url', 'test3', 'test3', 'test3_k8s', 1);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;

-- 테이블 k8sti.user 구조 내보내기
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(16) NOT NULL,
  `pw` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uname` (`uname`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- 테이블 데이터 k8sti.user:~3 rows (대략적) 내보내기
DELETE FROM `user`;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `uname`, `pw`) VALUES
	(1, 'admin', 'pbkdf2:sha256:150000$wJp5kE5Q$aa7f8b32c941e7f0f531272e3eba1ed3afc6638af86f802c1714f1989ad144b6'),
	(2, 'test1', 'pbkdf2:sha256:150000$TXXvk9vW$3b1e3fc5ab003428d2c582969c0c4c6a85a5c5b4e068dcbe15449d1984a8f57a'),
	(3, 'test2', 'pbkdf2:sha256:150000$tqMTmsBz$c78f78acf107918194a1f7b91823a69cf778f39aa5f5b3af1eccf5961255dead');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
