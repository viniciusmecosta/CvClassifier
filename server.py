from dotenv import load_dotenv
from fastapi import FastAPI
from app.pdfparser.controllers.PdfParserController import router
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app= FastAPI()
app.include_router(router)