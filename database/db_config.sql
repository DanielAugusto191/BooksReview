CREATE TABLE IF NOT EXISTS `User` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS `Book`(
	`id` varchar(15) PRIMARY KEY NOT NULL,
  	`title` varchar(100) NOT NULL,
  	`cover` varchar(100),
  	`description` varchar(500),
	`rate` FLOAT
);

CREATE TABLE IF NOT EXISTS `Review`(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	`date` DATE,
	`rate` FLOAT,
	`fk_User` INTEGER NOT NULL,
	`fk_Book` INTEGER NOT NULL,
	FOREIGN KEY(fk_User) REFERENCES User(id),
	FOREIGN KEY(fk_Book) REFERENCES Book(id)
);