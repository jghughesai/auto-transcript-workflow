import logging
from drive import *
from drive_activity import *
from ai_summary import *

logging.basicConfig(level=logging.INFO)

def main(api_key):
  try:
    client = set_openai_key(api_key)
    service1, creds = authorize_google_apis()
    activities = fetch_activities(service1)

    if not activities:
      logging.info("No activity detected.")
      return "failed"
    
    logging.info("Recent activity detected.")
    target_ids, target_names = get_file_info(activities)
    logging.info(f"target_ids: {target_ids}. target_names: {target_names}")

    service2, folder_id = access_google_drive(creds)
    files_dict = download_target_files(service2, target_ids, target_names)

    summary_dict = generate_summaries(files_dict, client)

    create_output_files(summary_dict['responses'])
    upload_summaries(service2, folder_id)

    return "success"
  except AuthorizationError as e:
    logging.error(f"AuthorizationError in main: {e}")
    return "authorization_error"
  except ActivityFetchError as e:
    logging.error(f"ActivityFetchError in main: {e}")
    return "activity_error"
  except Exception as e:
    logging.error(f"Unexpected global error: {e}")
    return "error"
  

def authorize_google_apis():
  service1, creds = authorize_activity_api()
  if service1 is None or creds is None:
      notify_user("Unable to authenticate and retrieve google activity drive credentials.")
      raise Exception("Google API authorization failed")
  return service1, creds

def fetch_activities(service):
  try:
    time_filter = get_time_filter()
    activities = get_activities(service, time_filter)
    if activities == "unknown":
      notify_user("Error getting user's activities from Google Drive.")
      raise Exception("Error fetching activities")
    return activities
  except ActivityFetchError as e:
    logging.error(f"ActivityFetchError in fetch_activities: {e}")
    raise

def access_google_drive(creds):
  service, folder_id = get_drive_files(creds)
  if service is None or folder_id is None:
      notify_user("Unable to access Google Drive. Check your network connection and try again later.")
      raise Exception("Google Drive access failed")
  return service, folder_id

def download_target_files(service2, target_ids, target_names):
  files_dict = download_files(service2, target_ids, target_names)
  if files_dict is None:
    notify_user("Unable to download files.")
    raise Exception("File download failed")
  return files_dict

def generate_summaries(files_dict, client):
  summary_dict = get_summary(files_dict, client)
  if summary_dict is None:
    notify_user("Unable to generate summary for transcript.")
    raise Exception("Summary generation failed")
  return summary_dict

def create_output_files(summaries):
  try:
    for summary in summaries:
      file_name = summary['name']
      file_content = summary['summary_content']

      f = open(f"files/Summary-{file_name}.docx", "w+")
      f.write(file_content)
  except IndexError as e:
    logging.error(f"Index error creating temporary summary files to local dir: {e}")
  except Exception as e:
    logging.error(f"Unexpected error occured: {e}")

def upload_summaries(service, folder_id):
  try:
    upload_file(service, folder_id)
  except Exception as e:
    logging.error(f"Unexpected error occurred during file upload: {e}")
    raise

def notify_user(message):
  print(message)

if __name__ == "__main__":
  main()