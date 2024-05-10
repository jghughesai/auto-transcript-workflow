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
    target_names = get_file_names(activities)
    print(f"target names: {target_names}")

    file_ids, file_names, service2 = get_drive_files(creds, target_names)

    files_dict = download_files(service2, file_names, file_ids)

    summary_dict = get_summary(files_dict)

    print(f"\n\nSummaries: {summary_dict}")

if __name__ == "__main__":
  main()