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


# Set up the variablesc
tenant_id = tenant_id
client_id = client_id
client_secret = client_secret
resource_url = 'https://graph.microsoft.com'
api_version = 'v1.0'
user_email = 'delivery@y-data.co'  # replace with the email address of the user you want to send the email on behalf ofd
recipient_email = input('Enter the recipient email address: ')
email_subject = 'Test email'
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

# Construct the email message
msg = MIMEMultipart()
msg['Subject'] = email_subject
msg['From'] = user_email
msg['To'] = recipient_email

# Create and attach the message body
text = MIMEText(email_body)
msg.attach(text)

# Attach the file from directory
attachment_dir = masterdir + '/01-projects/01-segmentation/04-summary/'

# Attach all files in the directory
for file_path in glob.glob(attachment_dir + '*.xlsx'):
    with open(file_path, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='octet-stream')
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        msg.attach(attachment)
email_message = {
    "message": {
        "subject": email_subject,
        "body": {
            "contentType": "Text",
            "content": email_body
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": recipient_email
                }
            }
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
else:
    print('Error sending email.')
    print(response.text)

print("returning to menu")
print('')
os.system('python '+masterdir +'/01-projects/01-segmentation/MenuTerminal.py')