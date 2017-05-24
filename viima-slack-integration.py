import requests
import json
from credentials import viima_login_url, viima_email, viima_password, slack_token
import sched, time

from flask import Flask
app = Flask(__name__)

sch = sched.scheduler(time.time, time.sleep)

# Renaming the idea names according to the slack channel naming convention.
def slack_channel_naming_convention(name):
	name = name.replace(" ", "-").lower()
	for j in name:
		if j.isalnum() or j == "-" or j == "_":
			pass
		else:
			name = name.replace(j,"")
	name = name[0:21]
	return name

def periodic_checking(s):
	print "checking for update in Viima..."
	
	# Determine all ideas in Viima
	# Here ideas refer to those colored circles 
	idea_response = s.get("https://dangerzone.viima.com/api/customers/71/items/")
	ideas = []
		
	# Edit idea names according to the Naming rule in Slack.
	for i in idea_response.json():
		name = slack_channel_naming_convention(str(i['name']))
		desc = str(i['description'])
		ideas.append({'name': name, 'description': desc})

	# List info of all channels in Slack
	response = requests.post("https://slack.com/api/channels.list", data={"token": slack_token})
	slack_channels_info = []
	for i in response.json()['channels']:
		slack_channels_info.append({'name': str(i['name']), 
										'purpose': str(i['purpose']['value']),
										'channel_id': str(i['id'])})

	# Feature 1: Create new channels if it is missing in Slack
	for (i,j) in [(x['name'], x['description']) for x in ideas]:
		if i not in [y['name'] for y in slack_channels_info]:
			response = requests.post("https://slack.com/api/channels.create", 
										data={"token": slack_token, "name": i})			
			
			# Adding the info of new channel to "slack_channels_info"
			channel_id = response.json()['channel']['id']
			slack_channels_info.append({'name': str(i), 
											'purpose': j[0:250],
											'channel_id': channel_id})

			# Set the purpose of this new channel
			response_setPurpose = requests.post("https://slack.com/api/channels.setPurpose",
												data={"token": slack_token, 
														"channel": channel_id, 
														"purpose": j[0:250]})
			
		# Feature 2: Update 'purpose' in slack channel if 'description' in Viima
		# is modified
		elif j != [p['purpose'] for p in slack_channels_info if p['name'] == i][0]:
			for k in slack_channels_info:
				if k['name'] == i and k['purpose'] != j[0:250]:
					response_setPurpose = requests.post("https://slack.com/api/channels.setPurpose",
														data={"token": slack_token, 
																"channel": k['channel_id'], 
																"purpose": j[0:250]})
	# Feature 3: Posting messages in slack.
	# Determine all comments in Viima
	comments_in_ideas_response = s.get("https://dangerzone.viima.com/api/customers/71/comments/")
	comments_in_ideas = []

	for i in comments_in_ideas_response.json():
		channel_name = [p['name'] for p in idea_response.json() if p['id']==i['item']][0]
		if not i['parent']:
			comments_in_ideas.append({'channel name': slack_channel_naming_convention(channel_name), 
										'comment': i['content']})

	# Writing down statements to a given slack channel.
	for i in comments_in_ideas:
		if [p['name'] for p in slack_channels_info if p['name']==i['channel name']]:
			channel_id = [p['channel_id'] for p in slack_channels_info if p['name']==i['channel name']][0]		
			# Check history of 'channel_id'
			channel_history_response = requests.post("https://slack.com/api/channels.history",
														data = {"token": slack_token, 
														"channel": channel_id})
			# if a comment in an idea isn't present in the corresponding channel,
			# then post the comment to that channel.
			if i['comment'] not in [p['text'] for p in channel_history_response.json()['messages']]:
				response = requests.post("https://slack.com/api/chat.postMessage", 
											data={"token": slack_token,	
													"channel": channel_id, 
													"text": i['comment']})
	sch.enter(60*2, 1, periodic_checking, (s,))
	sch.run()

@app.route("/")
def integration():
	with requests.Session() as s:
		
		# Login to Viima
		login_response = s.get(viima_login_url)
		csrf_token = login_response.cookies['csrftoken'] # Retrieving the csrftoken
		login_data = dict(email = viima_email, 
							password = viima_password, 
							csrfmiddlewaretoken = csrf_token)
		login_response = s.post(viima_login_url, data = login_data) # an authorized request
		
		# Perioding checking of new items and comments every two minutes.
		periodic_checking(s)

	return "Integration of Viima and Slack occured. Check it out :)"

if __name__ == "__main__":
	app.run()