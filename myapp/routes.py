from . import app
from flask import request, render_template, flash, redirect, url_for, session
import mysql.connector
from myapp import coc_api
import datetime

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
    news_data = []
    # For Gold Pass data
    news_data = coc_api.GameInfo(coc_api.get_gp())
    news_data.gpStart = news_data.gpStart[:8]
    news_data.gpEnd = news_data.gpEnd[:8]
    news_data.gpStart = str(datetime.datetime(int(news_data.gpStart[:4]), int(news_data.gpStart[4:6]), int(news_data.gpStart[6:8])))[:10]
    news_data.gpEnd = str(datetime.datetime(int(news_data.gpEnd[:4]), int(news_data.gpEnd[4:6]), int(news_data.gpEnd[6:8])))[:10]
    news = news_data

    info = ["Info Item 1", "Info Item 2", "Info Item 3"]

    user_logged_in = 'username' in session
    return render_template('home.html', user_logged_in = user_logged_in, news= news, info = info)

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
            return redirect(url_for('view_accounts'))
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


@app.route('/view_accounts')
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
        account_data_list.append(account_data)

    user_logged_in = 'username' in session
    return render_template('view_accounts.html', accounts=accounts, account_data_list=account_data_list, user_logged_in = user_logged_in)

@app.route('/add', methods=['GET', 'POST'])
def add_account():
    if 'username' not in session:
        flash('You need to be logged in to add a user')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        account = request.form['id']

        # check if the account exists
        response = (coc_api.get_user(account))
        if response == "User does not exist":
            return redirect(url_for('add_account'))

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO accounts (username, id) VALUES (%s, %s)", (username, account))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Account added successfully')
        return redirect(url_for('view_accounts'))
    else:
        user_logged_in = 'username' in session
        return render_template('add_account.html', user_logged_in = user_logged_in)

@app.route('/view_accounts/account_details', methods=['GET'])
def view_account():
    if 'username' not in session:
        flash('You need to be logged in to add a user')
        return redirect(url_for('login'))

    if request.method == 'GET':
        tag = request.args.get('id')
        info = coc_api.PlayerInfo(coc_api.get_user(tag[1:]))
        user_logged_in = 'username' in session
        return render_template('account_details.html', id=tag, user_logged_in=user_logged_in, info=info)
