from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bot_gem import query


# -------------------------
# FastAPI application
# -------------------------

app = FastAPI(
    title="AI Image Analyzer API",
    version="1.0.0"
)


# -------------------------
# CORS
# -------------------------

# During development, you can allow your frontend.
# Tighten this to your actual frontend domain in production.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #change this to the frontend website
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)


# -------------------------
# Health check
# -------------------------

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "AI Image Analyzer API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# -------------------------
# Image analysis
# -------------------------

@app.post("/api/analyse")
async def analyse(
    image: UploadFile = File(...)
):

    # -------------------------
    # Validate file type
    # -------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }
    content_type = image.content_type
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type."
        )


    # -------------------------
    # Read image
    # -------------------------

    image_data = await image.read()


    # TODO:
    # Add a maximum file-size check here.
    #
    # Example:
    #
    # MAX_SIZE = 10 * 1024 * 1024
    #
    # if len(image_data) > MAX_SIZE:
    #     raise HTTPException(
    #         status_code=413,
    #         detail="Image is too large."
    #     )


    return query(image_data, content_type)