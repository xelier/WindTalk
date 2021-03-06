/*
SQLyog Ultimate v12.5.1 (64 bit)
MySQL - 8.0.11 : Database - forfundb
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`forfundb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;

create user 'forfun'@'%' identified by 'xelier';

grant ALL on forfundb.* to 'forfun'@'%';

USE `forfundb`;

/*Table structure for table `user` */


DROP TABLE IF EXISTS `USER`;

CREATE TABLE `USER` (
  `ID` int(11) NOT NULL AUTO_INCREMENT COMMENT '唯一标识',
  `USERNAME` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名',
  `PASSWORD` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `NICKNAME` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '昵称',
  `ROLE` int(1) NOT NULL DEFAULT '1' COMMENT '用户角色',
  `EMAIL` varchar(255) NOT NULL COMMENT '电子邮件',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `ARTICLE`;

CREATE TABLE `ARTICLE` (
  `ARTICLE_ID` int(11) NOT NULL COMMENT '文章ID',
  `TITLE` varchar(200) NOT NULL COMMENT '文章标题',
  `CONTENT` text NOT NULL COMMENT '文章内容',
  `CREATE_USER` int(11) NOT NULL COMMENT '创建者',
  `DESCRIPTION` text NOT NULL COMMENT '保留字段，作为文章简介',
  `CREATE_TIME` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`ARTICLE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `COMMENT`;

CREATE TABLE `COMMENT` (
  `COMMENT_ID` int(11) NOT NULL COMMENT '主键，文章唯一标示',
  `ARTICLE_ID` int(11) NOT NULL COMMENT '外键，文章唯一标示',
  `EMAIL` varchar(50) NOT NULL COMMENT '游客邮箱',
  `CONTENT` text NOT NULL COMMENT '评论内容',
  `CREATE_TIME` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`COMMENT_ID`),
  CONSTRAINT `FK_ARTICLE` FOREIGN KEY (`ARTICLE_ID`) REFERENCES `article` (`ARTICLE_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `IMAGE`;

CREATE TABLE `IMAGE` (
  `IMAGE_ID` int(11) NOT NULL COMMENT '图片的唯一标示',
  `ARTICLE_ID` int(11) NOT NULL COMMENT '图片所属文章',
  `FILE_PATH` varchar(100) NOT NULL COMMENT '文件路径',
  `CREATE_DATE` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`IMAGE_ID`),
  KEY `FK_IMG` (`ARTICLE_ID`),
  CONSTRAINT `FK_IMG` FOREIGN KEY (`ARTICLE_ID`) REFERENCES `article` (`ARTICLE_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



DROP TABLE IF EXISTS `SEQUENCE`;

CREATE TABLE `SEQUENCE` (
  `NAME` varchar(50) COLLATE utf8_bin NOT NULL COMMENT '序列的名字',
  `CURRENT_VALUE` int(11) NOT NULL COMMENT '序列的当前值',
  `INCREMENT` int(11) NOT NULL DEFAULT '1' COMMENT '序列的自增值',
  PRIMARY KEY (`NAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



DROP FUNCTION IF EXISTS CURRVAL;
CREATE  FUNCTION CURRVAL(seq_name VARCHAR(50)) RETURNS int(11)
    READS SQL DATA
    DETERMINISTIC
BEGIN
DECLARE VALUE INTEGER;
SET VALUE = 0;
SELECT CURRENT_VALUE INTO VALUE FROM SEQUENCE WHERE NAME = seq_name;
RETURN VALUE;
END



DROP FUNCTION IF EXISTS NEXTVAL;
CREATE FUNCTION NEXTVAL (seq_name VARCHAR(50))
     RETURNS INTEGER
     LANGUAGE SQL
     DETERMINISTIC
     CONTAINS SQL
     SQL SECURITY DEFINER
     COMMENT ''
BEGIN
     UPDATE SEQUENCE
          SET CURRENT_VALUE = CURRENT_VALUE + INCREMENT
          WHERE NAME = seq_name;
     RETURN currval(seq_name);
END


DROP FUNCTION IF EXISTS SETVAL;
CREATE FUNCTION SETVAL (seq_name VARCHAR(50), value INTEGER)
     RETURNS INTEGER
     LANGUAGE SQL
     DETERMINISTIC
     CONTAINS SQL
     SQL SECURITY DEFINER
     COMMENT ''
BEGIN
     UPDATE sequence
          SET CURRENT_VALUE = value
          WHERE NAME = seq_name;
     RETURN CURRVAL(seq_name);
END



INSERT INTO SEQUENCE VALUES ('USER_ID_SEQ', 0, 1);/*添加一个sequence名称和初始值，以及自增幅度*/

SELECT SETVAL('USER_ID_SEQ', 1);/*设置指定sequence的初始值*/

SELECT CURRVAL('USER_ID_SEQ');/*查询指定sequence的当前值*/

SELECT NEXTVAL('USER_ID_SEQ');/*查询指定sequence的下一个值*/



DROP TABLE IF EXISTS `OP_LOG`;

CREATE TABLE `OP_LOG` (
  `IP_HOST` varchar(50) COLLATE utf8_bin COMMENT '来源ip',
  `INTERFACE_NAME`  varchar(50) COLLATE utf8_bin COMMENT '接口名',
  `TIME` TIMESTAMP DEFAULT NOW() COMMENT '时间',
  `ID` int(11) DEFAULT '-1' COMMENT '操作人'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


ALTER TABLE ARTICLE ADD COLUMN 'TITLE' VARCHAR(200) NOT NULL COMMENT '文章标题';

INSERT INTO SEQUENCE VALUES ('ARTICLE_ID_SEQ', 0, 1);
INSERT INTO SEQUENCE VALUES ('COMMENT_ID_SEQ', 0, 1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
