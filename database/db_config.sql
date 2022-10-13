CREATE TABLE IF NOT EXISTS `accounts` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL
);