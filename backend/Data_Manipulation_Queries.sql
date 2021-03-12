-- get all passengers by occupation
SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
FROM Passengers WHERE occupation = %s;

-- get all passengers regardless of occupation
SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
FROM Passengers;


-- get all of active commuters passes (like not expired)
select d1.commuter_pass_id, d1.cost, d1.start_date, d1.end_date, d3.trainline_company, 
d3.trainline_id, d2.email, d2.passenger_id from
(SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, cp.passenger_id, 
cp.trainline_id from Commuter_Passes cp) d1
LEFT JOIN
(select pa.email, pa.passenger_id from Passengers pa) as d2
on d1.passenger_id = d2.passenger_id
INNER JOIN
(select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
on d3.trainline_id = d1.trainline_id
where d1.start_date <= now() AND d1.end_date >= now()
order by d1.commuter_pass_id;

-- get all of commuters passes (whether active or inactive)
select d1.commuter_pass_id, d1.cost, d1.start_date, d1.end_date, d3.trainline_company, 
d3.trainline_id, d2.email, d2.passenger_id from
(SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, cp.passenger_id, 
cp.trainline_id from Commuter_Passes cp) d1
LEFT JOIN
(select pa.email, pa.passenger_id from Passengers pa) as d2
on d1.passenger_id = d2.passenger_id
INNER JOIN
(select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
on d3.trainline_id = d1.trainline_id
order by d1.commuter_pass_id;


-- get all registered trainlines and the count of their active commuters
select tl.trainline_id, tl.trainline_company, IFNULL(COUNT(x.trainline_id), 0) from Trainlines tl
LEFT JOIN
(select d3.trainline_id, d3.trainline_company, d1.start_date, d1.end_date from
(SELECT cp.commuter_pass_id, cp.start_date, cp.end_date, cp.trainline_id from Commuter_Passes cp
where cp.start_date < now() AND now() < cp.end_date) d1
LEFT JOIN
(select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
on d3.trainline_id = d1.trainline_id) as x
on tl.trainline_id = x.trainline_id
group by tl.trainline_id;


-- get all registered stations and their respective prefecture jurisdiction
SELECT st.station_id AS "Station ID", st.station_name AS "Station Name", 
pf.prefecture_name AS "Prefecture Jurisdiction", pf.prefecture_id AS "Prefecture ID"
FROM Stations st INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id ORDER BY station_id;


-- get all participating prefectures in this database program
SELECT * from Prefectures;

-- get all passengers who can come to or might have been to the selected prefecture via their commuter passes
SELECT fq.passenger_id, fq.first_name, fq.last_name, fq.birthdate, fq.occupation, fq.email FROM 
(SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate, pa.occupation, pa.email, pf.prefecture_name
FROM Passengers pa 
INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
INNER JOIN Stations st ON ts.station_id = st.station_id
INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
AS fq 
WHERE fq.prefecture_name = %s GROUP BY passenger_id;

-- get all passengers who can come to or might have been to ALL prefectures via their commuter passes
SELECT fq.passenger_id, fq.first_name, fq.last_name, fq.birthdate, fq.occupation, fq.email FROM 
(SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate, pa.occupation, pa.email, pf.prefecture_name
FROM Passengers pa 
INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
INNER JOIN Stations st ON ts.station_id = st.station_id
INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
AS fq GROUP BY passenger_id;


-- get all train line and statons relationship

-- sort by trainline
SELECT ts.trainline_and_station_id, tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
INNER JOIN Stations st ON ts.station_id = st.station_id
ORDER BY tl.trainline_id;

-- sort by station
SELECT ts.trainline_and_station_id, st.station_id, st.station_name, tl.trainline_company, tl.trainline_id
FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
INNER JOIN Stations st ON ts.station_id = st.station_id
ORDER BY st.station_id;






-- add a new Passenger
INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email) VALUES (%s, %s, %s, %s, %s);

-- add a new Commuter Pass
INSERT INTO Commuter_Passes (cost, start_date, end_date, passenger_id, trainline_id) VALUES (%s, %s, %s, %s, %s);

-- add a new Train Line
INSERT INTO Trainlines (trainline_company) VALUES (%s)

-- add a new Station
INSERT INTO Stations (station_name, prefecture_id) VALUES (%s, %s);

-- add a new Prefecture
INSERT INTO Prefectures (prefecture_name) VALUES (%s)

-- associate a trainline with a station (M-to-M relationship addition)
INSERT INTO Trainlines_and_Stations (trainline_id, station_id) VALUES (%s, %s);






-- update a Passenger's data based on submission of the Update Passenger input form 
UPDATE Passengers SET first_name = %s, last_name = %s, birthdate = %s, occupation = %s, email = %s WHERE passenger_id = %s;

-- update a Commuter Pass' data based on submission of the Update Commuter_Pass input form 
UPDATE Commuter_Passes SET cost = %s, start_date = %s, end_date = %s, passenger_id = %s, trainline_id = %s WHERE commuter_pass_id = %s;

-- update a Trainlines's data based on submission of the Update Trainline input form 
UPDATE Trainlines SET trainline_company = %s WHERE trainline_id = %s;

-- update a Stations's data based on submission of the Update Station input form 
UPDATE Stations SET station_name = %s, prefecture_id = %s WHERE station_id = %s;

-- update a Prefecture's data based on submission of the Update Prefecture input form 
UPDATE Prefectures SET prefecture_name = %s WHERE prefecture_id = %s;






-- delete a Passenger
DELETE FROM Passengers WHERE passenger_id = %s;

-- delete a Commuter Pass
DELETE FROM Commuter_Passes WHERE commuter_pass_id = %s;

-- delete a Train Line
DELETE FROM Trainlines WHERE trainline_id = %s;

-- delete a Station
DELETE FROM Stations WHERE station_id = %s;

-- delete a Prefecture
DELETE FROM Prefectures WHERE prefecture_id = %s

-- delete a relationship between Trainline and Station (M-to-M relationship deletion)
DELETE FROM Trainlines_and_Stations WHERE trainline_and_station_id = %s
