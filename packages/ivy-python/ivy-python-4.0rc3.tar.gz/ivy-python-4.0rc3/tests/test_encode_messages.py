import threading
import unittest

from ivy import ivy

MSG_IDENTIFIER = 21
MSG_HEADER = '%i %i %c' % (ivy.MSG, MSG_IDENTIFIER, ivy.ARG_START)
EOL = chr(10)


class IvyClientTest(ivy.IvyClient):
    def __init__(self):
        self.status = ivy.INITIALIZED
        self.ping_ts = []
        self.ping_lock = threading.Lock()

        class TestSocket:
            def send(self, msg: str = '', client: IvyClientTest = self):
                client.msg_sent = msg

        self.socket = TestSocket()


class TestEncodeMessage(unittest.TestCase):
    """"""

    def setUp(self):
        self.client = IvyClientTest()

    def check_sent(self, raw_msg):
        self.assertEqual(self.client.msg_sent, raw_msg)

    def test_send_new_subscription(self):
        c = self.client
        c.send_new_subscription(12, 'blah (blah)?')
        self.check_sent(b'1 12\x02blah (blah)?\n')

    def test_send_message(self):
        c = self.client
        c.send_message(2, ('',))
        self.check_sent(b'2 2\x02\x03\n')
        c.send_message(5, ('one',))
        self.check_sent(b'2 5\x02one\x03\n')
        c.send_message(6, ('one', 'two'))
        self.check_sent(b'2 6\x02one\x03two\x03\n')

    def test_send_error(self):
        c = self.client
        c.send_error(99, 'iik')
        # rien en ivyprobe-c
        self.check_sent(b'3 99\x02iik\n')

    def test_remove_subscription(self):
        c = self.client
        c.remove_subscription(14)
        self.check_sent(b'4 14\x02\n')

    def test_encode_direct_message(self):
        self.client.send_direct_message(72, '')
        self.check_sent(b'7 72\x02\n')
        self.client.send_direct_message(72, ' ')
        self.check_sent(b'7 72\x02 \n')
        self.client.send_direct_message(72, '  ')
        self.check_sent(b'7 72\x02  \n')
        self.client.send_direct_message(8, 'abc')
        self.check_sent(b'7 8\x02abc\n')
        self.client.send_direct_message(8, 'abc def')
        self.check_sent(b'7 8\x02abc def\n')

    def test_encode_die_message(self):
        self.client.send_die_message()
        self.check_sent(b'8 0\x02\n')
        self.client.send_die_message(42)
        self.check_sent(b'8 42\x02\n')  # check: existe dans le protocole?
        self.client.send_die_message(41, 'plus one')
        self.check_sent(b'8 41\x02plus one\n')  # id. vérifier

    def test_encode_ping(self):
        c = self.client
        c.send_ping()
        # ivy-c: count 1, 2, 3 sur chaque agent avec reset à la déco.
        self.check_sent(b'9 0\x02\n')

    def test_encode_pong(self):
        c = self.client
        c.send_pong(12)
        self.check_sent(b'10 12\x02\n')

    def test_wave_bye(self):
        c = self.client
        c.wave_bye()
        # rien en ivyprobe-c
        self.check_sent(b'0 0\x02\n')
