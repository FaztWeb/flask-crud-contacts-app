from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

# initializations
app = Flask(__name__)

# Mysql Connection
mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flaskcrud"
)

# settings
app.secret_key = "mysecretkey"

# creating a database
mycursor = mysql.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS flaskcrud ")

# creating an sql table "contacts"
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS contacts (contactsID INT NULL AUTO_INCREMENT, fullname VARCHAR(60), email VARCHAR(255), phone VARCHAR(30),  PRIMARY KEY (contactsID) )")

# routes
@app.route('/')
def Index():
    mycursor.execute('SELECT * FROM contacts')
    data = mycursor.fetchall()
    return render_template('index.html', contacts=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        mycursor.execute(
            "INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    mycursor.execute(f'SELECT * FROM contacts WHERE contactsID = {id}')
    data = mycursor.fetchall()
    mycursor.close()
    print(data[0])
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        mycursor.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE contactsID = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_contact(id):
    mycursor.execute(f'DELETE FROM contacts WHERE contactsID = {id}')
    mysql.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))
