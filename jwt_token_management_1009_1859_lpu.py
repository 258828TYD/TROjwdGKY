# 代码生成时间: 2025-10-09 18:59:52
import jwt
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR

# Secret key for JWT
SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'

# Function to create a new JWT token
def create_access_token(data: dict, expires_delta=None):
    """
    Create a new JWT token.

    :param data: The payload of the JWT token.
    :param expires_delta: The expiration time for the token.
    :return: A JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.timedelta(seconds=expires_delta)
        to_encode.update({"exp": datetime.datetime.utcnow() + expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to decode a JWT token
def decode_token(token):
    """
    Decode a JWT token and return the payload.

    :param token: The JWT token to decode.
    :return: The decoded payload.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

# Function to verify the token and return the user if valid
def verify_token(request: Request):
    """
    Verify the JWT token in the request headers and return the user if valid.

    :param request: The incoming request.
    :return: A JSON response with the user data if the token is valid, otherwise a 401 error.
    """
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse(
            content={"detail": "No token provided."}, status_code=HTTP_401_UNAUTHORIZED
        )
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            content={"detail": "Token expired."}, status_code=HTTP_401_UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            content={"detail": "Invalid token."}, status_code=HTTP_401_UNAUTHORIZED
        )
    return JSONResponse(content=payload)

# Example route to demonstrate token verification
async def token_route(request: Request):
    """
    A route that requires a valid JWT token to access.

    :param request: The incoming request.
    :return: A response with the user data if the token is valid, otherwise a 401 error.
    """
    try:
        response = verify_token(request)
        return response
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

# Example route to create a new JWT token
async def create_token_route(request: Request):
    """
    A route to create a new JWT token.

    :param request: The incoming request.
    :return: A response with the new JWT token.
    """
    try:
        data = await request.json()
        token = create_access_token(data)
        return JSONResponse(content={"token": token})
    except Exception as e:
        return JSONResponse(
            content={"detail": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

# Example Starlette application
app = Starlette()
app.add_route("/token", token_route)
app.add_route("/create-token", create_token_route)

# Run the application using the following command:
# uvicorn jwt_token_management:app --reload