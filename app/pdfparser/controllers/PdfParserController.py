from typing import Annotated
from fastapi import APIRouter, UploadFile, File
from app.pdfparser.services.PdfParserService import pdfParserService

router= APIRouter()

class PdfParserController:
    def __init__(self) -> None:
        pass

    @router.post('/')
    def parse(file: UploadFile):
        print(f'receiving the file {file.filename} ...')
        print('returning file content')
        return pdfParserService.echoContent(file)

pdfParseController= PdfParserController()

