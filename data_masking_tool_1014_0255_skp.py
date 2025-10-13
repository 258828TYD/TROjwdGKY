# 代码生成时间: 2025-10-14 02:55:24
import re
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 数据脱敏工具类
class DataMaskingTool:
    def __init__(self):
        # 可以根据需要配置更多的脱敏规则
        self.rules = {
            'phone': self.mask_phone,
            'email': self.mask_email,
            'id_card': self.mask_id_card
        }

    def mask(self, data):
        """
        主脱敏函数，根据数据类型进行脱敏
        :param data: 待脱敏的数据
        :return: 脱敏后的数据
        """
        for key, value in data.items():
            if key in self.rules:
                data[key] = self.rules[key](value)
        return data

    def mask_phone(self, phone):
        """
        电话脱敏
        :param phone: 原始电话号码
        :return: 脱敏后的电话号码
        """
        return re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', phone)

    def mask_email(self, email):
        """
        邮箱脱敏
        :param email: 原始邮箱地址
        :return: 脱敏后的邮箱地址
        """
        local_part, domain = email.split('@')
        return local_part[0] + '*'*(len(local_part)-1) + '@' + domain

    def mask_id_card(self, id_card):
        """
        身份证脱敏
        :param id_card: 原始身份证号码
        :return: 脱敏后的身份证号码
        """
        return re.sub(r'(\d{6})\d{8}(\d{4})', r'\1*****\2', id_card)

# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
routes = [
    Route('/', DataMaskingEndpoint()),
]

# 添加路由到Starlette应用
app.add_routes(routes)

# 数据脱敏端点类
class DataMaskingEndpoint:
    def __init__(self, request):
        self.request = request
        self.masking_tool = DataMaskingTool()

    async def __call__(self, request):
        """
        处理请求并返回脱敏后的数据
        :param request: 请求对象
        :return: 脱敏后的数据
        """
        try:
            data = await request.json()
            masked_data = self.masking_tool.mask(data)
            return JSONResponse(masked_data)
        except Exception as e:
            # 错误处理
            return JSONResponse({'error': str(e)}, status_code=500)
