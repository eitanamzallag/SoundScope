function startAnimation() {
    const scoreContainer = document.querySelector(".popularity");
    if (!scoreContainer) return; // Prevent errors if element isn't found

    let finalScore = parseInt(scoreContainer.getAttribute("data-score")) || 0;
    let scoreElement = document.getElementById("score");
    let currentScore = { value: 0 }; // GSAP animates this object instead

    // Define color ranges from low to high scores
    const colorStops = [
        "#1db954", // Green (0-10)
        "#2ecc71", // Light Green (11-20)
        "#f1c40f", // Yellow (21-30)
        "#f39c12", // Orange (31-40)
        "#e67e22", // Deep Orange (41-50)
        "#d35400", // Reddish Orange (51-60)
        "#c0392b", // Red (61-70)
        "#9b59b6", // Purple (71-80)
        "#8e44ad", // Dark Purple (81-90)
        "#3498db"  // Blue (91-100)
    ];

    gsap.to(currentScore, {
        value: finalScore,
        duration: 4, // Adjust for speed
        ease: "power2.out",
        onUpdate: function () {
            scoreElement.innerText = Math.floor(currentScore.value) + "% popularity";

            // Calculate the color based on score progression
            let progress = currentScore.value / 100; // Normalize score (0 to 1)
            let colorIndex = Math.min(Math.floor(progress * colorStops.length), colorStops.length - 1);
            let newColor = colorStops[colorIndex];

            // Apply background color change to the entire page
            gsap.to("body", { backgroundColor: newColor, duration: 0.5 });
        },
        onComplete: function () {
            updateDescription(finalScore);
            gsap.to("body", { backgroundColor: "#222222", duration: 0.5 });
        }
    });

    function updateDescription(score) {
        let descriptions = {
            0: "Your music taste is truly unique—you're discovering hidden gems before anyone else!",
            1: "You're on the fringe of mainstream—your taste is rare but appreciated by a select few.",
            2: "You're still off the beaten path, enjoying underrated tracks with a growing audience.",
            3: "A mix of niche and known—your taste balances individuality with some mainstream appeal.",
            4: "Right in the middle! Your playlist has both underground hits and popular favorites.",
            5: "You enjoy the best of both worlds—mainstream hits with a touch of personal flair.",
            6: "Your music taste is widely appreciated, featuring popular tracks with some unique picks.",
            7: "You're in tune with trending music—your taste aligns closely with what’s popular now.",
            8: "Your playlists are filled with crowd-pleasers—your music taste is a hit with the masses!",
            9: "You have peak mainstream taste! Your favorite songs dominate the charts and playlists."
        };

        let descriptionIndex = Math.min(Math.floor(score / 10), 9);
        let descriptionText = descriptions[descriptionIndex] || "Your music taste is unique!";

        gsap.to("#description", {
            opacity: 0,
            duration: 0.5,
            onComplete: function () {
                document.getElementById("description").innerText = descriptionText;
                gsap.to("#description", { opacity: 1, duration: 0.5 });
            }
        });
    }
}

// **Trigger animation when section enters the viewport**
function observeSection() {
    const popularitySection = document.querySelector(".popularity");
    if (!popularitySection) return;

    let observer = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    startAnimation();
                    observer.unobserve(entry.target); // Stop observing once triggered
                }
            });
        },
        { threshold: 0.5 } // Trigger when 50% of the section is visible
    );

    observer.observe(popularitySection);
}

// Ensure GSAP is loaded before running
if (typeof gsap === 'undefined') {
    const script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js";
    script.onload = () => observeSection();
    document.head.appendChild(script);
} else {
    observeSection();
}
