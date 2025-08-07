# 代码生成时间: 2025-08-07 16:26:50
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Request, Response
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware, AuthenticationBackend, AuthCredentials, SimpleUser
import uvicorn
from jose import JWTError, jwt
from typing import Optional
import datetime

# 配置JWT密钥和过期时间
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        # 提取JWT令牌
        auth = request.headers.get("Authorization")
        if auth is None:
            return None
        # 令牌需要以Bearer开头
        prefix, token = auth.split()
        if not auth.startswith("Bearer"):
            return None
        credentials = AuthCredentials(['authenticated'])
        try:
            # 验证JWT令牌
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            if user_id is None:
                return None
            # 可以扩展用户验证逻辑，例如查询数据库验证用户
            # user = user_db.get(user_id)
            return SimpleUser(user_id), credentials
        except JWTError:
            return None

# 用户登录表单数据验证
def validate_login_form(form):
    if not form['username'] or not form['password']:
        raise ValueError("Username and password are required")

# 登录逻辑
async def login(request: Request):
    form = await request.json()
    try:
        validate_login_form(form)
    except ValueError as e:
        return JSONResponse({'detail': str(e)}, status_code=HTTP_400_BAD_REQUEST)
    # 这里应该是数据库校验逻辑
    # if not authenticate(form['username'], form['password']):
    #     return JSONResponse({'detail': 'Incorrect username or password'}, status_code=HTTP_401_UNAUTHORIZED)
    # 生成JWT令牌
    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {'exp': expires, 'user_id': 1}  # 假设的用户ID
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return JSONResponse({'token': token}, status_code=HTTP_200_OK)

# 创建Starlette应用并添加路由和中间件
app = Starlette(
    middleware=[
        Middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())
    ],
    routes=[
        Route("/login", login, methods=["POST"]),
    ]
)

# 启动服务
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
