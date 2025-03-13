from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

# Azure ML Endpoint details
AZURE_ML_URL = "https://ensono.westeurope.inference.ml.azure.com/score"  # Update this
API_KEY = "7Eq9c1wwzQTkdcAw1cyhTac5JxQCYwNup9ywt1KWfg4kpWOeDXTwJQQJ99BCAAAAAAAAAAAAINFRAZML3317"  # Replace with your actual API key

@app.post("/ask")
async def ask_question(request_data: dict):
    try:
        question = request_data.get("question", "")
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")

        data = {"question": question}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json",
        }

        response = requests.post(AZURE_ML_URL, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {"answer": response.json()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

