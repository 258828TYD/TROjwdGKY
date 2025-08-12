# 代码生成时间: 2025-08-12 19:55:04
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import plotly.graph_objects as go

# Initialize templates environment
templates = Jinja2Templates(directory="templates")

# Define the routes
routes = [
    Route("/", endpoint=home, methods=["GET"]),
    Route("/chart", endpoint=create_chart, methods=["POST"]),
    Mount("/static", app=StaticFiles(directory="static")),
]

# Create a Starlette application
app = Starlette(debug=True, routes=routes)

# Root route for the web application
async def home(request):
    # Render the home template
    return templates.TemplateResponse("index.html", {"request": request})

# Route to handle chart creation
async def create_chart(request):
    try:
        # Get data from the request form
        data = await request.form()
        x = data.get("x")
        y = data.get("y")
        type = data.get("type")
        
        # Check if all required data is provided
        if not all([x, y, type]):
            return JSONResponse(
                content={"error": "Missing data. Please provide x, y, and type."},
                status_code=400
            )
        
        # Create a chart based on the type
        if type == "line":
            chart = go.Figure(data=[go.Scatter(x=x, y=y)])
        elif type == "bar":
            chart = go.Figure(data=[go.Bar(x=x, y=y)])
        else:
            return JSONResponse(
                content={"error": "Unsupported chart type."},
                status_code=400
            )
        
        # Generate the chart image and return it
        image = chart.to_image(format="PNG")
        return Response(image, media_type="image/png")
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# Run the application using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Template for the index page
# templates/index.html
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Interactive Chart Generator</title>
#         <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
#     </head>
#     <body>
#         <h1>Interactive Chart Generator</h1>
#         <form action="/chart" method="post" enctype="multipart/form-data">
#             <label for="x">X-axis data (CSV):</label>
#             <input type="text" id="x" name="x" required>
#             <label for="y">Y-axis data (CSV):</label>
#             <input type="text" id="y" name="y" required>
#             <label for="type">Chart type:</label>
#             <select id="type" name="type" required>
#                 <option value="line">Line Chart</option>
#                 <option value="bar">Bar Chart</option>
#             </select>
#             <button type="submit">Generate Chart</button>
#         </form>
#     </body>
# </html>
