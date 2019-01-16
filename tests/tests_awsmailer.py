import unittest
from email.mime.text import MIMEText
import email.utils

from awsmailer import is_valid_email
from awsmailer import read_parse_msg
from awsmailer import read_already_notified
from awsmailer import read_recipients_lists
from awsmailer import should_skip
from awsmailer import create_smtp_msg

class TestAWSMailer(unittest.TestCase):

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("valid@some.com"))
        self.assertTrue(is_valid_email("valid@some.company"))
        self.assertTrue(is_valid_email("valid.dot@some.com"))
        self.assertTrue(is_valid_email("va123@some.com"))
        self.assertFalse(is_valid_email("invalidvalidsome.com"))
        self.assertFalse(is_valid_email("@@some.com"))

    def test_read_parse_msg(self):
        (subject, txt, html) = read_parse_msg("tests/resources/message.txt")
        self.assertEqual(subject, "Test")
        self.assertEqual(txt, "This is the body")
        self.assertEqual(html, "<html><body></html>")

    def test_read_already_notified(self):
        notified = read_already_notified("tests/resources/notified.list")
        self.assertTrue("abcd@nosuch.com" in notified)
        self.assertTrue("1234@nosuch.org" in notified)

    def test_read_recipients_lists(self):
        recs = read_recipients_lists("tests/resources/contacts")
        self.assertTrue("123@lol.com" in recs)
        self.assertTrue("abc@lol.com" in recs)

    def test_should_skip(self):
        notified = {"skipme@dot.com" : 1}
        self.assertTrue(should_skip("skipme@dot.com", notified))
        self.assertTrue(should_skip("bademaildot.com", notified))

    def test_create_smtp_msg(self):
        recipient_list = ["rec1", "rec2"]
        parts = ["plain_text", "html"]
        msg = create_smtp_msg("subject", "sendername", "sender",
                              recipient_list, parts[0], parts[1])
        self.assertEqual(msg["subject"], "subject")
        self.assertEqual(msg["From"],
                         email.utils.formataddr(("sendername", "sender")))
        self.assertEqual(msg["Bcc"], ",".join(recipient_list))
        counter = 0
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            self.assertEqual(part.get_payload(), parts[counter])
            counter += 1
