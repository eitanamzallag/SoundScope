let isScrolling = false;
let lastScrollTime = 0;

document.addEventListener("wheel", (event) => {
    if (isScrolling) {
        console.log("🚫 Scroll ignored: animation in progress.");
        return;
    }

    let panels = document.querySelectorAll(".panel");
    let viewportHeight = window.innerHeight;
    let currentScroll = window.scrollY;
    let now = performance.now();

    if (now - lastScrollTime < 400) {
        console.log("⚠ Scroll ignored: Too fast.");
        return;
    }
    lastScrollTime = now;

    let nearestPanelIndex = Math.round(currentScroll / viewportHeight);
    let targetPanelIndex = event.deltaY > 0 ? nearestPanelIndex + 1 : nearestPanelIndex - 1;

    // Ensure target panel is within bounds
    targetPanelIndex = Math.max(0, Math.min(targetPanelIndex, panels.length - 1));

    let targetPosition = targetPanelIndex * viewportHeight;

    console.log("➡ Moving to Panel:", targetPanelIndex, "at position:", targetPosition);

    if (targetPosition !== currentScroll) {
        isScrolling = true;
        smoothScrollTo(targetPosition, 600);
    }

    event.preventDefault();
}, { passive: false });

function smoothScrollTo(target, duration) {
    let start = window.scrollY;
    let distance = target - start;
    let startTime = performance.now();

    function scrollStep(timestamp) {
        let elapsed = timestamp - startTime;
        let progress = Math.min(elapsed / duration, 1);
        let easedProgress = easeOutQuad(progress);
        let newPosition = start + distance * easedProgress;

        window.scrollTo(0, newPosition);

        if (progress < 1) {
            requestAnimationFrame(scrollStep);
        } else {
            console.log("🏁 Final snap to:", target);
            window.scrollTo(0, target); // Ensure perfect alignment
            isScrolling = false;

            // ✅ Force fade-in for visible panels
            setTimeout(() => {
                fadeInPanels();
            }, 50);
        }
    }

    requestAnimationFrame(scrollStep);
}

// ✅ Improved fade-in detection
function fadeInPanels() {
    let panels = document.querySelectorAll(".panel");
    let viewportHeight = window.innerHeight;

    panels.forEach((panel, index) => {
        let rect = panel.getBoundingClientRect();
        console.log(`🔎 Checking Panel ${index}: top=${rect.top}, height=${rect.height}, viewport=${viewportHeight}`);

        // ✅ Ensures panel is fully in view before fading in
        if (rect.top >= -5 && rect.top < viewportHeight * 0.9) {
            if (!panel.classList.contains("visible")) {
                panel.classList.add("visible");
                panel.style.opacity = "1";
                panel.style.visibility = "visible";
                console.log(`🎉 Panel ${index} is now visible!`);
            }
        }
    });

    // Final check after a short delay
    setTimeout(() => {
        panels.forEach((panel, index) => {
            if (panel.classList.contains("visible")) {
                panel.style.opacity = "1";
                panel.style.visibility = "visible";
                console.log(`✅ Panel ${index} forced visible.`);
            }
        });
    }, 100);
}

// ✅ Ensure first panel is always visible on load
document.addEventListener("DOMContentLoaded", () => {
    let firstPanel = document.querySelector(".panel:first-child");
    if (firstPanel) {
        firstPanel.classList.add("visible");
        firstPanel.style.opacity = "1";
        firstPanel.style.visibility = "visible";
    }
    fadeInPanels();
});

// ✅ Ensure visibility check on manual scrolling
document.addEventListener("scroll", fadeInPanels);
document.addEventListener("resize", fadeInPanels);

function easeOutQuad(t) {
    return t * (2 - t);
}
