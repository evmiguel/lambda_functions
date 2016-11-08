from oauth2client import client

def get_token(event):
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri='https://api.erikamiguel.com/consult/authorize')
    if 'code' not in event["code"]:
        auth_uri = flow.step1_get_authorize_url()
        print auth_uri
        return auth_uri
    else:
        code = event["code"]
        credentials = flow.step2_exchange(code)
        print credentials

def lambda_handler(event, context):
    get_token(event)


if __name__ == "__main__":
    lambda_handler({}, "context")
