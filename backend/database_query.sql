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
    home_station varchar(255) NOT NULL,
    phone_number varchar(255),
    email varchar(255) NOT NULL
    );

-- Query to create Commuter_Passes table.
CREATE TABLE Commuter_Passes (
	commuter_pass_id int NOT NULL PRIMARY KEY auto_increment,
	cost decimal(10,2) NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	passenger_id int, 
	FOREIGN KEY (passenger_id) REFERENCES Passengers (passenger_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- Query to create Trainlines table.
CREATE TABLE Trainlines (
	trainlines_id int NOT NULL PRIMARY KEY auto_increment,
	trainline_company text NOT NULL
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

-- Query to create Commuter_Passes_and_Trainlines relationship table.
CREATE TABLE Commuter_Passes_and_Trainlines (
	commuter_pass_and_trainline_id int NOT NULL PRIMARY KEY auto_increment,
	commuter_pass_id int,
	FOREIGN KEY (commuter_pass_id) REFERENCES Commuter_Passes (commuter_pass_id)
	ON UPDATE CASCADE ON DELETE CASCADE,
	trainlines_id int,
	FOREIGN KEY (trainlines_id) REFERENCES Trainlines (trainlines_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);

-- Query to create Trainlines_and_Stations relationship table.
CREATE TABLE Trainlines_and_Stations (
	trainline_and_station_id int NOT NULL PRIMARY KEY auto_increment,
	trainlines_id int,
	FOREIGN KEY (trainlines_id) REFERENCES Trainlines (trainlines_id)
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





