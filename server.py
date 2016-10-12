from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key= 'Secret'
mysql = MySQLConnector(app,'mydb')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

@app.route('/')
def index():
    query = "SELECT * FROM friends"                          
    friends = mysql.query_db(query)                           
    return render_template('index.html', all_friends=friends) 

@app.route('/add_friend', methods=['POST'])
def create():
	error = 0

	if len(request.form['email']) < 1:
		error += 1
		flash("Email cannot be blank!")
	elif not EMAIL_REGEX.match(request.form['email']):
		error += 1
		flash("Invalid Email Address!")
	else:
		flash("Success with your email!")

	if len(request.form['first_name']) < 1:
		error += 1
		flash("First Name cannot be blank!")
	elif not (request.form['first_name'].isalpha()):
		error += 1
		flash("Invalid Name! Only letters allowed!")
	else:
		flash("Success with first name!")                      # END OF FIRST NAME

	if len(request.form['last_name']) < 1:
		error += 1
		flash("Last Name cannot be blank!")
	elif not (request.form['last_name'].isalpha()):
		error += 1
		flash("Invalid Name! Only letters allowed!")
	else:
		flash("Success with last name!")                         # END OF LAST NAME
	if error == 0:
		query = "INSERT INTO friends (first_name, last_name, email, created_at) VALUES (:first_name, :last_name, :email, NOW())"
		data = {
			 'first_name': request.form['first_name'], 
			 'last_name':  request.form['last_name'],
			 'email': request.form['email']
			}
		mysql.query_db(query, data)


	return redirect('/')

@app.route('/update/<friend_id>') 
def update(friend_id):
	query = "SELECT * FROM friends WHERE id=:id"
	data = {
			'id': friend_id
	}
	friend = mysql.query_db(query, data)
	return render_template('update.html', friend = friend)

@app.route('/confirmupdate/<friend_id>', methods=['POST'])
def confirmupdate(friend_id):
	print "hello"
	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id= :id"
	data = {
			 'id': friend_id,
			 'first_name': request.form['first_name'], 
			 'last_name':  request.form['last_name'],
			 'email': request.form['email']
           }
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/delete/<friend_id>') 
def delete(friend_id):
	query = "SELECT * FROM friends WHERE id=:id"
	data = {
			'id': friend_id
	}
	friend = mysql.query_db(query, data)
	return render_template('delete.html', friend = friend)

@app.route('/deleteuser/<friend_id>')
def deleteuser(friend_id):
	query = "DELETE FROM friends WHERE id = :id"
	data = {
			'id': friend_id
			}
	mysql.query_db(query, data)
	return redirect('/')



app.run(debug=True)








