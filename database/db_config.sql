CREATE TABLE IF NOT EXISTS `User` (
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
	`bio` TEXT,
	`profile_pic` varchar(500)
);

CREATE TABLE IF NOT EXISTS `Book`(
	`id` varchar(30) PRIMARY KEY NOT NULL,
  	`title` varchar(100) NOT NULL,
  	`cover` varchar(300),
	`author` varchar(100),
  	`description` varchar(500),
	`rate` FLOAT
);

CREATE TABLE IF NOT EXISTS `Review`(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	`date` TIMESTAMP,
	`review` TEXT,
	`fk_User` INTEGER NOT NULL,
	`fk_Book` varchar(30) NOT NULL,
	FOREIGN KEY(fk_User) REFERENCES User(id),
	FOREIGN KEY(fk_Book) REFERENCES Book(id)
);

CREATE TABLE IF NOT EXISTS `Rate`(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	`date` TIMESTAMP,
	`rate` FLOAT,
	`fk_User` INTEGER NOT NULL,
	`fk_Book` varchar(30) NOT NULL,
	FOREIGN KEY(fk_User) REFERENCES User(id),
	FOREIGN KEY(fk_Book) REFERENCES Book(id)
);

CREATE TABLE IF NOT EXISTS `Status`(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	`date` TIMESTAMP,
	`status` INTEGER,
	`fk_User` INTEGER NOT NULL,
	`fk_Book` varchar(30) NOT NULL,
	FOREIGN KEY(fk_User) REFERENCES User(id),
	FOREIGN KEY(fk_Book) REFERENCES Book(id)
);

CREATE TABLE IF NOT EXISTS `Favorites`(
	`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	`fk_User` INTEGER NOT NULL,
	`fk_Book` varchar(30) NOT NULL,
	FOREIGN KEY(fk_User) REFERENCES User(id),
	FOREIGN KEY(fk_Book) REFERENCES Book(id)
);