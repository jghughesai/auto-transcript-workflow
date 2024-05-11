from drive import *
from drive_activity import *
from ai_summary import *

def main():
  # Authorize google API
  service1, creds = authorize_activity_api()
  time_filter = get_time_filter()
  activities = get_activities(service1, time_filter)

  if not activities:
    print("No activity.")
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
    print("\n\nget_summary func call completed.")
    print(f"summary_dict: {summary_dict}")

    create_output_files(summary_dict['responses'])
    print("\n\ncreate_output_files func call completed.")

    upload_file(service2, folder_id)
    print("\n\nupload_file func call completed.")


def create_output_files(summaries):
  for summary in summaries:
    file_name = summary['name']
    file_content = summary['summary_content']

    f = open(f"files/Summary-{file_name}", "w+")
    f.write(file_content)

def notify_user(message):
  print(message)

if __name__ == "__main__":
  main()