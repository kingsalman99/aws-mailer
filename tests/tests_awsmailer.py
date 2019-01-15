import unittest
import awsmailer

class TestAWSMailer(unittest.TestCase):

    def test_get_a_logger(self):
        logger = get_a_logger()
        self.assertIsNotNone(logger)
