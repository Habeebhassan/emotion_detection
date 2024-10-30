from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
import json

# Path to your downloaded OAuth credentials file
CLIENT_SECRETS_FILE = "./client_secret_393908793020-tahceb69n7oigbhks4havcjciguec1m0.apps.googleusercontent.com.json"

# Scopes required for the Generative Language API
SCOPES = ["https://www.googleapis.com/auth/generative-language.tuning", "https://www.googleapis.com/auth/cloud-platform"]

# Perform the OAuth 2.0 flow to get credentials
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=8080)

# Now you have the OAuth token
access_token = credentials.token

# Use the access token in your API request
api_key = "AIzaSyD46CMD2uVfdLQYTgCHTaqX7A4VSQpadSg"
api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Input text to test emotion detection
input_text = "I'm feeling anxious about tomorrow. Analyze the emotional state of the speaker."

# Payload with text content to analyze
payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": input_text
                }
            ]
        }
    ]
}

# Set up headers for authorization
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send the request to Gemini API
response = requests.post(f"{api_endpoint}?key={api_key}", json=payload, headers=headers)

# Process the response
if response.status_code == 200:
    result = response.json()
    
    # Log the parsed result
    print("Parsed Emotion Analysis Result:", json.dumps(result, indent=4))
    
    emotion_text = result.get("contents", [{}])[0].get("parts", [{}])[0].get("text", "")
    print("Emotion Analysis Result:", emotion_text)
else:
    print(f"Error: {response.status_code}, {response.text}")


# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# import requests
# import json

# # Path to your downloaded OAuth credentials file
# CLIENT_SECRETS_FILE = "./client_secret_393908793020-tahceb69n7oigbhks4havcjciguec1m0.apps.googleusercontent.com.json"

# # Scopes required for the Generative Language API
# SCOPES = ["https://www.googleapis.com/auth/generative-language.tuning", "https://www.googleapis.com/auth/cloud-platform"]

# # Perform the OAuth 2.0 flow to get credentials
# flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
# credentials = flow.run_local_server(port=8080)

# # Now you have the OAuth token
# access_token = credentials.token

# # Use the access token in your API request
# api_key = "AIzaSyD46CMD2uVfdLQYTgCHTaqX7A4VSQpadSg"
# api_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# input_text = "I'm feeling anxious about tomorrow."

# payload = {
#     "contents": [
#         {
#             "parts": [
#                 {
#                     "text": input_text
#                 }
#             ]
#         }
#     ]
# }

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }

# response = requests.post(f"{api_endpoint}?key={api_key}", json=payload, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     result = response.json()
#     print("Response from API:", json.dumps(result, indent=4))
# else:
#     print(f"Error: {response.status_code}, {response.text}")