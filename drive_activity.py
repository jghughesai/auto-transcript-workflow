import os.path
import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from datetime import timezone

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.activity.readonly"]


FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID")

class AuthorizationError(Exception):
  pass

class ActivityFetchError(Exception):
  pass

def authorize_activity_api():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time.
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
    service = build("driveactivity", "v2", credentials=creds)
    return service, creds
  except HttpError as e:
    logging.error(f"Error during activity api authorization: {e}")
    raise AuthorizationError(f"Failed to authorize activity API: {e}")
  except Exception as e:
    logging.error(f"Error during activity api authorization: {e}")
    raise AuthorizationError(f"Failed to authorize activity API: {e}")

def get_activities(service, time_filter):
  try:
    results = service.activity().query(body={
            "pageSize": 10,
            "ancestorName": f"items/{FOLDER_ID}",
            "filter": f"time >= \"{time_filter}\" detail.action_detail_case:(CREATE MOVE)"
        }).execute()
    activities = results.get("activities", [])
    if not activities:
      return None
    else:
      return activities
  except HttpError as e:
    logging.error(f"Error fetching activities: {e}")
    raise ActivityFetchError(f"Failed to fetch activities: {e}")
  except Exception as e:
    logging.error(f"Error fetching activities: {e}")
    raise ActivityFetchError(f"Failed to fetch activities: {e}")

def get_file_info(activities):
    file_ids = []
    file_names = []
    for activity in activities:
      try:
        ids = map(get_target_ids, activity["targets"])
        names = map(get_target_titles, activity["targets"])
        ids_str = ",".join(ids)
        names_str = ",".join(names)
        file_ids.append(ids_str)
        file_names.append(names_str)
      except Exception as e:
        logging.error(f"Error in get_file_info: {e}")
        raise
    return file_ids, file_names

def get_time_filter():
  four_hours_ago = datetime.datetime.now(timezone.utc) - datetime.timedelta(minutes=4)
  time_filter = four_hours_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
  return time_filter

def get_target_ids(target):
  try:
    if "driveItem" in target:
      name = target["driveItem"].get("name", "unknown")
      target_id = name[6:]
      return target_id
    if "drive" in target:
      name = target["drive"].get("name", "unknown")
      target_id = name[6:]
      return target_id
    if "fileComment" in target:
      parent = target["fileComment"].get("parent", {})
      name = parent.get("name", "unknown")
      target_id = name[6:]
      return target_id
  except Exception as e:
    logging.error(f"Error getting target ID: {e}")
    raise

def get_target_titles(target):
  try:
    if "driveItem" in target:
      title = target["driveItem"].get("title", "unknown")
      return title
    if "drive" in target:
      title = target["drive"].get("title", "unknown")
      return title
    if "fileComment" in target:
      parent = target["fileComment"].get("parent", {})
      title = parent.get("title", "unknown")
      return title
  except Exception as e:
    logging.error(f"Error getting target title: {e}")
    raise
