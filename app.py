from flask import Flask, render_template, request, redirect, json # add `json`
from waitress import serve
import os
import database.db_connector as db
db_connection = db.connect_to_database()



# Configuration
app = Flask(__name__)






# Routes 

@app.route('/')
def root():
    return render_template("main.jinja")









@app.route('/passengers', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def passengers():

    query_occupation = '''SELECT occupation FROM Passengers GROUP BY occupation;'''

    cursor_occupation = db.execute_query(db_connection = db_connection, query = query_occupation)
    results_occupation = cursor_occupation.fetchall()




    if request.method == 'POST':
        form = request.form
        first_name = form['first_name']
        last_name = form['last_name']
        birthdate = form['birthdate']
        occupation = form['occupation']
        email = form['email']


        query_insert = '''INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email) VALUES (%s, %s, %s, %s, %s)'''
        data_insert = [first_name, last_name, birthdate, occupation, email]

        cursor_insert = db.execute_query(db_connection = db_connection, query = query_insert, query_params = data_insert)

        return redirect("/passengers")



    # occupation = "Student"

    # query = '''SELECT passenger_id AS "Passenger ID", first_name AS "First Name", last_name AS "Last Name", birthdate AS "Birthdate", occupation AS "Occupation", email AS "Email" FROM Passengers where occupation = "''' + occupation + '''";'''


    query = '''SELECT last_name AS "Last Name", first_name AS "First Name", passenger_id AS "Passenger ID", birthdate AS "Birthdate", occupation AS "Occupation", email AS "Email" FROM Passengers ORDER BY last_name'''

    cursor = db.execute_query(db_connection = db_connection, query = query)
    results_one = cursor.fetchall()




    results = [results_one, results_occupation]
    return render_template("Passengers.jinja", Passengers = results)











@app.route('/commuter-passes', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def commuter_passes():


    if request.method == 'POST':
        form = request.form

        
        email = form['passenger_email']
        cost = form['cost']
        start_date = form['start_date']
        end_date = form['end_date']
        trainline_id = int(form['trainline'])

        passenger_id = None
        if email != '':
            query_passenger = '''SELECT passenger_id FROM Passengers WHERE email = "''' + email + '''";'''
            cursor = db.execute_query(db_connection = db_connection, query = query_passenger)
            results = list(cursor.fetchall())
            if results != []:
                passenger_id = int(results[0]['passenger_id'])
        


        query_insert = '''INSERT INTO Commuter_Passes (cost, start_date, end_date, passenger_id, trainline_id) VALUES (%s, %s, %s, %s, %s)'''
        data_insert = [cost, start_date, end_date, passenger_id, trainline_id]

        cursor_insert = db.execute_query(db_connection = db_connection, query = query_insert, query_params = data_insert)

        return redirect("/commuter-passes")




    query = '''SELECT d1.commuter_pass_id AS "Commuter Pass ID", d1.cost AS "Cost Paid", d1.start_date AS "Start Date", d1.end_date AS "End Date", d3.trainline_company AS "Trainline Access", 
        d3.trainline_id AS "Trainline ID", d2.email AS "Passenger's Email", d2.passenger_id AS "Passenger's ID" from
        (SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, cp.passenger_id, 
        cp.trainline_id from Commuter_Passes cp) d1
        LEFT JOIN
        (select pa.email, pa.passenger_id from Passengers pa) as d2
        on d1.passenger_id = d2.passenger_id
        INNER JOIN
        (select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
        on d3.trainline_id = d1.trainline_id
        where d1.start_date < now() AND d1.end_date > now()
        order by d1.commuter_pass_id;'''

    cursor = db.execute_query(db_connection = db_connection, query = query)
    results_one = cursor.fetchall()


    query_trainline = '''SELECT trainline_id, trainline_company FROM Trainlines;'''
    cursor_trainline = db.execute_query(db_connection = db_connection, query = query_trainline)
    results_trainline = cursor_trainline.fetchall()

    results = [results_one, results_trainline]
    return render_template("Commuter_Passes.jinja", Commuter_Passes = results)







@app.route('/trainlines', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def trainlines():
    

    if request.method == 'POST':
        form = request.form
        trainline_company = form['trainline']

        query_insert = '''INSERT INTO Trainlines (trainline_company) VALUES (%s)'''
        data_insert = [trainline_company]

        cursor_insert = db.execute_query(db_connection = db_connection, query = query_insert, query_params = data_insert)

        return redirect("/trainlines")



    query = '''SELECT tl.trainline_id AS "Trainline ID", tl.trainline_company AS "Trainline Name", IFNULL(COUNT(x.trainline_id), 0) AS "Number of Active Commuters" from
        Trainlines tl
        LEFT JOIN
        (select d3.trainline_id, d3.trainline_company, d1.start_date, d1.end_date from
        (SELECT cp.commuter_pass_id, cp.start_date, cp.end_date, cp.trainline_id from Commuter_Passes cp
        where cp.start_date < now() AND now() < cp.end_date) d1
        LEFT JOIN
        (select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
        on d3.trainline_id = d1.trainline_id) as x
        on tl.trainline_id = x.trainline_id
        group by tl.trainline_id;'''

    cursor = db.execute_query(db_connection = db_connection, query = query)
    results = cursor.fetchall()
    return render_template("Trainlines.jinja", Trainlines = results)






@app.route('/stations', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def stations():

    query = '''SELECT st.station_id AS "Station ID", st.station_name AS "Station Name", pf.prefecture_name AS "Prefecture Jurisdiction", pf.prefecture_id AS "Prefecture ID"
        FROM Stations st INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id;'''

    cursor = db.execute_query(db_connection = db_connection, query = query)
    results = cursor.fetchall()
    return render_template("Stations.jinja", Stations = results)






@app.route('/prefectures', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def prefectures():


    if request.method == 'POST':
        form = request.form
        prefecture_name = form['prefecture']

        query_insert = '''INSERT INTO Prefectures (prefecture_name) VALUES (%s)'''
        data_insert = [prefecture_name]

        cursor_insert = db.execute_query(db_connection = db_connection, query = query_insert, query_params = data_insert)

        return redirect("/prefectures")



    query_one = '''SELECT prefecture_id AS "Prefecture ID", prefecture_name AS "Prefecture Name" from Prefectures;'''

    cursor_one = db.execute_query(db_connection = db_connection, query = query_one)
    results_one = cursor_one.fetchall()


    query_two = '''SELECT fq.passenger_id AS "Passenger ID", fq.first_name AS "First Name", fq.last_name AS "Last Name", fq.birthdate AS "Birthdate", fq.occupation AS "Occupation", fq.email AS "Email"
        FROM 
        (SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate, pa.occupation, pa.email, pf.prefecture_name
        FROM Passengers pa 
        INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
        INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
        INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id
        INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
        AS fq 
        WHERE fq.prefecture_name = "Tokyo Prefecture";'''

    cursor_two = db.execute_query(db_connection = db_connection, query = query_two)
    results_two = cursor_two.fetchall()



    results = [results_one, results_two]
    return render_template("Prefectures.jinja", Prefectures = results)






@app.route('/trainlines-and-stations', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def trainlines_and_stations():


    query_one = '''SELECT tl.trainline_id AS "Trainline ID", tl.trainline_company AS "Trainline Name", st.station_name AS "Station Name", st.station_id AS "Station ID"
        FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id
        ORDER BY tl.trainline_id;'''

    cursor_one = db.execute_query(db_connection = db_connection, query = query_one)
    results_one = cursor_one.fetchall()


    query_two = '''SELECT st.station_id AS "Station ID", st.station_name AS "Station Name", tl.trainline_company AS "Trainline Name", tl.trainline_id AS "Trainline ID" 
        FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id
        ORDER BY st.station_id;'''

    cursor_two = db.execute_query(db_connection = db_connection, query = query_two)
    results_two = cursor_two.fetchall()


    results = [results_one, results_two]
    return render_template("Trainlines_and_Stations.jinja", Trainlines_and_Stations = results)













# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 2077)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 
