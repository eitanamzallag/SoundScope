function fetchCurrentSong() {
    fetch('/current_song')  // Call the Flask API route
        .then(response => response.json()) // Convert response to JSON
        .then(data => {
            // Update song name
            document.querySelector(".curr-track-name").textContent = data.track_name;
            
            // Update album cover
            document.querySelector(".curr_track_photo").src = data.track_photo;
            console.log(data.playback);
            // Show/hide animation based on playback
            setTimeout(() => {
                let soundWave = document.querySelector(".sound-wave");
                if (soundWave) {
                    soundWave.style.display = data.playback ? "flex" : "none";
                } else {
                    console.warn("Warning: .sound-wave element not found (retrying).");
                }
            }, 50);
        })
        .catch(error => console.error("Error fetching song:", error));
}

// Call the function every 5 seconds
setInterval(fetchCurrentSong, 5000);

// Run immediately on page load
document.addEventListener("DOMContentLoaded", fetchCurrentSong);
