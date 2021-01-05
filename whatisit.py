from dotenv import load_dotenv
from email.message import EmailMessage
from smtplib import SMTP, SMTPException, SMTPAuthenticationError
from urllib import request
from os import getenv
import logging

# Configure logging
logging.basicConfig(filename='whats-my-ip-again.log', level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# Get credentials from .env
load_dotenv()
gmail_user = getenv('GMAIL_USER')
gmail_password = getenv('GMAIL_PASSWORD')

# Open file containing current IP address, or create's it if it doesn't exist
with open('current_ip', 'a+') as f:
    # Go to start of file
    f.seek(0)

    # Read the current IP address from file
    current_ip = f.readline()

    # Fetch IP address from public API
    url = 'http://bot.whatismyipaddress.com'
    res = request.urlopen(url)
    fetched_IP = res.read().decode('utf-8')

    if current_ip != fetched_IP:
        # Log and save new IP
        logging.info('New IP address: ' + fetched_IP)
        f.truncate(0)
        f.write(fetched_IP)
        # Generate the email
        email = EmailMessage()
        email['Subject'] = 'IP address was changed'
        email['From'] = gmail_user
        email['To'] = gmail_user
        email.set_content(f'New IP address is {fetched_IP}')
        # Send email using Gmail. Requires enabling of Less Secure Apps in account (not recommended)
        try:
            server = SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, gmail_user, email.as_string())
            logging.info(f'Email notification sent to {gmail_user}')
        except SMTPAuthenticationError:
            logging.error('Incorrect username or password supplied to Gmail')
        except SMTPException as e:
            logging.error('Could not send email')
            logging.exception(e)
