# auto-transcript-workflow

Auto Transcript Workflow
Description
Auto Transcript Workflow is an app designed to streamline the process of summarizing meeting transcripts. It monitors a Google Drive folder called "Transcripts Inputs" for new files, extracts the text, and uses the OpenAI Chat Completion API to generate a detailed summary. The summary is then saved in another Google Drive folder named "Transcript Outputs".

Features
Automated Transcript Monitoring: Tracks the "Transcripts Inputs" folder for new files.
Text Extraction: Extracts text from newly added files.
AI-Powered Summarization: Uses the OpenAI Chat Completion API to create detailed summaries.
Organized Output: Saves the generated summaries in the "Transcript Outputs" folder.
Secure Access: Includes a sign-in form on the landing page with inputs for username and password, currently configured for single-user access.
Installation
Note: This app is currently not deployed and is primarily for demonstrating programming abilities.

Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/auto-transcript-workflow.git
cd auto-transcript-workflow
Set Up Dependencies:

Ensure you have Python installed.
Install the required packages:
bash
Copy code
pip install -r requirements.txt
Configure API Keys:

Set up your Google Drive API and Google Drive Activity API.
Obtain your OpenAI API key.
Place these keys in a .env file in the root directory:
makefile
Copy code
GOOGLE_DRIVE_API_KEY=your_google_drive_api_key
OPENAI_API_KEY=your_openai_api_key
Run the Application:

bash
Copy code
python app.py
Usage
Sign In: Access the app and sign in using the configured credentials.
Add Transcripts: Place your meeting transcript files in the "Transcripts Inputs" folder on your Google Drive.
Generate Summaries: The app will automatically detect new files, process them, and generate summaries saved in the "Transcript Outputs" folder.
Configuration
There are no additional configurations required at this time.

Contributing
Currently, there are no guidelines for contributing to this project.

License
This project does not have a specified license.

Contact Information
For questions or feedback, please contact jghughesai@gmail.com.

Screenshots
Include screenshots here

Credits
APIs Used:
Google Drive API
Google Drive Activity API
OpenAI API
