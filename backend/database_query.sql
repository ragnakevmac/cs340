-------------------------------------------------------------------------------------------
-- Queries to create tables.
-------------------------------------------------------------------------------------------

-- Query to create Passengers table.
CREATE TABLE Passengers (
    passenger_id int NOT NULL PRIMARY KEY auto_increment,
    first_name varchar(255) NOT NULL,
	last_name varchar(255) NOT NULL,
    birthdate date NOT NULL,
    occupation varchar(255) NOT NULL,
    email varchar(255) NOT NULL
    );

-- Query to create Trainlines table.
CREATE TABLE Trainlines (
	trainline_id int NOT NULL PRIMARY KEY auto_increment,
	trainline_company text NOT NULL
);

-- Query to create Commuter_Passes table.
CREATE TABLE Commuter_Passes (
	commuter_pass_id int NOT NULL PRIMARY KEY auto_increment,
	cost decimal(10,2) NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	passenger_id int, 
	FOREIGN KEY (passenger_id) REFERENCES Passengers (passenger_id)
	ON UPDATE CASCADE ON DELETE CASCADE,
	trainline_id int,
	FOREIGN KEY (trainline_id) REFERENCES Trainlines (trainline_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- Query to create Prefectures table.
CREATE TABLE Prefectures (
	prefecture_id int NOT NULL PRIMARY KEY auto_increment,
	prefecture_name text NOT NULL
);

-- Query to create Stations table.
CREATE TABLE Stations (
	station_id int NOT NULL PRIMARY KEY auto_increment,
	station_name varchar(255) NOT NULL,
	prefecture_id int,
	FOREIGN KEY (prefecture_id) REFERENCES Prefectures (prefecture_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- Query to create Trainlines_and_Stations relationship table.
CREATE TABLE Trainlines_and_Stations (
	trainline_and_station_id int NOT NULL PRIMARY KEY auto_increment,
	trainline_id int,
	FOREIGN KEY (trainline_id) REFERENCES Trainlines (trainline_id)
	ON UPDATE CASCADE ON DELETE CASCADE,
	station_id int,
	FOREIGN KEY (station_id) REFERENCES Stations (station_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-------------------------------------------------------------------------------------------
-- Queries to insert data.
-------------------------------------------------------------------------------------------

-- Query to insert data into the Trailines table.
-- Data from: https://en.wikipedia.org/wiki/East_Japan_Railway_Company#Lines
INSERT INTO Trainlines (trainline_company)
VALUES ("Yokosuka Line"),
("Yamanote Line"),
("Tokaido Line"),
("Nambu Line"),
("Narita Line"),
("Negishi Line"),
("Ito Line"),
("Ome Line"),
("Yokohama Line"),
("Shonan-Shinjuku Line");

-- Query to insert data into the Prefectures table.
-- Data from: https://en.wikipedia.org/wiki/Kant%C5%8D_region
INSERT INTO Prefectures (prefecture_name)
VALUES ("Ibaraki"),
("Tochigi"),
("Gunma"),
("Saitamal"),
("Chiba"),
("Kanagawa"),
("Tokyo");

-- Querty to insert data into the Stations table.
-- Data from: https://en.wikipedia.org/wiki/East_Japan_Railway_Company#Lines
INSERT INTO Stations (station_name)
VALUES ("Shinjuku Sation"),
("Ikebukuro Sation"),
("Tokyo Sation"),
("Yokohama Sation"),
("Shinagawa Station"),
("Shibuya Station"),
("Shimbashi Station"),
("Omiya Station"),
("Akihabara Station"),
("Kita-Senju Station");

-- Query to insert data into the Passengers table.
INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email)
VALUES ("Hiro", "Honda", "1994-4-10", "Office Worker", "taru@pmail.com"),
("Yasu", "Yamanoto", "1987-9-11", "Chef", "hiro@pmail.com"),
("Pancho", "Villa", "1985-3-11", "Handyman", "pancho@pmail.com"),
("Mario", "Bross", "1970-1-1", "Comedian", "mario@pmail.com");

-- Query to insert data into the Commuter_Passes table.
INSERT INTO Commuter_Passes (cost, start_date, end_date)
VALUES (132.00, "2021-2-10", "2021-6-10"),
(66.00, "2021-2-12", "2021-4-12"),
(33.00, "2021-2-20", "2021-3-20"),
(198.00, "2021-2-25", "2021-8-25");

-----------------------------------------------------------------------------------------------------
-- Queries to insert foreign keys.
-----------------------------------------------------------------------------------------------------

-- Querty to insert Commuter_Passes foreign keys.
INSERT INTO Commuter_Passes (passenger_id, trainline_id)
VALUES ((SELECT passenger_id FROM Passengers WHERE first_name = "Hiro" AND last_name = "Honda"), 
	(SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yokohama Line"));








