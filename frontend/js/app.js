
import config from './config.js';

document.getElementById('text-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the form from resetting and refreshing the page.
    
    const inputText = document.getElementById('inputText').value.trim();
    
    if (!inputText) {
        alert("Please enter some text.");
        return;
    }
    
    const emotionElement = document.getElementById('emotion');
    const confidenceElement = document.getElementById('confidence');
    
    try {
        // Log the request to check if everything is correct before sending
        console.log('Sending request with input text:', inputText);

        // Make a POST request to the Django API for text analysis
        const response = await fetch('http://127.0.0.1:8000/api/analyze-text/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ input_text: inputText })  // Only send input_text
        });

        // Log the response status
        console.log('Response Status:', response.status);  // Log the response status

        if (!response.ok) {
            // Handle errors in the response
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Response Data:', data);  // Log the response data
        
        if (data.error) {
            emotionElement.textContent = `Error: ${data.error}`;
            confidenceElement.textContent = "";
        } else {
            emotionElement.textContent = data.predicted_emotion || "Unknown";
            confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
        }
    } catch (error) {
        console.error('Error:', error);  // Log the error
        emotionElement.textContent = `Error: ${error.message}`;
        confidenceElement.textContent = "";
    }
});


// document.getElementById('text-form').addEventListener('submit', async function(event) {
//     event.preventDefault();
    
//     const inputText = document.getElementById('inputText').value.trim();
    
//     if (!inputText) {
//         alert("Please enter some text.");
//         return;
//     }
    
//     const emotionElement = document.getElementById('emotion');
//     const confidenceElement = document.getElementById('confidence');
    
//     try {
//         const response = await fetch(`${config.apiBaseUrl}/analyze-text/`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ input_text: inputText })  // Only send input_text
//         });

//         if (!response.ok) {
//             throw new Error(`Error: ${response.status} ${response.statusText}`);
//         }

//         const data = await response.json();
        
//         if (data.error) {
//             emotionElement.textContent = `Error: ${data.error}`;
//             confidenceElement.textContent = "";
//         } else {
//             emotionElement.textContent = data.predicted_emotion || "Unknown";
//             confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         emotionElement.textContent = `Error: ${error.message}`;
//         confidenceElement.textContent = "";
//     }
// });

// document.getElementById('audio-form').addEventListener('submit', async function(event) {
//     event.preventDefault();
    
//     const inputAudio = document.getElementById('inputAudio').files[0];
//     const emotionElement = document.getElementById('emotion');
//     const confidenceElement = document.getElementById('confidence');

//     if (!inputAudio) {
//         alert("Please select an audio file to upload.");
//         return;
//     }
    
//     try {
//         // Prepare form data
//         const formData = new FormData();
//         formData.append("audio_file", inputAudio);
        
//         // Make a POST request to the Django API for audio analysis
//         const response = await fetch(`${config.apiBaseUrl}/analyze-audio/`, {
//             method: 'POST',
//             body: formData
//         });

//         const data = await response.json();
        
//         // Display the audio analysis results
//         emotionElement.textContent = data.predicted_emotion || "N/A";
//         confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
//     } catch (error) {
//         emotionElement.textContent = "Error: " + error.message;
//         confidenceElement.textContent = "";
//     }
// });

// // app.js
// import config from './config.js';

// document.getElementById('text-form').addEventListener('submit', async function(event) {
//     event.preventDefault();
    
//     const inputText = document.getElementById('inputText').value;
//     const emotionElement = document.getElementById('emotion');
//     const confidenceElement = document.getElementById('confidence');
    
//     try {
//         // Make a POST request to the Django API for text analysis
//         const response = await fetch(`${config.apiBaseUrl}/analyze-text/`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ input_text: inputText })
//         });

//         const data = await response.json();
        
//         // Display the text analysis results
//         emotionElement.textContent = data.predicted_emotion || "N/A";
//         confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
//     } catch (error) {
//         emotionElement.textContent = "Error: " + error.message;
//         confidenceElement.textContent = "";
//     }
// });

// document.getElementById('audio-form').addEventListener('submit', async function(event) {
//     event.preventDefault();
    
//     const inputAudio = document.getElementById('inputAudio').files[0];
//     const emotionElement = document.getElementById('emotion');
//     const confidenceElement = document.getElementById('confidence');

//     if (!inputAudio) {
//         alert("Please select an audio file to upload.");
//         return;
//     }
    
//     try {
//         // Prepare form data
//         const formData = new FormData();
//         formData.append("audio_file", inputAudio);
        
//         // Make a POST request to the Django API for audio analysis
//         const response = await fetch(`${config.apiBaseUrl}/analyze-audio/`, {
//             method: 'POST',
//             body: formData
//         });

//         const data = await response.json();
        
//         // Display the audio analysis results
//         emotionElement.textContent = data.predicted_emotion || "N/A";
//         confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
//     } catch (error) {
//         emotionElement.textContent = "Error: " + error.message;
//         confidenceElement.textContent = "";
//     }
// });


// // app.js
// import config from './config.js';

// document.getElementById('text-form').addEventListener('submit', async function(event) {
//     event.preventDefault();
    
//     const inputText = document.getElementById('inputText').value;
//     const emotionElement = document.getElementById('emotion');
//     const confidenceElement = document.getElementById('confidence');
    
//     try {
//         // Make a POST request to the Django API for text analysis
//         const response = await fetch(`${config.apiBaseUrl}/analyze-text/`, {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ input_text: inputText })
//         });

//         const data = await response.json();
        
//         // Display the text analysis results
//         emotionElement.textContent = data.predicted_emotion || "N/A";
//         confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
//     } catch (error) {
//         emotionElement.textContent = "Error: " + error.message;
//         confidenceElement.textContent = "";
//     }
// });

// document.getElementById('audio-form').addEventListener('submit', async function(event) {
//     event.preventDefault();
    
//     const inputAudio = document.getElementById('inputAudio').files[0];
//     const emotionElement = document.getElementById('emotion');
//     const confidenceElement = document.getElementById('confidence');

//     if (!inputAudio) {
//         alert("Please select an audio file to upload.");
//         return;
//     }
    
//     try {
//         // Prepare form data
//         const formData = new FormData();
//         formData.append("audio_file", inputAudio);
        
//         // Make a POST request to the Django API for audio analysis
//         const response = await fetch(`${config.apiBaseUrl}/analyze-audio/`, {
//             method: 'POST',
//             body: formData
//         });

//         const data = await response.json();
        
//         // Display the audio analysis results
//         emotionElement.textContent = data.predicted_emotion || "N/A";
//         confidenceElement.textContent = data.confidence_score ? data.confidence_score.toFixed(2) : "N/A";
//     } catch (error) {
//         emotionElement.textContent = "Error: " + error.message;
//         confidenceElement.textContent = "";
//     }
// });