-- add a new Passenger
INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email) VALUES 
(:first_name_input, :last_name_input, :birthdate_input, :occupation_input, :email_input)

-- add a new Commuter Pass
INSERT INTO Commuter_Passes (passenger_id, cost, start_date, end_date, trainline) VALUES 
(:passenger_id_input, :cost_input, :start_date_input, :end_date_input, :trainline_id_from_dropdown_input)

-- add a new Train Line
INSERT INTO Trainlines (trainline_company) VALUES 
(:trainline_company_input)

-- add a new Station
INSERT INTO Stations (station_name, prefecture) VALUES 
(:station_name_input, :prefecture_id_from_dropdown_input)

-- add a new Prefecture
INSERT INTO Prefectures (prefecture_name) VALUES 
(:prefecture_name_input)

-- associate a trainline with a station (M-to-M relationship addition)
INSERT INTO Trainlines_and_Stations (trainline_id, station_id) VALUES 
(:trainline_id_from_dropdown_input, :station_ids_from_checkbox_inputs)

-- associate a station with a trainline (M-to-M relationship addition)
INSERT INTO Trainlines_and_Stations (station_id, trainline_id) VALUES 
(:station_id_from_dropdown_input, :trainline_ids_from_checkbox_inputs)


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
