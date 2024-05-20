import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

class GetSummaryError(Exception):
  pass

def set_openai_key(api_key):
  return OpenAI(api_key=api_key)

def get_summary(files, client):
  try:
    response_dict = {
      "responses": []
    }
    for file in files["files"]:
      file_name = file["name"]
      file_id = file["id"]
      file_content = file["file_content"]

      completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
        {"role": "system", "content": "You are an expert summarizer of work meeting transcripts."},
        {"role": "user", "content": f"Create a detailed and accurate summary of the following work meeting transcript: {file_content}"}
        ]
      )

      response_dict["responses"].append({
          "name": file_name,
          "id": file_id,
          "summary_content": completion.choices[0].message.content
        })

    return response_dict
  except Exception as e:
    logging.error(f"Unexpected error getting ai generated summary: {e}")
    raise GetSummaryError(f"Unexpected error getting ai generated summary: {e}")