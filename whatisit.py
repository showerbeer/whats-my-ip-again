from dotenv import load_dotenv
from email.message import EmailMessage
from smtplib import SMTP, SMTPException, SMTPAuthenticationError
import os
import logging
import urllib.request
import urllib.parse

# Configure logging
logging.basicConfig(filename='whats-my-ip-again.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# Get credentials from .env
load_dotenv()
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

# Open file containing current IP address, or create is not exists
f = open('current_ip', 'a+')

# Go to start of file
f.seek(0)

# Read the current IP address from file
current_ip = f.readline()

# Fetch IP address from public API
url = 'http://bot.whatismyipaddress.com'
res = urllib.request.urlopen(url)
fetched_IP = res.read().decode('utf-8')


def generate_email(from_email, to_email, new_ip_address):
    msg = EmailMessage()
    msg['Subject'] = 'IP address was changed'
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(f'New IP address is {new_ip_address}')
    return msg


if current_ip != fetched_IP:
    logging.info('New IP found: ' + fetched_IP)
    f.truncate(0)
    f.write(fetched_IP)
    # Send email using Gmail. Requires enabling of Less Secure Apps in account (not recommended)
    try:
        email = generate_email(gmail_user, gmail_user, fetched_IP)
        server = SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, gmail_user, email.as_string())
    except SMTPAuthenticationError:
        logging.error('Incorrect username or password supplied to Gmail')
    except SMTPException as e:
        logging.error('Could not send email')
        logging.exception(e)

# Close the file after writing
f.close()
