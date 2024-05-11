import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from datetime import timezone

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.activity.readonly"]


FOLDER_ID = "1LmIfg3k1lb9qkRRXz7N8wvZxn4Dqpjt7"

def main():
  service = authorize_activity_api()
  time_filter = get_time_filter()
  activities = get_activities(service, time_filter)
  if not activities:
    print("No activity.")
  else:
    file_names = get_file_names(activities)
    print(f"file names: {file_names}")

def authorize_activity_api():
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

  service = build("driveactivity", "v2", credentials=creds)
  return service, creds

def get_activities(service, time_filter):
  results = service.activity().query(body={
          "pageSize": 10,
          "ancestorName": f"items/{FOLDER_ID}",
          "filter": f"time >= \"{time_filter}\" detail.action_detail_case:CREATE"
      }).execute()
  activities = results.get("activities", [])
  if not activities:
    return None
  else:
    return activities
  
def get_file_names(activities):
    file_ids = []
    file_names = []
    for activity in activities:
      ids, names = map(get_target_info, activity["targets"])
      ids_str = ",".join(ids)
      names_str = ",".join(names)
      file_ids.append(ids_str)
      file_names.append(names_str)
    print(f"file_ids in get_file_names func: {file_ids}")
    return file_ids, file_names

def get_time_filter():
  four_hours_ago = datetime.datetime.now(timezone.utc) - datetime.timedelta(minutes=4)
  time_filter = four_hours_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
  return time_filter

def get_target_info(target):
  try:
    if "driveItem" in target:
      title = target["driveItem"].get("title", "unknown")
      name = target["driveItem"].get("name", "unknown")
      print(f"name id: {name}")
      target_id = name[6:]
      print(f"target_id: {target_id}")
      return target_id, title
    if "drive" in target:
      title = target["drive"].get("title", "unknown")
      name = target["drive"].get("name", "unknown")
      print(f"name id: {name}")
      target_id = name[6:]
      print(f"target_id: {target_id}")
      return target_id, title
    if "fileComment" in target:
      parent = target["fileComment"].get("parent", {})
      title = parent.get("title", "unknown")
      name = parent.get("name", "unknown")
      print(f"name id: {name}")
      target_id = name[6:]
      print(f"target_id: {target_id}")
      return target_id, title
  except Exception as e:
    return f"Error getting target title: {e}"

if __name__ == "__main__":
  main()