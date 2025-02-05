from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import numpy as np
import requests
import imghdr

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
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch image")

        image_type = imghdr.what(None, h=response.content[:32])
        if image_type not in ['jpeg', 'png']:
            raise HTTPException(status_code=400, detail="Unsupported image format")

        with Image.open(BytesIO(response.content)) as image:
            filtered_image = apply_filter(image, filter_type)
            img_byte_arr = BytesIO()
            filtered_image.save(img_byte_arr, format="JPEG")
            img_byte_arr.seek(0)

            return StreamingResponse(img_byte_arr, media_type="image/jpeg")

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
