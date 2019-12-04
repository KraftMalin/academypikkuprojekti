import json
import boto3
import os
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('chreetings')
CHARSET = 'UTF-8'



def saveEvilQDB(recipient, evil_quote):
    table.put_item(
       Item={
            'recipientemail': recipient,
            'insult': evil_quote
            }
            )

def searchDuplicatesDB(recipient, evil_quote):
    duplicate = table.query(
        KeyConditionExpression=Key('recipientemail').eq(recipient)
    )
    for i in duplicate['Items']:
        if(i['insult'] == evil_quote):
            evil_quote = getEvilQuote()
            searchDuplicatesDB(recipient, evil_quote)
    saveEvilQDB(recipient, evil_quote)



def getEvilQuote():
    response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json', allow_redirects=False)
    quote = response.json()
    return quote['insult']

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
    evil_quote = getEvilQuote()

    //if evil_quote == dynamoDB:ssa, evil_quote = getEvilQuote()

    _message = "Message from: " + name + "\nEmail: " + source + "\nMessage content: " + message 
    body_text = 'Hi ' + recipient + ', here is a seasons greeting for you: \n\n' + getEvilQuote() + '\n\n' + message 
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


