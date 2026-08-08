import os
import base64

from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from google import genai
from google.genai import types
from fastapi import HTTPException


# Load environment variables
load_dotenv()


# -------------------------
# Configuration
# -------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")


client = genai.Client(api_key=API_KEY)


# -------------------------
# Output schema
# -------------------------

Equipment = Literal[
    "tank",
    "pump",
    "valve",
    "water supply"
]


class Mistake(BaseModel):
    start: Equipment
    stop: Equipment
    comment: str


class ImageAnalysis(BaseModel):
    mistakes: list[Mistake]


# -------------------------
# Gemini query
# -------------------------

def query(image_data, content_type):

    try:

        response = client.models.generate_content(
            model="gemini-3-flash-preview",

            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=content_type
                ),

                """
You are a teacher whose job is to mark a student's paper.

The paper contains a sketch of a water flow diagram.
Each arrow signifies the direction of water flow.

The correct answer is:

start: tank, stop: pump
start: pump, stop: valve
start: valve, stop: tank
start: water supply, stop: tank

Analyze the student's diagram and identify any incorrect
connections.

For every incorrect connection, create one object containing:

- "start": the equipment where the student's arrow starts
- "stop": the equipment where the student's arrow ends
- "comment": a short explanation of why the connection is wrong

For example, if the student drew:

pump → tank

when the correct direction is:

tank → pump

output a mistake with:

start: pump
stop: tank
comment: explain that the flow should go from tank to pump

Only report incorrect connections.

If all connections are correct, return an empty mistakes list.

Do not output anything other than the required JSON structure.
"""
            ],

            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ImageAnalysis,
            )
        )


        # -------------------------
        # Parse Gemini response
        # -------------------------

        result = ImageAnalysis.model_validate_json(
            response.text
        )


        print(result)

        return {
            "success": True,
            "analysis": result.model_dump()
        }


    except Exception as e:

        print("Gemini error:", e)

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze image."
        )