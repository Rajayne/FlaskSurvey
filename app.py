from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension

# Create templates folder and tell Flask to use it
app = Flask(__name__,template_folder='templates')

app.debug = True
# Debug Toolbar Requirement
app.config['SECRET_KEY'] = 'key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

from surveys import satisfaction_survey

@app.route('/')
def home():
    return render_template('home.html')

RESPONSES = []

@app.route('/question')
def question():
    return render_template('question.html')