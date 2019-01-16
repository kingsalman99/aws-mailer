# aws-mailer
A small python program that lets you send a mail to a list of recipients via AWS SES SMTP service.

## Info:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html

## Features
* Retries upon failure (see `config.py`) for relevant settings.
* Periodic refresh of AWS SMTP Server connection to alleviate recycling of backend servers done by AWS.
* Bookkeeping to avoid resending the message to recipients that already got it once.
* SES service imposes limits both on the rate and on the total number of emails you may send
over a period. Limits vary on regular not-sandboxed users and are quite small for new (sandboxed) users.
 Consult AWS documentation for details.

## Setup

### Environment Variables:
```
export SENDER_SMTP=sender_email@sender_domain.com
export SENDERNAME_SMTP=sender_name
export USERNAME_SMTP=your_AWS_SES_ACCOUNT_USERNAME
export PASSWORD_SMTP=your_AWS_SES_ACCOUNT_PASSWORD
export AWS_SMTP_HOST=AWS_SMTP_HOST_eg_email-smtp.us-east-1.amazonaws.com
export AWS_SMTP_PORT=AWS_SMTP_PORT_eg_587
```
`SENDER_SMTP` and `SENDERNAME_SMTP` (i.e. the user and his email address that the
message will be sent from must be a SES registered user and domain. See AWS documentation
above for details.

### Recipients lists:
Have your recipients as new line separated lists inside directory
`contacts` (there's an example list in the code already)

Craft your message according to the example in `example_message.txt`. Paste the
relevant sections in between the markers (`__SUBJECT`, etc).

## Execution:
`python3 awsmailer.py`

## Outputs
`notified.flatdb` a list of send emails (adresses). Leave that in place if you
want to restart sending operation and do not want to sent duplicate emails to
addresses that had one email already.

`awsmailer.log` log (this only grows, i.e. you probably want to delete it or
  archive it after a while).

## Execute Tests:
`python3 -m unittest tests/tests_*`
