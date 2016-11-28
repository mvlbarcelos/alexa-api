from chalice import Chalice
import boto3
import logging
import json

# logger=logging.getLogger()
app = Chalice(app_name='alexa-api')
app.debug = True

def confirmation(data):
	ret = {'version':'1.0', 'response': {
    'outputSpeech': {
      'type': 'PlainText',
      'text': 'Your confirmation mtf'
    }}}
	return ret

actions = {'NewConfirmation': confirmation}

@app.route('/alexa', methods=['POST'])
def alexa():
	# data = app.current_request.json_body
	data = json.loads(app.current_request.raw_body)
	intentName = data['request']['intent']['name']
	x = actions[intentName](data)
	print x
	# dynamodb = boto3.resource('dynamodb')
	# table = dynamodb.Table('fiainteractions')
	# table.put_item(Item=data)
	
	return x



# The view function above will return {'hello': 'world'}
# whenver you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {'hello': 'james'}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.json_body
#     # Suppose we had some 'db' object that we used to
#     # read/write from our database.
#     # user_id = db.create_user(user_as_json)
#     return {'user_id': user_id}
#
# See the README documentation for more examples.
#
