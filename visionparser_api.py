from dotenv import load_dotenv
load_dotenv()

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

@app.post("/parse-pdf/")
async def parse_pdf(request: Request, file: UploadFile = File(...)):
    # Save the uploaded file to a temporary file
    print(request.headers['x-edge-auth'])
    print(os.getenv("EDGE_SECRET"))

    if (request.headers['x-edge-auth'] != os.getenv("EDGE_SECRET")):
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

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