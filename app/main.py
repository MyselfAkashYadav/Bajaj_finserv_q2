from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.extractor import extract_lab_tests
from models.schemas import LabTestResponse
from fastapi.responses import JSONResponse
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title="Lab Test Extraction API",
    docs_url=None, 
    redoc_url=None
)

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_path)

@app.get("/")
async def root():
    return {"message": "Lab Test Extraction API is running"}

@app.get("/get-lab-tests", response_class=HTMLResponse)
async def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/get-lab-tests", response_model=LabTestResponse)
async def get_lab_tests(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
        
    try:
    
        contents = await file.read()
    
        logger.info(f"Processing image: {file.filename}")
        result = extract_lab_tests(contents)
        return LabTestResponse(is_success=True, data=result)
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return JSONResponse(
            content={"is_success": False, "error": str(e)}, 
            status_code=500
        )