from fastapi import FastAPI
from app.pdfparser.controllers.PdfParserController import router
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app= FastAPI()
app.include_router(router)