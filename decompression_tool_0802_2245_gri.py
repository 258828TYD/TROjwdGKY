# 代码生成时间: 2025-08-02 22:45:18
import shutil
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.requests import Request
import zipfile
import tarfile
import gzip
import io

class DecompressionTool:
    """A class for handling file decompression."""
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def decompress_zip(self, file_stream):
        """Decompress a ZIP file to the output folder."""
        with zipfile.ZipFile(file_stream, 'r') as zip_ref:
            zip_ref.extractall(self.output_folder)

    def decompress_tar(self, file_stream):
        """Decompress a TAR file to the output folder."""
        with tarfile.TarFile(file_stream, 'r') as tar_ref:
            tar_ref.extractall(self.output_folder)

    def decompress_gz(self, file_stream):
        """Decompress a GZIP file to the output folder."""
        with gzip.GzipFile(file_stream, 'rb') as gzip_ref:
            decompressed_data = gzip_ref.read()
            with open(self.output_folder + os.path.basename(file_stream.name), 'wb') as out_file:
                out_file.write(decompressed_data)

    def decompress(self, file_stream):
        """Decompress the file based on its extension."""
        try:
            if file_stream.name.endswith('.zip'):
                return self.decompress_zip(file_stream)
            elif file_stream.name.endswith(('.tar', '.tar.gz', '.tgz')):
                return self.decompress_tar(file_stream)
            elif file_stream.name.endswith('.gz'):
                return self.decompress_gz(file_stream)
            else:
                raise ValueError('Unsupported file type.')
        except Exception as e:
            return str(e)

async def decompress_file(request: Request):
    """An endpoint to handle file decompression."""
    file = await request.form()
    file_stream = file.get('file')
    if file_stream is None:
        return Response('No file received', status_code=400)

    decompress_tool = DecompressionTool(request.app.state.output_folder)
    response_content = decompress_tool.decompress(file_stream.file)
    if isinstance(response_content, str):
        return Response(response_content, status_code=500)  # Handle error
    return Response('File decompressed successfully.', status_code=200)

def create_decompression_app(output_folder):
    """Create a Starlette app for file decompression."""
    app = Starlette(debug=True)
    app.state.output_folder = output_folder
    app.add_route('/decompress', decompress_file, methods=['POST'])
    return app

# Example usage:
if __name__ == '__main__':
    output_folder = 'decompressed_files'  # Specify the output folder
    app = create_decompression_app(output_folder)
    app.run()  # Start the server