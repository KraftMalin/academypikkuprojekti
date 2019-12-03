import json
import boto3
import os
from botocore.vendored import requests

CHARSET = 'UTF-8'

def getEvilQuote():
    response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json', allow_redirects=False)
    quote = response.json()
    return quote['insult']

def parseMessageToHTML(recipient, evil_quote, message, name):
    response = requests.get('https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwjd8rvl1ZnmAhWyxaYKHQ8HCkcQjRx6BAgBEAQ&url=https%3A%2F%2Fblog.mypostcard.com%2Fen%2Fhistory-of-christmas-cards%2F&psig=AOvVaw0U3RLoKJ47v7SDFr3Gepym&ust=1575469048889106', allow_redirects=False)
    message = '''
    <html>
    <head> Dear ''' + recipient + '''</head> 
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
    return 'I am sure your friend *krhm*, appriciates your effort'


