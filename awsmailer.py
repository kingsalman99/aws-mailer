#!/usr/bin/env python3
import smtplib
import os
import re
import sys
import time
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import listdir
from os.path import isfile, join
import config as cfg
from smtp_server import SMTPServer


def is_valid_email(email):
    """
    Simple regex email addr checker
    """
    if len(email) > 5:
        if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,20})$", email) != None:
            return True
    return False


def read_parse_msg(path):
    """
    A simple parser. See example_message.txt for the proper message format.
    """
    keys = ["__SUBJECT", "__BODY_TEXT", "__BODY_HTML"]
    msg = {}
    for k in keys:
        msg[k] = []

    key = None
    count = 0
    with open(path) as fh:
        for ln in fh:
            line = ln.strip()
            count += 1
            # found a key - beggining or ending of a section
            if line in keys:
                # if no current key this is a beginning
                if key == None:
                    key = line
                # if current key same as the one we found this is an ending
                elif key in line:
                    key = None
                # else input is malformed - abort
                else:
                    cfg.log.error("Malformed message on line: %s" % count)
            # normal input
            else:
                if key is not None:
                    msg[key].append(line)
    return( "".join(msg["__SUBJECT"]),
            "".join(msg["__BODY_TEXT"]),
            "".join(msg["__BODY_HTML"]) )


def read_already_notified(notified_fpath):
    """
    Reads list of already notified addresses and adds them in a dictionary.
    """
    notified = {}
    if os.path.isfile(notified_fpath):
        cfg.log.info("Loading already notified recipients.")
        count = 0
        with open(notified_fpath) as fh:
            for line in fh:
                count += 1
                notified[line.strip().lower()] = 1
        cfg.log.info("Loaded %s notified recipients." % count)
    return notified


def read_recipients_lists(dirpath):
    """
    All files inside the "contacts" directory are read through.
    The files should contain lists of emails addresses separated by new lines.
    """
    recipients_list = []
    files = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    for f in files:
        with open(join(dirpath, f)) as fh:
            for line in fh:
                recipients_list.append(line.strip())
    cfg.log.info("Loaded %s recipients from %s lists" % (len(recipients_list),
                                                        len(files)))
    return recipients_list


def create_smtp_msg(subject, sendername, sender, recipient_list,
                    body_text, body_html):
    """
    Creates an smtp message
    """
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email.utils.formataddr((sendername, sender))
    msg["Bcc"] = ",".join(recipient_list)
    # Comment or delete the next line if you are not using a configuration set
    #msg.add_header("X-SES-CONFIGURATION-SET",CONFIGURATION_SET)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body_text, "plain")
    part2 = MIMEText(body_html, "html")
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    return msg


def should_skip(recipient, notified):
    """
    Should recipient be skipped?
    """
    if not is_valid_email(recipient):
        cfg.log.info("Ignoring %s (malformed email)" % recipient)
        return True
    if recipient in notified:
        cfg.log.info("Ignoring %s (already in notified list)" % recipient)
        return True
    return False


if __name__ == "__main__":
    server = SMTPServer()
    cfg.log.info(">> Sending batch emails with message:")
    (subject, body_txt, body_html) = read_parse_msg(cfg.MSG_FILE)
    cfg.log.info("Message Subject: %s" % subject)
    cfg.log.info("Message Text: %s" % body_txt)
    cfg.log.info("Message HTML: %s" % body_html)
    notified = read_already_notified(cfg.NOTIFIED_FILE)
    all_recipients_list = read_recipients_lists(cfg.RECIPIENTS_DIR)

    mail_count = 0
    total_count = 0
    recipients_batch = []
    start_time = time.time()
    for rec in all_recipients_list:
        total_count += 1
        recipient = rec.strip().lower()
        if not should_skip(recipient, notified):
            recipients_batch.append(recipient)
        if len(recipients_batch) == cfg.MAX_RECS_PER_BATCH or total_count == len(all_recipients_list):
            msg = create_smtp_msg(subject, cfg.SENDERNAME, cfg.SENDER, recipients_batch,
                                  body_txt, body_html)
            mail_count += server.batch_send(cfg.SENDER, recipients_batch, msg, notified)
            recipients_batch.clear()
            elapsed_time = time.time() - start_time
            cfg.log.info("Sent %s mails in %s mins" % (mail_count, round(elapsed_time/60,2)))
            # Throttle down
            time.sleep(cfg.COOL_DOWN)
    server.close()
