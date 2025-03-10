from fastapi import UploadFile
import os
import tempfile
import fitz
from app.AIModel.AIModel import aiModel
from app.AIModel.domain.classmap import classes, levels
from app.pdfparser.controllers.typings.ClassifyOutput import ClassifyOutput
import logging

logger = logging.getLogger(__name__)

class PdfParserService:
    def __init__(self) -> None:
        pass

    def echoContent(self, file: UploadFile) -> str | int:
        try:
            fd, temp_path = tempfile.mkstemp(suffix=".pdf")
            with os.fdopen(fd, "wb") as temp_file:
                temp_file.write(file.file.read())

            text = ""
            with fitz.open(temp_path) as doc:
                for page in doc:
                    text += page.get_text("text")

            os.remove(temp_path)
            return text
        except Exception as e:
            logger.error(f'Erro ao processar o PDF: {e}')
            return -1

    def classifyCv(self, file: UploadFile) -> ClassifyOutput | None:
        text = self.echoContent(file)

        if isinstance(text, int):
            return None

        cvv_class_data = aiModel.parseCvvClass(text)
        cvv_level_data = aiModel.parseCvvLevel(text)

        result = ClassifyOutput(**{
            "cv_class": classes[cvv_class_data.cv_class],
            "cv_class_prob": cvv_class_data.cv_prob,
            "cv_level": levels[cvv_level_data.cvv_level],
            "cv_level_prob": cvv_level_data.cvv_level_prob
        })

        return result

pdfParserService = PdfParserService()
