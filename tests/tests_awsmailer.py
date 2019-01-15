import unittest
from awsmailer import get_a_logger, is_valid_email
from awsmailer import read_parse_msg, read_already_notified

class TestAWSMailer(unittest.TestCase):

    def test_get_a_logger(self):
        logger = get_a_logger()
        self.assertIsNotNone(logger)

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
        logger = get_a_logger()
        notified = read_already_notified('tests/resources/notified.list', logger)
        self.assertTrue('abcd@nosuch.com' in notified)
        self.assertTrue('1234@nosuch.org' in notified)
