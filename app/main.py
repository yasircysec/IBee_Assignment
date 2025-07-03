import os
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Query, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from . import models, database
from .utils import validate_csv_and_extract_data
import pandas as pd
import logging
import io
import secrets
from openai import OpenAI

# Setup logging
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI app with metadata
app = FastAPI(
    title="CSV Upload & Query API",
    description="Upload, validate, store, and search CSV data with logging and AI assistant.",
    version="1.1.0",
    contact={"name": "Yasir A", "email": "yasircysec@gmail.com"},
    docs_url="/docs",
    redoc_url=None
)

# Basic HTTP auth setup
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

# Log all incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url.path} | Query: {request.url.query}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

# Root check with authentication
@app.get("/")
def root(user: str = Depends(authenticate)):
    return {"message": f"Welcome {user}, CSV API is up and running!"}

# Upload and validate CSV
@app.post("/upload")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(database.get_db), user: str = Depends(authenticate)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    try:
        contents = file.file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(contents))
        cleaned_data = validate_csv_and_extract_data(df)

        for item in cleaned_data:
            record = models.Record(**item)
            db.add(record)
        db.commit()

        return {"message": f"Uploaded {len(cleaned_data)} records successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fetch all records
@app.get("/records")
def get_all_records(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), user: str = Depends(authenticate)):
    records = db.query(models.Record).offset(skip).limit(limit).all()
    return records

# Search records by filters
@app.get("/records/search")
def search_records(
    min_age: int = Query(None),
    max_age: int = Query(None),
    name: str = Query(None),
    db: Session = Depends(database.get_db),
    user: str = Depends(authenticate)
):
    query = db.query(models.Record)
    if min_age is not None:
        query = query.filter(models.Record.age >= min_age)
    if max_age is not None:
        query = query.filter(models.Record.age <= max_age)
    if name is not None:
        query = query.filter(models.Record.name.ilike(f"%{name}%"))

    return query.all()

# Ask AI about uploaded data
@app.post("/ask-ai")
def ask_ai(question: str, db: Session = Depends(database.get_db), user: str = Depends(authenticate)):
    records = db.query(models.Record).all()
    if not records:
        raise HTTPException(status_code=404, detail="No data available to answer questions.")

    df = pd.DataFrame([r.__dict__ for r in records])
    df.drop(columns=["_sa_instance_state"], inplace=True)

    prompt = f"""
    You are a data assistant. Answer the following question based on this CSV data:

    {df.to_csv(index=False)}

    Question: {question}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful CSV data assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))