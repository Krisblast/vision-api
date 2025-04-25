Vision API - Local Document Parsing Service

This project wraps the vision-parse package with a simple FastAPI service that allows you to extract structured Markdown content from PDFs using OpenAI's gpt-4o vision model.

🧰 Requirements

Python 3.9+

Poetry OR pip

OpenAI API key (for GPT-4o)

🚀 Quickstart

1. Clone the Repo

git clone https://github.com/your-org/vision-api
cd vision-api

2. Set Up Your Environment

Option A: Using Poetry (recommended)

poetry install

Option B: Using pip

pip install -r requirements.txt

If requirements.txt is missing, manually install:

pip install fastapi uvicorn python-multipart vision-parse openai python-dotenv

3. Add .env file

Create a .env file in the root of the project:

OPENAI_API_KEY=sk-...
EDGE_SECRET=supersecurekey

4. Start the API Server

uvicorn visionparser_api:app --host 0.0.0.0 --port 8000 --reload

5. Test It

Visit Swagger docs:

http://localhost:8000/docs

Upload a PDF via the /parse-pdf/ endpoint.

🔐 Security

To restrict access to the API, requests must include a header:

x-edge-auth: supersecurekey

This key must match EDGE_SECRET in your .env.

📦 Project Structure

vision-api/
├── visionparser_api.py     # Main FastAPI app
├── .env                    # API keys and secrets
├── requirements.txt        # (Optional) pip dependencies
└── README.md               # You're reading it!

✨ Notes

The service uses gpt-4o with image_mode="url" to analyze PDF pages.

Input must be PDF files (other formats not supported yet).

Output is an array of Markdown strings (one per page).

🛠️ TODO

Add support for returning raw JSON field extraction

Optional LLM selector (Gemini, Azure OpenAI)

Dockerfile for containerization