from oauth2client.client import OAuth2Credentials
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
import httplib2
import sys
import os

drive_service = ""

def get_credential():
    with open(os.path.expanduser(sys.argv[1])) as data_file:
        data = data_file.read()
    creds = OAuth2Credentials.from_json(data)
    http_auth = creds.authorize(httplib2.Http())
    return http_auth

def get_service():
    global drive_service
    if drive_service == "":
        auth = get_credential()
        drive_service = discovery.build('drive', 'v3', http=auth)
    return drive_service

def get_file_id():
    drive_service = get_service()
    file = drive_service.files().list(q=sys.argv[2]).execute()['files'][0]
    return file['id']



def upload_file():
    drive_service = get_service()
    id = get_file_id()
    file_metadata = {
        'mimeType': 'application/octet-stream'
    }
    media = MediaFileUpload(os.path.expanduser(sys.argv[3]),
                            mimetype='application/octet-stream',
                            resumable=True)

    file = drive_service.files().update(fileId=id,body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print 'File ID: %s' % file.get('id')
    
def upload_file_to_drive():
    upload_file()


if __name__ == "__main__":
    upload_file_to_drive()



