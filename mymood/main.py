from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def start_app():
    start_msg = """
                Hello. You can tell me about your day, take an assessment, 
                or as me to look for professional help... Which would you like?
                """
    return question(start_msg)

@ask.intent("FeelingIntent")
def feelings():
    exit_msg = "How do you feel?"
    return question(exit_msg)


@ask.intent("AssessmentIntent")
def assessment():
    exit_msg = "Here is a question"
    return question(exit_msg)

@ask.intent("SuggestionIntent")
def suggest():
    exit_msg = "Here are some suggestions"
    return statement(exit_msg)

@ask.intent("ExitIntent")
def exit_app():
    exit_msg = "Goodbye."
    return statement(exit_msg)

@ask.intent("AMAZON.StopIntent")
def stop_intent():
    exit_msg = "Farewell"
    return statement(exit_msg)

@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
    exit_msg = "Sayonara"
    return statement(exit_msg)

@ask.intent("AMAZON.HelpIntent")
def help_intent():    
    help_msg = "Here is help"
    return statement(help_msg)


if __name__ == '__main__':
    app.run(debug=True)