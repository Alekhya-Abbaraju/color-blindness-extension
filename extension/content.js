function applyColorBlindnessFilter(filterType) {
    document.querySelectorAll("img").forEach((img) => {
        const imageUrl = img.src;
        console.log(`Original image URL: ${imageUrl}`); // Check URL

        if(!imageUrl){
            console.error('Image has no src attribute');
        }
        const apiUrl = `http://localhost:8000/process-image/?filter_type=${filterType}&image_url=${encodeURIComponent(imageUrl)}`;
        console.log(`API URL: ${apiUrl}`); // Check the constructed API URL

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    console.error("Server returned an error:", response.status, response.statusText);
                    return response.json().then(err => {
                      throw new Error(`HTTP error! status: ${response.status}, error: ${JSON.stringify(err)}`);
                    });
                }
                return response.blob()
            })
            .then(blob => {
                img.src = URL.createObjectURL(blob);
            })
            .catch(error => console.error("Error applying filter:", error));
    });

    console.log(`Filter applied: ${filterType}`);
}