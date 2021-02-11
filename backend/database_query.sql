-- Query to create Passengers table.
CREATE TABLE Passengers (
    passenger_id int not null primary key auto_increment,
    first_name varchar(255) not null,
	last_name varchar(255) not null,
    birthdate date not null,
    occupation varchar(255) not null,
    home_station varchar(255) not null,
    phone_number varchar(255),
    email varchar(255) not null
    );

-- Query to create Commuter_Passes table.
CREATE TABLE Commuter_Passes (
	commuter_pass_id int NOT NULL PRIMARY KEY auto_increment,
	cost decimal(10,2),
	start_date date NOT NULL,
	end_date date NOT NULL,
	passenger_id int, 
	FOREIGN KEY (passenger_id) REFERENCES Passengers (passenger_id)
	ON UPDATE CASCADE ON DELETE CASCADE
);