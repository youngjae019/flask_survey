from flask import Flask, redirect, render_template, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES = "responses"

app = Flask(__name__)
app.config['SECRET KEY'] = "it-is-a-secret!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

@app.route("/")
def survey_home_page():
    """Show survey title and start button"""

    return render_template("start_survey.html", survey=survey)

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Show current question"""
    responses = session.get(RESPONSES)

    if (responses is None):
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question"""

    choice = request.form['answer'] # get choice response
    responses = session[RESPONSES] # add to session RESPONSES list
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("complete.html")
