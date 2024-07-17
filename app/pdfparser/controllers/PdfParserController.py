from fastapi import APIRouter, UploadFile
from app.pdfparser.services.PdfParserService import pdfParserService
from app.pdfparser.controllers.typings.ClassifyOutput import ClassifyOutput
import logging
logger= logging.getLogger(__name__)
router= APIRouter()

class PdfParserController:
    def __init__(self) -> None:
        pass

    @router.post('/')
    def classify(file: UploadFile) -> ClassifyOutput:
        logger.info('Received file')
        cvvClassification= pdfParserService.classifyCv(file)
        
        result= ClassifyOutput(**{
            "cv_class": cvvClassification.cv_class,
            "cv_class_prob": cvvClassification.cv_class_prob,
            "cv_level": cvvClassification.cv_level,
            "cv_level_prob": cvvClassification.cv_level_prob,
        })

        logger.info('Returning data')
        return result

pdfParseController= PdfParserController()

