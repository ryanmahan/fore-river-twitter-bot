# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import re
import dateutil.parser
from twython import Twython
from auth import (
	consumer_key,
	consumer_secret,
	access_token,
	access_token_secret
)
import time
from datetime import datetime, timedelta


# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def getEmails(query):
	# Variable creds will store the user access token.
	# If no valid token found, we will create one.
	creds = None

	# The file token.pickle contains the user access token.
	# Check if it exists
	if os.path.exists('token.pickle'):

		# Read the token from the file and store it in the variable creds
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)

	# If credentials are not available or are invalid, ask the user to log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)

		# Save the access token in token.pickle file for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Connect to the Gmail API
	service = build('gmail', 'v1', credentials=creds)
	# request a list of all the messages
	result = service.users().messages().list(userId='me', q=query).execute()
	# We can also pass maxResults to get any number of emails. Like this:
	# result = service.users().messages().list(maxResults=200, userId='me').execute()
	messages = result.get('messages');
	if messages is None: return [];
	emails = []
	# iterate through all the messages
	for msg in messages:
		# Get the message from its id
		txt = service.users().messages().get(userId='me', id=msg['id']).execute()
		service.users().messages().modify(userId='me', id=msg['id'], body={ 'removeLabelIds': ['UNREAD']}).execute() 

		# Get value of 'payload' from dictionary 'txt'
		payload = txt['payload']

		# The Body of the message is in Encrypted format. So, we have to decode it. 
		# Get the data and decode it with base 64 decoder. 
		parts = payload.get('parts')[0] 
		data = parts['body']['data'] 
		data = data.replace("-","+").replace("_","/") 
		decoded_data = base64.b64decode(data) 
		email = decoded_data.decode("utf-8")
		emails.append(email.replace("\r\n", " "))

	return emails

def getDates(text):
	match = re.search('The Fore River Bridge is scheduled to open at(.+?)to allow', text)
	dates = []
	time_pattern = re.compile(r'(\d{1,2} a.m.?|\d{1,2} p.m.?|\d{1,2}:\d{2} a.m.?|\d{1,2}:\d{2} p.m.?)')
	if match != None:
		sentence = match.group(1)
		start_at = 0
		for date in re.finditer(r'(\w+, \w+\.* [0-9]{1,2})', sentence):
			for time in time_pattern.finditer(sentence, pos=start_at, endpos=date.span()[0]):
				dates.append(time.group(1) + " " + date.group(1))
			start_at = date.span()[1];
	return dates

twitter = Twython(
		consumer_key,
		consumer_secret,
		access_token,
		access_token_secret
	)

SUFFIX = "\n#ForeRiverBridge #traffic"

def send_notice(date):
	twitter.update_status(status="The Fore River Bridge will open at " + date + SUFFIX);

def send_reminder(date):
	twitter.update_status(status="The Fore River Bridge will be opening soon at " + date.strftime("%-I:%M %P") + SUFFIX)

openings = []
print("Server started")
while(True):
	# if connection fails, sleep for 5 and try again.
	try:
		messages = getEmails("subject:Fore River Bridge is:unread")
	except:
		time.sleep(5*60)
		break;
	for message in messages:
		dates = getDates(message)
		for date in dates:
			openings.append(dateutil.parser.parse(date))
			send_notice(date);
	for opening in openings:
		# happening within 30 min and not in the past
		if opening - datetime.now() < timedelta(minutes=37) and opening - datetime.now() > timedelta(minutes=0):
			openings.remove(opening);
			send_reminder(opening)
	# sleep for fifteen minutes
	time.sleep(15 * 60)