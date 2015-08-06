from flask import Flask
import pymongo

# make a client 
client = pymongo.MongoClient()

# get a database
db = client.testlogin

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')

from logintester import views
