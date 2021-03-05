from flask import Flask, render_template
from flask import request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query
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

        # Prevents duplication during registration
        query_u = """SELECT email FROM Passengers where email = %s;"""
        data_u = [em]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()
        if result_u != ():
            return render_template('Passengers_Unique.html')


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


        if occupation == 'showall':
            query1_filter = """SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
            FROM Passengers"""
            result1_filter = execute_query(db_connection, query1_filter).fetchall()

        else:
            query1_filter = """SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
                FROM Passengers WHERE occupation = %s;"""
            data1_filter = [occupation]
            result1_filter = execute_query(db_connection, query1_filter, data1_filter).fetchall()


        query2_dropdown = """SELECT occupation FROM Passengers  GROUP BY occupation;"""
        result2_dropdown = execute_query(db_connection, query2_dropdown).fetchall()

        results = [result1_filter, result2_dropdown]
        return render_template('Passengers.html', rows=results)
            



@webapp.route('/Passengers_Update/<int:id>', methods=['POST','GET'])
def passengers_update(id):

    db_connection = connect_to_database()
    
    if request.method == 'GET':
        print('The GET request')
        people_query = """SELECT passenger_id, first_name, last_name, birthdate, occupation, email 
            FROM Passengers WHERE passenger_id = %s"""  % (id)
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        return render_template("Passengers_Update.html", person = people_result)

    elif request.method == 'POST':
        passenger_id = id
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = request.form['birthdate']
        occupation = request.form['occupation']
        email = request.form['email']

        # Prevents duplication during registration
        query_u = """SELECT email FROM Passengers where email = %s;"""
        data_u = [email]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()

        query_u_em = """SELECT email FROM Passengers where passenger_id = %s;"""
        data_u_em = [passenger_id]
        result_u_em = execute_query(db_connection, query_u_em, data_u_em).fetchall()

        if result_u != () and result_u_em[0][0] != email:
            return render_template('Passengers_Unique.html')


        query = "UPDATE Passengers SET first_name = %s, last_name = %s, birthdate = %s, occupation = %s,  email = %s WHERE passenger_id = %s"
        data = [first_name, last_name, birthdate, occupation, email, int(passenger_id),]
        result = execute_query(db_connection, query, data)

        return redirect('/Passengers')




@webapp.route('/Passengers_Delete/<int:id>')
def passenger_delete(id):
    '''deletes a person with the given id'''
    db_connection = connect_to_database()
    query = "DELETE FROM Passengers WHERE passenger_id = %s"
    data = [id,]

    result = execute_query(db_connection, query, data)
    return redirect('/Passengers')




@webapp.route('/Commuter_Passes', methods=['POST', 'GET'])
def commuter_passes():

    db_connection = connect_to_database()

    if request.method == 'POST':

        em = request.form['email']
        cos = request.form['cost']
        st = request.form['start_date']
        ed = request.form['end_date']
        tid = request.form['trainline']

        pid = None
        if em != '':
            query_passenger = """SELECT passenger_id FROM Passengers WHERE email = %s GROUP BY passenger_id;"""
            data_passenger_em = [em]
            pid_fetch = list(execute_query(db_connection, query_passenger, data_passenger_em).fetchall())
            print("PRINT!!!!!!!!!!!!!!!!!!!!", pid_fetch)
            if pid_fetch != []:
                pid = int(pid_fetch[0][0])


        query = """INSERT INTO Commuter_Passes (cost, start_date, end_date, passenger_id, trainline_id) 
            VALUES (%s, %s, %s, %s, %s);"""

        data = [int(cos), st, ed, pid, int(tid)]
        execute_query(db_connection, query, data)
        return redirect('/Commuter_Passes')


    else:
        query1_showall = """select d1.commuter_pass_id, d1.cost, d1.start_date, d1.end_date, d3.trainline_company, 
    	d3.trainline_id, d2.email, d2.passenger_id from
    	(SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, cp.passenger_id, 
    	cp.trainline_id from Commuter_Passes cp) d1
    	LEFT JOIN
    	(select pa.email, pa.passenger_id from Passengers pa) as d2
    	on d1.passenger_id = d2.passenger_id
    	INNER JOIN
    	(select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
    	on d3.trainline_id = d1.trainline_id
        order by d1.commuter_pass_id;"""
        result1_showall = execute_query(db_connection, query1_showall).fetchall()

        query2_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
        result2_dropdown_tl = execute_query(db_connection, query2_dropdown_tl).fetchall()

        query3_dropdown_em = """SELECT email FROM Passengers;"""
        result3_dropdown_em = execute_query(db_connection, query3_dropdown_em).fetchall()

        results = [result1_showall, result2_dropdown_tl, result3_dropdown_em]
        return render_template('Commuter_Passes.html', rows=results)




@webapp.route('/Commuter_Passes_Search', methods=['POST', 'GET'])
def commuter_passes_search():

    db_connection = connect_to_database()

    if request.method == 'POST':

        query1_filter = """select d1.commuter_pass_id, d1.cost, d1.start_date, d1.end_date, d3.trainline_company, 
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
    	order by d1.commuter_pass_id;"""
        result1_filter = execute_query(db_connection, query1_filter).fetchall()

        query2_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
        result2_dropdown_tl = execute_query(db_connection, query2_dropdown_tl).fetchall()

        query3_dropdown_em = """SELECT email FROM Passengers;"""
        result3_dropdown_em = execute_query(db_connection, query3_dropdown_em).fetchall()

        results = [result1_filter, result2_dropdown_tl, result3_dropdown_em]
        return render_template('Commuter_Passes_Filter.html', rows=results)





@webapp.route('/Commuter_Passes_Update/<int:id>', methods=['POST','GET'])
def commuter_passes_update(id):

    db_connection = connect_to_database()
    
    if request.method == 'GET':
        
        query1_showall = """select d1.commuter_pass_id, d1.cost, d1.start_date, d1.end_date, d3.trainline_company, 
        d3.trainline_id, d2.email, d2.passenger_id from
        (SELECT cp.commuter_pass_id, cp.cost, cp.start_date, cp.end_date, cp.passenger_id, 
        cp.trainline_id from Commuter_Passes cp) d1
        LEFT JOIN
        (select pa.email, pa.passenger_id from Passengers pa) as d2
        on d1.passenger_id = d2.passenger_id
        INNER JOIN
        (select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
        on d3.trainline_id = d1.trainline_id
        AND d1.commuter_pass_id = %s"""  % (id)
        result1_showall = execute_query(db_connection, query1_showall).fetchone()

        query2_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
        result2_dropdown_tl = execute_query(db_connection, query2_dropdown_tl).fetchall()

        query3_dropdown_em = """SELECT email FROM Passengers;"""
        result3_dropdown_em = execute_query(db_connection, query3_dropdown_em).fetchall()

        results = [result1_showall, result2_dropdown_tl, result3_dropdown_em]
        return render_template('Commuter_Passes_Update.html', rows=results)


    elif request.method == 'POST':
        cid = id
        em = request.form['email']
        cos = request.form['cost']
        st = request.form['start_date']
        ed = request.form['end_date']
        tid = request.form['trainline']

        pid = None
        if em != '':
            query_passenger = """SELECT passenger_id FROM Passengers WHERE email = %s GROUP BY passenger_id;"""
            data_passenger_em = [em]
            pid_fetch = list(execute_query(db_connection, query_passenger, data_passenger_em).fetchall())
            print("PRINT!!!!!!!!!!!!!!!!!!!!", pid_fetch)
            if pid_fetch != []:
                pid = int(pid_fetch[0][0])


        query = """UPDATE Commuter_Passes SET cost = %s, start_date = %s, end_date = %s, passenger_id = %s, trainline_id = %s
                    WHERE commuter_pass_id = %s;"""

        data = [int(cos), st, ed, pid, int(tid), int(cid)]
        execute_query(db_connection, query, data)
        return redirect('/Commuter_Passes')




@webapp.route('/Commuter_Passes_Delete/<int:id>')
def commuter_passes_delete(id):

    db_connection = connect_to_database()

    query = "DELETE FROM Commuter_Passes WHERE commuter_pass_id = %s"
    data = [id,]

    result = execute_query(db_connection, query, data)
    return redirect('/Commuter_Passes')




@webapp.route('/Trainlines', methods=['POST', 'GET'])
def Trainlines():
    db_connection = connect_to_database()

    if request.method == 'POST':
        print('Add new trainline')
        trainline = request.form['trainline']

        # Prevents duplication during registration
        query_u = """SELECT trainline_company FROM Trainlines where trainline_company = %s;"""
        data_u = [trainline]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()
        if result_u != ():
            return render_template('Trainlines_Unique.html')


        query = '''INSERT INTO Trainlines (trainline_company) VALUES (%s)'''
        datat = [trainline]
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




@webapp.route('/Trainlines_Update/<int:id>', methods=['POST','GET'])
def trainlines_update(id):

    db_connection = connect_to_database()
    
    if request.method == 'GET':

        query = """select tl.trainline_id, tl.trainline_company, IFNULL(COUNT(x.trainline_id), 0) from Trainlines tl
        LEFT JOIN
        (select d3.trainline_id, d3.trainline_company, d1.start_date, d1.end_date from
        (SELECT cp.commuter_pass_id, cp.start_date, cp.end_date, cp.trainline_id from Commuter_Passes cp
        where cp.start_date < now() AND now() < cp.end_date) d1
        LEFT JOIN
        (select tl.trainline_id, tl.trainline_company from Trainlines tl) as d3
        on d3.trainline_id = d1.trainline_id) as x
        on tl.trainline_id = x.trainline_id
        WHERE tl.trainline_id = %s"""  % (id)
        result = execute_query(db_connection, query).fetchone()
        return render_template('Trainlines_Update.html', rows=result)

    if request.method == 'POST':
        
        tid = id
        trainline = request.form['trainline']

        # Prevents duplication during registration
        query_u = """SELECT trainline_company FROM Trainlines where trainline_company = %s;"""
        data_u = [trainline]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()
        if result_u != ():
            return render_template('Trainlines_Unique.html')

        query = """UPDATE Trainlines SET trainline_company = %s WHERE trainline_id = %s"""
        data = [trainline, int(tid)]
        execute_query(db_connection, query, data)
        return redirect('/Trainlines')




@webapp.route('/Trainlines_Delete/<int:id>')
def trainlines_delete(id):

    db_connection = connect_to_database()

    query = "DELETE FROM Trainlines WHERE trainline_id = %s"
    data = [id,]

    result = execute_query(db_connection, query, data)
    return redirect('/Trainlines')




@webapp.route('/Stations', methods=['POST', 'GET'])
def Stations():
    db_connection = connect_to_database()

    if request.method == 'POST':
        s = request.form['station']
        p = request.form['prefecture']

        # Prevents duplication during registration
        query_u = """SELECT station_name FROM Stations where station_name = %s;"""
        data_u = [s]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()
        if result_u != ():
            return render_template('Stations_Unique.html')


        query = """INSERT INTO Stations (station_name, prefecture_id) VALUES 
		 (%s, %s);"""
        data = [s, int(p),]
        execute_query(db_connection, query, data)
        return redirect('/Stations')

    else:
        query1_show = """SELECT st.station_id AS "Station ID", st.station_name AS "Station Name", 
    	pf.prefecture_name AS "Prefecture Jurisdiction", pf.prefecture_id AS "Prefecture ID"
    	FROM Stations st INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id ORDER BY station_id;"""
        result1_show = execute_query(db_connection, query1_show).fetchall()

        query2_dropdown_pr = """SELECT prefecture_id, prefecture_name FROM Prefectures GROUP BY prefecture_id;"""
        result2_dropdown_pr = execute_query(db_connection, query2_dropdown_pr).fetchall()


        results = [result1_show, result2_dropdown_pr]
        return render_template('Stations.html', rows=results)




@webapp.route('/Stations_Update/<int:id>', methods=['POST','GET'])
def stations_update(id):

    db_connection = connect_to_database()
    
    if request.method == 'GET':

        query1_show = """SELECT st.station_id AS "Station ID", st.station_name AS "Station Name", 
        pf.prefecture_name AS "Prefecture Jurisdiction", pf.prefecture_id AS "Prefecture ID"
        FROM Stations st INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id WHERE st.station_id = %s;""" % (id)
        result1_show = execute_query(db_connection, query1_show).fetchone()

        query2_dropdown_pr = """SELECT prefecture_id, prefecture_name FROM Prefectures GROUP BY prefecture_id;"""
        result2_dropdown_pr = execute_query(db_connection, query2_dropdown_pr).fetchall()


        results = [result1_show, result2_dropdown_pr]
        return render_template('Stations_Update.html', rows=results)


    if request.method == 'POST':

        s = request.form['station']
        p = request.form['prefecture']

        # Prevents duplication during registration
        query_u = """SELECT station_name FROM Stations where station_name = %s;"""
        data_u = [s]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()

        query_u_id = """SELECT station_id FROM Stations where station_name = %s;"""
        data_u_id = [s]
        result_u_id = execute_query(db_connection, query_u_id, data_u_id).fetchall()

        if result_u != () and result_u_id[0][0] != id:
            return render_template('Stations_Unique.html')
        
        query = """UPDATE Stations SET station_name = %s, prefecture_id = %s WHERE station_id = %s"""
        data = [s, int(p), id]
        execute_query(db_connection, query, data)
        return redirect('/Stations')
        



@webapp.route('/Stations_Delete/<int:id>')
def stations_delete(id):

    db_connection = connect_to_database()

    query = "DELETE FROM Stations WHERE station_id = %s"
    data = [id,]

    result = execute_query(db_connection, query, data)
    return redirect('/Stations')







@webapp.route('/Prefectures', methods=['POST', 'GET'])
def Prefectures():
    db_connection = connect_to_database()

    if request.method == 'POST':
        p = request.form['prefecture']

        # Prevents duplication during registration
        query_u = """SELECT prefecture_name FROM Prefectures where prefecture_name = %s;"""
        data_u = [p]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()
        if result_u != ():
            return render_template('Prefectures_Unique.html')


        query = """INSERT INTO Prefectures (prefecture_name) VALUES (%s)"""
        data = [p]
        execute_query(db_connection, query, data)
        return redirect('/Prefectures')
    else:
        query1_show_pr = """SELECT * from Prefectures;"""
        result1_show_pr = execute_query(db_connection, query1_show_pr).fetchall()

        query2_show_pa = """SELECT fq.passenger_id AS "Passenger ID", fq.first_name AS "First Name", fq.last_name AS "Last Name",
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
    	 AS fq GROUP BY passenger_id;"""
        result2_show_pa = execute_query(db_connection, query2_show_pa).fetchall()

        query3_dropdown_pr = """SELECT prefecture_id, prefecture_name FROM Prefectures GROUP BY prefecture_id;"""
        result3_dropdown_pr = execute_query(db_connection, query3_dropdown_pr).fetchall()


        results = [result1_show_pr, result2_show_pa, result3_dropdown_pr]
        return render_template('Prefectures.html', rows=results)



@webapp.route('/Prefectures_Search', methods=['POST', 'GET'])
def prefectures_search():
    db_connection = connect_to_database()

    if request.method == 'POST':
        query1_show_pr = """SELECT * from Prefectures;"""
        result1_show_pr = execute_query(db_connection, query1_show_pr).fetchall()
        
        prefecture = request.form['prefecture']
        query2_show_pa = """SELECT fq.passenger_id, fq.first_name, fq.last_name, fq.birthdate, fq.occupation, fq.email FROM 
        (SELECT pa.passenger_id, pa.first_name, pa.last_name, pa.birthdate, pa.occupation, pa.email, pf.prefecture_name
        FROM Passengers pa 
        INNER JOIN Commuter_Passes cp ON pa.passenger_id = cp.passenger_id
        INNER JOIN Trainlines tl ON cp.trainline_id = tl.trainline_id
        INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id
        INNER JOIN Prefectures pf ON st.prefecture_id = pf.prefecture_id) 
        AS fq 
        WHERE fq.prefecture_name = %s GROUP BY passenger_id;"""
        data = [prefecture]
        result2_show_pa = execute_query(db_connection, query2_show_pa, data).fetchall()

        query3_dropdown_pr = """SELECT prefecture_id, prefecture_name FROM Prefectures GROUP BY prefecture_id;"""
        result3_dropdown_pr = execute_query(db_connection, query3_dropdown_pr).fetchall()


        results = [result1_show_pr, result2_show_pa, result3_dropdown_pr]
        return render_template('Prefectures.html', rows=results)

    else:
        query1_show_pr = """SELECT * from Prefectures;"""
        result1_show_pr = execute_query(db_connection, query1_show_pr).fetchall()

        query2_show_pa = """SELECT fq.passenger_id AS "Passenger ID", fq.first_name AS "First Name", fq.last_name AS "Last Name",
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
    	 AS fq GROUP BY passenger_id;"""
        result2_show_pa = execute_query(db_connection, query2_show_pa).fetchall()

        query3_dropdown_pr = """SELECT prefecture_id, prefecture_name FROM Prefectures GROUP BY prefecture_id;"""
        result3_dropdown_pr = execute_query(db_connection, query3_dropdown_pr).fetchall()


        results = [result1_show_pr, result2_show_pa, result3_dropdown_pr]
        return render_template('Prefectures.html', rows=results)




@webapp.route('/Prefectures_Update/<int:id>', methods=['POST','GET'])
def prefectures_update(id):

    db_connection = connect_to_database()
    
    if request.method == 'GET':

        query1_show = """SELECT prefecture_id, prefecture_name FROM Prefectures WHERE prefecture_id = %s;""" % (id)
        results = execute_query(db_connection, query1_show).fetchone()

        return render_template('Prefectures_Update.html', rows=results)


    if request.method == 'POST':

        prid = id
        prefecture = request.form['prefecture']

        # Prevents duplication during registration
        query_u = """SELECT prefecture_name FROM Prefectures where prefecture_name = %s;"""
        data_u = [prefecture]
        result_u = execute_query(db_connection, query_u, data_u).fetchall()
        if result_u != ():
            return render_template('Prefectures_Unique.html')

        query = """UPDATE Prefectures SET prefecture_name = %s WHERE prefecture_id = %s"""
        data = [prefecture, int(prid)]
        execute_query(db_connection, query, data)
        return redirect('/Prefectures')




@webapp.route('/Prefectures_Delete/<int:id>')
def prefectures_delete(id):

    db_connection = connect_to_database()

    query = "DELETE FROM Prefectures WHERE prefecture_id = %s"
    data = [id,]

    result = execute_query(db_connection, query, data)
    return redirect('/Prefectures')







@webapp.route('/Trainlines_and_Stations', methods=['POST', 'GET'])
def Trainlines_and_Stations():
    db_connection = connect_to_database()

    if request.method == 'POST':
        tl = request.form['trainline']
        st = request.form['station']

        # Prevents duplication during registration
        query = """SELECT trainline_id, station_id FROM Trainlines_and_Stations where trainline_id = %s AND station_id = %s;"""
        data = [tl, st]
        result = execute_query(db_connection, query, data).fetchall()
        if result != ():
            return render_template('Trainlines_and_Stations_Unique.html')


        query = """INSERT INTO Trainlines_and_Stations (trainline_id, station_id) VALUES 
    	 (%s, %s);"""
        data = [int(tl), int(st),]
        execute_query(db_connection, query, data)
        return redirect('/Trainlines_and_Stations')

    else:
        query = """SELECT ts.trainline_and_station_id, tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
    	FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
    	INNER JOIN Stations st ON ts.station_id = st.station_id ORDER BY tl.trainline_id;; """
        result = execute_query(db_connection, query).fetchall()
            
        query_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
        result_dropdown_tl = execute_query(db_connection, query_dropdown_tl).fetchall()

        query_dropdown_st = """SELECT station_id, station_name FROM Stations GROUP BY station_id;"""
        result_dropdown_st = execute_query(db_connection, query_dropdown_st).fetchall()

        dropdown = [result_dropdown_tl, result_dropdown_st]
        header = ["trainline", "Trainline ID", "Trainline", "Station", "Station ID"]
        return render_template('Trainlines_and_Stations.html', rows=result, header=header, dropdown=dropdown)




@webapp.route('/Trainlines_and_Stations_Search', methods=['POST', 'GET'])
def trainlines_and_stations_search():
    db_connection = connect_to_database()

    if request.method == 'POST':
        if request.form["ts"] == "trainlines":

            query = """SELECT ts.trainline_and_station_id, tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
            FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
            INNER JOIN Stations st ON ts.station_id = st.station_id
            ORDER BY tl.trainline_id;"""
            result = execute_query(db_connection, query).fetchall()

            query_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
            result_dropdown_tl = execute_query(db_connection, query_dropdown_tl).fetchall()

            query_dropdown_st = """SELECT station_id, station_name FROM Stations GROUP BY station_id;"""
            result_dropdown_st = execute_query(db_connection, query_dropdown_st).fetchall()

            dropdown = [result_dropdown_tl, result_dropdown_st]
            header = ["trainline", "Trainline ID", "Trainline", "Station", "Station ID"]
            return render_template('Trainlines_and_Stations.html', rows=result, header=header, dropdown=dropdown)

        if request.form["ts"] == "stations":
            query = """SELECT ts.trainline_and_station_id, st.station_id, st.station_name, tl.trainline_company, tl.trainline_id
            FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
            INNER JOIN Stations st ON ts.station_id = st.station_id
            ORDER BY st.station_id;"""
            result = execute_query(db_connection, query).fetchall()
            
            query_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
            result_dropdown_tl = execute_query(db_connection, query_dropdown_tl).fetchall()

            query_dropdown_st = """SELECT station_id, station_name FROM Stations GROUP BY station_id;"""
            result_dropdown_st = execute_query(db_connection, query_dropdown_st).fetchall()

            dropdown = [result_dropdown_tl, result_dropdown_st]
            header = ["station", "Station ID", "Station", "Trainline", "Trainline ID"]
            return render_template('Trainlines_and_Stations.html', rows=result, header=header, dropdown=dropdown)

    else:
        query = """SELECT ts.trainline_and_station_id, tl.trainline_id, tl.trainline_company, st.station_name, st.station_id
        FROM Trainlines tl INNER JOIN Trainlines_and_Stations ts ON tl.trainline_id = ts.trainline_id
        INNER JOIN Stations st ON ts.station_id = st.station_id; """
        result = execute_query(db_connection, query).fetchall()
    
        query_dropdown_tl = """SELECT trainline_id, trainline_company FROM Trainlines GROUP BY trainline_id;"""
        result_dropdown_tl = execute_query(db_connection, query_dropdown_tl).fetchall()

        query_dropdown_st = """SELECT station_id, station_name FROM Stations GROUP BY station_id;"""
        result_dropdown_st = execute_query(db_connection, query_dropdown_st).fetchall()

        dropdown = [result_dropdown_tl, result_dropdown_st]
        header = ["trainline", "Trainline ID", "Trainline", "Station", "Station ID"]
        return render_template('Trainlines_and_Stations.html', rows=result, header=header, dropdown=dropdown)




@webapp.route('/delete_relationship/<int:id>')
def ts_delete(id):

    db_connection = connect_to_database()

    query = "DELETE FROM Trainlines_and_Stations WHERE trainline_and_station_id = %s"
    data = [id,]

    result = execute_query(db_connection, query, data)
    return redirect('/Trainlines_and_Stations')
























#-------------------------------------------------------------------------------------------------------------------------------------------------------------

# @webapp.route('/browse_bsg_people')
# #the name of this function is just a cosmetic thing
# def browse_people():
#     print("Fetching and rendering people web page")
#     db_connection = connect_to_database()
#     query = "SELECT fname, lname, homeworld, age, character_id from bsg_people;"
#     result = execute_query(db_connection, query).fetchall()
#     print(result)
#     return render_template('people_browse.html', rows=result)

# @webapp.route('/add_new_people', methods=['POST','GET'])
# def add_new_people():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         query = 'SELECT planet_id, name from bsg_planets'
#         result = execute_query(db_connection, query).fetchall()
#         print(result)

#         return render_template('people_add_new.html', planets = result)
#     elif request.method == 'POST':
#         print("Add new people!")
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#         data = (fname, lname, age, homeworld)
#         execute_query(db_connection, query, data)
#         return ('Person added!')


# @webapp.route('/home')
# def home():
#     db_connection = connect_to_database()
#     query = "DROP TABLE IF EXISTS diagnostic;"
#     execute_query(db_connection, query)
#     query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
#     execute_query(db_connection, query)
#     query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
#     execute_query(db_connection, query)
#     query = "SELECT * from diagnostic;"
#     result = execute_query(db_connection, query)
#     for r in result:
#         print(f"{r[0]}, {r[1]}")
#     return render_template('home.html', result = result)

# @webapp.route('/db_test')
# def test_database_connection():
#     print("Executing a sample query on the database using the credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from bsg_people;"
#     result = execute_query(db_connection, query)
#     return render_template('db_test.html', rows=result)

# #display update form and process any updates, using the same function
# @webapp.route('/update_people/<int:id>', methods=['POST','GET'])
# def update_people(id):
#     print('In the function')
#     db_connection = connect_to_database()
#     #display existing data
#     if request.method == 'GET':
#         print('The GET request')
#         people_query = 'SELECT character_id, fname, lname, homeworld, age from bsg_people WHERE character_id = %s'  % (id)
#         people_result = execute_query(db_connection, people_query).fetchone()

#         if people_result == None:
#             return "No such person found!"

#         planets_query = 'SELECT planet_id, name from bsg_planets'
#         planets_results = execute_query(db_connection, planets_query).fetchall()

#         print('Returning')
#         return render_template('people_update.html', planets = planets_results, person = people_result)
#     elif request.method == 'POST':
#         print('The POST request')
#         character_id = request.form['character_id']
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']

#         query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE character_id = %s"
#         data = (fname, lname, age, homeworld, character_id)
#         result = execute_query(db_connection, query, data)
#         print(str(result.rowcount) + " row(s) updated")

#         return redirect('/browse_bsg_people')

# @webapp.route('/delete_people/<int:id>')
# def delete_people(id):
#     '''deletes a person with the given id'''
#     db_connection = connect_to_database()
#     query = "DELETE FROM bsg_people WHERE character_id = %s"
#     data = (id,)

#     result = execute_query(db_connection, query, data)
#     return (str(result.rowcount) + "row deleted")



