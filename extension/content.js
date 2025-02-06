function applyColorBlindnessFilter(filterType) {
    document.querySelectorAll("img").forEach((img) => {
        const imageUrl = img.src;

        if (!imageUrl.startsWith("http")) {
            console.warn("Skipping image (Invalid URL):", imageUrl);
            return;
        }

        const apiUrl = `http://localhost:8000/process-image/?filter_type=${filterType}&image_url=${encodeURIComponent(imageUrl)}`;
        console.log("API Request:", apiUrl);

        fetch(apiUrl)
            .then(async response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        console.error("API Error:", err.detail);
                        throw new Error(`API error: ${err.detail}`);
                    });
                }
                return response.blob();
            })
            .then(blob => {
                const objectUrl = URL.createObjectURL(blob);
                img.src = objectUrl;
            })
            .catch(error => console.error("Failed to apply filter:", error));
    });

    console.log(`Filter applied: ${filterType}`);
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.filter) {
        applyColorBlindnessFilter(request.filter);
    }
});
