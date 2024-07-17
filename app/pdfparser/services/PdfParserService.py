from fastapi import UploadFile
import tempfile
import textract
from app.AIModel.AIModel import aiModel
from app.AIModel.domain.classmap import classes
from app.AIModel.domain.classmap import levels
from app.pdfparser.controllers.typings.ClassifyOutput import ClassifyOutput
import logging

logger= logging.getLogger(__name__)

class PdfParserService:
    def __init__(self) -> None:
        pass

    def echoContent(self, file: UploadFile) -> str | int:
        try:
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                temp.write(file.file.read())
                temp.flush()
                context = textract.process(temp.name,encoding='utf-8',extension=".pdf")
                return str(context)           
        except Exception as e:
            logger.error(f'Erro ao processar o PDF: {e}')
            return -1
    
    def classifyCv(self, file: UploadFile) -> ClassifyOutput:
        text= self.echoContent(file)
        
        if type(text) is int:
            return None
        
        cvv_class_data= aiModel.parseCvvClass(text)
        cvv_level_data= aiModel.parseCvvLevel(text)

        result = ClassifyOutput(**{
            "cv_class": classes[cvv_class_data.cv_class],
            "cv_class_prob": cvv_class_data.cv_prob,
            "cv_level": levels[cvv_level_data.cvv_level],
            "cv_level_prob": cvv_level_data.cvv_level_prob            
        })

        return result

pdfParserService= PdfParserService()

