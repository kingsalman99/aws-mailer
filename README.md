# aws-mailer
A small python program that lets you send a mail to a list of recipients via AWS SES SMTP service.

## Info:
https://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html

## Environment Variables:
```
export SENDER_SMTP=sender_email@sender_domain.com
export SENDERNAME_SMTP=sender_name
export USERNAME_SMTP=your_AWS_SES_ACCOUNT_USERNAME
export PASSWORD_SMTP=your_AWS_SES_ACCOUNT_PASSWORD
```

## Setup:
You need to have your recipients as new line separated lists inside directory
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
