import smtplib
import os
import logging
import re
import sys
import time
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config as cfg

class SMTPServer:
    server = None
    last_timestamp = time.time()

    def refresh_smtp_server(self):
        """
        Gets or refreshes a connection to an AWS SES SMTP server
        """
        try:
            self.server = smtplib.SMTP(cfg.HOST, cfg.PORT)
            self.server.ehlo()
            self.server.starttls()
            #smtplib docs recommend calling ehlo() before & after starttls()
            self.server.ehlo()
            self.server.login(cfg.USERNAME_SMTP, cfg.PASSWORD_SMTP)
            cfg.log.info("Logged in SMTP server %s" % cfg.HOST)
        except Exception as e:
            cfg.log.error(e)
            self.server.close()
            sys.exit(2)
        self.last_timestamp = time.time()
        cfg.log.info('New smtp server connection created. TS: %s' % self.last_timestamp)


    def batch_send(self, sender, recipients_batch, msg, notified):
        """
        Sends an smtp msg as a blind copy (bcc) to a list of recipients
        """
        if len(recipients_batch) == 0:
            cfg.log.info("No recipients. Exiting")
            sys.exit(0)
        if not self.server:
            cfg.log.info("No SMTP server connection. Getting one...")
            self.refresh_smtp_server()
        if time.time() - self.last_timestamp > cfg.SERVER_TTL:
            cfg.log.info("SMTP Server connection exceeded TTL (%s). Getting a new one..." % (time.time() - LAST_SERVER_TIMESTAMP))
            self.refresh_smtp_server()
        mail_count = 0
        retries = 0
        while True:
            try:
                self.server.sendmail(sender, recipients_batch, msg.as_string())
                for recipient in recipients_batch:
                    cfg.log.info("%s done" % recipient)
                    with open(cfg.NOTIFIED_FILE, "a") as fh:
                        fh.write("%s\n" % recipient)
                        notified[recipient] = 1
                        mail_count += 1
            except Exception as e:
                cfg.log.error(e)
                retries += 1
                time.sleep(retries * cfg.WAIT_ON_ERROR)
                cfg.log.info('Retry %s' % retries)
                self.refresh_smtp_server()
                if retries >= cfg.MAX_RETRIES:
                    cfg.log.error('Max retries reached. Aborting.')
                    self.server.close()
                    sys.exit(1)
                continue
            # break out of while if no exception
            break
        return mail_count

    def set_retries(self, retries):
        cfg.MAX_RETRIES = retries

    def set_retries_interval(self, interval):
        cfg.WAIT_ON_ERROR = interval

    def close(self):
        if self.server:
            self.server.close()
