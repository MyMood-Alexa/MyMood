from flask import Flask, render_template
from flask_ask import context, request, version, Ask, statement, question, session
from Interaction import Interaction
import locator
import database
import datetime


app = Flask(__name__)
ask = Ask(app, '/')

interaction = None

#TODO fix all hardcoded responses
#TODO get time for when a session started
@ask.launch
def start_app():
    global interaction
    
    session_id = "{}".format(session.sessionId)
    session_time = datetime.datetime.now()
    interaction = Interaction(session_id, session_time)
    
    start_msg = """
                Hello. You can tell me about your day, take an assessment, 
                or ask me to look for professional help... Which would you like?
                """
    reprompt_msg =  """
                Would you like to talk about your day, take an assessment,
                or look for professional help?
                """
    
    interaction.update_response(start_msg)
    return question(start_msg) \
        .reprompt(reprompt_msg)


@ask.intent("FeelingIntent")
def feelings():
    exit_msg = "How do you feel?"
    reprompt_msg = "I didn't get that. How are you feeling?"
    #interaction.update_response(response) 
    return question(exit_msg) \
        .reprompt(reprompt_msg)


@ask.intent("MoodResponseIntent")
def mood_response():
    #TODO get user's response and add to the database
    #interaction.update_response(response) 
    pass


@ask.intent("AssessmentIntent")
def assessment():
    exit_msg = "Here is a question"
    reprompt_msg = "Here is the same question"
    #interaction.update_response(response) 
    return question(exit_msg) \
        .reprompt(reprompt_msg)


@ask.intent("SuggestionIntent")
def suggest():
    exit_msg = "Here are some suggestions"
    return statement(exit_msg)
	

@ask.intent("ProfessionalHelpIntent")
def prohelp():
    return locator.find_nearby_help()


@ask.intent("ExitIntent")
def exit_app():
    exit_msg = "Goodbye."
    database.add_responses(interaction) 
    return statement(exit_msg)


@ask.intent("AMAZON.StopIntent")
def stop_intent():
    exit_msg = "Farewell"
    database.add_responses(interaction) 
    return statement(exit_msg)


@ask.intent("AMAZON.CancelIntent")
def cancel_intent():
    exit_msg = "Sayonara"
    database.add_responses(interaction) 
    return statement(exit_msg)


@ask.session_ended
def session_ended():
    database.add_responses(interaction) 
    return "{}", 200


@ask.intent("AMAZON.HelpIntent")
def help_intent():    
    help_msg = "Here is help"
    return statement(help_msg)

if __name__ == '__main__':
    app.run(debug=True)
    
