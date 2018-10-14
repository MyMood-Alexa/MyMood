from flask import Flask, render_template
from flask_ask import context, request, Ask, statement, question, session
from interaction import Interaction
import constants
import database
import datetime
import locator
import random


app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def start_app():
    init_session()
    session.attributes['State'] = "None"
    session.attributes['Repeat'] = constants.STARTUP_MSG
    append_response(constants.STARTUP_MSG)
    return question(constants.STARTUP_MSG) \
        .reprompt(constants.RETRY_MSG + constants.HELP_MSG)


@ask.intent('SentimentIntent')
def sentiment_intent(phrase):
    if (session.attributes.get('session_id') is None):
        init_session()
    if (session.attributes.get('State') is None
        or session.attributes['State'] == "None"):
        session.attributes['State'] = "Sentiment"
    elif (session.attributes['State'] != "Sentiment"):
        return route_state()

    if (phrase is None):
        session.attributes['State'] = "None"
        session.attributes['Repeat'] = (constants.RETRY_MSG + 
                                        constants.SENTIMENT_PROMPT)
        return question(constants.RETRY_MSG + constants.SENTIMENT_PROMPT) \
            .reprompt(constants.RETRY_MSG + constants.SENTIMENT_PROMPT)
    else:
        msg = "Today, {}.".format(phrase)
        session.attributes['State'] = "None"
        session.attributes['Repeat'] = msg + constants.CONTINUE_PROMPT
        append_response(msg + constants.CONTINUE_PROMPT)
        return question(msg + constants.CONTINUE_PROMPT) \
            .reprompt(constants.CONTINUE_PROMPT)


# Differential Diagnosis Decision Tree constructed from DSM-IV
@ask.intent('AssessmentIntent')
def assessment_intent():
    if (session.attributes.get('session_id') is None):
        init_session()
    if (session.attributes.get('State') is None
        or session.attributes['State'] == "None"):
        session.attributes['State'] = "Assessment"
        session.attributes['assess_response'] = "unknown"
        session.attributes['assess_step'] = "0"
        session.attributes['assess_manic'] = "unknown"
        session.attributes['assess_hypomanic'] = "unknown"
        session.attributes['assess_major_dep'] = "unknown"
        session.attributes['assess_mixed'] = "unknown"
    elif (session.attributes['State'] != "Assessment"):
        return route_state()

    responses = {'-1': "I encountered a problem. You will have to start over. "
                       "Sorry for the inconvenience",
                 '1': "I will ask you a series of questions to try to "
                      "evaluate you. Please answer with yes or no. "
                      "Are you in a depressed, elevated, or irritable mood?",
                 '2': "Are you suffering from a general medical condition "
                      "with physiological effects?",
                 '3': "Are you taking any drugs or medication?",
                 '4': "Have you been impaired or hospitalized while being "
                      "irritable for over a week?",
                 '5': "Have others noticed you being irritable for four or "
                      "more days?",
                 '6': "Have you experienced depression or loss of interest "
                      "unrelated to a recent death for two weeks or more?",
                 '7': "Have you been depressed or irritable everyday for "
                      "one week or more?",
                 '8': "Do you see or hear things that are not real when "
                      "you are not depressed nor irritable?",
                 '9': "Have you been experiencing these delusions or "
                      "hallucinations for at least two weeks before feeling "
                      "depressed or irritable?",
                 '10': "Have you experienced periods of depression for two or "
                       "more years?",
                 '11': "Have you been depressed more often than not for two "
                       "or more years?",
                 '12': "Have you been stressed?",
                 '13': "mood disorder due to a general medical condition.",
                 '14': "substance induced mood disorder.",
                 '16': "bipolar one disorder.",
                 '17': "bipolar type of schizoaffective disorder.",
                 '18': "not otherwise specified bipolar disorder superimposed "
                       "on a psychotic disorder.",
                 '19': "bipolar two disorder.",
                 '20': "cyclothymimc disorder.",
                 '21': "not otherwise specified bipolar disorder.",
                 '22': "major depressive disorder.",
                 '23': "depressive type schizoaffective disorder.",
                 '24': "not otherwise specified depressive disorder "
                       "superimposed on a psychotic disorder.",
                 '25': "dysthymic disorder.",
                 '26': "adjustment disorder with depressed mood.",
                 '27': "not otherwise specified depressive disorder.",
                 '28': "no mood disorder.",
                 }

    if (session.attributes['assess_step'] == "0"):
        session.attributes['assess_step'] = "1"
    elif (session.attributes['assess_response'] == "unknown"):
        return question(constants.RETRY_MSG + session.attributes['Repeat']) \
            .reprompt(constants.RETRY_MSG + session.attributes['Repeat'])
    elif (session.attributes['assess_step'] == "1"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "2"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_step'] = "28"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "2"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "13"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_step'] = "3"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "3"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "14"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_step'] = "4"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "4"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_manic'] = "yes"
            session.attributes['assess_step'] = "6"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_manic'] = "no"
            session.attributes['assess_step'] = "5"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "5"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_hypomanic'] = "yes"
            session.attributes['assess_step'] = "6"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_hypomanic'] = "no"
            session.attributes['assess_step'] = "6"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "6"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_major_dep'] = "yes"
            session.attributes['assess_step'] = "7"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_major_dep'] = "no"
            session.attributes['assess_step'] = "7"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "7"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_mixed'] = "yes"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_mixed'] = "no"
        else:
            session.attributes['assess_step'] = "-1"
        if (session.attributes['assess_manic'] == "yes"
            or session.attributes['assess_mixed'] == "yes"):
            session.attributes['assess_step'] = "8"
        else:
            if (session.attributes['assess_hypomanic'] == "yes"
                and session.attributes['assess_major_dep'] == "yes"):
                session.attributes['assess_step'] = "19"
            else:
                session.attributes['assess_step'] = "10"
    elif (session.attributes['assess_step'] == "8"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "9"
        elif (session.attributes['assess_response'] == "no"):
            if (session.attributes['assess_manic'] == "yes"
                or session.attributes['assess_mixed'] == "yes"):
                session.attributes['assess_step'] = "16"
            else:
                session.attributes['assess_step'] = "22"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "9"):
        if (session.attributes['assess_manic'] == "yes"
            or session.attributes['assess_mixed'] == "yes"):
            if (session.attributes['assess_response'] == "yes"):
                session.attributes['assess_step'] = "17"
            elif (session.attributes['assess_response'] == "no"):
                session.attributes['assess_step'] = "18"
            else:
                session.attributes['assess_step'] = "-1"
        else:
            if (session.attributes['assess_response'] == "yes"):
                session.attributes['assess_step'] = "23"
            elif (session.attributes['assess_response'] == "no"):
                session.attributes['assess_step'] = "24"
            else:
                session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "10"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "20"
        elif (session.attributes['assess_response'] == "no"):
            if (session.attributes['assess_manic'] == "yes"
                or session.attributes['assess_hypomanic'] == "yes"):
                session.attributes['assess_step'] = "21"
            else:
                if (session.attributes['assess_major_dep'] == "yes"):
                    session.attributes['assess_step'] = "8"
                else:
                    session.attributes['assess_step'] = "11"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "11"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "25"
        elif (session.attributes['assess_response'] == "no"):
            session.attributes['assess_step'] = "12"
        else:
            session.attributes['assess_step'] = "-1"
    elif (session.attributes['assess_step'] == "12"):
        if (session.attributes['assess_response'] == "yes"):
            session.attributes['assess_step'] = "26"
        elif (session.attributes['assess_response'] == "no"):
            if (session.attributes['assess_manic'] == "yes"
                or session.attributes['assess_hypomanic'] == "yes"
                or session.attributes['assess_major_dep'] == "yes"
                or session.attributes['assess_mixed'] == "yes"):
                session.attributes['assess_step'] = "27"
            else:
                session.attributes['assess_step'] = "28"
        else:
            session.attributes['assess_step'] = "-1"
    else:
        session.attributes['assess_step'] = "-1"

    next_step = responses.get(session.attributes['assess_step'], "-1")
    stepInt = int(session.attributes['assess_step'])

    # assessment complete
    if (stepInt > 12 or stepInt < 0):
        if (stepInt == 28):
            msg = ("Congratulations. You have {}".format(next_step) + 
                   constants.CONTINUE_PROMPT)
        elif (stepInt > 12):
            msg = ("You may be experiencing a {}. Keep in mind, I am not an "
                   "expert. Seek professional advice if you must."
                   .format(next_step) + constants.CONTINUE_PROMPT)
        else:
            # return error message
            msg = next_step + constants.CONTINUE_PROMPT
        session.attributes['State'] = "None"
        session.attributes['Repeat'] = msg
        append_response(msg)
        return question(msg) \
            .reprompt(constants.CONTINUE_PROMPT)
    else:
        msg = next_step
        session.attributes['assess_response'] = "unknown"
        session.attributes['Repeat'] = msg
        append_response(next_step)
        return question(msg) \
            .reprompt(constants.RETRY_MSG + msg)


@ask.intent('ProfessionalHelpIntent')
def pro_help_intent():
    if (session.attributes.get('session_id') is None):
        init_session()
    if (session.attributes.get('State') is None
        or session.attributes['State'] == "None"):
        session.attributes['State'] = "ProfessionalHelp"
    elif (session.attributes['State'] != "ProfessionalHelp"):
        return route_state()
        
    helps = locator.find_nearby_help()
    session.attributes['State'] = "None"
    session.attributes['Repeat'] = helps + constants.CONTINUE_PROMPT
    append_response(helps + constants.CONTINUE_PROMPT)
    return question(helps + constants.CONTINUE_PROMPT) \
        .reprompt(constants.CONTINUE_PROMPT)


@ask.intent('AMAZON.YesIntent')
def yes_intent():
    if (session.attributes['State'] == "Assessment"):
        session.attributes['assess_response'] = "yes"
        append_response("yes")
        return assessment_intent()
    return question(constants.RETRY_MSG + constants.HELP_MSG) \
        .reprompt(constants.RETRY_MSG + constants.HELP_MSG)


@ask.intent('AMAZON.NoIntent')
def no_intent():
    if (session.attributes['State'] == "Assessment"):
        session.attributes['assess_response'] = "no"
        append_response("no")
        return assessment_intent()
    return question(constants.RETRY_MSG + constants.HELP_MSG) \
        .reprompt(constants.RETRY_MSG + constants.HELP_MSG)


@ask.intent('AMAZON.RepeatIntent')
def repeat_intent():
    if (session.attributes.get('Repeat') is None):
        return question(constants.REPEAT_ERROR)
    return question(session.attributes['Repeat'])


@ask.intent('AMAZON.HelpIntent')
def help_intent():
    session.attributes['State'] = "None"
    session.attributes['Repeat'] = constants.HELP_MSG
    return question(constants.HELP_MSG) \
        .reprompt(constants.RETRY_MSG + constants.HELP_MSG)


@ask.intent('AMAZON.NavigateHomeIntent')
def nav_home_intent():
    exit_msg = random.choice(constants.EXIT_MSG)
    append_response(exit_msg)
    add_database()
    return statement(exit_msg)


@ask.intent('AMAZON.StopIntent')
def stop_intent():
    exit_msg = random.choice(constants.EXIT_MSG)
    append_response(exit_msg)
    add_database()
    return statement(exit_msg)


@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    exit_msg = random.choice(constants.EXIT_MSG)
    append_response(exit_msg)
    add_database()
    return statement(exit_msg)


@ask.session_ended
def session_ended():
    add_database()
    return "{}", 200


def route_state():
    if (session.attributes['State'] == "Sentiment"):
        return sentiment_intent("")
    elif (session.attributes['State'] == "Assessment"):
        return assessment_intent()
    elif (session.attributes['State'] == "ProfessionalHelp"):
        return pro_help_intent()
    else:
        return help_intent()


def init_session():
    session.attributes['session_id'] = "{}".format(session.sessionId)
    session.attributes['session_time'] = str(datetime.datetime.now())
    session.attributes['responses'] = []
    session.attributes['device_id'] = ("{}"
                                       .format(context.System.device.deviceId))
    session.attributes['user_id'] = "{}".format(session.user.userId)


def append_response(response):
    session.attributes['responses'].append(response)


def add_database():
    database.add_interaction(session.attributes['session_id'],
                             session.attributes['session_time'],
                             session.attributes['responses'],
                             session.attributes['device_id'],
                             session.attributes['user_id'])


if __name__ == '__main__':
    app.run(debug=True)
