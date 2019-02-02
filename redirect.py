from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
import ssl

CLIENT_ID = "" #enter your client ID here
KEY = '' #enter the name of the key here
CERTIFICATE = '' #enter the name of the certificate here


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        #Get the Auth Code
        path, _, query_string = self.path.partition('?')
        code = parse_qs(query_string)['code'][0]

        #Post Access Token Request
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = { 'grant_type': 'authorization_code', 
                 'access_type': 'offline', 
                 'code': code, 
                 'client_id': CLIENT_ID, 
                 'redirect_uri': 'http://127.0.0.1'}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        
        #returned just to test that it's working
        self.wfile.write(authReply.text.encode())

httpd = HTTPServer(('localhost', 5000), Handler)

#SSL cert
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile=KEY, 
        certfile=CERTIFICATE, server_side=True)

httpd.serve_forever()