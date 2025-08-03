# 代码生成时间: 2025-08-03 22:05:24
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
import logging

# 设置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentConverterService:
    """
    文档格式转换器服务类
    """
    def __init__(self):
        pass

    def convert_to_pdf(self, docx_file: UploadFile):
        try:
            # 将DOCX文件保存到临时路径
            with open('temp.docx', 'wb') as buffer:
                shutil.copyfileobj(docx_file.file, buffer)

            # 使用python-docx库将DOCX转换为PDF
            document = Document('temp.docx')
            for paragraph in document.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # 保存转换后的PDF文件
            document.save('temp.pdf')
            return FileResponse('temp.pdf', media_type='application/pdf')
        except Exception as e:
            logger.error(f"转换失败: {e}")
            raise StarletteHTTPException(status_code=500, detail="转换失败")
        finally:
            # 清理临时文件
            if os.path.exists('temp.docx'):
                os.remove('temp.docx')
            if os.path.exists('temp.pdf'):
                os.remove('temp.pdf')

# 创建Starlette应用
app = Starlette(debug=True)

# 添加路由
app.add_route('/upload', DocumentConverterService().convert_to_pdf, methods=['POST'])
