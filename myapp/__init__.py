from flask import Flask
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'
from myapp import routes

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123",
  database="COC_APP"
)

mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE users (username VARCHAR(255), password VARCHAR(255), email VARCHAR(255))")
# mycursor.execute("CREATE TABLE accounts (username VARCHAR(255), id VARCHAR(255))")