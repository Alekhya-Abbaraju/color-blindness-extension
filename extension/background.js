chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "applyFilter") {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: applyColorBlindnessFilter,
                args: [request.filterType]
            });
        });
    }
});
