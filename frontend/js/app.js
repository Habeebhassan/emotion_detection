import config from './config.js';

document.getElementById('text-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const inputText = document.getElementById('inputText').value.trim();
    
    if (!inputText) {
        alert("Please enter some text.");
        return;
    }
    
    const emotionElement = document.getElementById('emotion');
    const confidenceElement = document.getElementById('confidence');
    
    try {
        const response = await fetch(`${config.apiBaseUrl}/analyze-text/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ input_text: inputText })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }
        
        const data = await response.json();
        
        console.log('Response Data:', data);

        if (data.error) {
            emotionElement.textContent = `Error: ${data.error}`;
            confidenceElement.textContent = "";
        } else {
            emotionElement.textContent = data.predicted_emotion || "Unknown";
            confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
        }
    } catch (error) {
        console.error('Error:', error);
        emotionElement.textContent = `Error: ${error.message}`;
        confidenceElement.textContent = "";
    }
});

document.getElementById('audio-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const inputAudio = document.getElementById('inputAudio').files[0];
    const emotionElement = document.getElementById('emotion');
    const confidenceElement = document.getElementById('confidence');
    const transcriptElement = document.getElementById('transcript');
    const transcribedTextContainer = document.getElementById('transcribed-text');

    if (!inputAudio) {
        alert("Please select an audio file to upload.");
        return;
    }
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append("audio_file", inputAudio);
        
        // Make a POST request to the Django API for audio analysis
        const response = await fetch(`${config.apiBaseUrl}/analyze-audio/`, {
            method: 'POST',
            body: formData
        });

        // Check for HTTP error response
        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        
        // Display the audio analysis results
        emotionElement.textContent = data.predicted_emotion || "Unknown";
        confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";

        // Display transcription if available
        if (data.transcript_text) {
            transcriptElement.textContent = data.transcript_text;
            transcribedTextContainer.style.display = "block"; // Show transcription text
        } else {
            transcribedTextContainer.style.display = "none";  // Hide if no transcription
        }
    } catch (error) {
        console.error('Error:', error);
        emotionElement.textContent = "Error: " + error.message;
        confidenceElement.textContent = "";
        transcribedTextContainer.style.display = "none";  // Hide transcription on error
    }
});