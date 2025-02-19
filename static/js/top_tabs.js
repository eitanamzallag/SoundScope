document.addEventListener("DOMContentLoaded", function () {
    // Select each tab group independently
    document.querySelectorAll(".tabs").forEach(tabContainer => {
        const tabs = tabContainer.querySelectorAll("ul li");
        const section = tabContainer.closest(".panel"); // Get the correct section
        const contents = section.querySelectorAll(".tab-content");

        tabs.forEach(tab => {
            tab.addEventListener("click", function () {
                // Remove "is-active" from all tabs in this section
                tabs.forEach(t => t.classList.remove("is-active"));

                // Remove "is-active" from all content in this section
                contents.forEach(c => c.classList.remove("is-active"));

                // Get the tab's corresponding content
                const tabId = this.dataset.tab;
                const activeContent = section.querySelector(`#${tabId}`);

                // If content exists, activate it
                if (activeContent) {
                    this.classList.add("is-active");
                    activeContent.classList.add("is-active");
                } else {
                    console.warn(`No content found for tab: ${tabId}`);
                }
            });
        });
    });
});
