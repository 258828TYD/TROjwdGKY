# 代码生成时间: 2025-08-12 08:07:48
import asyncio
from starlette.config import Config
from sqlalchemy import create_engine, pool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session

# 配置文件
config = Config('.env')

# 数据库连接池管理类
class DatabasePoolManager:
    def __init__(self):
        # 初始化数据库连接池
        self.engine = self.create_engine()
        self.session_factory = self.create_session_factory()
        self.session: Session = self.session_factory()

    def create_engine(self) -> engine:
        """创建数据库引擎"""
        url = config("DATABASE_URL")
        engine = create_engine(url, echo=config("SQLALCHEMY_ECHO", cast=bool), pool_size=config("SQLALCHEMY_POOL_SIZE", cast=int), max_overflow=config("SQLALCHEMY_MAX_OVERFLOW", cast=int))
        return engine

    def create_session_factory(self):
        """创建会话工厂"""
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return SessionLocal

    def get_session(self) -> Session:
        """获取会话"""
        try:
            session = self.session_factory()
            return session
        except SQLAlchemyError as e:
            raise RuntimeError(f"Failed to create session: {e}")

    async def close_session(self):
        """关闭会话"""
        await self.session.close()
        self.session = self.session_factory()

# 异步上下文管理器
class AsyncSessionScope:
    def __init__(self, db: DatabasePoolManager):
        self.db = db

    async def __aenter__(self):
        self.session = self.db.get_session()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        if exc_type:
            # 如果有异常，回滚事务
            await self.session.rollback()
        else:
            # 如果没有异常，提交事务
            await self.session.commit()

# 使用示例
async def main():
    db = DatabasePoolManager()
    async with AsyncSessionScope(db) as session:
        # 使用session执行数据库操作
        pass

# 运行主函数
if __name__ == '__main__':
    asyncio.run(main())