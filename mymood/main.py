from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')

#TODO fix all hardcoded responses

@ask.launch
def start_app():
    start_msg = """
                Hello. You can tell me about your day, take an assessment, 
                or ask me to look for professional help... Which would you like?
                """
    reprompt_msg =  """
                Would you like to talk about your day, take an assessment,
                or look for professional help?
                """
    return question(start_msg) \
        .reprompt(reprompt_msg)

@ask.intent("FeelingIntent")
def feelings():
    exit_msg = "How do you feel?"
    reprompt_msg = "I didn't get that. How are you feeling?"
    return question(exit_msg) \
        .reprompt(reprompt_msg)


@ask.intent("MoodResponseIntent")
def mood_response():
    pass

@ask.intent("AssessmentIntent")
def assessment():
    exit_msg = "Here is a question"
    reprompt_msg = "Here is the same question"
    return question(exit_msg) \
        .reprompt(reprompt_msg)

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