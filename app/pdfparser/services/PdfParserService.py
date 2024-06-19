from fastapi import UploadFile
import tempfile
import textract

class PdfParserService:
    def __init__(self) -> None:
        pass

    def echoContent(self, file: UploadFile):
        try:
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                temp.write(file.file.read())
                temp.flush()
                context = textract.process(temp.name,encoding='utf-8',extension=".pdf")
                return context            
        except Exception as e:
            return f"Erro ao processar o PDF: {e}"

pdfParserService= PdfParserService()

