import unittest

from ivy import ivy

MSG_IDENTIFIER = 21
MSG_HEADER = '%i %i %c' % (ivy.MSG, MSG_IDENTIFIER, ivy.ARG_START)
EOL = chr(10)


class TestDecodeMSG(unittest.TestCase):
    'Tests the processing of valid, well-formed MSG protocol messages'

    def test_no_parameter(self):
        msg = MSG_HEADER
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(msg_type, ivy.MSG)
        self.assertEqual(msg_id, MSG_IDENTIFIER)
        self.assertEqual(tuple(params), ())  # params == '', *params == ()

    def test_one_parameter(self):
        msg = MSG_HEADER + 'hello' + ivy.ARG_END
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(tuple(params), ('hello',))

    def test_multiple_parameters(self):
        parameters = ('hello', 'world', '!')
        msg = MSG_HEADER + ivy.ARG_END.join(parameters) + ivy.ARG_END
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(tuple(params), parameters)


class TestDecodeMSG_withoutTrailingETX(unittest.TestCase):
    '''Tests that messages sent with the last parameter not terminted
    with an ETX char are processed as in ivy-c
    '''

    def test_one_empty_parameter(self):
        '''A lonely, not ETX-terminated empty parameter is interpreted as: no
        parameter supplied
        '''
        msg = MSG_HEADER + ''  # yes: + '' is basically a no-op :)
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(tuple(params), ())

    def test_one_non_empty_parameter(self):
        msg = MSG_HEADER + 'hello'
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(tuple(params), ('hello',))

    def test_multiple_parameters_last_one_empty(self):
        '''
        When the last parameter is not ETX-terminated, there is no last
        parameter!
        '''
        parameters = ('hello', 'world', '')
        msg = MSG_HEADER + ivy.ARG_END.join(parameters)
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(tuple(params), parameters[:2])

    def test_multiple_parameters_last_one_non_empty(self):
        parameters = ('hello', 'world', '!')
        msg = MSG_HEADER + ivy.ARG_END.join(parameters)
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(tuple(params), parameters)


class TestDecode(unittest.TestCase):
    def test_decode_direct_msg(self):
        # msg is the empty string
        msg = '7 12\x02'
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(ivy.DIRECT_MSG, msg_type)
        self.assertEqual(12, msg_id)
        self.assertSequenceEqual(('',), params)

        # msg is one whitespace
        msg = '7 12\x02 '
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(ivy.DIRECT_MSG, msg_type)
        self.assertEqual(12, msg_id)
        self.assertSequenceEqual((' ',), params)

        # msg: two whitespaces
        msg = '7 1\x02  '
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(ivy.DIRECT_MSG, msg_type)
        self.assertEqual(1, msg_id)
        self.assertSequenceEqual(('  ',), params)

        # generic message w/ whitespaces
        msg = '7 7\x02abc def ghi'
        msg_type, msg_id, params = ivy.decode_msg(msg)
        self.assertEqual(ivy.DIRECT_MSG, msg_type)
        self.assertEqual(7, msg_id)
        self.assertSequenceEqual(('abc def ghi',), params)
