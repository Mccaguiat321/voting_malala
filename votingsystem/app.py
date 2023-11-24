from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cruds'
mysql = MySQL(app)

def fetch_first_numbercheck_value():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    tables = [row[0] for row in cur.fetchall()]
    data = {}
    for table in tables:
        cur.execute(f"SHOW COLUMNS FROM {table}")
        columns = [row[0] for row in cur.fetchall()]
        if "numbercheck" in columns:
            cur.execute(f"SELECT numbercheck FROM {table} LIMIT 1")
            value = cur.fetchone()
            if value:
                data[table] = value[0]
    cur.close()
    return data
@app.route('/', methods=['GET', 'POST'])
def newboto():
    tables_and_rows = fetch_tables_and_rows()
    numbercheck_data = fetch_first_numbercheck_value()
    return render_template('botohan.html', tables_and_rows=tables_and_rows,numbercheck_data=numbercheck_data)
@app.route('/admin')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM president")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', students=data)
@app.route('/vice_president')
def Pres():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vice_president")
    data = cur.fetchall()
    cur.close()
    return render_template('vice_pres.html', students=data)
@app.route('/secretary')
def secretary():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM secretary")
    data = cur.fetchall()
    cur.close()
    return render_template('secretary.html', students=data)
@app.route('/treasurer')
def treasurer():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM botomo")
    data = cur.fetchall()
    cur.close()
    return render_template('treasurer.html', students=data)
@app.route('/delete_all', methods=['POST'])
def delete_all():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM botomo")
    mysql.connection.commit()
    cur.close()
    return redirect('/treasurer')
@app.route('/admin')
def Indexx():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM president")
    president_data = cur.fetchall()

    cur.execute("SELECT * FROM vice_president")
    vice_president_data = cur.fetchall()

    cur.execute("SELECT * FROM secretary")
    secretary = cur.fetchall()

    cur.execute("SELECT * FROM treasurer")
    treasurer = cur.fetchall()
    cur.close()
    return render_template('admin.html', president_data=president_data, vice_president_data=vice_president_data, secretary=secretary, treasurer= treasurer)
@app.route('/')
def vice_president():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM vice_president")
    data = cur.fetchall()
    cur.close()
    return render_template('admin.html', students=data)
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO president (id,name) VALUES (NULL,%s)", (name,))
        mysql.connection.commit()
        return redirect(url_for('Index'))
@app.route('/inserts', methods = ['POST'])
def inserts():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO vice_president (id,name) VALUES (NULL,%s)", (name,))
        mysql.connection.commit()
        return redirect(url_for('Pres'))
@app.route('/insertss', methods = ['POST'])
def insertss():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO secretary (id,name) VALUES (NULL,%s)", (name,))
        mysql.connection.commit()
        return redirect(url_for('secretary'))
@app.route('/insertsss', methods = ['POST'])
def insertsss():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO treasurer (id,name) VALUES (NULL,%s)", (name,))
        mysql.connection.commit()
        return redirect(url_for('treasurer'))
@app.route('/update_value', methods=['POST'])
def update_value():
    input_name = request.form.get('president')
    vice_president = request.form.get('vice_president')
    secretary = request.form.get('secretary')
    treasurer = request.form.get('treasurer')
    voters = request.form.get('idnumber')
    cur = mysql.connection.cursor()
    query = "SELECT * FROM votes WHERE voters_number = %s"
    cur.execute(query, (voters,))
    result = cur.fetchone()
    if result:
        cur.close()
        flash("THE DATA ID NUMBER IS ALREADY IN THE DATABASE")
        return redirect(url_for('Indexx'))
    else:
        cur.execute("INSERT INTO votes (id, voters_number) VALUES (NULL, %s)", (voters,))
        mysql.connection.commit()

        if input_name:
            cur.execute("SELECT boto FROM president WHERE name = %s", (input_name,))
            current_value = cur.fetchone()

            if current_value is not None:
                cur.execute("UPDATE president SET boto = boto + 1 WHERE name = %s", (input_name,))
                mysql.connection.commit()
              
            else:
               flash("You have already voted for the president.")

        if vice_president:
            cur.execute("SELECT boto FROM vice_president WHERE name = %s", (vice_president,))
            current_value_vp = cur.fetchone()

            if current_value_vp is not None:
                cur.execute("UPDATE vice_president SET boto = boto + 1 WHERE name = %s", (vice_president,))
                mysql.connection.commit()
            else:
                flash("You have already voted for the vice president.")


        if secretary:
            cur.execute("SELECT boto FROM secretary WHERE name = %s", (secretary,))
            current_value_vps = cur.fetchone()

            if current_value_vps is not None:
                cur.execute("UPDATE secretary SET boto = boto + 1 WHERE name = %s", (secretary,))
                mysql.connection.commit()
             
            else:
                flash("You have already voted for the secretary.")

        if treasurer:
            cur.execute("SELECT boto FROM treasurer WHERE name = %s", (treasurer,))
            current_value_vpss = cur.fetchone()

            if current_value_vpss is not None:
                cur.execute("UPDATE treasurer SET boto = boto + 1 WHERE name = %s", (treasurer,))
                mysql.connection.commit()
            else:
                flash("You have already voted for the treasurer.")


        cur.close()
        flash(f"Voted Successfully NUMBER {voters}")
        return redirect(url_for('Indexx'))

@app.route('/update_values', methods=['POST'])
def update_values():
    voter_id = request.form.get('idnumber')
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM botomo WHERE voters_number = %s"
    cursor.execute(query, (voter_id,))
    result = cursor.fetchone()

    if result:
        flash("THE DATA ID NUMBER IS ALREADY IN THE DATABASE")
        return redirect(url_for('newboto'))  

    cursor.execute("INSERT INTO botomo (id, voters_number) VALUES (NULL, %s)", (voter_id,))
    mysql.connection.commit()

    cur = mysql.connection.cursor()

    for position, values in request.form.lists():
        if position != 'idnumber':
            for data in values:
                if data:
                    handle_position_vote(cur, position, 'name', 'boto', data)
    
    flash("VOTE SUCCESSFULLY")
    return redirect(url_for('newboto'))  

def handle_position_vote(cursor, position_table, name_column, boto_column, input_name):
    cursor.execute(f"SELECT {boto_column} FROM {position_table} WHERE {name_column} = %s", (input_name,))
    current_value = cursor.fetchone()

    if current_value is not None:
        voter_id = request.form.get('idnumber')
        cursor.execute(f"UPDATE {position_table} SET {boto_column} = {boto_column} + 1 WHERE {name_column} = %s", (input_name,))
        mysql.connection.commit()
    else:
        flash(f"You have already voted for the {position_table}.")

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM president WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))
@app.route('/deletes/<string:id_data>', methods = ['GET'])
def deletes(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM vice_president WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Pres'))
@app.route('/deletess/<string:id_data>', methods = ['GET'])
def deletess(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM secretary WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('secretary'))
@app.route('/deletesss/<string:id_data>', methods = ['GET'])
def deletesss(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM botomo WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('treasurer'))
@app.route('/updates', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE president SET name=%s
        WHERE id=%s
        """, (name, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Pres'))  
@app.route('/updatess', methods= ['POST', 'GET'])
def updates():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE vice_president SET name=%s
        WHERE id=%s
        """, (name, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Pres'))
@app.route('/updatesss', methods= ['POST', 'GET'])
def updatess():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE secretary SET name=%s
        WHERE id=%s
        """, (name, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('secretary'))
@app.route('/dsasss', methods=['POST', 'GET'])
def dsad():
    if request.method == 'POST':
        id_data = request.form['id']
        idmopo = request.form['idmopo']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE botomo SET voters_number=%s
        WHERE id=%s
        """, (idmopo, id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()  
        cur.close()
    return redirect(url_for('treasurer'))
@app.route('/admin')
def Indexs():
    return render_template('admin.html')
def fetch_tables_and_rows():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    tables = [row[0] for row in cur.fetchall()]
    table_data = {}

    for table in tables:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        table_data[table] = rows

    cur.close()
    return table_data
@app.route('/newcandidate', methods=['GET', 'POST'])
def newcandi():
    table_name = None
    numbercheck = None

    if request.method == 'POST':
        table_name = request.form.get('table_name')
        numbercheck = request.form.get('numbercheck')
        firstcandi = request.form.get('firstcandi')

        if table_name:
            cur = mysql.connection.cursor()
            cur.execute(f"SHOW TABLES LIKE '{table_name}'")
            existing_table = cur.fetchone()
            cur.close()

            if existing_table:
                flash("Table already exists. Choose a different name.", "danger")
            else:
                cur = mysql.connection.cursor()
                cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), boto INT, numbercheck INT)")
                cur.execute(f"INSERT INTO {table_name} (name,boto,numbercheck) VALUES (%s,%s,%s)", (firstcandi,0, numbercheck))
                mysql.connection.commit()
                cur.close()
                flash("Position Created Successfully", "success")

    tables_and_rows = fetch_tables_and_rows()

    return render_template('add_candi.html', tables_and_rows=tables_and_rows, table=table_name)
@app.route('/candidatesko', methods=['GET', 'POST'])
def candidatesko():
    tables_and_rows = fetch_tables_and_rows()
    numbercheck_datas = fetch_first_numbercheck_value()
    return render_template('candidates.html', tables_and_rows=tables_and_rows,numbercheck_data=numbercheck_datas )

#BAGo
@app.route('/deletessss/<string:table>/<string:id_data>', methods=['GET'])
def deletessssss(table, id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"DELETE FROM {table} WHERE id=%s", (id_data,))
        mysql.connection.commit()
        flash("Record has been deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting record: {str(e)}", "error")
    finally:
        cur.close()

    return redirect(url_for('candidatesko'))  
@app.route('/deletepos/<string:table>/', methods=['GET'])
def deletepos(table):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"DROP TABLE {table}")
        mysql.connection.commit()
        cur.close()
        flash("Table Has Been Deleted Successfully", "success")
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    return redirect(url_for('candidatesko'))

@app.route('/updatessssss/<string:table>/<string:id_data>', methods=['GET', 'POST'])
def update_record(table, id_data):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        new_name = request.form['name']

        cur.execute("SELECT * FROM {} WHERE name=%s AND id!=%s".format(table), (new_name, id_data))
        existing_record = cur.fetchone()

        if existing_record:
            flash("Record with name '{}' already exists".format(new_name), "danger")
            cur.close()
            return redirect(url_for('candidatesko'))
        else:
            cur.execute("UPDATE {} SET name=%s WHERE id=%s".format(table), (new_name, id_data))
            mysql.connection.commit()
            cur.close()
            flash("Record Has Been Updated Successfully", "success")
            return redirect(url_for('candidatesko'))

    cur.execute(f"SELECT * FROM {table} WHERE id=%s", (id_data,))
    row = cur.fetchone()
    cur.close()

    return render_template('newcandi.html', table=table, id_data=id_data, row=row)

@app.route('/add/<string:table>', methods=['GET', 'POST'])
def newinsert(table):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form.get('name')  
        values = request.form['values'] 
        
        cur.execute("SELECT * FROM {} WHERE name = %s".format(table), (name,))
        existing_record = cur.fetchone()
        
        if existing_record:
            flash("Record with name '{}' already exists".format(name), "danger")
            cur.close()
            return redirect(url_for('candidatesko'))
        else:
            cur.execute("INSERT INTO {} (name, boto,numbercheck) VALUES (%s, 0,%s)".format(table), (name,values))
            mysql.connection.commit()
            cur.close()
            flash("Record Has Been Updated Successfully", "success")
            return redirect(url_for('candidatesko'))

    return render_template('add_candi.html', table=table)
def mgatoto():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    tables = [row[0] for row in cur.fetchall()]
    table_data = {}

    for table in tables:
        if table != 'botomo':
            cur.execute(f"SELECT * FROM {table} ORDER BY boto DESC")
            rows = cur.fetchall()
            table_data[table] = rows

    cur.close()
    return table_data
@app.route('/mgaboto', methods=['GET', 'POST'])
def mgaboto():
    tables_and_rows = mgatoto()
    return render_template('mgaboto.html', tables_and_rows=tables_and_rows,  )

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)

