import os
import base64
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import HTTPException
# Load environment variables
load_dotenv()


# -------------------------
# Configuration
# -------------------------

API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")


client = OpenAI(api_key=API_KEY)

# Only these values are allowed
Equipment = Literal[
    "tank",
    "pump",
    "valve",
    "water supply"
]


class mistake(BaseModel):
    start: Equipment
    stop: Equipment
    comment: str

class ImageAnalysis(BaseModel):
    mistakes: list[mistake]


def query(image_data, content_type):
    base64_image = base64.b64encode(image_data).decode("utf-8")

    try:

        response = client.responses.parse(
            model="gpt-5",

            input=[
                {
                    "role": "system",
                    "content": """
You are a teacher whose job is to mark your student's paper.
The paper contains a sketch of a water flow diagram. Each arrow signifies water flow. Start and stop represents the flow of water.

Given the answer
start: tank, stop: pump,
start: pump, stop: valve, 
start: valve, stop: tank
start: water supply, stop: tank

If a student drew an arrow from pump to tank and arrow from valve to pump.
Output
start:pump, stop:tank comment: This is wrong as it should go the other way around
start:valve, stop:pump : This is wrong because
Signifying that he has to work on these two connections. 
Do not output anything other than the required JSON structure.
""",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": (
                                f"data:{content_type};"
                                f"base64,{base64_image}"
                            ),
                            "detail": "high"
                        }
                    ]
                }
            ],

            text_format=ImageAnalysis
        )

        result = response.output_parsed
        print(result)
        return {
            "success": True,
            "analysis": result.model_dump()
        }

    except Exception as e:

        print("OpenAI error:", e)

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze image."
        )
