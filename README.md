# Emotion Detection & Mood Prediction API

This project provides an API that detects emotions from both text and audio inputs, with a frontend for interaction. The backend, built with Django, supports endpoints for text and audio emotion analysis, while the frontend, implemented with HTML, CSS, and JavaScript, connects to the API and displays results.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Emotion Labels](#emotion-labels)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)
  - [Using the Application](#using-the-application)
- [API Endpoints](#api-endpoints)
- [License](#license)

---

## Project Overview
The Emotion Detection & Mood Prediction API is designed to predict emotions based on user-provided text or audio files. The goal is to provide meaningful emotional analysis for applications in mental health and well-being. The API integrates external services for text analysis and voice transcription to derive predictions.

## Technologies Used
- **Backend**: Django, Django REST framework
- **Frontend**: HTML, CSS, JavaScript
- **Model**: Mental-BERT model (for text-based and audio-based emotion classification)
- **API Integrations**: AssemblyAI (for audio transcription), Gemini (for text-based emotion analysis)
- **Development Tools**: VSCode, Live Server (for frontend development)
- **Environment**: Virtualenv for Python dependency management

## Features
- Text-based emotion detection
- Audio-based emotion detection with transcription
- Confidence scores for predictions
- User-friendly frontend interface
- Cross-Origin Resource Sharing (CORS) setup for frontend-backend communication

---

## Emotion Labels
The project currently uses the **Mental-BERT** model, pre-trained for emotion classification, with a specific set of binary labels relevant to mental health. These labels include:

- **Depression / No Depression**
- **Suicide / No Suicide**
- **Distress / No Distress**

The model is configured to classify each input (text or transcribed audio) according to these categories, making it particularly useful for mental health screening applications.

---

## Installation

### Prerequisites
- Python 3.x
- Node.js
- Virtualenv (for Python)
- Visual Studio Code (recommended for using Live Server)

### Backend Setup
1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set Up Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Django Settings**:
   - Ensure that your Django `settings.py` is set up to handle audio file uploads with `MEDIA_ROOT` and `MEDIA_URL`.
   - Configure any required API keys for AssemblyAI and Gemini in your settings.

5. **Run Django Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Start the Backend Server**:
    ```bash
    python manage.py runserver
    ```

### Frontend Setup
The frontend will be served through VSCode's Live Server to bypass CORS issues.

1. **Open the Project in VSCode**:
   Open the project directory in Visual Studio Code.

2. **Install Live Server Extension**:
   - In VSCode, go to Extensions and install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension.

3. **Start Live Server**:
   - Right-click on `index.html` in the frontend directory and select **"Open with Live Server"**.
   - The frontend should be accessible at `http://127.0.0.1:5500` or a similar port.

---

## Usage

### Running the Backend
- Make sure the virtual environment is activated.
- Start the backend server with:
    ```bash
    python manage.py runserver
    ```

### Running the Frontend
- Open `index.html` in VSCode and start it with Live Server to bypass CORS.
- This should open a new browser window with the application running on a local port.

### Using the Application
1. **Text Analysis**:
   - Enter a piece of text in the "Enter Text" field and click **"Analyze Emotion"**.
   - The predicted emotion and confidence score will appear below.

2. **Audio Analysis**:
   - Select an audio file by clicking **"Upload Audio"**.
   - Click **"Analyze Audio Emotion"** to submit.
   - The results, including a transcription (if available), predicted emotion, and confidence score, will display below.

### API Endpoints
- **Text Analysis**: `/analyze-text/`
  - Method: `POST`
  - Payload: `{ "input_text": "<text>" }`
  - Response: `{ "predicted_emotion": "<emotion>", "confidence_score": <score> }`

- **Audio Analysis**: `/analyze-audio/`
  - Method: `POST`
  - Payload: Audio file in form-data format
  - Response: `{ "predicted_emotion": "<emotion>", "confidence_score": <score>, "transcript": "<text>" }`

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.
