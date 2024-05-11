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

def get_drive_files(creds):
  try:
    service = build("drive", "v3", credentials=creds)
    folder_response = service.files().list(
    q="name='file test' and mimeType='application/vnd.google-apps.folder'",
    spaces="drive",
    fields="files(id, name)"
    ).execute()

    folder_response_result = folder_response.get("files", [])
    folder_id = folder_response_result[0].get("id")

    # file_ids = []
    # print(f"file_ids: {file_ids}")

    # for target_id in target_ids:
    #     print(f"target_id in bad loop: {target_id}")
    #     file_response = service.files().list(
    #     q = f"'{folder_id}' in parents",
    #     fields="files(id, name)"
    #     ).execute()
    #     files = file_response["files"]
    #     print(f"\n\n\nfiles response: {files}\n\n\n")
    #     for file in files:
    #       if file['id'] == target_id:
    #         print(f"file['id'] matches target_id.")
    #         print(f"file['id'] {file['id']}")
    #         print(f"target_id {target_id}")
    #       file_ids.append(file["id"])
    #       # print(f"file[id]: {file['id']}")
    #       # print(f"file_ids: {file_ids}")

    return service, folder_id

  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred getting the list of files: {error}")
    return f"An error occurred getting the list of files: {error}"

def download_files(service, file_ids, file_names):
  files_dict = {
    "files": [
    ]
  }

  print(f"file_names in download_files(): {file_names}")
  print(f"file_ids in download_files(): {file_ids}")

  try:
    for file_name, file_id in zip(file_names, file_ids):
      request = service.files().get_media(fileId=file_id)

      file_buffer = io.BytesIO()
      test = str(file_buffer)

      downloader = MediaIoBaseDownload(file_buffer, request)
      done = False
      while done is False:
        status, done = downloader.next_chunk()
      file_buffer.seek(0)
      file_str = file_buffer.read().decode('utf-8')

      files_dict["files"].append({
        "name": file_name,
        "id": file_id,
        "file_content": file_str
      })
    return files_dict
  
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred downloading the file(s): {error}")

def upload_file(service, folder_id):
  for file in os.listdir('files'):
      file_metadata = {
        "name": file,
        "parents": [folder_id]
      }

      media = MediaFileUpload(f"files/{file}")
      upload_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

      print(f"\nUploaded file: {file}.")
  
  delete_files_in_dir()

def delete_files_in_dir():
  try:
    files = os.listdir("files")
    for file in files:
      file_path = os.path.join("files", file)
      if os.path.isfile(file_path):
        os.remove(file_path)
    print("All files deleted successfully.")
  
  except OSError:
    print("Error occured while deleting files.")