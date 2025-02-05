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
            .then(response => {
                if (!response.ok) {
                    console.error("API Error:", response.status);
                    return response.json().then(err => {
                        throw new Error(`API error: ${JSON.stringify(err)}`);
                    });
                }
                return response.blob();
            })
            .then(blob => {
                img.src = URL.createObjectURL(blob);
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
