# 代码生成时间: 2025-08-14 08:10:11
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from typing import List, Dict

# 确保已经安装nltk和下载相关数据包（nltk.download('punkt'), nltk.download('stopwords')）

class TextFileAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def tokenize(self, text: str) -> List[str]:
        """将文本分词"""
        words = word_tokenize(text)
        return [word.lower() for word in words if word.isalpha()]

    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        """移除停用词"""
        return [word for word in tokens if word not in self.stop_words]

    def lemmatize(self, tokens: List[str]) -> List[str]:
        """词形还原"""
        return [self.lemmatizer.lemmatize(word) for word in tokens]

    def analyze(self) -> Dict[str, int]:
        """分析文本文件内容"""
        try:
            with open(self.file_path, 'r') as file:
                text = file.read()
            tokens = self.tokenize(text)
            tokens = self.remove_stop_words(tokens)
            tokens = self.lemmatize(tokens)
            return dict.fromkeys(tokens, 0)
        except FileNotFoundError:
            raise StarletteHTTPException(status_code=404, detail="File not found")
        except Exception as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))

# Starlette 应用
app = Starlette(debug=True)

@app.route("/analyze", methods=["POST"])
async def analyze_text(request):
    "