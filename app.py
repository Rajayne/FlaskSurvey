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

# QUESTIONS = {
#     0: "Question 1",
#     1: "Question 2",
#     2: "Question 3",
#     3: "Question 4",
#     4: "Question 5",
# }

# Int: indicates id should be converted to integer
# .get(var, alt) if var not found will return alt i.e. no post 5
# @app.route('/question/<int:id>')
# def find_question(id):
#     question = QUESTIONS.get(id, "Question not found")
#     return f"<p>{question}</p>"

@app.route('/question')
def find_question():
    return render_template('question.html')

@app.route('/answer', methods=["POST"])
def save_answer():
    answer = request.form.get('answer',None)
    if answer == None:
        flash('Please select an option!')
        return redirect('/question')
    elif answer in RESPONSES:
        flash("Question already answered!", "error")
        return redirect('/')
    else:
        RESPONSES.append(answer)
        flash("Question answered!", "success")
        return redirect('/question')