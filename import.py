import boto3
import xmltodict, json
import uuid


client = boto3.client('s3')
response = client.get_object(Bucket='fia-alerts', Key='20150724013515473' )
content = response["Body"].read()
o = xmltodict.parse(content)

alert = { 'id': str(uuid.uuid1()),
		  'city',
		   'eventType',
		   'lat',
		   'lng',
		   'timestamp',
		   'title' }



