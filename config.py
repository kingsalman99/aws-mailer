import os

# max recipients per batch
MAX_RECS_PER_BATCH = 50
# secs to cool down in between batches
COOL_DOWN = 2
# retries consts
WAIT_ON_ERROR = 5
MAX_RETRIES = 5
# refresh smtp server connection after 10 mins
SERVER_TTL = 10 * 60.0
# persist notified users here - do not delete this file
NOTIFIED_FILE = 'notified.flatdb'
# implicit input - files with lists of who is to be notified should live in this dir
RECIPIENTS_DIR = 'contacts'
# what is to be mailed - see example_message.txt for an example/layout
MSG_FILE = 'message.txt'

# This address must be verified in AWS SES
SENDER = os.environ['SENDER_SMTP']
SENDERNAME = os.environ['SENDERNAME_SMTP']
# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = os.environ['USERNAME_SMTP']
# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = os.environ['PASSWORD_SMTP']
# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
#CONFIGURATION_SET = "ConfigSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon),
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
# endpoint in the appropriate region.
HOST = os.getenv('AWS_SMTP_HOST', "email-smtp.us-east-1.amazonaws.com")
PORT = os.getenv('AWS_SMTP_PORT', 587)
