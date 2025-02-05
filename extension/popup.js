document.getElementById("applyFilterButton").addEventListener("click", () => {
    const filter = document.getElementById("filterSelect").value;
    
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { filter: filter });
    });
});
