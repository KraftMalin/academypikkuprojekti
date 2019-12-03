import json
import boto3
import os
from botocore.vendored import requests


def getEvilQuote():
    response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json', allow_redirects=False)
    quote = response.json()
    return quote['insult']

def sendEmail(event, context):
    data = event['body']
    name = data ['name']    
    source = data['source']    
    subject = data['subject']
    message = data['message']    
    destination = data['destination']
    _message = "Message from: " + name + "\nEmail: " + source + "\nMessage content: " + message 
    evil_quote = getEvilQuote()
    
    client = boto3.client('ses' )    
        
    response = client.send_email(
        Destination={
            'ToAddresses': [destination]
            },
        Message={
            'Body': {
                'Html': {
                    'Data': evil_quote,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=source,
    )
    return _message + ' ' + evil_quote


