let mediaRecorder;
let chunks = [];
let uploadedChunks = [];
let totalChunkCount = 0;

const streamUploadUrl = '/save-stream/';
const saveAudioUrl = '/save-audio/';
const timeSlice = 5000;

const startRecordingButton = document.getElementById('startRecording');
const stopRecordingButton = document.getElementById('stopRecording');
const saveRecordingButton = document.getElementById('saveRecording');
const audioPreview = document.getElementById('audioPreview');
const resetRecordingButton = document.getElementById('resetRecording');

const csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

startRecordingButton.addEventListener('click', startRecording);
stopRecordingButton.addEventListener('click', stopRecording);
saveRecordingButton.addEventListener('click', saveRecording);
resetRecordingButton.addEventListener('click', resetRecording);

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (stream) {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    totalChunkCount += 1;
                    chunks.push(event.data);
                    uploadChunk(event.data, totalChunkCount);
                }
            };

            mediaRecorder.onstop = function() {
                const audioBlob = new Blob(chunks, { type: 'audio/webm' });
                audioPreview.src = URL.createObjectURL(audioBlob);
                saveRecordingButton.disabled = false;
            };

            startRecordingButton.disabled = true;
            stopRecordingButton.disabled = false;
            resetRecordingButton.disabled = true;

            chunks = [];
            mediaRecorder.start(timeSlice);
        } else {
            console.error('Failed to access microphone or no media stream available');
        }
    } catch (error) {
        console.error('Error accessing microphone:', error);
    }
}


function stopRecording() {
    mediaRecorder.stop();
    startRecordingButton.disabled = false;
    stopRecordingButton.disabled = true;
    resetRecordingButton.disabled = false;
}

async function saveRecording() {
    if (uploadedChunks.length <= 0) {
        console.error('No audio data recorded');
        return;
    }

    const formData = new FormData();
    formData.append('file_chunks', JSON.stringify(uploadedChunks));


    const response = await sendRequest(saveAudioUrl, 'POST', formData);
    if (response.ok) {
        let responseBody = await response.json();
        console.log(responseBody['file_name']);
    } else {
        console.error('Failed to save recording');
    }
}

function resetRecording() {
    audioPreview.src = '';
    saveRecordingButton.disabled = true;
    resetRecordingButton.disabled = true;
    resetRecordingButton.disabled = false;
}

async function uploadChunk(data, chunkCount){
    const formData = new FormData();
    formData.append('chunk', data);
    formData.append('chunk_count', chunkCount);

    const response = await sendRequest(streamUploadUrl, 'POST', formData);
    if (response.ok) {
        let responseBody = await response.json();
        uploadedChunks.push(responseBody['file_name']);
    } else {
        console.error('Failed to save recording');
    }

}

async function sendRequest(requestUrl, requestType, data){
    try {
        return await fetch(requestUrl, {
            headers: {
                'X-CSRFToken': csrfToken
            },
            method: requestType,
            body: data
        });
    } catch (error) {
        console.error('Error saving recording:', error);
    }
}