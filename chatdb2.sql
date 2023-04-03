USE chatdb;
CREATE TABLE publickey(
	id int PRIMARY KEY AUTO_INCREMENT,
	uid int NOT NULL,
	pubkey varchar(1024) NOT NULL,
	FOREIGN KEY (uid) REFERENCES users (id)
);