https://travis-ci.org/zerogvt/aws-mailer.svg?branch=master

# aws-mailer
A small python program that lets you send a mail to a list of recipients via AWS Simple Email Service (SES).

## Info
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html

## Features/Notes
* Retries upon failure (see `config.py` for relevant settings).
* Periodic refresh of AWS SMTP Server connection to alleviate recycling of backend servers done by AWS (see `config.py` for relevant settings).
* Bookkeeping to avoid resending the message to recipients that already got it once.
* SES service imposes limits both on the rate and on the total number of emails you may send
over a period. Limits vary on regular not-sandboxed users and are quite small for new (sandboxed) users.
 Consult AWS documentation for details.

## Setup

### Operational Settings
`config.py` carries several settings pertaining to retries and batch sizes.

### Environment Variables
You need to export next environmental variables:
```
export SENDER_SMTP=sender_email@sender_domain.com
export SENDERNAME_SMTP=sender_name
export USERNAME_SMTP=your_AWS_SES_ACCOUNT_USERNAME
export PASSWORD_SMTP=your_AWS_SES_ACCOUNT_PASSWORD
export AWS_SMTP_HOST=AWS_SMTP_HOST_eg_email-smtp.us-east-1.amazonaws.com
export AWS_SMTP_PORT=AWS_SMTP_PORT_eg_587
```
`SENDER_SMTP` and `SENDERNAME_SMTP` (i.e. the user and his email address that the
message will be sent from) must be a SES registered user and domain. See AWS documentation
above for details.

### Recipients Lists
Have your recipients as new line separated lists inside directory
`contacts` (there's an example list in the code already)

### Message Format
Craft your message according to the example in `example_message.txt`. Paste the
relevant sections in between the markers (`__SUBJECT`, etc). At the moment the message
supports 2 MIME parts, a simple text and an HTML. Enter both as plain text inside the
relevant sections (`__BODY_TEXT` and `__BODY_HTML` respectively).

## Execution
`python3 awsmailer.py`

## Outputs
* `notified.flatdb`: a list of addresses where the message was sent. Leave that in place if you
want to restart sending operation and do not want to sent duplicate emails to
addresses that had one email already.

* `awsmailer.log`: log (this only grows, i.e. you probably want to delete it or
  archive it after a while).

## Execute Tests
`python3 -m unittest tests/tests_*`
