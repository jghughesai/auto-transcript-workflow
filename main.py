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

client = OpenAI()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def main():
  files_dict = download_files()

  summary_dict = get_summary(files_dict)

def get_summary(files):
  for file in files["files"]:
    file_content = file["file_content"]

    completion = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
      {"role": "system", "content": "You are an expert summarizer of work meeting transcripts."},
      {"role": "user", "content": f"Create a detailed and accurate summary of the following work meeting transcript: {file_content}"}
      ]
    )

    print(f"\nSummary: {completion.choices[0].message.content}")
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
  
  files_dict = {
    "files": [
    ]
  }

  try:
    files = file_response["files"]
    for file in files:
      file_name = file.get("name")
      print(f"file_name: {file_name}")
      file_id = file.get("id")
      print(file_id)
      request = service.files().get_media(fileId=file_id)
      print("request works")
      file_buffer = io.BytesIO()
      downloader = MediaIoBaseDownload(file_buffer, request)
      done = False
      while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}.")
      file_str = str(file_buffer.getvalue())
      print(file_str)

      files_dict["files"].append({
        "name": file_name,
        "id": file_id,
        "file_content": file_str
      })
    return files_dict
  
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred downloading the file(s): {error}")

if __name__ == "__main__":
  main()