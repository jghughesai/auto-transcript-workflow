from drive import *
from drive_activity import *
from ai_summary import *

def main():
  try:
    # Authorize google API
    service1, creds = authorize_activity_api()
    if service1 is None or creds is None:
      notify_user("Unable to authenticate and retrieve google activity drive credentials.")
      return
    time_filter = get_time_filter()
    activities = get_activities(service1, time_filter)
    if activities == "unknown":
      notify_user("Error getting user's activities from Google Drive.")
      return

    if not activities:
      print("No activity.")
      return None
    else:
      print("Recent activity:")
      target_ids, target_names = get_file_info(activities)
      print("\n\nget_file_name func call completed.")
      print(f"target ids: {target_ids}")
      print(f"target names: {target_names}")
      
      service2, folder_id = get_drive_files(creds)
      if service2 is None or folder_id is None:
        notify_user("Unable to access Google Drive. Please check your network connection and try again later.")
        return
      print("\n\nget_drive_files func call completed.")

      files_dict = download_files(service2, target_ids, target_names)
      if files_dict is None:
        notify_user("Unable to download files.")
        return
      print("\n\ndownload_files func call completed.")
      print(f"files_dict: {files_dict}")

      summary_dict = get_summary(files_dict)
      if summary_dict is None:
        notify_user("Unable to get summary for transcript.")
        return
      print("\n\nget_summary func call completed.")
      print(f"summary_dict: {summary_dict}")
      
      create_output_files(summary_dict['responses'])
      print("\n\ncreate_output_files func call completed.")

      upload_file(service2, folder_id)
      print("\n\nupload_file func call completed.")
      return "success"
  except Exception as e:
    logging.error(f"Unexpected global error: {e}")
    return

def create_output_files(summaries):
  try:
    for summary in summaries:
      file_name = summary['name']
      file_content = summary['summary_content']

      f = open(f"files/Summary-{file_name}", "w+")
      f.write(file_content)
  except IndexError as e:
    logging.error(f"Index error creating temporary summary files to local dir: {e}")
    return
  except Exception as e:
    logging.error(f"Unexpected error occured: {e}")

def notify_user(message):
  print(message)

if __name__ == "__main__":
  main()