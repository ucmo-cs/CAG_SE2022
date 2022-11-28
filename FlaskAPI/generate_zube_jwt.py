from datetime import datetime, timedelta
from re import match
import sys
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from jwt import encode
import requests

class handleRequests():
    def __init__(self, api):
        self.api = api
    
    def buildHeader(self, method, CLIENT_ID, tokenSigning=None):
        temp_token = tokenSigning or self.api.authenticated_token
        headers = {
            'Authorization': 'Bearer %s' % temp_token,
            'X-Client-ID': CLIENT_ID,
            'Accept': 'application/json'
        }
        if method == 'post':
            headers['Content-Type'] = 'application/json'
        return headers

    def callRequest(self, url, headers, method='get', post_data=None):
        # print('url: %s' % url)
        # print('headers: %s' % headers)
        response = getattr(requests, method)(url, headers=headers, data=post_data)
        return self._manage_response(response)

    @staticmethod
    def _manage_response(res):
        if res.status_code != 200:
            sys.stderr.write('HTTP Satus code(Error): %s' % res.status_code)
            if res.reason:
                sys.stderr.write(' %s' % res.reason)
            print('\n')
            sys.exit(1)
        return res

class createToken():
    TOKEN_URL = 'https://zube.io/api/users/tokens'
    encoding_algorithm = 'RS256'
    expire_JWT = 20

    def __init__(self, CLIENT_ID=None, KEY=None):
        self.CLIENT_ID = CLIENT_ID
        self._private_key = self._read_key_file(KEY)
        self.authenticated_token = None
        

    @staticmethod
    def _read_key_file(pemfile):
        try:
            with open(pemfile, 'rb') as KEY:
                private_pem_key = serialization.load_pem_private_key(
                    KEY.read(),
                    password=None,
                    backend=default_backend()
                )
        except (ValueError, FileNotFoundError) as err:
            sys.stderr.write('%s\n' % err)
            sys.exit(1)

        return private_pem_key

    def signJWT(self):
        payload = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.expire_JWT),
            'iss': self.CLIENT_ID
        }
        # Need to add exception handling
        temp_token = encode(payload, self._private_key, self.encoding_algorithm)
        return temp_token
    

   
    def generateFinalToken(self):
        """
            This function returns a JWT access token valid for 24 hours!
        """
        # Call Build Header function
        headers = handleRequests(None).buildHeader(
            method='get', CLIENT_ID=self.CLIENT_ID, tokenSigning=self.signJWT())

        # Make a POST request on the token URL using above header information
        response = handleRequests(None).callRequest(
            self.TOKEN_URL, headers, method='post')

        if not match(r'^{"access_token"\:".+"}$', response.text):
            print('Hey God, what did I do wrong! \n God: You are retrieving maliciois Token!')
            sys.exit()

        return response.json()['access_token']


class ZubeAPI(createToken):
    def __init__(self, **kwargs):
        # Need to add Exception handling
        super(ZubeAPI, self).__init__(**kwargs)