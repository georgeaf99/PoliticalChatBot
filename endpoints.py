import flask

from flask import request

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "PoliticalChatBot is up and running!"
