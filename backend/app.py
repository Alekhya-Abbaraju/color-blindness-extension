from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests

app = FastAPI()

# Enable CORS for all origins (can be restricted later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the image processing API"}

def apply_filter(image: Image, filter_type: str) -> Image:
    """Applies the selected color blindness filter to the image."""
    image = image.convert("RGB")
    img_array = np.array(image)

    filter_map = {
        'protanopia': np.array([[0.567, 0.433, 0], [0.558, 0.442, 0], [0, 0.242, 0.758]]),
        'deutanopia': np.array([[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.3, 0.7]]),
        'tritanopia': np.array([[0.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, 0.525]]),
    }

    if filter_type not in filter_map:
        raise ValueError("Invalid filter type")

    transformation_matrix = filter_map[filter_type]
    transformed = np.dot(img_array[..., :3], transformation_matrix.T)
    transformed = np.clip(transformed, 0, 255).astype(np.uint8)

    return Image.fromarray(transformed)
from fastapi import HTTPException
import imghdr

@app.get("/process-image/")
async def process_image(
    filter_type: str = Query(..., enum=["protanopia", "deutanopia", "tritanopia"]),
    image_url: str = Query(..., regex="https?://.*")
):
    try:
        # Download the image
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image from URL")

        # Check the file type
        image_type = imghdr.what(None, response.content)
        if image_type not in ['jpeg', 'png']:
            raise HTTPException(status_code=400, detail="Unsupported image format")

        # Process image
        with Image.open(BytesIO(response.content)) as image:
            filtered_image = apply_filter(image, filter_type)
            img_byte_arr = BytesIO()
            filtered_image.save(img_byte_arr, format="JPEG")
            img_byte_arr.seek(0)

            return StreamingResponse(img_byte_arr, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
