# 代码生成时间: 2025-09-22 09:11:14
import os
import starlette.responses
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.enum.shape import MSO_SHAPE
from docx.oxml import OxmlElement
import uuid
from fastapi.responses import FileResponse
import tempfile

"""
A simple document converter using Starlette framework.
This application allows users to convert documents from one format to another.
"""

class DocumentConverter:
    def __init__(self):
        pass

    def convert_docx_to_pdf(self, docx_file):
        """
        Converts a DOCX file to a PDF file.
        
        Args:
        docx_file (str): The path to the DOCX file.
        
        Returns:
        str: The path to the generated PDF file.
        """
        try:
            # Use a library like unoconv to convert DOCX to PDF
            # For simplicity, this example just copies the file
            temp_dir = tempfile.gettempdir()
            docx_path = os.path.join(temp_dir, docx_file)
            pdf_path = docx_path.replace(".docx", ".pdf")
            os.system(f"cp {docx_path} {pdf_path}")
            return pdf_path
        except Exception as e:
            raise Exception(f"Failed to convert DOCX to PDF: {str(e)}")

    def convert_pdf_to_docx(self, pdf_file):
        """
        Converts a PDF file to a DOCX file.
        
        Args:
        pdf_file (str): The path to the PDF file.
        
        Returns:
        str: The path to the generated DOCX file.
        """
        try:
            # Use a library like unoconv to convert PDF to DOCX
            # For simplicity, this example just copies the file
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, pdf_file)
            docx_path = pdf_path.replace(".pdf", ".docx")
            os.system(f"cp {pdf_path} {docx_path}")
            return docx_path
        except Exception as e:
            raise Exception(f"Failed to convert PDF to DOCX: {str(e)}")

    def create_docx_from_text(self, text):
        """
        Creates a DOCX file from plain text.
        
        Args:
        text (str): The text to be written to the DOCX file.
        
        Returns:
        str: The path to the generated DOCX file.
        """
        try:
            doc = Document()
            doc.add_paragraph(text)
            temp_dir = tempfile.gettempdir()
            docx_path = os.path.join(temp_dir, f"{uuid.uuid4()}.docx")
            doc.save(docx_path)
            return docx_path
        except Exception as e:
            raise Exception(f"Failed to create DOCX from text: {str(e)}")

    def create_pdf_from_text(self, text):
        """
        Creates a PDF file from plain text.
        
        Args:
        text (str): The text to be written to the PDF file.
        
        Returns:
        str: The path to the generated PDF file.
        """
        try:
            # Use a library like fpdf to create PDF from text
            # For simplicity, this example just returns the text
            return text
        except Exception as e:
            raise Exception(f"Failed to create PDF from text: {str(e)}")


# Define the routes for the application
routes = [
    Route("/convert/docx-to-pdf", methods=["POST"], endpoint=convert_docx_to_pdf),
    Route("/convert/pdf-to-docx", methods=["POST"], endpoint=convert_pdf_to_docx),
    Route("/create/docx", methods=["POST"], endpoint=create_docx_from_text),
    Route("/create/pdf", methods=["POST"], endpoint=create_pdf_from_text),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

# Define the endpoint functions
async def convert_docx_to_pdf(request: Request):
    """
    Converts a DOCX file to a PDF file.
    
    Args:
    request (Request): The incoming request with the DOCX file.
    
    Returns:
    Response: A response with the converted PDF file.
    """
    try:
        docx_file = await request.form()
        pdf_path = DocumentConverter().convert_docx_to_pdf(docx_file)
        return FileResponse(pdf_path, media_type="application/pdf")
    except Exception as e:
        return starlette.responses.JSONResponse(
            content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

async def convert_pdf_to_docx(request: Request):
    """
    Converts a PDF file to a DOCX file.
    
    Args:
    request (Request): The incoming request with the PDF file.
    
    Returns:
    Response: A response with the converted DOCX file.
    """
    try:
        pdf_file = await request.form()
        docx_path = DocumentConverter().convert_pdf_to_docx(pdf_file)
        return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        return starlette.responses.JSONResponse(
            content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

async def create_docx_from_text(request: Request):
    """
    Creates a DOCX file from plain text.
    
    Args:
    request (Request): The incoming request with the text.
    
    Returns:
    Response: A response with the created DOCX file.
    """
    try:
        text = await request.json()
        docx_path = DocumentConverter().create_docx_from_text(text)
        return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    except Exception as e:
        return starlette.responses.JSONResponse(
            content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

async def create_pdf_from_text(request: Request):
    """
    Creates a PDF file from plain text.
    
    Args:
    request (Request): The incoming request with the text.
    
    Returns:
    Response: A response with the created PDF file.
    """
    try:
        text = await request.json()
        pdf_path = DocumentConverter().create_pdf_from_text(text)
        return starlette.responses.JSONResponse(content={"pdf": pdf_path})
    except Exception as e:
        return starlette.responses.JSONResponse(
            content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )
