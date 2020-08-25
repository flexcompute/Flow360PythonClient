import hashlib
from unittest import TestCase

from flow360client.authentication import authentication_api


class TestGetAPIAuthentication(TestCase):
    def test_getAPIAuthentication(self):
        email = 'zhenglei2010fall@gmail.com'
        password = 'Monday@2012'
        salt = '5ac0e45f46654d70bda109477f10c299'
        password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        authentication_api(email, password)
