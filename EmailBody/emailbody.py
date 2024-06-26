import sys
import os

# Define the function that takes tickerSymbol as an argument
def generate_email_body(tickerSymbol):
    
    # Use the tickerSymbol in the email body
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MBS Stock Trading Signal Project</title>
    </head>
    <body>
        <h1>MBS Stock Trading Signal Project</h1>
        <a href="https://github.com/Dandata0101" target="_blank">
            <img src="https://img.shields.io/badge/Author-DanRamirez-2ea44f?style=for-the-badge" alt="Author - DanRamirez">
        </a>

        <img src="https://img.shields.io/badge/PYTHON-3.11-red?style=for-the-badge&logo=python&logoColor=white" alt="Python - Version"><br>

        <h3>Documentation and Details</h3>
        <p style="margin-bottom: 0;">The following email contains the results for our stock signal Big Data project <strong><u>{tickerSymbol}</u></strong> data for Dr. Chen's course on <strong><u>Big Data: application to Business</u></strong>.</p>

        <p style="margin-bottom: 0;">The contains the following items:</p>
        <ul style="margin-top: 0;">
            <li>Charted data from selected stock.</li>
            <li>Full data output by day.</li>
        </ul>

        <a href="https://github.com/Dandata0101/mbs-Stock-signal-project" target="_blank">Click here for the project documentation on Github</a>

        <p> -----This is email sent using the Microsoft Graph API.</p>

    </body>
    </html>
    """
    return email_body