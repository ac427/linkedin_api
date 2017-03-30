#!/usr/bin/python

## imports 
from flask import Flask,redirect, request
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
import ConfigParser

#config
Config = ConfigParser.ConfigParser()
Config.read("config")
client_id=Config.get ("config", "API_KEY")
client_secret =Config.get ("config", "API_SECRET")
authorization_base_url = 'https://www.linkedin.com/uas/oauth2/authorization'
token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'

linkedin = OAuth2Session(client_id, redirect_uri='http://localhost:8080/auth/linkedin/callback')
linkedin = linkedin_compliance_fix(linkedin)
authorization_url, state = linkedin.authorization_url(authorization_base_url)

## make sure to run this command before starting app or configure SSL . (how to set inside app, for later )
SSL_ENV='export OAUTHLIB_INSECURE_TRANSPORT=1'



app = Flask(__name__)


@app.route('/')
def init():
   #config
   Config = ConfigParser.ConfigParser()
   Config.read("config")
   client_id=Config.get ("config", "API_KEY")
   client_secret =Config.get ("config", "API_SECRET")
   authorization_base_url = 'https://www.linkedin.com/uas/oauth2/authorization'
   token_url = 'https://www.linkedin.com/uas/oauth2/accessToken'

   linkedin = OAuth2Session(client_id, redirect_uri='http://localhost:8080/auth/linkedin/callback')
   linkedin = linkedin_compliance_fix(linkedin)
   authorization_url, state = linkedin.authorization_url(authorization_base_url)
## redirect to linked in to get code & session 
   return redirect(authorization_url)

@app.route('/auth/linkedin/callback')
def auth():

   response_url= request.url
   code = request.args.get('code')

   # for some reason response_url is not getting #! values in url at the end; so use code 
   linkedin.fetch_token(token_url,client_secret=client_secret,code=code)

   #Fetch a protected resource, i.e. user profile
   people = linkedin.get('https://api.linkedin.com/v1/people/~?format=json')
   return  people.content

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8080)
