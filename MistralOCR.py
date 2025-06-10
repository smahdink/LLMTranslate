from mistralai import Mistral
import sys
from pathlib import Path
from LLMTranslate import filenameFromPath


def ocrCall(path, mistral_client):
    uploaded_pdf = mistral_client.files.upload(
        file={
            "file_name": filenameFromPath(path),
            "content": open(path, "rb"),
        },
        purpose="ocr"
    )

    mistral_client.files.retrieve(file_id=uploaded_pdf.id)
    signed_url = mistral_client.files.get_signed_url(file_id=uploaded_pdf.id)

    ocr_response = mistral_client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )
    with open(filenameFromPath(path) + " ocred.md", "w") as file:
        for page in range(len(ocr_response.pages)):
            file.write(ocr_response.pages[page].markdown + "\n" + "---\n")
