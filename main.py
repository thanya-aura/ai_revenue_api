from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from agents import revenue_standard, revenue_intermediate, revenue_advanced
import pandas as pd
from io import BytesIO
from typing import Dict

app = FastAPI(
    title="Revenue Intelligence API",
    description="Multi-project Revenue AI Analysis with Standard, Intermediate, and Advanced Agents.",
    version="1.0",
    servers=[
        {"url": "https://ai-revenue-api.onrender.com"}
    ]
)

def read_excel_file(file: UploadFile) -> Dict[str, pd.DataFrame]:
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only .xls or .xlsx files are accepted")
    try:
        content = file.file.read()
        return pd.read_excel(BytesIO(content), sheet_name=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {e}")

@app.get("/")
async def health_check():
    return {"message": "🚀 Revenue Intelligence API is live. Visit /docs to test the endpoints."}

@app.post("/analyze/{agent_type}")
async def analyze(agent_type: str, file: UploadFile = File(...)):
    try:
        data = read_excel_file(file)
        print(f"📦 Uploaded file: {file.filename}")
        print(f"📊 Detected sheets: {list(data.keys())}")
        print(f"🧠 Agent requested: {agent_type}")

        if agent_type == "standard":
            if "Sheet1" not in data:
                raise HTTPException(status_code=400, detail="Sheet1 is required for the standard agent.")
            result = revenue_standard.process(data["Sheet1"])

        elif agent_type == "intermediate":
            result = revenue_intermediate.analyze_multi_project_revenue(data)

        elif agent_type == "advanced":
            result = revenue_advanced.analyze_revenue_advanced(data)

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid agent_type. Must be one of: standard, intermediate, advanced."
            )

        print("✅ Agent output generated successfully.")
        return JSONResponse(content=result)

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")