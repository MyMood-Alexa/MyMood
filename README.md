# MyMood

## Project Details

My Mood is an interactive Alexa application that a user can talk about their day with. The goal of this application is to improve, assess, and get help for the user's mental state.

### Features

MyMood has three main features:  
* Sentiment analysis based on user's raw input
	* Activated with the keyword "Today". Ex: "Today, it's my birthday"
	* Currently passes the input to a Naive-Bayes classifier to determine the sentiment. Classifier is trained with data set provided by [sentiment140](http://help.sentiment140.com/for-students)
	* Responds with congratulatory or sympathetic statement based on classification
* Diagnose the user for depression with a series of questions
	* Activated with the intent trigger "take an assessment"
	* Questions are based off of the Diagnostic and Statistical Manual of Mental Disorders, 4th Edition
	* Computes using a decision tree constructed based on the "Differential Diagnosis of Mood Disorders" from the manual above
* Locate a nearby clinic using the set Alexa location in conjunction with Google Places API
	* Activated with the intent trigger "look for professional help"
	* Sends a get request to the  [Amazon Device Address API](https://developer.amazon.com/docs/custom-skills/device-address-api.html)  if the user has granted authorization
	* Uses the location obtained to retrieve the details of a nearby mental health institute by issuing a series of get requests to [Google Places API](https://developers.google.com/places/)

### Components

<p align="center">
  <img src = "https://drive.google.com/uc?export=view&id=1oDAHkM4pLZJn5z0aW71tEY96WwmWjvTW">
  <br>Components Overview Figure
</p>

The following is a list of components relevant to MyMood:
* [Python 3](https://www.python.org/downloads/) - General purpose programming language with well maintained machine learning libraries
* [Flask-Ask](http://flask-ask.readthedocs.io/en/latest/) - A flask extension to create Alexa skills using Python to streamline the development process
* [Amazon Echo](https://www.amazon.com/Amazon-Echo-And-Alexa-Devices/b?ie=UTF8&node=9818047011) - Hardware device also known as Amazon Alexa. The target platform that this application will run on
* [Alexa Skills Kit](https://developer.amazon.com/alexa-skills-kit) - API used to create Alexa skills by handling the properties of the skill
* [Amazon Web Services](https://aws.amazon.com/) - Provides on-demand cloud computing platforms such as Lambda and DynamoDB
* [Amazon Lambda](https://aws.amazon.com/lambda/) - Event-driven server-less computing platform used by Alexa skills. It is also used for machine learning model computing
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) - A NoSQL database service managed on the cloud. Used to gather anonymous interactions as data for researchers and system improvement
* [Google Places API](https://developers.google.com/places/) - Provides local clinic information based on the user's location

## On-Boarding Guide

### Development Team Guidelines

#### Scrum Process

* Issues are tracked on [Waffle.io](https://waffle.io/lydarren/MyMood)
* Sprints start Tuesday morning and end Monday night
* Developers should attempt to have their tasks completed by Saturday and address feedback by Monday night

#### Developer Guidelines

* There are 3 repositories total:  [Dev Guide & User Manual](https://github.com/MyMood-Alexa/MyMood-DevGuideUserManual),  [Database Interface](https://github.com/MyMood-Alexa/MyMood-Interface), and  [Alexa App](https://github.com/lydarren/MyMood)
* Python code should follow the  [PEP8 style](https://www.python.org/dev/peps/pep-0008/). Use [PEP8 online tool](http://pep8online.com/) if unsure
* [Interface](mymood.me) code runs on HTML, CSS, and JavaScript. They should follow these conventions:
[https://www.w3schools.com/html/html5_syntax.asp](https://www.w3schools.com/html/html5_syntax.asp)
[https://google.github.io/styleguide/htmlcssguide.html](https://google.github.io/styleguide/htmlcssguide.html)
[https://www.w3schools.com/js/js_conventions.asp](https://www.w3schools.com/js/js_conventions.asp)
One exception is that we prefer
```
if(...) {
	...
}
else {
	...
}
```
over
```
if(...) {
	...
} else {
	...
}
```
* Code should be tested before issuing a pull request
* Code needs to be reviewed and receive the approval of 2 other developers before being rebased and merged
* There should be 1 commit per task, even if changes were made in response to feedback. This makes issue tracking and bug fixing a lot easier. Each commit should also have a matching issue in waffle with the same header
    E.g. If the task is to add a button to the interface, there should only be 1 commit for it in the commit tree

### Environment Setup Instructions

#### Python Environment

1.  Download and Install  [Anaconda and Spyder](https://www.anaconda.com/download/)
2.  Using the Anaconda Prompt:  
    Check that Python 3.x is installed with ```python --version```
    Use: ```conda install python=3.6``` and ```conda update python``` if it isn't
    Install Flask-Ask framework with ```conda install -c anaconda flask``` on the Anaconda Prompt

#### DynamoDB

1. Follow instructions to set up  [AWS CLI](https://docs.aws.amazon.com/lambda/latest/dg/setup-awscli.html)
2. Install boto3 on anaconda with:
```
conda install -c anaconda boto3
```
3. Follow instructions to configure  [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
4. Run create_table() from database.py
5. DynamoDB commands can be found [here](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html#cli-aws-dynamodb)


#### Google Places API

1.  For local testing, get a Google Places API key  [here](https://developers.google.com/places/web-service/get-api-key)
2.  Create a config file in your local mymood repository named 'config.py'
3.  Insert your API key in config.py as ```API_KEY='YOUR_KEY'```

#### Local Testing

1. Download  [ngrok](https://ngrok.com/download)
2. Run main.py on Spyder
3. Without stopping main.py, run ngrok.exe and enter 'ngrok http 5000'
4. Copy the forwarding endpoint, which looks something like ```https://4986f389.ngrok.io```. Make sure it's the https endpoint
5. Go to Alexa Developer Console and under Build > Endpoint, paste the ngrok https endpoint in default region. Select 'My development endpoint is a subdomain of a domain...' and click 'Save Endpoints'
<p align="center">
  <img src = "https://drive.google.com/uc?export=view&id=1w2ONmfh4Zj_SgD-pWvx4Z-Ksua3Iqzie">
  <br>Ngrok Endpoint in Alexa Skill Console
</p>

6. Test through the Developer Console or with your Alexa
7. Terminate main.py and ngrok when you have finished testing

### Useful GitHub Commands

#### Setting Up the Local Repository

1. Fork organization’s master repository at [https://github.com/lydarren/MyMood](https://github.com/lydarren/MyMood) to your own GitHub
2. ```git clone https://github.com/<your_github_id>/MyMood```
3. ```git remote -v``` should show 2 origin links
4. ```git remote add upstream [https://github.com/lydarren/MyMood```
5. ```git remote -v``` should show 2 origin links and 2 upstream links

#### Pull Request Workflow

1. ```git commit -m "<waffle_issue_header>"``` to add your changes to a commit, or ```git commit --amend --no-edit``` to amend your topmost commit without adding another commit. Use ```git rebase -i``` to correct an even older commit.
2. ```git pull --rebase upstream master``` to get the latest source code from the master repository while putting your commits on top
3. ```git push``` to push to your forked repository, or ```git push upstream <your_local_branch>:<remote_branch>``` to push to your branch on the master repository
4. Submit pull request:
	* If needed to fulfill a subtask: Add “required by #<issue_number>” to pull review description
	* If needed to fix a bug: Add “closes #<issue_number>” to pull review description
	* Attach testing screenshots to you pull review description
5. Address any feedback regarding your pull request and retest if needed. When your pull review has received at least 2 approvals, it can be rebased and merged

### Waffle management

* Epics should have <feature_abbreviation-milestone_number> tags
	Ex: Sentiment Analysis Milestone 1 would look like this: [SA-1]
* To add a subtask to an epic, add "child of #<epic_issue_number>" and "connects #<epic_issue_number>" to the subtask description