import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

async def send_email(users, plume):
    for user in users:
        msg = EmailMessage()
        msg['Subject'] = 'Latest Plume News Update'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = user["email"]

        # Use f-strings to format the message content
        msg.set_content(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Plume News Update</title>
            <style>
                body {{
                    font-family: Lato, sans-serif;
                    background-color: #F5F8FA;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .header {{
                    background-color: #00A4BD;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 36px;
                }}
                .content {{
                    padding: 20px;
                }}
                .content h2 {{
                    font-size: 28px;
                    font-weight: 900;
                    margin-top: 0;
                }}
                .content p {{
                    font-size: 18px;
                    line-height: 1.6;
                }}
                .link {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 15px;
                    background-color: #00A4BD;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                .link:hover {{
                    background-color: #007B93;
                    color:white;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    font-size: 14px;
                    color: #777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Plume News Update</h1>
                </div>
                <div class="content">
                    <h2>Latest Plume Alert</h2>
                    <p>Hi {user["name"]},</p>
                    <p>We have detected a new plume event at {plume["datetime"]}</p>
                    <p>To explore the latest plume map and see the details, please click the button below:</p>
                    <a class="link" href='{plume["link"]}' target="_blank">View Plume Map</a>
                </div>
                <div class="footer">
                    <p>&copy; 2024 GHG Exploration. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        ''', subtype='html')

        # Send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
