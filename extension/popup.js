// When a user selects a filter, send a message to apply the filter on all images
document.getElementById("applyFilterButton").addEventListener("click", () => {
    const filter = document.getElementById("filterSelect").value;
    
    // Send a message to the content script to apply the selected filter
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { filter: filter });
    });
});
