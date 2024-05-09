import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from datetime import timezone

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.activity.readonly"]

FOLDER_ID = "1LmIfg3k1lb9qkRRXz7N8wvZxn4Dqpjt7"

titles = []

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
  return service

def get_activities(service, time_filter):
  results = service.activity().query(body={
          "pageSize": 10,
          "ancestorName": f"items/{FOLDER_ID}",
          "filter": f"time >= \"{time_filter}\" detail.action_detail_case:CREATE"
      }).execute()
  activities = results.get("activities", [])
  if not activities:
    print("No activity.")
    return None
  else:
    print("Recent activity:")
    return activities
  
def get_file_names(activities):
  for activity in activities:
    targets = map(getTargetInfo, activity["targets"])
    targets_str = ""
    target_name = targets_str.join(targets)

    print(f"target name: {target_name}")
    return target_name

def get_time_filter():
  four_hours_ago = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=4)
  time_filter = four_hours_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
  print(time_filter)
  return time_filter

def getTargetInfo():
  pass