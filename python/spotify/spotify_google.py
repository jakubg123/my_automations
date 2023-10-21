from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

creds = None
creds = service_account.Credentials.from_service_account_file(
        '/home/jakubg/my_automations/python/spotify/credentials.json', scopes=['https://www.googleapis.com/auth/drive.file'])

drive_service = build('drive', 'v3', credentials=creds)

def upload_file(file_name, mime_type, folder_id):
    media = MediaFileUpload(file_name, mimetype=mime_type)
    request = drive_service.files().create(
        media_body=media,
        body={
            'name': file_name,
            'parents': [folder_id]
        }
    )
    response = request.execute()
    return response

