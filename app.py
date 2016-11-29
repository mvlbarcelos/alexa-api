from chalice import Chalice
import boto3
import json
import uuid

app = Chalice(app_name='alexa-api')
app.debug = True

def writeDynamo(data):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table('fiainteractions')
	table.put_item(Item=data)
	pass

def confirmation(data):
	id = data['request']['intent']['slots']['eventId']['value']
	ret = {'version':'1.0', 'response': {
	'outputSpeech': {
	  'type': 'PlainText',
	  'text': 'Event id %s is Confirmed' % id
	}}}
	x = {'eventId': id,
	'status': 'CONFIRMED',
	'id': str(uuid.uuid1())}
	
	writeDynamo(x)
	return ret

def notConfirmed(data):
	id = data['request']['intent']['slots']['eventId']['value']
	ret = {'version':'1.0', 'response': {
	'outputSpeech': {
	  'type': 'PlainText',
	  'text': 'Event id %s Not Confirmed' % id
	}}}
	x = {'eventId': id,
		 'status': 'NOT_CONFIRMED',
		 'id': str(uuid.uuid1())}

	writeDynamo(x)
	return ret

def default(data):
	ret = {'version':'1.0', 'response': {
	'outputSpeech': {
	  'type': 'PlainText',
	  'text': 'What did you say?'
	}}}
	return ret

actions = {'NewConfirmation': confirmation,
		  'NewDisconfirmation': notConfirmed,
		  'default': default}

@app.route('/alexa', methods=['POST'])
def alexa():
	data = json.loads(app.current_request.raw_body)
	intentName = data['request'].get('intent', {'name': 'default'})['name']
	x = actions[intentName](data)
	print data
	# dynamodb = boto3.resource('dynamodb')
	# table = dynamodb.Table('fiainteractions')
	# table.put_item(Item=data)
	
	return x
