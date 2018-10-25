SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `lj_xiaoqu`
-- ----------------------------
DROP TABLE IF EXISTS `lj_xiaoqu`;
CREATE TABLE `lj_xiaoqu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `community` varchar(255) DEFAULT NULL,
  `residence_name` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `coordinate` varchar(255) DEFAULT NULL,
  `build_time` varchar(255) DEFAULT NULL,
  `property_price` varchar(255) DEFAULT NULL,
  `property_company` varchar(255) DEFAULT NULL,
  `developer` varchar(255) DEFAULT NULL,
  `total_buildings` varchar(255) DEFAULT NULL,
  `total_houses` varchar(255) DEFAULT NULL,
  `bsn_dt` varchar(255) DEFAULT NULL,
  `tms` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `webst_nm` varchar(255) DEFAULT NULL,
  `crawl_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7726 DEFAULT CHARSET=utf8mb4;