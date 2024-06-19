from fastapi import FastAPI
from app.pdfparser.controllers.PdfParserController import router

app= FastAPI()
app.include_router(router)