// Main JavaScript for Yoga Pose Detection

// Load health information on page load
document.addEventListener('DOMContentLoaded', function() {
    loadHealthInfo();
});

// Load system health information
async function loadHealthInfo() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        const healthInfo = document.getElementById('healthInfo');
        if (data.status === 'ok') {
            healthInfo.innerHTML = `
                <p><strong>Status:</strong> <span style="color: #28a745;">✓ System Online</span></p>
                <p><strong>OpenCV Version:</strong> ${data.versions.opencv}</p>
                <p><strong>MediaPipe Version:</strong> ${data.versions.mediapipe}</p>
                <p><strong>NumPy Version:</strong> ${data.versions.numpy}</p>
            `;
        } else {
            healthInfo.innerHTML = '<p style="color: #e74c3c;">✗ System Error</p>';
        }
    } catch (error) {
        console.error('Error loading health info:', error);
        document.getElementById('healthInfo').innerHTML = 
            '<p style="color: #e74c3c;">✗ Unable to connect to server</p>';
    }
}

// Start video feed
function startVideo() {
    const videoFeed = document.getElementById('videoFeed');
    videoFeed.style.display = 'block';
    videoFeed.src = '/video_feed?' + new Date().getTime();
    console.log('Video feed started');
}

// Stop video feed
function stopVideo() {
    const videoFeed = document.getElementById('videoFeed');
    videoFeed.src = '';
    videoFeed.style.display = 'none';
    console.log('Video feed stopped');
}

// Handle user form submission
document.getElementById('userForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        experience: document.getElementById('experience').value
    };
    
    try {
        const response = await fetch('/api/save_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        const messageDiv = document.getElementById('message');
        
        if (data.status === 'success') {
            messageDiv.className = 'success';
            messageDiv.textContent = '✓ User data saved successfully!';
            document.getElementById('userForm').reset();
        } else {
            messageDiv.className = 'error';
            messageDiv.textContent = '✗ Error: ' + data.message;
        }
        
        // Hide message after 3 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
        
    } catch (error) {
        console.error('Error saving user:', error);
        const messageDiv = document.getElementById('message');
        messageDiv.className = 'error';
        messageDiv.textContent = '✗ Failed to save user data';
    }
});

// Optional: Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Press 'S' to start video
    if (e.key === 's' || e.key === 'S') {
        startVideo();
    }
    // Press 'X' to stop video
    if (e.key === 'x' || e.key === 'X') {
        stopVideo();
    }
});

console.log('Yoga Pose Detection App Loaded - TEAM CODEASTRA');
