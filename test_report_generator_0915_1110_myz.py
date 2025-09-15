# 代码生成时间: 2025-09-15 11:10:36
# test_report_generator.py

"""
A Test Report Generator using the Starlette framework.
"""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import json
import datetime
import uuid

class TestReportGenerator:
    """
    A class responsible for generating test reports.
    """
    def __init__(self):
        self.reports = {}

    def generate_report(self, test_name, results):
        """
        Generate a test report with a unique ID and given results.
        :param test_name: The name of the test.
        :param results: A dictionary of test results.
        :return: A report ID and the report data.
        """
        report_id = str(uuid.uuid4())
        report_data = {
            'id': report_id,
            'test_name': test_name,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'results': results
        }
        self.reports[report_id] = report_data
        return report_id, report_data

    def get_report(self, report_id):
        """
        Retrieve a test report by its ID.
        :param report_id: The unique ID of the report.
        :return: The report data if found, otherwise None.
        """
        return self.reports.get(report_id)

app = Starlette(debug=True, routes=[
    Route("/generate", endpoint=lambda request: generate_report_view(request)),
    Route("/reports/{report_id}", endpoint=lambda request: get_report_view(request))
])

async def generate_report_view(request: Request):
    """
    An endpoint to generate a test report.
    """
    try:
        test_name = request.query_params.get("test_name")
        results = await request.json()
        test_report_generator = TestReportGenerator()
        report_id, report_data = test_report_generator.generate_report(test_name, results)
        return JSONResponse(content=report_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

async def get_report_view(request: Request):
    """
    An endpoint to retrieve a test report by ID.
    """
    try:
        report_id = request.path_params.get("report_id")
        test_report_generator = TestReportGenerator()
        report_data = test_report_generator.get_report(report_id)
        if report_data:
            return JSONResponse(content=report_data)
        else:
            return JSONResponse(content={"error": "Report not found."}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
