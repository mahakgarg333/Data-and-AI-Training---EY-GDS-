from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from datetime import datetime
import os, logging, re

# ------------------ LOGGING CONFIG ------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("QnA-Bot")

# ------------------ ENV & API INIT ------------------
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not API_KEY:
    logger.error("Missing OpenRouter API key. Please set it in .env file.")
    raise ValueError("OPENROUTER_API_KEY not found!")

try:
    llm = ChatOpenAI(
        model="mistralai/mistral-7b-instruct",
        temperature=0.3,
        max_tokens=250,
        api_key=API_KEY,
        base_url=BASE_URL
    )
    logger.info("LLM model initialized successfully.")
except Exception as e:
    logger.exception("Failed to initialize model.")
    raise e

app = FastAPI(title="Enhanced QnA Bot")

# ------------------ HELPERS ------------------
def clean_text(text: str) -> str:
    if not text:
        return ""
    patterns = [
        r"<.*?>", r"\[/?INST\]", r"^\W+|\W+$", r"\s+"
    ]
    cleaned = text
    for p in patterns:
        cleaned = re.sub(p, " ", cleaned)
    return cleaned.strip()

def get_date():
    return datetime.now().strftime("%Y-%m-%d")

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def reverse_text(s: str):
    return s[::-1].strip()

def add_numbers(q: str) -> Optional[int]:
    nums = re.findall(r'\d+', q)
    if len(nums) >= 2:
        return sum(map(int, nums))
    return None

# ------------------ DATA MODEL ------------------
class Query(BaseModel):
    question: str

# ------------------ MAIN ENDPOINT ------------------
@app.post("/ask")
async def ask(query: Query):
    question = query.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    logger.info(f"User asked: {question}")

    try:
        # Handle built-in tools
        if "current date" in question.lower():
            answer = get_date()
        elif "current time" in question.lower():
            answer = get_time()
        elif "reverse" in question.lower():
            text = " ".join(question.split()[1:])
            answer = f"Reversed: {reverse_text(text)}"
        elif any(x in question.lower() for x in ["add", "sum", "plus"]):
            total = add_numbers(question)
            answer = f"The sum is {total}" if total else "Couldn't find valid numbers to add."
        else:
            llm_response = llm.invoke(question)
            answer = clean_text(llm_response.content)

        logger.info(f"Bot reply: {answer}")
        return {"answer": answer}

    except Exception as e:
        logger.exception("Processing error")
        raise HTTPException(status_code=500, detail=str(e))

#uvicorn qna_bot:app --reload
