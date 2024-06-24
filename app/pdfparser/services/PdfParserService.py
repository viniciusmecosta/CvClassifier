from fastapi import UploadFile
import tempfile
import textract
from app.AIModel.AIModel import aiModel
from app.AIModel.domain.classmap import classes
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
    
    def classifyCv(self, file: UploadFile) -> str:
        text= self.echoContent(file)
        if type(text) is int:
            return None
        
        classification= aiModel.parseCvv(text)
        return classes[classification]

pdfParserService= PdfParserService()

