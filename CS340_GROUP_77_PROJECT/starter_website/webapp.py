from flask import Flask, render_template
from flask import request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)


#---------------------------------------------------------------------------------------------
@webapp.route('/')
@webapp.route('/index')
def index():
    return render_template('index.html', title='Home')





@webapp.route('/Passengers', methods=['POST', 'GET'])
def passengers():

    db_connection = connect_to_database()

    if request.method == 'POST':
        ln = request.form['last_name']
        fn = request.form['first_name']
        bth = request.form['birthdate']
        op = request.form['occupation']
        em = request.form['email']
        query = """INSERT INTO Passengers (first_name, last_name, birthdate, occupation, email) 
            VALUES (%s, %s, %s, %s, %s);"""
        data = [fn, ln, bth, op, em,]
        execute_query(db_connection, query, data)
        return redirect('/Passengers')



    elif request.method == 'GET':

        query1_showall = """SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
            FROM Passengers;"""
        result1_showall = execute_query(db_connection, query1_showall).fetchall()


        query2_dropdown = """SELECT occupation FROM Passengers GROUP BY occupation;"""
        result2_dropdown = execute_query(db_connection, query2_dropdown).fetchall()



        results = [result1_showall, result2_dropdown]
        return render_template('Passengers.html', rows=results)



@webapp.route('/Passengers_Search', methods=['POST', 'GET'])
def passengers_search():

    db_connection = connect_to_database()

    if request.method == 'POST':

        occupation = request.form['occupation']

    

        query1_filter = """SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
            FROM Passengers WHERE occupation = %s;"""
        data1_filter = [occupation]
        result1_filter = execute_query(db_connection, query1_filter, data1_filter).fetchall()


        query2_dropdown = """SELECT occupation FROM Passengers  GROUP BY occupation;"""
        result2_dropdown = execute_query(db_connection, query2_dropdown).fetchall()



        results = [result1_filter, result2_dropdown]
        return render_template('Passengers.html', rows=results)
            








@webapp.route('/Commuter_Passes', methods=['POST', 'GET'])
def commuter_passes():

    db_connection = connect_to_database()

    if request.method == 'POST':
        em = request.form['email']
        cost = request.form['cost']
        st = request.form['start_date']
        ed = request.form['end_date']
        tl = request.form['trainline']
        query = """INSERT INTO Commuter_Passes (cost, start_date, end_date, trainline_id) 
            VALUES (%s, %s, %s, %s);"""
        data = [int(cost), st, ed, int(tl),]
        execute_query(db_connection, query, data)
        return redirect('/Commuter_Passes')

    else:
        query = """select d1.commuter_pass_id, d1.cost, d1.start_date, d1.end_date, d3.trainline_company, 
    	d3.trainline_id, d2.email, d2.passenger_id from
    	(SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, cp.passenger_id, 
    	cp.trainline_id from Commuter_Passes cp) d1
    	LEFT JOIN
    	(select pa.email, pa.passenger_id from Passengers pa) as d2
    	on d1.passenger_id = d2.passenger_id
    	INNER JOIN
    	(select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
    	on d3.trainline_id = d1.trainline_id
    	where d1.start_date < now() AND d1.end_date > now()
    	order by d1.commuter_pass_id;"""
        result = execute_query(db_connection, query).fetchall()
        return render_template('Commuter_Passes.html', rows=result)


@webapp.route('/Trainlines', methods=['POST', 'GET'])
def Trainlines():
    db_connection = connect_to_database()

    if request.method == 'POST':
        print('Add new trainline')
        trainline = request.form['trainline']
        query = '''INSERT INTO Trainlines (trainline_company) VALUES (%s)'''
        datat = [trainline,]
        execute_query(db_connection, query, datat)
        return redirect('/Trainlines')

    else:
        query = """select tl.trainline_id, tl.trainline_company, IFNULL(COUNT(x.trainline_id), 0) from Trainlines tl
    	LEFT JOIN
    	(select d3.trainline_id, d3.trainline_company, d1.start_date, d1.end_date from
    	(SELECT cp.commuter_pass_id, cp.start_date, cp.end_date, cp.trainline_id from Commuter_Passes cp
    	where cp.start_date < now() AND now() < cp.end_date) d1
    	LEFT JOIN
    	(select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
    	on d3.trainline_id = d1.trainline_id) as x
    	on tl.trainline_id = x.trainline_id
    	group by tl.trainline_id;"""
        result = execute_query(db_connection, query).fetchall()
        return render_template('Trainlines.html', rows=result)

@webapp.route('/Stations', methods=['POST', 'GET'])
def Stations():
    db_connection = connect_to_database()

    if request.method == 'POST':
        s = request.form['station']
        p = request.form['prefecture']
        query = """INSERT INTO Stations (station_name, prefecture_id) VALUES 
		 (%s, %s);"""
        data = [s, int(p),]
        execute_query(db_connection, query, data)
        return redirect('/Stations')

    else:
        query = """SELECT st.station_id AS "Station ID", st.station_name AS "Station Name", 
    	pf.prefecture_name AS "Prefecture Jurisdiction", pf.prefecture_id AS "Prefecture ID"
    	FROM Stations st INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id; """
        result = execute_query(db_connection, query).fetchall()
        return render_template('Stations.html', rows=result)

@webapp.route('/Prefectures', methods=['POST', 'GET'])
def Prefectures():
    db_connection = connect_to_database()

    if request.method == 'POST':
        p = request.form['prefecture']
        query = """INSERT INTO Prefectures (Prefecture_name) VALUES (%s)"""
        data = [p,]
        execute_query(db_connection, query, data)
        return redirect('/Prefectures')
    else:
        query = """SELECT * from Prefectures;"""
        result = execute_query(db_connection, query).fetchall()
        query2 = """SELECT fq.passenger_id AS "Passenger ID", fq.first_name AS "First Name", fq.last_name AS "Last Name",
    	fq.birthdate AS "Birthdate", fq.occupation AS "Occupation", fq.email AS "Email"
    	 FROM 
    	 (SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate,
    	 pa.occupation, pa.email, pf.prefecture_name
    	 FROM Passengers pa 
    	 INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
    	 INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
    	 INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
    	 INNER JOIN Stations st ON ts.station_id = st.station_id
    	 INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
    	 AS fq;"""
        result2 = execute_query(db_connection, query2).fetchall()
        return render_template('Prefectures.html', rows=result, rows2=result2)


@webapp.route('/Prefectures_Search', methods=['POST', 'GET'])
def prefectures_search():
    db_connection = connect_to_database()

    if request.method == 'POST':
        query = """SELECT * from Prefectures;"""
        result = execute_query(db_connection, query).fetchall()
        
        prefecture = request.form['prefecture']
        query = """SELECT fq.passenger_id, fq.first_name, fq.last_name, fq.birthdate, fq.occupation, fq.email FROM 
        (SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate, pa.occupation, pa.email, pf.prefecture_name
        FROM Passengers pa 
        INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
        INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
        INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id
        INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
        AS fq 
        WHERE fq.prefecture_name = %s;"""
        data = [prefecture,]
        result2 = execute_query(db_connection, query, data).fetchall()
        return render_template('Prefectures.html', rows=result, rows2=result2)

    else:
        query = """SELECT * from Prefectures;"""
        result = execute_query(db_connection, query).fetchall()
        query2 = """SELECT fq.passenger_id AS "Passenger ID", fq.first_name AS "First Name", fq.last_name AS "Last Name",
        fq.birthdate AS "Birthdate", fq.occupation AS "Occupation", fq.email AS "Email"
         FROM 
         (SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate,
         pa.occupation, pa.email, pf.prefecture_name
         FROM Passengers pa 
         INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
         INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
         INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
         INNER JOIN Stations st ON ts.station_id = st.station_id
         INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
         AS fq;"""
        result2 = execute_query(db_connection, query2).fetchall()
        return render_template('Prefectures.html', rows=result, rows2=result2)


@webapp.route('/Trainlines_and_Stations', methods=['POST', 'GET'])
def Trainlines_and_Stations():
    db_connection = connect_to_database()

    if request.method == 'POST':
        tl = request.form['trainline']
        st = request.form['station']
        query = """INSERT INTO Trainlines_and_Stations (trainline_id, station_id) VALUES 
    	 (%s, %s);"""
        data = [int(tl), int(st),]
        execute_query(db_connection, query, data)
        return redirect('/Trainlines_and_Stations')

    else:
        query = """SELECT tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
    	FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
    	INNER JOIN Stations st ON ts.station_id = st.station_id; """
        result = execute_query(db_connection, query).fetchall()
        return render_template('Trainlines_and_Stations.html', rows=result)


@webapp.route('/Trainlines_and_Stations_Search', methods=['POST', 'GET'])
def trainlines_and_stations_search():
    db_connection = connect_to_database()


    if request.method == 'POST':
        if request.form["ts"] == "trainlines":
            query = """SELECT tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
            FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
            INNER JOIN Stations st ON ts.station_id = st.station_id
            ORDER BY tl.trainline_id;"""
            result = execute_query(db_connection, query).fetchall()
            return render_template('Trainlines_and_Stations.html', rows=result)

        else:
            query = """SELECT tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
            FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
            INNER JOIN Stations st ON ts.station_id = st.station_id
            ORDER BY st.station_id;"""
            result = execute_query(db_connection, query).fetchall()
            return render_template('Trainlines_and_Stations.html', rows=result)

    else:
        query = """SELECT tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
        FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id; """
        result = execute_query(db_connection, query).fetchall()
        return render_template('Trainlines_and_Stations.html', rows=result)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------

@webapp.route('/browse_bsg_people')
#the name of this function is just a cosmetic thing
def browse_people():
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = "SELECT fname, lname, homeworld, age, character_id from bsg_people;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('people_browse.html', rows=result)

@webapp.route('/add_new_people', methods=['POST','GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT planet_id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('people_add_new.html', planets = result)
    elif request.method == 'POST':
        print("Add new people!")
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
        data = (fname, lname, age, homeworld)
        execute_query(db_connection, query, data)
        return ('Person added!')


@webapp.route('/home')
def home():
    db_connection = connect_to_database()
    query = "DROP TABLE IF EXISTS diagnostic;"
    execute_query(db_connection, query)
    query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
    execute_query(db_connection, query)
    query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
    execute_query(db_connection, query)
    query = "SELECT * from diagnostic;"
    result = execute_query(db_connection, query)
    for r in result:
        print(f"{r[0]}, {r[1]}")
    return render_template('home.html', result = result)

@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)

#display update form and process any updates, using the same function
@webapp.route('/update_people/<int:id>', methods=['POST','GET'])
def update_people(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s'  % (id)
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        planets_query = 'SELECT planet_id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall()

        print('Returning')
        return render_template('people_update.html', planets = planets_results, person = people_result)
    elif request.method == 'POST':
        print('The POST request')
        character_id = request.form['character_id']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_bsg_people')

@webapp.route('/delete_people/<int:id>')
def delete_people(id):
    '''deletes a person with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM bsg_people WHERE character_id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return (str(result.rowcount) + "row deleted")



