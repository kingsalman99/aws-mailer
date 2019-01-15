import unittest
from awsmailer import is_valid_email
from awsmailer import read_parse_msg
from awsmailer import read_already_notified
from awsmailer import read_recipients_lists

class TestAWSMailer(unittest.TestCase):

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("valid@some.com"))
        self.assertTrue(is_valid_email("valid@some.company"))
        self.assertTrue(is_valid_email("valid.dot@some.com"))
        self.assertTrue(is_valid_email("va123@some.com"))
        self.assertFalse(is_valid_email("invalidvalidsome.com"))
        self.assertFalse(is_valid_email("@@some.com"))

    def test_read_parse_msg(self):
        (subject, txt, html) = read_parse_msg('tests/resources/message.txt')
        self.assertEqual(subject, "Test")
        self.assertEqual(txt, "This is the body")
        self.assertEqual(html, "<html><body></html>")

    def test_read_already_notified(self):
        notified = read_already_notified('tests/resources/notified.list')
        self.assertTrue('abcd@nosuch.com' in notified)
        self.assertTrue('1234@nosuch.org' in notified)

    def test_read_recipients_lists(self):
        recs = read_recipients_lists('tests/resources/contacts')
        self.assertTrue('123@lol.com' in recs)
        self.assertTrue('abc@lol.com' in recs)
