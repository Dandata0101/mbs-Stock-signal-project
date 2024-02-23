import requests
import json
import configparser
import sys, os
import warnings
import base64
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

sys.path.append(os.path.realpath('..'))
warnings.filterwarnings("ignore")
os.system('cls' if os.name == 'nt' else 'clear')
masterdir = os.getcwd()

import configparser
config = configparser.ConfigParser()
config.read(masterdir+'/01-config/pw-config.ini')
tenant_id = config.get('msftparam', 'tenant_id')
client_id = config.get('msftparam', 'client_id')
client_secret = config.get('msftparam', 'client_secret')

# Set up the variables
tenant_id = tenant_id
client_id = client_id
client_secret = client_secret
resource_url = 'https://graph.microsoft.com'
api_version = 'v1.0'
user_email = 'mbs-bigdata-delivery@y-data.fr'  # replace with the email address of the user you want to send the email on behalf of
recipient_emails_input = input('Enter recipient email addresses separated by a comma: ')
recipient_emails = recipient_emails_input.split(',')  # Split the input string into a list
email_subject = 'MBS Big data Stock project'
email_body = 'This is a test email sent using the Microsoft Graph API.'

# Get an access token using client secret
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource_url
}
response = requests.post(token_url, headers=headers, data=data)
try:
    token = response.json()['access_token']
except KeyError:
    print(f"Failed to retrieve access token: {response.json()['error_description']}")
    exit(1)

# Construct the email message (MIME part, not used with Graph API in this script)
msg = MIMEMultipart()
msg['Subject'] = email_subject
msg['From'] = user_email
# 'To' field in MIME message is not used for multiple recipients in Graph API, shown for completeness
msg['To'] = ", ".join(recipient_emails) 

# Create and attach the message body
text = MIMEText(email_body)
msg.attach(text)

# Attach the file from directory
attachment_dir = masterdir + '/03-output/'

# Construct email_message for Graph API with multiple recipients
email_message = {
    "message": {
        "subject": email_subject,
        "body": {
            "contentType": "Text",
            "content": email_body
        },
        "toRecipients": [
            {"emailAddress": {"address": email.strip()}} for email in recipient_emails
        ],
        "attachments": [
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": os.path.basename(file_path),
                "contentBytes": base64.b64encode(open(file_path, "rb").read()).decode(),
            } for file_path in glob.glob(attachment_dir + '*.xlsx')
        ]
    },
    "saveToSentItems": "true"
}

# Send the email using the Microsoft Graph API
send_email_url = f'{resource_url}/{api_version}/users/{user_email}/sendMail'
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}
response = requests.post(send_email_url, headers=headers, data=json.dumps(email_message))

# Check the response
if response.status_code == 202:
    print('Email sent successfully.')
    sys.exit(0)  # Exit script after successful email send
else:
    print('Error sending email.')
    print(response.text)