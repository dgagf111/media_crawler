"""
功能: 事务管理器
描述: 数据库事务管理和SQL操作封装

TransactionManager 类提供了以下主要功能:
1. 事务控制: 使用上下文管理器确保事务的正确提交或回滚
2. CRUD操作: 封装了增删改查等基本数据库操作
3. 批量操作: 支持批量添加、更新和删除
4. 参数化查询: 提供安全的参数化查询方法，防止SQL注入

使用示例:

1. 基本CRUD操作:
session = Session()
with TransactionManager(session) as tm:
    # 插入数据
    user = User(name='Alice', age=30)
    tm.add(user)
    
    # 查询数据
    users = tm.query(User).all()
    
    # 更新数据
    user = tm.query(User).filter_by(name='Alice').first()
    tm.update(user, {'age': 31})
    
    # 删除数据
    tm.delete(user)

2. 批量操作:
with TransactionManager(session) as tm:
    # 批量添加
    users = [User(name='Charlie', age=35), User(name='David', age=40)]
    tm.add_all(users)
    
    # 批量更新
    tm.bulk_update(User, {"age": 30}, User.age < 30)
    
    # 批量删除
    tm.bulk_delete(User, User.age > 50)

3. 参数化查询（防SQL注入）:
with TransactionManager(session) as tm:
    query = "SELECT * FROM users WHERE username = :username AND age > :age"
    params = {"username": user_input, "age": 18}
    result = tm.execute_parameterized_query(query, params)
    for row in result:
        print(row)

注意:
- 使用 with 语句确保事务的正确处理
- 对于直接的SQL操作，优先使用 execute_parameterized_query 方法以防止SQL注入
- 批量操作可以显著提高大量数据处理的效率
"""

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import text
from sqlalchemy import text

class TransactionManager:
    def __init__(self, session):
        self.session = session
        self.affected_rows = 0
        self._transaction = None

    def __enter__(self):
        if not self.session.in_transaction():
            self._transaction = self.session.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self._transaction:
                self._transaction.rollback()
        else:
            if self._transaction:
                self._transaction.commit()
        self._transaction = None

    def add(self, instance):
        """向会话中添加单个实例"""
        self.session.add(instance)
        self.session.flush()  # 刷新会话以获取新插入记录的ID
        self.affected_rows = 1
        return self.affected_rows

    def add_all(self, instances):
        """向会话中添加多个实例"""
        self.session.add_all(instances)
        self.session.flush()  # 刷新会话以获取新插入记录的ID
        self.affected_rows = len(instances)
        return self.affected_rows

    def query(self, *entities):
        """创建查询"""
        return self.session.query(*entities)

    def delete(self, instance):
        """从会话中删除个实例"""
        if instance not in self.session:
            raise ValueError("Instance is not in the session")
        self.session.delete(instance)
        self.affected_rows = 1
        return self.affected_rows

    def update(self, instance, values):
        """更新单个实例"""
        if instance not in self.session:
            raise NoResultFound("Instance not found in the database")
        for key, value in values.items():
            setattr(instance, key, value)
        self.affected_rows = 1
        return self.affected_rows

    def bulk_update(self, model, values, condition=None):
        """批量更新多个实例"""
        query = self.session.query(model)
        if condition is not None:
            query = query.filter(condition)
        self.affected_rows = query.update(values, synchronize_session='fetch')
        return self.affected_rows

    def bulk_delete(self, model, condition=None):
        """批量删除多个实例"""
        query = self.session.query(model)
        if condition is not None:
            query = query.filter(condition)
        self.affected_rows = query.delete(synchronize_session='fetch')
        return self.affected_rows

    def get_affected_rows(self):
        """获取受影响的行数"""
        return self.affected_rows

    def execute_parameterized_query(self, query, params=None):
        """
        执行参数化查询以防止SQL注入
        :param query: SQL查询字符串，使用:param形式的参数占位符
        :param params: 包含参数值的字典
        :return: 查询结果
        """
        try:
            result = self.session.execute(text(query), params or {})
            return result
        except Exception as e:
            logger.error(f"执行参数化查询时出错: {e}")
            raise