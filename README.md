## Viima Slack Integration

This microservice is developed for integrating Viima with Slack. In particular, Viima's tutorial board is integrated with Slack through its REST JSON APIs. This work uses Flask for the integration.

## The Integration System

Imagine a situation where few members of an organisation (let’s say, the CEO or the Ideation Guy) uses Viima’s idea development tool. They want their new ideas to be directly communicated to rest of their teammates through their Slack tool. 

In order to achieve so, an Integration is developed. It comprises of three primary features.

Feature 1 is creating new channels in Slack. This new channels correspond to the new ideas created in the Viima’s tutorial board. Note that idea here refers to the coloured circles in Viima’s tutorial board.

Feature 2 is regarding posting and updating the purpose of a given Slack channel with the the description provided for that corresponding idea in Viima.

Feature 3 is about posting messages to corresponding channels in Slack. These comments are taken from Viima’s tutorial board.

## Built With

* [Flask](http://flask.pocoo.org) - The micro web framework used.
* [Requests](http://docs.python-requests.org/en/master/) - For making http request calls to Slack and Viima.
* Python version 2.7 is used for programming.

## Quick start
Create a virtual environment:
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```
Once the virtual environment is activated, install dependencies with
```
pip install -r requirements.txt
```

Download the project from GitHub with:
```
git clone https://github.com/palashpulsar/viima-slack-integration.git
```

After cloning the project, go to [credentials.py](/credentials.py) and include your credential information.

Go to the project and run as follows:
```
cd viima-slack-integration
python viima-slack-integration.py
```
Then open a browser and enter: 
```
http://127.0.0.1:5000/
```