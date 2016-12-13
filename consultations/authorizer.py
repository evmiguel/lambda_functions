from oauth2client import client
import httplib2

def get_token(event):
    flow = client.flow_from_clientsecrets('client_secrets.json',
                                          scope=event['scope'],
                                          redirect_uri='https://api.erikamiguel.com/consult/auth')
    flow.params['include_granted_scopes'] = 'true'
    flow.params['access_type'] = 'offline'
    if 'code' in event['code']:
        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        return { "auth_uri" : auth_uri}
    else:
        code = event["code"]
        print code
        credentials = flow.step2_exchange(code)
        print credentials.to_json()
        http_auth = credentials.authorize(httplib2.Http())

def lambda_handler(event, context):
    get_token(event)


if __name__ == "__main__":
    lambda_handler({"scope":"google_url"}, "context")
