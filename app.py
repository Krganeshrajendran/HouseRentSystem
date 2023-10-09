from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json
import os

app = Flask(__name__)

connection = sqlite3.connect('Database.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS intercity(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, rooms TEXT, brooms TEXT, feets TEXT, furnished TEXT, area1 TEXT, street TEXT, ccity TEXT, lcity TEXT, area TEXT, sdate TEXT, edate TEXT, datetime TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS intercity_book(id TEXT, name TEXT, phone TEXT, email TEXT, rooms TEXT, brooms TEXT, feets TEXT, furnished TEXT, area1 TEXT, street TEXT, ccity TEXT, lcity TEXT, area TEXT, sdate TEXT, edate TEXT, datetime TEXT, buyer TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS intracity(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, email TEXT, rooms TEXT, brooms TEXT, feets TEXT, furnished TEXT, area1 TEXT, street TEXT, ccity TEXT, area TEXT, sdate TEXT, edate TEXT, datetime TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS intracity_book(id TEXT, name TEXT, phone TEXT, email TEXT, rooms TEXT, brooms TEXT, feets TEXT, furnished TEXT, area1 TEXT, street TEXT, ccity TEXT, area TEXT, sdate TEXT, edate TEXT, datetime TEXT, buyer TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, location TEXT, DOB TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS admin(name TEXT, password TEXT)"""
cursor.execute(command)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM admin WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            connection = sqlite3.connect('Database.db')
            cursor = connection.cursor()

            query = "SELECT * FROM intracity"
            cursor.execute(query)
            result1 = cursor.fetchall()
            heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished','Current city', 'Area', 'Street Address', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

            query = "SELECT * FROM intercity"
            cursor.execute(query)
            result2 = cursor.fetchall()
            heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address', 'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']
            return render_template('adminlog.html', intralen=len(result1), interlen=len(result2), heading1=heading1, result1=result1, heading2=heading2, result2=result2)

        else:
            return render_template('index.html', msg=json.dumps("Sorry, Incorrect Credentials Provided,  Try Again"))
        
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password, mobile, email FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            f = open('Session.txt', 'w')
            f.write(result[0]+','+result[2]+','+result[3])
            f.close()
            return render_template('userlog.html', msg=json.dumps("Successfully log in"))
        else:
            return render_template('index.html', msg=json.dumps("Sorry, Incorrect Credentials Provided,  Try Again"))
        

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        DOB = request.form['dob']

        cursor.execute("INSERT INTO user (name, location, DOB, password, mobile, email) VALUES ('"+name+"', '"+location+"', '"+DOB+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg=json.dumps("Successfully Registered"))
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/userhome')
def userhome():
    return render_template('userlog.html')

@app.route('/interpost')
def interpost():
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    query = "SELECT * FROM intercity"
    cursor.execute(query)
    result1 = cursor.fetchall()
    heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']
    return render_template('interposts.html', interlen=len(result1), heading1=heading1, result1=result1)

@app.route('/intrapost')
def intrapost():
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    query = "SELECT * FROM intracity"
    cursor.execute(query)
    result2 = cursor.fetchall()
    heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']
    return render_template('intraposts.html', intralen=len(result2), heading2=heading2, result2=result2)

@app.route('/intersearch', methods=['GET', 'POST'])
def intersearch():
    if request.method == 'POST':
        city = request.form['city']
        area = request.form['area']

        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM intercity where lcity='"+city+"' and area = '"+area+"'"
        cursor.execute(query)
        result1 = cursor.fetchall()
        heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

        return render_template('interposts.html', interlen=len(result1), heading1=heading1, result1=result1)
    return render_template('interposts.html')

@app.route('/intrasearch', methods=['GET', 'POST'])
def intrasearch():
    if request.method == 'POST':
        city = request.form['city']
        area = request.form['area']

        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM intracity where area = '"+area+"'"
        cursor.execute(query)
        result2 = cursor.fetchall()
        print(result2)
        heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

        return render_template('intraposts.html', intralen=len(result2), heading2=heading2, result2=result2)
    return render_template('intraposts.html')

@app.route('/editinterpost/<Id>')
def editinterpost(Id):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    cursor.execute("DELETE FROM intercity WHERE id = '"+Id+"'")
    connection.commit()

    query = "SELECT * FROM intercity"
    cursor.execute(query)
    result2 = cursor.fetchall()
    heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']
   
    query = "SELECT * FROM intracity"
    cursor.execute(query)
    result1 = cursor.fetchall()
    heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

    return render_template('adminlog.html', interlen=len(result2), intralen=len(result1), heading1=heading1, result1=result1, heading2=heading2, result2=result2)

@app.route('/editintrapost/<Id>')
def editintrapost(Id):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    cursor.execute("delete from intracity where id = '"+Id+"'")
    connection.commit()

    query = "SELECT * FROM intercity"
    cursor.execute(query)
    result2 = cursor.fetchall()
    heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']
    
    query = "SELECT * FROM intracity"
    cursor.execute(query)
    result1 = cursor.fetchall()
    heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

    return render_template('adminlog.html', interlen=len(result2), intralen=len(result1), heading1=heading1, result1=result1, heading2=heading2, result2=result2)

@app.route('/intercity', methods=['GET', 'POST'])
def intercity():
    if request.method == 'POST':
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        details = request.form

        f = open('Session.txt', 'r')
        user_info = f.read()
        f.close()
        user_info = user_info.split(',')

        data = [user_info[0], user_info[1], user_info[2]]
        for row in details:
            data.append(details[row])
        
        
        from datetime import datetime
        today = datetime.now()
        data.append(today)

        cursor.execute("INSERT INTO intercity (name, phone, email, rooms, brooms, feets, furnished, area1, street, ccity, lcity, area, sdate, edate, datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
        connection.commit()

        return render_template('userlog.html', msg=json.dumps("Successfully updated"))
    return render_template('userlog.html')
    
@app.route('/intracity', methods=['GET', 'POST'])
def intracity():
    if request.method == 'POST':
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        details = request.form

        f = open('Session.txt', 'r')
        user_info = f.read()
        f.close()
        user_info = user_info.split(',')

        data = [user_info[0], user_info[1], user_info[2]]

        for row in details:
            data.append(details[row])
        
        from datetime import datetime
        today = datetime.now()
        data.append(today)

        cursor.execute("INSERT INTO intracity (name, phone, email, rooms, brooms, feets, furnished, area1, street, ccity, area, sdate, edate, datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
        connection.commit()

        return render_template('userlog.html', msg=json.dumps("Successfully updated"))
    return render_template('userlog.html')

@app.route('/adminintersearch', methods=['GET', 'POST'])
def adminintersearch():
    if request.method == 'POST':
        query = str(request.form['query'])
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM intercity where id = '"+query+"' ")
        result2 = cursor.fetchall()
        heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

        cursor.execute("SELECT * FROM intracity")
        result1 = cursor.fetchall()
        heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

        return render_template('adminlog.html', interlen=len(result2), intralen=len(result1), heading1=heading1, result1=result1, heading2=heading2, result2=result2)
    
    return render_template('adminlog.html')

@app.route('/adminintrasearch', methods=['GET', 'POST'])
def adminintrasearch():
    if request.method == 'POST':
        query = str(request.form['query'])
        connection = sqlite3.connect('Database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM intercity")
        result2 = cursor.fetchall()
        heading1 = ['ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

        cursor.execute("SELECT * FROM intracity where id = '"+query+"'")
        result1 = cursor.fetchall()
        heading2 = ['ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address',  'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

        return render_template('adminlog.html', interlen=len(result2), intralen=len(result1), heading1=heading1, result1=result1, heading2=heading2, result2=result2)

    return render_template('adminlog.html')


@app.route('/book_intercity/<Id>')
def book_intercity(Id):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    f = open('Session.txt', 'r')
    user_info = f.read()
    f.close()
    user_info = user_info.split(',')

    email = user_info[2]

    cursor.execute("SELECT * FROM intercity where id='"+Id+"'")
    result2 = cursor.fetchone()
    result2 = list(result2)
    result2.append(email)

    cursor.execute("insert into intercity_book values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", result2)
    connection.commit()

    cursor.execute("DELETE FROM intercity where id='"+Id+"'")
    connection.commit()

    return redirect(url_for('interpost'))
    


@app.route('/book_intracity/<Id>')
def book_intracity(Id):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    f = open('Session.txt', 'r')
    user_info = f.read()
    f.close()
    user_info = user_info.split(',')

    email = user_info[2]

    cursor.execute("SELECT * FROM intracity where id='"+Id+"'")
    result2 = cursor.fetchone()
    result2 = list(result2)
    result2.append(email)

    cursor.execute("insert into intracity_book values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", result2)
    connection.commit()

    cursor.execute("DELETE FROM intracity where id='"+Id+"'")
    connection.commit()

    return redirect(url_for('intrapost'))


@app.route('/bookedpost')
def bookedpost():
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()

    query = "SELECT * FROM intracity_book"
    cursor.execute(query)
    result1 = cursor.fetchall()

    heading2 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished','Current city', 'Area', 'Street Address', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']

    query = "SELECT * FROM intercity_book"
    cursor.execute(query)
    result2 = cursor.fetchall()

    heading1 = ['Unique ID', 'Owner Name', 'Owner Phone No','Owner Gmail','No of Bedrooms', 'No of Bathrooms', 'Square feets', 'Furnished', 'Current city', 'Area', 'Street Address', 'City looking for', 'Area interested in', 'Agreement Start date', 'Agreement End date', 'Date and Timestamp']
    return render_template('booked.html', intralen=len(result1), interlen=len(result2), heading1=heading1, result1=result1, heading2=heading2, result2=result2)

if __name__ == "__main__":
    app.run(debug=True)
