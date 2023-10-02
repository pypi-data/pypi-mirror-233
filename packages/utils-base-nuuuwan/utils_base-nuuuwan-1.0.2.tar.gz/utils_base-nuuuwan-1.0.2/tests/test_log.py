import unittest

from utils_base import Log, _log


class TestCase(unittest.TestCase):
    def test_log(self):
        for __log in [_log, Log('custom')]:
            self.assertIsNotNone(__log)
            for func in [
                __log.debug,
                __log.info,
                __log.warning,
                __log.error,
                __log.critical,
            ]:
                print('before')
                func('test')
                print('after')


if __name__ == '__main__':
    unittest.main()
