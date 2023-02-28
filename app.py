from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# Create templates folder and tell Flask to use it
app = Flask(__name__,template_folder='templates')
app.debug = True
app.config['SECRET_KEY'] = 'key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.route('/')
def show_start():
    return render_template('start.html', survey=survey)


@app.route('/begin', methods=["POST"])
def start_survey():
    """Clear session of responses."""
    session[RESPONSES_KEY] = []

    return redirect("/question/0")


@app.route('/question/<int:id>')
def show_question(id):
    """Display current question using id"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # Accessing question page too soon
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        # Already answered all questions
        return redirect("/end")
    if (len(responses) != id):
        # Tryin to access questions out of order
        flash(f"Please answer survey question below to continue.")
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[id]
    return render_template(
        "question.html", question_num=id, question=question)


@app.route('/answer', methods=["POST"])
def save_answer():
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
       
    if (len(responses) == len(survey.questions)):
        return redirect('/end')
    else:
        return redirect(f"/question/{len(responses)}")

@app.route('/end')
def thankyou():
    return render_template('end.html')