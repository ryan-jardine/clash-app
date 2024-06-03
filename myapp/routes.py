from . import app
from flask import request, render_template, flash, redirect, url_for, session
import mysql.connector
from myapp import coc_api

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="COC_APP"
    )
    return connection

@app.route('/')
def main():
    if 'username' in session:
        return render_template('loggedin_home.html')
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out')
    return redirect(url_for('login'))


# Handles loading both the page, and querying the database
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and user['password'] == password:
            session['username'] = username
            flash('Login Success')
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            flash('Invalid username or password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Username or email already exists')
            cursor.close()
            connection.close()
            return redirect(url_for('login'))


        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                       (username, password, email))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Registration successful')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        flash('You are not logged in')
        return redirect(url_for('login'))

@app.route('/dashboard/view_accounts')
def view_accounts():
    if 'username' not in session:
        flash('You need to be logged in to view accounts')
        return redirect(url_for('login'))

    username = session['username']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id FROM accounts WHERE username = %s", (username,))
    accounts = cursor.fetchall()
    cursor.close()
    connection.close()

    # Fetch additional data from the API for each account
    account_data_list = []
    for account in accounts:
        account_data = coc_api.PlayerInfo(coc_api.get_user(account['id']))
        #account_data = coc_api.get_user(account['id'])
        account_data_list.append(account_data)

    return render_template('view_accounts.html', accounts=accounts, account_data_list=account_data_list)

@app.route('/dashboard/add', methods=['GET', 'POST'])
def add_account():
    if 'username' not in session:
        flash('You need to be logged in to add a user')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        account = request.form['id']


        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts (username, id) VALUES (%s, %s)", (username, account))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Account added successfully')
        return redirect(url_for('dashboard'))
    else:
        return render_template('add_account.html')
