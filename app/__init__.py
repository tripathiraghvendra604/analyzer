from flask import Flask
from mongokit import Connection


# configuring mongodb
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('config')
connection = Connection(app.config['MONGODB_HOST'],
						app.config['MONGODB_PORT'])

app.secret_key= 'GuessItIfUCan'
		
from app import views, models
