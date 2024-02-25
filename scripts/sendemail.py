import requests
import json
import configparser
import sys, os
import warnings
import base64
import glob
from EmailBody.emailbody import email_body

# Setup and configuration
warnings.filterwarnings("ignore")
os.system('cls' if os.name == 'nt' else 'clear')
masterdir = os.getcwd()
print(masterdir)

config = configparser.ConfigParser()
config.read(os.path.join(masterdir, '01-config', 'pw-config.ini'))
tenant_id = config.get('msftparam', 'tenant_id')
client_id = config.get('msftparam', 'client_id')
client_secret = config.get('msftparam', 'client_secret')

# Set up the variables
resource_url = 'https://graph.microsoft.com'
api_version = 'v1.0'
user_email = 'mbs-bigdata-delivery@y-data.fr'  # Replace with the actual sender email
recipient_emails_input = input('Enter recipient email addresses separated by a comma: ')
recipient_emails = recipient_emails_input.split(',')

email_subject = 'MBS Big Data Stock Project'

# Load the HTML email body from the file
email_body = email_body

# Get an access token using client credentials
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource_url
}
response = requests.post(token_url, headers=headers, data=data)
if response.status_code != 200:
    print(f"Failed to retrieve access token: {response.json().get('error_description', 'No error description')}")
    exit(1)
token = response.json()['access_token']

# Prepare attachments
attachment_dir = os.path.join(masterdir, '03-output')
attachments = [
    {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": os.path.basename(file_path),
        "contentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "contentBytes": base64.b64encode(open(file_path, "rb").read()).decode()
    } for file_path in glob.glob(os.path.join(attachment_dir, '*.xlsx'))
]

# Construct email_message for Graph API with HTML content, multiple recipients, and attachments
email_message = {
    "message": {
        "subject": email_subject,
        "body": {
            "contentType": "HTML",
            "content": email_body
        },
        "toRecipients": [
            {"emailAddress": {"address": email.strip()}} for email in recipient_emails
        ],
        "attachments": attachments
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
else:
    print('Error sending email:', response.text)
