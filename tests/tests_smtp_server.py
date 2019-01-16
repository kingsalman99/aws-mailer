import unittest
from mock import patch, Mock, call
from smtp_server import SMTPServer


class TestSMTPServer(unittest.TestCase):

    @patch.object(SMTPServer, "refresh_smtp_server")
    def test_batch_send(self, mock_refresh):
        server = SMTPServer()
        server.set_retries(0)
        try:
            server.batch_send("sender", ["rec1"], "msg", {})
        except:
            pass
        mock_refresh.assert_called()

    @patch.object(SMTPServer, "refresh_smtp_server")
    def test_batch_send_retries(self, mock_refresh):
        server = SMTPServer()
        server.set_retries(3)
        server.set_retries_interval(0)
        try:
            server.batch_send("sender", ["rec1"], "msg", {})
        except:
            pass
        calls = [call(), call(), call()]
        mock_refresh.assert_has_calls(calls, any_order=True)

    @patch.object(SMTPServer, "refresh_smtp_server")
    def test_batch_send_empty_recs(self, mock_refresh):
        server = SMTPServer()
        try:
            server.batch_send("sender", [], "msg", {})
        except:
            pass
        self.assertFalse(mock_refresh.called)
