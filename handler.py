import json
import boto3
import os
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('chreetings')
CHARSET = 'UTF-8'

def saveEvilQDB(recipient, evil_quote):
    try:
        table.put_item(
        Item={
                'recipientemail': recipient,
                'insult': evil_quote
                }
                )
        return True
    except:
        return False
    

def getEvilQuote(recipient):
    i = 0
    while i <= 10:
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json', allow_redirects=False)
        quote = response.json()
        if saveEvilQDB(recipient, quote):
            return quote
        i += 1 

    return "it's all said and done"


def parseMessageToHTML(recipient, evil_quote, message, name):
    message = '''
    <html>
    <head></head>
    <body> 
    <h2> Hi! ''' +  recipient +  ''',</h2><br><h3>Your 'friend', ''' + name + ''' wanted to send you a christmas card</h3>
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFp_BGp2qV2LkH78OVatRc8u8N5vLe1RtnO-5mD6_EzCq93u7qtw&s">
    <br>Wishing that "''' + evil_quote + '''"<br>And finally, a few personal words:<br>''' + message + '''
    <br><h3> With LOVE,<br>''' + name + '''!</h3>
    </body>
    </html>
    '''
    return message
    

def sendEmail(event, context):
    data = event['body']
    name = data ['name']    
    source = data['source']    
    subject = data['subject']
    message = data['message']
    recipient = data['recipient']    
    destination = data['destination']
    evil_quote = getEvilQuote(recipient)

    _message = "Message from: " + name + "\nEmail: " + source + "\nMessage content: " + message 
    body_text = 'Hi ' + recipient + ', here is a seasons greeting for you: \n\n' + evil_quote + '\n\n' + message 
    body_html = parseMessageToHTML(recipient, evil_quote, message, name)
    
    
    client = boto3.client('ses' )    
        
    response = client.send_email(
        Destination={
            'ToAddresses': [destination]
            },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': body_html,
                },
                'Text': {
                    'Data': body_text,
                    'Charset': CHARSET,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=source,
    )
    return 'I am sure your friend *krhm*, appriciates your effort. Your friend was wished: ' + evil_quote


