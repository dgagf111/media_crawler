from .mysql import MySQL_Database

# 创建别名以保持向后兼容
Database = MySQL_Database

# 导出主要类
__all__ = ['MySQL_Database', 'Database']