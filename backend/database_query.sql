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

------------------------------------------------------------------------------------------------
-- Queries to insert data into the tables.
------------------------------------------------------------------------------------------------

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
("Saitama"),
("Chiba"),
("Kanagawa"),
("Tokyo");

-- Querty to insert data into the Stations table.
-- Data from: https://en.wikipedia.org/wiki/East_Japan_Railway_Company#Lines
INSERT INTO Stations (station_name, prefecture_id)
VALUES ("Shinjuku Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo")),
("Ikebukuro Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo")),
("Tokyo Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo")),
("Yokohama Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Kanagawa")),
("Shinagawa Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Kanagawa")),
("Shibuya Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo")),
("Shimbashi Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo")),
("Omiya Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Saitama")),
("Akihabara Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo")),
("Kita-Senju Station", (SELECT prefecture_id FROM Prefectures WHERE prefecture_name = "Tokyo"));

-- Query to insert data into the Passengers table.
INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email)
VALUES ("Hiro", "Honda", "1994-4-10", "Office Worker", "taru@pmail.com"),
("Yasu", "Yamanoto", "1987-9-11", "Chef", "hiro@pmail.com"),
("Pancho", "Villa", "1985-3-11", "Handyman", "pancho@pmail.com"),
("Mario", "Bross", "1970-1-1", "Comedian", "mario@pmail.com");

-- Query to insert data into the Commuter_Passes table.
INSERT INTO Commuter_Passes (cost, start_date, end_date, passenger_id, trainline_id)
VALUES (132.00, "2021-2-10", "2021-6-10", 
(SELECT passenger_id FROM Passengers WHERE first_name = "Hiro" AND last_name = "Honda"),
(SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yokohama Line")),
(66.00, "2021-2-12", "2021-4-12", 
(SELECT passenger_id FROM Passengers WHERE first_name = "Yasu" AND last_name = "Yamanoto"),
(SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yamanote Line")),
(33.00, "2021-2-20", "2021-3-20", 
(SELECT passenger_id FROM Passengers WHERE first_name = "Pancho" AND last_name = "Villa"),
(SELECT trainline_id FROM Trainlines WHERE trainline_company = "Ome Line")),
(198.00, "2021-2-25", "2021-8-25", 
(SELECT passenger_id FROM Passengers WHERE first_name = "Mario" AND last_name = "Bross"),
(SELECT trainline_id FROM Trainlines WHERE trainline_company = "Shonan-Shinjuku Line"));

-----------------------------------------------------------------------------------------------------
-- Queries to insert foreign keys into the relationships table.
-----------------------------------------------------------------------------------------------------

INSERT INTO Trainlines_and_Stations (trainline_id, station_id)
VALUES ((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yamanote Line"),
(SELECT station_id FROM Stations WHERE station_name = "Tokyo Station")),
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Yokosuka Line"),
(SELECT station_id FROM Stations WHERE station_name = "Yokohama Station")),
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Narita Line"),
(SELECT station_id FROM Stations WHERE station_name = "Shinagawa Station")),
((SELECT trainline_id FROM Trainlines WHERE trainline_company = "Shonan-Shinjuku Line"),
(SELECT station_id FROM Stations WHERE station_name = "Shimbashi Station"));
