from chalice import Chalice
import boto3
import json
import uuid
import time
import decimal
from toolz import merge
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import string

app = Chalice(app_name='alexa-api')
app.debug = True

latAndLog = {'Los Angeles' : {'lng': '-118.6919106', 'lat':  '34.0201812' },
             'Vegas' : {'lng': '-115.3150822', 'lat': '36.1249185' },
             'Las Vegas' : {'lng': '-115.3150822', 'lat': '36.1249185' },
             'San Francisco': {'lng': '-122.4726193', 'lat': '37.7576948' }}


def writeDynamo(data):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('FIAAlertsJSON')
	table.put_item(Item=data)
	pass


def get_events(data):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('FIAAlertsJSON')

	location = data['request']['intent']['slots']['location']['value']
	
	response = table.scan(
    	FilterExpression=Attr('city').eq(location))
	items = response['Items']
	
	if len(items) > 0:
		text = ["A %s was report in %s at %s" % (item['eventType'], item['city'], item['timestamp'])
				for item in items]
		return {'version':'1.0', 'response': {
		'outputSpeech': {
	  	'type': 'PlainText',
	  	'text': string.join(text, " and also ")
		}}}
	else:
		return {'version':'1.0', 'response': {
			'outputSpeech': {
	  		'type': 'PlainText',
	  		'text': 'No alerts in %s' % (location, )
		}}}		



def new_event(data):
	eventType = data['request']['intent']['slots']['eventType']['value']
	location = data['request']['intent']['slots']['location']['value']
	time = datetime.strptime(data['request']['timestamp'], "%Y-%m-%dT%XZ").strftime("%I:%M%p")

	alert = merge({'eventType': eventType,			 
			 'id': str(uuid.uuid1()),
			 'title': "A(n) %s is happening in %s" % (eventType, location),
			 'city': location,
			 'timestamp': time },
			 latAndLog[location])

	writeDynamo(alert)
	return {'version':'1.0', 'response': {
			'outputSpeech': {
		  	'type': 'PlainText',
		  	'text': 'Thank you for the information about the %s in %s' % (eventType, location)
			}}}
		

def default(data):
 	ret = {'version':'1.0', 'response': {
 	'outputSpeech': {
 	  'type': 'PlainText',
 	  'text': 'What did you say?'
 	}}}

 	return ret

actions = {'NewEvent': new_event,
 		  'GetEvents': get_events,
 		  'default': default}

@app.route('/alexa', methods=['POST'])
def alexa():
	ret = {}
	try:
		data = json.loads(app.current_request.raw_body)
		print data
	
		intentName = data['request']['intent']['name']
		ret = actions[intentName](data)
	except Exception as e:
		print e
		ret = {'version':'1.0', 'response': {
		'outputSpeech': {
		  'type': 'PlainText',
		  'text': 'Sorry, i wasn\'t able to understand you'
		}}} 
	
	return ret
