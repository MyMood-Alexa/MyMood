from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, '/')

@ask.launch
def start_app():
    start_msg = "Hello."
    return question(start_msg);

@ask.intent("ExitIntent")
def exit_app():
    exit_msg = "Goodbye."
    return statement(exit_msg)


if __name__ == '__main__':
    app.run(debug=True)