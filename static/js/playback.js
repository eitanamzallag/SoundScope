document.getElementById("play-button").addEventListener("click", function() {
    fetch("/play", { method: "POST" })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error("Error:", error));
});