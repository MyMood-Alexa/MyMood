from flask import Flask, render_template
from flask_ask import context, request, Ask, statement, question, session
import locator
import database
import datetime
from interaction import Interaction


app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def start_app():
    init_session()

    start_msg = ("Hello. You can tell me about your day,")
    """ take an assessment, "
                 "or ask me to look for professional help... "
                 "Which would you like?")"""

    reprompt_msg = ("Would you like to talk about your day, "
                    "take an assessment, or look for professional help?")

    session.attributes['State'] = "None"

    session.attributes['responses'].append(start_msg)

    return question(start_msg) \
        .reprompt(reprompt_msg)


@ask.intent('FeelingIntent')
def feelings():
    exit_msg = "How do you feel?"
    reprompt_msg = "I didn't get that. How are you feeling?"
    return question(exit_msg) \
        .reprompt(reprompt_msg)


@ask.intent('MoodResponseIntent')
def mood_response():
    pass


# Differential Diagnosis Decision Tree constructed from DSM-IV
@ask.intent('AssessmentIntent')
def assessment():
    # initialize sessionid if it hasnt been already
    if (session.attributes.get('session_id') is None):
        init_session()
    # initiate assessment response for checking
    if (session.attributes.get('assess_response') is None):
        session.attributes['assess_response'] = "unknown"
    # turn on state
    if (session.attributes.get('State') is None
        or session.attributes['State'] != "Assessment"
        or session.attributes['assess_response'] == "unknown"):
        session.attributes['State'] = "Assessment"
        session.attributes['assess_step'] = "0"
        session.attributes['assess_manic'] = "unknown"
        session.attributes['assess_hypomanic'] = "unknown"
        session.attributes['assess_major_dep'] = "unknown"
        session.attributes['assess_mixed'] = "unknown"

    # possible responses
    responses = {'-1': "I encountered a problem. You will have to start over. "
                       "Sorry for the inconvenience",
                 '1': "Are you in a depressed, elevated, or irritable mood?",
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
                 '13': "mood disorder due to a general medical condition",
                 '14': "substance induced mood disorder",
                 '16': "bipolar one disorder",
                 '17': "bipolar type of schizoaffective disorder",
                 '18': "not otherwise specified bipolar disorder superimposed "
                       "on a psychotic disorder",
                 '19': "bipolar two disorder",
                 '20': "cyclothymimc disorder",
                 '21': "not otherwise specified bipolar disorder",
                 '22': "major depressive disorder",
                 '23': "depressive type schizoaffective disorder",
                 '24': "not otherwise specified depressive disorder "
                       "superimposed on a psychotic disorder",
                 '25': "dysthymic disorder",
                 '26': "adjustment disorder with depressed mood",
                 '27': "not otherwise specified depressive disorder",
                 '28': "no mood disorder",
                 }

    # logic to pick pick correct question or answer
    if (session.attributes['assess_step'] == "0"):
        session.attributes['assess_step'] = "1"
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

    # prepare message
    next_step = responses.get(session.attributes['assess_step'], "-1")

    # convert assess_step to determine if assessment is done
    stepInt = int(session.attributes['assess_step'])

    # assessment complete
    if (stepInt > 12 or stepInt < 0):
        if (stepInt == 28):
            # return no disorder diagnosis
            msg = "Congratulations. You have {}".format(next_step)
        elif (stepInt > 12):
            # return disorder diagnosis
            msg = ("You may be experiencing a {}. Keep in mind, I am not an "
                   "expert. Seek professional advice if you must."
                   .format(next_step))
        else:
            # return error message
            msg = next_step
        # save result if user wants to repeat diagnosis / error message
        session.attributes['Repeat'] = msg
        reprompt_msg = ("Would you like to talk about your day, "
                        "take an assessment, or look for professional help?")

        # reset session state
        session.attributes['State'] = "None"
        return statement(msg)
    else:
        # reset assessment response
        session.attributes['assess_response'] = "unknown"
        # return next question
        msg = next_step
        # save msg if user wants to repeat
        session.attributes['Repeat'] = msg
        reprompt_msg = "I didn't quite get that, {}".format(msg)
        return question(msg) \
            .reprompt(reprompt_msg)


@ask.intent('SuggestionIntent')
def suggest():
    exit_msg = "Here are some suggestions"
    return statement(exit_msg)


@ask.intent('ProfessionalHelpIntent')
def pro_help():
    helps = locator.find_nearby_help()
    session.attributes['Repeat'] = helps
    return statement(helps)


@ask.intent('YesIntent')
def yes_intent():
    if (session.attributes['State'] == "Assessment"):
        session.attributes['assess_response'] = "yes"
        return assessment()
    return start_app()


@ask.intent('NoIntent')
def no_intent():
    if (session.attributes['State'] == "Assessment"):
        session.attributes['assess_response'] = "no"
        return assessment()
    return start_app()


@ask.intent('AMAZON.RepeatIntent')
def repeat_intent():
    if (session.attributes.get('Repeat') is None):
        return statement("Sorry there is nothing to repeat")
    repeat_msg = session.attributes['Repeat']
    return question(repeat_msg).reprompt(repeat_msg)


@ask.intent('ExitIntent')
def exit_app():
    exit_msg = "Goodbye."
    add_database()
    return statement(exit_msg)


@ask.intent('AMAZON.StopIntent')
def stop_intent():
    exit_msg = "Farewell"
    add_database()
    return statement(exit_msg)


@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
    add_database()
    exit_msg = "Sayonara"
    return statement(exit_msg)


@ask.session_ended
def session_ended():
    add_database()
    help_msg = "Here is help"
    return statement(help_msg)
    #return "{}", 200


@ask.intent('AMAZON.HelpIntent')
def help_intent():
    help_msg = "Here is help"
    return statement(help_msg)


def confirm():
    confirm_msg = ""
    return question(confirm_msg)


def init_session():
    session.attributes['session_id'] = "{}".format(session.sessionId)
    session.attributes['session_time'] = str(datetime.datetime.now())
    session.attributes['responses'] = []
    session.attributes['device_id'] = ("{}"
                                       .format(context.System.device.deviceId))
    session.attributes['user_id'] = "{}".format(session.user.userId)


def add_database():
    database.add_interaction(session.attributes['session_id'],
                             session.attributes['session_time'],
                             session.attributes['responses'],
                             session.attributes['device_id'],
                             session.attributes['user_id'])


if __name__ == '__main__':
    app.run(debug=True)
