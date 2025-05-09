from dotenv import load_dotenv
load_dotenv()

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security

API_KEY_NAME = "x-api-secret"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

from fastapi import HTTPException, status

import os

async def verify_api_key(api_key: str = Security(api_key_header)):
    expected_key = os.getenv("API_SECRET")
    if api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key",
        )
    return api_key

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from vision_parse import VisionParser
import tempfile
import os

app = FastAPI()

# Allow CORS from any origin (you can restrict this if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the VisionParser
parser = VisionParser(
    model_name="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),  # store your key in an env variable
    temperature=0.7,
    top_p=0.4,
    image_mode="url",
    detailed_extraction=False,
    enable_concurrency=True,
)

@app.post("/parse-pdf/", dependencies=[Security(verify_api_key)])
async def parse_pdf(request: Request, file: UploadFile = File(...)):
    # Save the uploaded file to a temporary file

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_pdf_path = temp_file.name

    try:
        # Convert PDF to markdown using VisionParser
        markdown_pages = parser.convert_pdf(temp_pdf_path)
        return JSONResponse(content={"markdown_pages": markdown_pages})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        # Clean up the temporary file
        os.remove(temp_pdf_path)