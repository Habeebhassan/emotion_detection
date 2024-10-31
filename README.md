# Emotion Detection & Mood Prediction API

This is an API service that detects emotions from text and audio inputs. It leverages external APIs for text analysis and voice transcription, integrating the functionality into a Django REST Framework application.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Troubleshooting](#troubleshooting)

---

## Features

- **Text Emotion Detection**: Detects emotions from a text input using a text analysis model.
- **Audio Emotion Detection**: Converts audio to text and analyzes the emotions in the spoken content.
- **Supports Multiple Emotions**: Analyzes content for multiple emotional categories, like joy, sadness, anger, etc.

---

## Prerequisites

Ensure the following are installed:

- Python 3.8+ 
- Django 4.x
- Django REST Framework
- Virtual Environment (recommended)
- External API access keys for:
  - AssemblyAI (for audio transcription)
  - Gemini or similar text analysis API (for emotion detection in text)

---

## Installation

Clone this repository and install the required dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/emotion-detection-api.git
cd emotion-detection-api
```

### Step 2: Set Up a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

Initialize the database by running migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Environment Setup

Configure your environment variables. In the project root, create a `.env` file to store sensitive configurations:

```plaintext
# .env file
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ASSEMBLYAI_API_KEY=your_assemblyai_key
GEMINI_API_KEY=your_gemini_key
```

> **Note**: Replace `your_secret_key`, `your_assemblyai_key`, and `your_gemini_key` with actual values.

---

## Running the API

1. **Start the Django Server**

   ```bash
   python manage.py runserver
   ```

2. **Access the API locally**

   By default, the API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

### 1. **Text Emotion Detection**

   - **URL**: `/api/analyze-text/`
   - **Method**: `POST`
   - **Content-Type**: `application/json`
   - **Request Body**:
     ```json
     {
       "text": "I am feeling really happy today!"
     }
     ```
   - **Response**:
     ```json
     {
       "text": "I am feeling really happy today!",
       "emotions": {
         "joy": 0.85,
         "sadness": 0.05,
         "anger": 0.02,
         "surprise": 0.08
       }
     }
     ```

### 2. **Audio Emotion Detection**

   - **URL**: `/api/analyze-audio/`
   - **Method**: `POST`
   - **Content-Type**: `multipart/form-data`
   - **Request Body**:
     - `audio_file`: Attach an audio file (e.g., .wav or .mp3)
   - **Response**:
     ```json
     {
       "transcription": "I'm excited to start this new project.",
       "emotions": {
         "joy": 0.78,
         "sadness": 0.1,
         "anger": 0.05,
         "surprise": 0.07
       }
     }
     ```

---

## Testing the API

You can use tools like **Postman** or **curl** to test the API.

### Example with curl

```bash
# Text Emotion Analysis
curl -X POST http://127.0.0.1:8000/api/analyze-text/ \
     -H "Content-Type: application/json" \
     -d '{"text": "Feeling grateful and happy"}'
```

```bash
# Audio Emotion Analysis
curl -X POST http://127.0.0.1:8000/api/analyze-audio/ \
     -F "audio_file=@path/to/your/audio/file.wav"
```

### Example with Postman

1. Open **Postman** and create a new **POST** request.
2. For text emotion analysis, go to **Body** > **raw**, select JSON format, and add the text input.
3. For audio emotion analysis, go to **Body** > **form-data**, and add `audio_file` as a key with an audio file as the value.

---

## Troubleshooting

1. **404 Not Found**: Ensure that the API endpoint URL is correct and that the server is running.
2. **500 Server Error**: Check if your API keys and environment variables are set correctly.
3. **AppRegistryNotReady**: Restart the server to load apps properly after making changes.
4. **Field Errors**: Ensure all model fields are properly declared in both the model and serializer.

---

## Contributing

Contributions are welcome! Please submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License.

---
