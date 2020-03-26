# import mysql.connector
# from mysql.connector import Error
# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='Users',
#                                          user='root',
#                                          password='a303578B')
#     mySql_Create_Table_Query = """CREATE TABLE users ( 
#                             username VARCHAR(45),
#                             password VARCHAR(45),
#                             ) """
#     cursor = connection.cursor()
#     result = cursor.execute(mySql_Create_Table_Query)
#     print("Users Table created successfully ")
# except mysql.connector.Error as error:
#     print("Failed to create table in MySQL: {}".format(error))
# finally:
#     if (connection.is_connected()):
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed")

# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode
# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='Users',
#                                          user='root',
#                                          password='a303578B')
#     mySql_insert_query = """INSERT INTO Users (username, password) 
#                            VALUES 
#                            ('username', 'password') """
#     cursor = connection.cursor()
#     result = cursor.execute(mySql_insert_query)
#     connection.commit()
#     print("Record inserted successfully into Courses table")
#     cursor.close()
# except mysql.connector.Error as error:
#     print("Failed to insert record into Courses table {}".format(error))
# finally:
#     if (connection.is_connected()):
#         connection.close()
#         print("MySQL connection is closed")

# import mysql.connector
# from mysql.connector import Error
# def insertVariblesIntoTable(idcourses, name, courseno, deptid, timecomp, freqperyear, allemp):
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                              database='Courses',
#                                              user='root',
#                                              password='a303578B')
#         cursor = connection.cursor()
#         mySql_insert_query = """INSERT INTO Courses (idcourses, name, courseno, deptid, timecomp, freqperyear, allemp) 
#                                 VALUES (%s, %s, %s, %s, %s, %s, %s) """
#         recordTuple = (idcourses, name, courseno, deptid, timecomp, freqperyear, allemp)
#         cursor.execute(mySql_insert_query, recordTuple)
#         connection.commit()
#         print("Record inserted successfully into Courses table")
#     except mysql.connector.Error as error:
#         print("Failed to insert into MySQL table {}".format(error))
#     finally:
#         if (connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")
# insertVariblesIntoTable(3, 'Machine Soldering', 3, 'QA', 0.66, 0, 0)
# insertVariblesIntoTable(4, 'Preservation, Packaging and Handling', 4, 'QA', 0.66, 0, 0)

import os
from os import environ
from wtforms import Form, DecimalField, IntegerField, StringField, validators, SubmitField
from wtforms.validators import DataRequired
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, url_for, redirect, flash, request, session

class LoginForm(Form):
    username = StringField('Username:', [validators.DataRequired(message=('asdf'))])
    password = StringField('Password:', [validators.DataRequired(message=('asdf'))])
    login = SubmitField('Login')

class AddCourseForm(Form):
    idcourses = IntegerField('ID:', [validators.DataRequired(message=('asdf'))])
    name = StringField('Name:', [validators.DataRequired(message=('asdf'))])
    courseno = StringField('Course No:', [validators.DataRequired(message=('asdf'))])
    deptid = StringField('Dept ID:', [validators.DataRequired(message=('asdf'))])
    timecomp = DecimalField('Time Comp:', [validators.DataRequired(message=('asdf'))])
    freqperyear = IntegerField('Freq per Year:', [validators.DataRequired(message=('asdf'))])
    allemp = StringField('All Employees?', [validators.DataRequired(message=('asdf'))])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.secret_key='my secret key'

@app.route('/login')
def login():
    loginform = LoginForm(request.form)
    return render_template('login.html', loginform=loginform)

@app.route('/<username>/<password>', methods=['POST'])
def index(username, password):
    loginform = LoginForm(request.form)
    try:
        connection = mysql.connector.connect(host='localhost',
                                    database='Courses',
                                    user='root',
                                    password='a303578B')
        cursor = connection.cursor()
        mySql_insert_Query = """ SELECT * FROM users.users WHERE username=%s AND password=%s """
        username = request.form['username']
        password = request.form['password']
        recordTuple = (username, password)
        cursor.execute(mySql_insert_Query, recordTuple)
        userpass = cursor.fetchone()
        # print(userpass)
    except Error as error:
        print(format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    if userpass is None:
        message = 'Wrong username or password!'
        flash(message)
        return render_template('login.html', loginform=loginform)
    elif request.form['username'] == userpass[0] and request.form['password'] == userpass[1]:
        return render_template('index.html', loginform=loginform, username=username, password=password, userpass=userpass)
    else:
        return render_template('login.html', loginform=loginform)
    
@app.route('/courses')
def courses():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='Courses',
                                            user='root',
                                            password='a303578B')
        sql_select_Query = "select * from Courses"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    return render_template('courses.html', len=len(records), records=records)

@app.route('/addcourseform', methods=['GET', 'POST'])
def addcourseform():
    form=AddCourseForm(request.form)
    return render_template('addcourseform.html', form=form)

@app.route('/addcourse/<idcourses>/<name>/<courseno>/<deptid>/<timecomp>/<freqperyear>/<allemp>', methods=['GET', 'POST'])
def addcourse(idcourses, name, courseno, deptid, timecomp, freqperyear, allemp):
    try:
        form=AddCourseForm(request.form)
        connection = mysql.connector.connect(host='localhost',
                                    database='Courses',
                                    user='root',
                                    password='a303578B')
        cursor = connection.cursor()
        mySql_insert_Query = """INSERT INTO Courses (idcourses, name, courseno, deptid, timecomp, freqperyear, allemp) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s) """
        recordTuple = (idcourses, name, courseno, deptid, timecomp, freqperyear, allemp)
        cursor.execute(mySql_insert_Query, recordTuple)
        connection.commit()
    except Error as error:
        print(format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
    if request.method == 'POST':
        return redirect(url_for('addcourse', idcourses=request.form['idcourses'], name=request.form['name'], courseno=request.form['courseno'], deptid=request.form['deptid'], timecomp=request.form['timecomp'], freqperyear=request.form['freqperyear'], allemp=request.form['allemp']))
    return render_template('addcourse.html', form=form, idcourses=idcourses, name=name, courseno=courseno, deptid=deptid, timecomp=timecomp, freqperyear=freqperyear, allemp=allemp)

@app.route('/singlecourse/<idcourses>')
def singlecourse(idcourses):
    connection = mysql.connector.connect(host='localhost',
                                            database='Courses',
                                            user='root',
                                            password='a303578B')
    # sql_select_Query = "select * from Courses where idcourses = %s"
    cursor = connection.cursor()
    cursor.execute('select * from Courses where idcourses = %s', (idcourses,))
    singlerecord = cursor.fetchone()
    if (connection.is_connected()):
            cursor.close()
            connection.close()
    return render_template('singlecourse.html', singlerecord=singlerecord, idcourses=idcourses)

@app.route('/delete/<idcourses>')
def delete(idcourses):
    connection = mysql.connector.connect(host='localhost',
                                            database='Courses',
                                            user='root',
                                            password='a303578B')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Courses WHERE idcourses = %s', (idcourses,))
    connection.commit()
    if (connection.is_connected()):
            cursor.close()
            connection.close()
    return render_template('delete.html', idcourses=idcourses)

@app.route('/empcourses')
def empcourses():     
    return render_template('empcourses.html')

# @app.route('/courses')
# def coursesno():
#     try:
#         connection = mysql.connector.connect(host='localhost',
#                                             database='Courses',
#                                             user='root',
#                                             password='a303578B')
#         sql_select_Query = "select courseno from Courses"
#         cursor = connection.cursor()
#         cursor.execute(sql_select_Query)
#         recordsno = cursor.fetchall()
#     except Error as e:
#         print("Error", e)
#     finally:
#         if (connection.is_connected()):
#             connection.close()
#             cursor.close()
#             print("Closed")
#     return render_template('courses.html', recordsno=recordsno)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
        app.run(debug=True)
