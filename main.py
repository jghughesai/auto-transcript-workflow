import os
import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def main():
  file_content = download_files()

def get_summary(file_content):
  pass

def download_files():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    folder_response = service.files().list(
      q="name='api test' and mimeType='application/vnd.google-apps.folder'",
      spaces="drive",
      fields="files(id, name)"
    ).execute()

    folder_response_result = folder_response.get("files", [])
    folder_id = folder_response_result[0].get("id")

    file_response = service.files().list(
      q = f"'{folder_id}' in parents",
      fields="files(id, name)"
    ).execute()

    print(f"{file_response}\n")

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred getting the list of files: {error}")
  
  files_content = {
    "files": [
      # {"name": "Name", "file_content": "content", "id": "12345"},
      # {"name": "Name", "file_content": "content", "id": "12345"}
    ]
  }

  try:
    files = file_response["files"]
    i = 0
    for file in files:
      print(i)
      file_id = file.get("id")
      print(file_id)
      request = service.files().get_media(fileId=file_id)
      print("request works")
      file = io.BytesIO()
      downloader = MediaIoBaseDownload(file, request)
      done = False
      while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}.")
      file_str = str(file.getvalue())
      print(file_str)
      files_content["files"] += [{f"file_content{i}": file_str}]
      print(f"files_content: {files_content}")
      i +=1
      return "hey"
  
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred downloading the file(s): {error}")

if __name__ == "__main__":
  main()