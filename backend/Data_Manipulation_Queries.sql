-- add a new Passenger
INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email) VALUES 
(:first_name_input, :last_name_input, :birthdate_input, :occupation_input, :email_input)

-- get all passengers by occupation
SELECT * FROM Passengers WHERE occupation = :person_occupation_selected_from_passegers_page;

-- add a new Commuter Pass
INSERT INTO Commuter_Passes (passenger_id, cost, start_date, end_date, trainline_id) VALUES 
(:passenger_id_input, :cost_input, :start_date_input, :end_date_input, :trainline_id_from_dropdown_input)

-- get all commuters passes by passengers ID or by commuter pass ID
 SELECT * FROM (SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, tl.trainline_company, tl.trainline_id, pa.first_name, pa.last_name, pa.passenger_id
 FROM Passengers pa INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.commuter_pass_id 
 INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id) AS fq WHERE fq.passenger_id = :passenger_id_input_from_commuter_passes_page;

 SELECT * FROM (SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, tl.trainline_company, tl.trainline_id, pa.first_name, pa.last_name, pa.passenger_id
 FROM Passengers pa INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.commuter_pass_id 
 INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id) AS fq WHERE fq.commuter_pass_id = :commuter_pass_id_input_from_commuter_passes_page;

-- add a new Train Line
INSERT INTO Trainlines (trainline_company) VALUES 
(:trainline_company_input)

-- add a new Station
INSERT INTO Stations (station_name, prefecture_id) VALUES 
(:station_name_input, :prefecture_id_from_dropdown_input)

-- get all registered stations
SELECT st.station_id, st.station_name, pf.prefecture_name, pf.prefecture_id
FROM Stations st INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id;

-- add a new Prefecture
INSERT INTO Prefectures (prefecture_name) VALUES 
(:prefecture_name_input)

-- get all participatin prefectures
SELECT * from Prefectures;

-- get all passengers who can come to the selected prefecture via their commuter passes
 SELECT fq.passenger_id, fq.first_name, fq.last_name, fq.birthdate, fq.occupation, fq.email
 FROM (SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate, pa.occupation, pa.email, pf.prefecture_name
 FROM Passengers pa INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.commuter_pass_id 
 INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
 INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
 INNER JOIN Stations st ON ts.station_id = st.station_id
 INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
 AS fq WHERE fq.prefecture_name = :prefecture_name_from_dropdown_input;

-- associate a trainline with a station (M-to-M relationship addition)
INSERT INTO Trainlines_and_Stations (trainline_id, station_id) VALUES 
(:trainline_id_from_dropdown_input, :station_ids_from_checkbox_inputs)

-- associate a station with a trainline (M-to-M relationship addition)
INSERT INTO Trainlines_and_Stations (station_id, trainline_id) VALUES 
(:station_id_from_dropdown_input, :trainline_ids_from_checkbox_inputs)

-- get all train line and statons relationship
-- sort by trainline
SELECT tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
INNER JOIN Stations st ON ts.station_id = st.station_id
GROUP BY tl.trainline_company ORDER BY tl.trainline_company DESC;
-- sort by station
SELECT tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
INNER JOIN Stations st ON ts.station_id = st.station_id
GROUP BY st.station_name ORDER BY st.station_name DESC;


-- update a Passenger's data based on submission of the Update Passenger input form 
UPDATE Passengers SET first_name = :first_name_input, last_name = :last_name_input, birthdate = :birthdate_input, occupation = :occupation_input, email = :email_input WHERE id = :passenger_id_from_the_update_form

-- update a Commuter Pass' data based on submission of the Update Commuter_Pass input form 
UPDATE Commuter_Passes SET passenger_id = :passenger_id_input, cost = :cost_input, start_date = :start_date_input, end_date = :end_date_input, trainline_id = :trainline_id_from_dropdown_input WHERE id = :commuter_pass_id_from_the_update_form

-- update a Trainlines's data based on submission of the Update Trainline input form 
UPDATE Trainlines SET trainline_company = :trainline_company_input WHERE id = :trainline_id_from_the_update_form

-- update a Stations's data based on submission of the Update Station input form 
UPDATE Stations SET station_name = :station_name_input, prefecture_id = :prefecture_id_from_dropdown_input WHERE id = :station_id_from_the_update_form

-- update a Prefecture's data based on submission of the Update Prefecture input form 
UPDATE Prefectures SET prefecture_name = :prefecture_name_input WHERE id = :prefecture_id_from_the_update_form


-- delete a Passenger
DELETE FROM Passengers WHERE passenger_id = :passenger_id_selected_from_delete_button

-- delete a Commuter Pass
DELETE FROM Commuter_Passes WHERE commuter_pass_id = :commuter_pass_id_selected_from_delete_button

-- delete a Train Line
DELETE FROM Trainlines WHERE trainline_id = :trainline_id_selected_from_delete_button

-- delete a Station
DELETE FROM Stations WHERE station_id = :station_id_selected_from_delete_button

-- delete a Prefecture
DELETE FROM Prefectures WHERE prefecture_id = :prefecture_id_selected_from_delete_button

-- dis-associate a trainline from a station (M-to-M relationship deletion)
DELETE FROM Trainlines_and_Stations WHERE trainline_id = :trainline_id_delete_button AND station_id = :station_id_delete_button
