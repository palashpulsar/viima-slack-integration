## Viima Slack Integration

This microservice is developed for integrating Viima with Slack. In particular, Viima's tutorial board is integrated with Slack through its REST JSON APIs. This work uses Flask for the integration.

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