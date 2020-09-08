import hashlib

from flow360client.authentication import authentication_api

def login(email, password):
    email = 'zhenglei2010fall@gmail.com'
    password = 'Monday@2012'
    salt = '5ac0e45f46654d70bda109477f10c299'
    password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    authentication_api(email, password)

