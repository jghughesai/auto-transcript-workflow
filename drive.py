import os
import os.path
import io
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

logging.basicConfig(level=logging.INFO)

class DriveAPIConnectionError(Exception):
  pass

class DownloadFileError(Exception):
  pass

class UploadFileError(Exception):
  pass

def get_drive_files(creds):
  try:
    service = build("drive", "v3", credentials=creds)
    folder_response = service.files().list(
    q="name='Transcript Outputs' and mimeType='application/vnd.google-apps.folder'",
    spaces="drive",
    fields="files(id, name)"
    ).execute()

    folder_response_result = folder_response.get("files", [])
    folder_id = folder_response_result[0].get("id")

    return service, folder_id

  except HttpError as e:
    logging.error(f"An error occurred getting the list of files: {e}")
    raise DriveAPIConnectionError("Error getting Google Drive API connection working.")
  except IndexError as e:
    logging.error(f"Index Error, no folders returned: {e}")
    raise DriveAPIConnectionError("Error getting Google Drive API connection working.")
  except Exception as e:
    logging.error(f"Unexpected error: {e}")
    raise DriveAPIConnectionError("Error getting Google Drive API connection working.")
  
def download_files(service, file_ids, file_names):
  files_dict = {
    "files": [
    ]
  }

  try:
    for file_name, file_id in zip(file_names, file_ids):
      request = service.files().export_media(fileId=file_id, mimeType='text/plain')

      file_buffer = io.BytesIO()

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
  
  except HttpError as e:
    # TODO(developer) - Handle errors from drive API.
    logging.error(f"An error occurred downloading the file(s): {e}")
    raise DownloadFileError(f"An error occurred downloading the file(s): {e}")
  except Exception as e:
    logging.error(f"Unexpected error downloading file(s): {e}")
    raise DownloadFileError(f"An error occurred downloading the file(s): {e}")
  
def upload_file(service, folder_id):
  try:
    for file in os.listdir('files'):
        file_metadata = {
          "name": file,
          "parents": [folder_id]
        }

        media = MediaFileUpload(f"files/{file}")
        service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    delete_files_in_dir()
  
    # delete_files_in_dir()
  except HttpError as e:
    logging.error(f"An error occurred uploading the file(s): {e}")
    raise UploadFileError(f"An error occurred uploading the file(s): {e}")
  except Exception as e:
    logging.error(f"An error occurred uploading the file(s): {e}")
    raise UploadFileError(f"An error occurred uploading the file(s): {e}")

def delete_files_in_dir():
  try:
    files = os.listdir("files")
    for file in files:
      file_path = os.path.join("files", file)
      if os.path.isfile(file_path):
        os.remove(file_path)
    logging.info("Successfully deleted all files in 'files'")
  
  except OSError as e:
    logging.error(f"An error occurred deleting the file(s): {e}")
    raise OSError