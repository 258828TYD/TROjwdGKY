# 代码生成时间: 2025-08-06 00:19:04
import os
from cryptography.fernet import Fernet
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
A simple Starlette application providing a REST API for password encryption and decryption."""


# Encryption key (should be a 32 url-safe base64-encoded bytes)
# This key is used to encrypt and decrypt the passwords.
# If you lose this key, all encrypted data will be lost.
# You can generate a new key using:
# Fernet.generate_key()
KEY = b'your_base64_encoded_32_bytes_key_here'

# Initialize Fernet with the provided key
cipher_suite = Fernet(KEY)

# API endpoint for encrypting passwords
def encrypt_password(request: 'Request') -> JSONResponse:
    """Encrypts the provided password and returns the encrypted password."""
    if 'password' not in request.query_params:
        return JSONResponse({'error': 'Password parameter is missing'}, status_code=400)
    password = request.query_params.get('password')
    # Encrypt the password
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    return JSONResponse({'encrypted_password': encrypted_password})

# API endpoint for decrypting passwords
def decrypt_password(request: 'Request') -> JSONResponse:
    """Decrypts the provided encrypted password and returns the original password."""
    if 'encrypted_password' not in request.query_params:
        return JSONResponse({'error': 'Encrypted password parameter is missing'}, status_code=400)
    encrypted_password = request.query_params.get('encrypted_password')
    try:
        # Decrypt the password
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        return JSONResponse({'decrypted_password': decrypted_password})
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

# Routes for the API
routes = [
    Route('/encrypt', encrypt_password, methods=['GET']),
    Route('/decrypt', decrypt_password, methods=['GET']),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

# Run the application if it's the main module
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)