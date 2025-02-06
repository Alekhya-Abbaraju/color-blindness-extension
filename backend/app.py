from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Color Blindness API is running!"}

# Color blindness filters
FILTERS = {
    'protanopia': np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]]),
    'deutanopia': np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]]),
    'tritanopia': np.array([[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]]),
}

def apply_filter(image: Image, filter_type: str) -> Image:
    """Applies the selected color blindness filter to the image."""
    if filter_type not in FILTERS:
        raise ValueError("Invalid filter type")
    
    image = image.convert("RGB")
    img_array = np.array(image)
    transformed = np.dot(img_array[..., :3], FILTERS[filter_type].T)
    transformed = np.clip(transformed, 0, 255).astype(np.uint8)
    return Image.fromarray(transformed)

@app.get("/process-image/")
async def process_image(
    filter_type: str = Query(..., enum=FILTERS.keys()),
    image_url: str = Query(..., regex="https?://.*")
):
    try:
        # Fetch image with headers to prevent blocking
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(image_url, headers=headers, stream=True)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image")

        # Read content and ensure it's an image
        content_type = response.headers.get("Content-Type", "")
        valid_mime_types = ["image/jpeg", "image/png"]

        if not any(mime in content_type for mime in valid_mime_types):
            raise HTTPException(status_code=400, detail=f"Unsupported image format: {content_type}")

        # Convert response content to Image
        image = Image.open(BytesIO(response.content))

        # Apply filter
        filtered_image = apply_filter(image, filter_type)
        
        # Convert to bytes for response
        img_byte_arr = BytesIO()
        filtered_image.save(img_byte_arr, format="JPEG")
        img_byte_arr.seek(0)

        return StreamingResponse(img_byte_arr, media_type="image/jpeg")

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
