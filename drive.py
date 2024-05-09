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

def get_drive_files(creds, file_names):
  try:
    service = build("drive", "v3", credentials=creds)
    folder_response = service.files().list(
    q="name='file test' and mimeType='application/vnd.google-apps.folder'",
    spaces="drive",
    fields="files(id, name)"
    ).execute()

    folder_response_result = folder_response.get("files", [])
    folder_id = folder_response_result[0].get("id")

    file_ids = []

    for file_name in file_names:
        print(f"file_name: {file_name}")
        file_response = service.files().list(
        q = f"name='{file_name}' and '{folder_id}' in parents",
        fields="files(id, name)"
        ).execute()
        print(f"file_response: {file_response}")
        files = file_response["files"]
        for file in files:
          file_ids.append(file["id"])

    return file_ids, file_names, service

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred getting the list of files: {error}")

def download_files(service, file_names, file_ids):
  files_dict = {
    "files": [
    ]
  }

  try:
    for file_name, file_id in zip(file_names, file_ids):
      print(f"file_name iteration: {file_name}")
      print(f"file_id iteration: {file_id}")
      request = service.files().get_media(fileId=file_id)
      file_buffer = io.BytesIO()
      downloader = MediaIoBaseDownload(file_buffer, request)
      done = False
      while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}.")
      file_str = str(file_buffer.getvalue())

      files_dict["files"].append({
        "name": file_name,
        "id": file_id,
        "file_content": file_str
      })
    return files_dict
  
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred downloading the file(s): {error}")