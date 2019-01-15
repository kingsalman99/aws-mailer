import unittest
from mock import patch, Mock

from smtp_server import SMTPServer


class TestSMTPServer(unittest.TestCase):

    @patch.object(SMTPServer, 'refresh_smtp_server')
    def test_batch_send(self, mock_refresh):
        server = SMTPServer()
        server.set_retries(0)
        try:
            server.batch_send('sender', ['rec1'], 'msg', {})
        except:
            pass
        mock_refresh.assert_called()
