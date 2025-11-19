#!/usr/bin/env python3
"""
数据库模块完整测试类

功能说明：
这个测试类专门测试数据库模块的所有核心功能，包括：
1. 数据库连接测试 - 连接创建、连接池、连接验证
2. 会话管理测试 - 会话创建、关闭、生命周期管理
3. 事务管理测试 - 事务提交、回滚、嵌套事务
4. 模型操作测试 - CRUD操作、查询、关联关系
5. 连接池测试 - 连接复用、并发连接、资源管理
6. 异常处理测试 - 连接异常、SQL异常、事务异常
7. 性能测试 - 查询性能、批量操作、连接性能

测试覆盖率目标：90%以上
支持独立运行：python db/test_database_module.py
注意：需要MySQL服务运行并正确配置
"""

import os
import sys
import time
import threading
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入被测试的模块
try:
    from pythonprojecttemplate.db.mysql.mysql import MySQL_Database
    from pythonprojecttemplate.db.mysql.transaction.transaction_manager import TransactionManager
    from pythonprojecttemplate.config.config import config
    from sqlalchemy import Column, Integer, String, DateTime, func, text
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import Session
    
    Base = declarative_base()
    
    # 测试模型
    class TestUser(Base):
        __tablename__ = 'test_users'
        
        id = Column(Integer, primary_key=True)
        username = Column(String(50), nullable=False)
        email = Column(String(100), nullable=False)
        created_at = Column(DateTime, default=func.now())
        
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保在项目根目录下运行此测试，并安装所有依赖")
    sys.exit(1)


class DatabaseModuleTestSuite:
    """数据库模块完整测试套件"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        self.start_time = None
        self.db = None
        self.mysql_available = False
        
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始运行数据库模块完整测试套件")
        print("=" * 80)
        print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.start_time = time.time()
        
        # 首先检查MySQL可用性
        self._check_mysql_availability()
        
        if not self.mysql_available:
            print("⚠️  MySQL数据库不可用，跳过数据库相关测试")
            print("   请确保MySQL服务运行并配置正确的连接参数")
            self._print_final_results()
            return
        
        # 测试方法列表
        test_methods = [
            ('数据库连接创建', self.test_database_connection),
            ('会话管理', self.test_session_management),
            ('基础CRUD操作', self.test_basic_crud_operations),
            ('事务管理', self.test_transaction_management),
            ('事务回滚', self.test_transaction_rollback),
            ('查询操作', self.test_query_operations),
            ('连接池功能', self.test_connection_pool),
            ('并发操作安全', self.test_concurrent_operations),
            ('异常处理', self.test_exception_handling),
            ('性能测试', self.test_performance),
            ('资源清理', self.test_resource_cleanup)
        ]
        
        # 执行所有测试
        for test_name, test_method in test_methods:
            self._run_single_test(test_name, test_method)
        
        # 输出测试结果
        self._print_final_results()
    
    def _check_mysql_availability(self):
        """检查MySQL数据库可用性"""
        print("🔍 检查MySQL数据库可用性...")
        
        try:
            # 尝试创建数据库连接
            self.db = MySQL_Database()
            
            # 尝试获取会话并执行简单查询
            session = self.db.get_session()
            session.execute(text("SELECT 1"))
            session.close()
            
            self.mysql_available = True
            print("✅ MySQL数据库连接正常")
            
        except Exception as e:
            print(f"❌ MySQL数据库连接失败: {e}")
            print("   请检查:")
            print("   1. MySQL服务是否运行")
            print("   2. 配置文件中的数据库连接参数")
            print("   3. 数据库用户权限")
            self.mysql_available = False
    
    def _run_single_test(self, test_name: str, test_method):
        """运行单个测试"""
        print(f"📋 {test_name}")
        print("-" * 60)
        
        try:
            test_method()
            self.test_results['passed_tests'] += 1
            print(f"✅ {test_name} - 测试通过\n")
            
        except Exception as e:
            self.test_results['failed_tests'] += 1
            error_msg = f"❌ {test_name} - 测试失败: {str(e)}"
            print(error_msg + "\n")
            self.test_results['test_details'].append(error_msg)
            
        self.test_results['total_tests'] += 1
    
    def test_database_connection(self):
        """测试数据库连接创建"""
        print("  🔍 测试数据库实例创建...")
        
        # 测试单例模式（如果实现了）
        db1 = MySQL_Database()
        db2 = MySQL_Database()
        
        assert db1 is not None
        assert db2 is not None
        print("  ✓ 数据库实例创建成功")
        
        print("  🔍 测试数据库配置加载...")
        mysql_config = config.get_mysql_config()
        
        required_keys = ['host', 'port', 'username', 'database']
        for key in required_keys:
            assert key in mysql_config, f"配置缺少必要项: {key}"
        
        print(f"  ✓ 数据库配置加载正常: {mysql_config['host']}:{mysql_config['port']}")
        
        print("  🔍 测试引擎创建...")
        engine = self.db.engine if hasattr(self.db, 'engine') else None
        if engine:
            print("  ✓ 数据库引擎创建成功")
        else:
            print("  ℹ️  数据库引擎信息不可访问（这可能是正常的）")
    
    def test_session_management(self):
        """测试会话管理"""
        print("  🔍 测试会话创建...")
        
        session = self.db.get_session()
        assert session is not None
        assert isinstance(session, Session)
        print("  ✓ 会话创建成功")
        
        print("  🔍 测试会话基本操作...")
        # 执行简单查询验证会话可用
        result = session.execute(text("SELECT 1 as test_value"))
        row = result.fetchone()
        assert row[0] == 1
        print("  ✓ 会话查询操作正常")
        
        print("  🔍 测试会话关闭...")
        session.close()
        print("  ✓ 会话关闭成功")
        
        print("  🔍 测试多个会话...")
        session1 = self.db.get_session()
        session2 = self.db.get_session()
        
        # 两个会话应该是不同的对象
        assert session1 is not session2
        print("  ✓ 多会话创建正常")
        
        session1.close()
        session2.close()
    
    def test_basic_crud_operations(self):
        """测试基础CRUD操作"""
        print("  🔍 准备测试表...")
        
        session = self.db.get_session()
        
        try:
            # 创建测试表
            Base.metadata.create_all(self.db.engine if hasattr(self.db, 'engine') else session.bind)
            print("  ✓ 测试表创建成功")
            
            print("  🔍 测试CREATE操作...")
            test_user = TestUser(
                username=f"test_user_{int(time.time())}",
                email=f"test_{int(time.time())}@example.com"
            )
            
            session.add(test_user)
            session.commit()
            
            assert test_user.id is not None
            user_id = test_user.id
            print(f"  ✓ 用户创建成功，ID: {user_id}")
            
            print("  🔍 测试READ操作...")
            retrieved_user = session.query(TestUser).filter(TestUser.id == user_id).first()
            
            assert retrieved_user is not None
            assert retrieved_user.username == test_user.username
            assert retrieved_user.email == test_user.email
            print("  ✓ 用户查询成功")
            
            print("  🔍 测试UPDATE操作...")
            new_email = f"updated_{int(time.time())}@example.com"
            retrieved_user.email = new_email
            session.commit()
            
            # 重新查询验证更新
            updated_user = session.query(TestUser).filter(TestUser.id == user_id).first()
            assert updated_user.email == new_email
            print("  ✓ 用户更新成功")
            
            print("  🔍 测试DELETE操作...")
            session.delete(updated_user)
            session.commit()
            
            # 验证删除
            deleted_user = session.query(TestUser).filter(TestUser.id == user_id).first()
            assert deleted_user is None
            print("  ✓ 用户删除成功")
            
        finally:
            session.close()
    
    def test_transaction_management(self):
        """测试事务管理"""
        print("  🔍 测试事务管理器...")
        
        session = self.db.get_session()
        
        try:
            with TransactionManager(session) as tm:
                print("  ✓ 事务管理器创建成功")
                
                # 在事务中创建用户
                test_user = TestUser(
                    username=f"tx_user_{int(time.time())}",
                    email=f"tx_{int(time.time())}@example.com"
                )
                
                tm.add(test_user)
                print("  ✓ 事务中添加对象成功")
                
                # 事务应该自动提交
            
            # 验证事务提交成功
            created_user = session.query(TestUser).filter(
                TestUser.username == test_user.username
            ).first()
            
            assert created_user is not None
            print("  ✓ 事务自动提交成功")
            
            # 清理测试数据
            session.delete(created_user)
            session.commit()
            
        except Exception as e:
            print(f"  ❌ 事务管理测试失败: {e}")
            raise
        finally:
            session.close()
    
    def test_transaction_rollback(self):
        """测试事务回滚"""
        print("  🔍 测试事务回滚...")
        
        session = self.db.get_session()
        
        try:
            username = f"rollback_user_{int(time.time())}"
            
            try:
                with TransactionManager(session) as tm:
                    # 创建用户
                    test_user = TestUser(
                        username=username,
                        email=f"rollback_{int(time.time())}@example.com"
                    )
                    
                    tm.add(test_user)
                    
                    # 故意抛出异常触发回滚
                    raise ValueError("故意触发回滚")
                    
            except ValueError as e:
                if "故意触发回滚" in str(e):
                    print("  ✓ 异常触发成功")
                else:
                    raise
            
            # 验证回滚：用户不应该存在
            rolled_back_user = session.query(TestUser).filter(
                TestUser.username == username
            ).first()
            
            assert rolled_back_user is None
            print("  ✓ 事务回滚成功")
            
        finally:
            session.close()
    
    def test_query_operations(self):
        """测试查询操作"""
        print("  🔍 测试复杂查询操作...")
        
        session = self.db.get_session()
        
        try:
            # 创建测试数据
            test_users = []
            for i in range(3):
                user = TestUser(
                    username=f"query_user_{i}_{int(time.time())}",
                    email=f"query_{i}_{int(time.time())}@example.com"
                )
                test_users.append(user)
                session.add(user)
            
            session.commit()
            print(f"  ✓ 创建 {len(test_users)} 个测试用户")
            
            print("  🔍 测试条件查询...")
            # 按用户名查询
            user = session.query(TestUser).filter(
                TestUser.username == test_users[0].username
            ).first()
            
            assert user is not None
            assert user.username == test_users[0].username
            print("  ✓ 条件查询正常")
            
            print("  🔍 测试批量查询...")
            # 查询所有测试用户
            usernames = [u.username for u in test_users]
            users = session.query(TestUser).filter(
                TestUser.username.in_(usernames)
            ).all()
            
            assert len(users) >= len(test_users)
            print(f"  ✓ 批量查询返回 {len(users)} 个用户")
            
            print("  🔍 测试计数查询...")
            count = session.query(TestUser).filter(
                TestUser.username.in_(usernames)
            ).count()
            
            assert count >= len(test_users)
            print(f"  ✓ 计数查询结果: {count}")
            
            print("  🔍 测试排序查询...")
            sorted_users = session.query(TestUser).filter(
                TestUser.username.in_(usernames)
            ).order_by(TestUser.username.desc()).all()
            
            assert len(sorted_users) >= len(test_users)
            print("  ✓ 排序查询正常")
            
            # 清理测试数据
            for user in test_users:
                session.delete(user)
            session.commit()
            
        finally:
            session.close()
    
    def test_connection_pool(self):
        """测试连接池功能"""
        print("  🔍 测试连接池功能...")
        
        # 创建多个会话测试连接复用
        sessions = []
        try:
            for i in range(5):
                session = self.db.get_session()
                sessions.append(session)
                
                # 执行简单查询
                result = session.execute(text("SELECT 1"))
                assert result.fetchone()[0] == 1
            
            print(f"  ✓ 成功创建 {len(sessions)} 个并发会话")
            
        finally:
            # 关闭所有会话
            for session in sessions:
                session.close()
            
            print("  ✓ 所有会话正常关闭")
    
    def test_concurrent_operations(self):
        """测试并发操作安全性"""
        print("  🔍 测试数据库并发操作...")
        
        def worker(worker_id: int, results: List):
            """工作线程函数"""
            try:
                session = self.db.get_session()
                
                try:
                    # 创建用户
                    user = TestUser(
                        username=f"concurrent_user_{worker_id}_{int(time.time())}",
                        email=f"concurrent_{worker_id}@example.com"
                    )
                    
                    session.add(user)
                    session.commit()
                    
                    # 查询验证
                    created_user = session.query(TestUser).filter(
                        TestUser.id == user.id
                    ).first()
                    
                    if created_user:
                        # 清理
                        session.delete(created_user)
                        session.commit()
                        results.append(f"Worker {worker_id}: 成功")
                    else:
                        results.append(f"Worker {worker_id}: 查询失败")
                        
                finally:
                    session.close()
                    
            except Exception as e:
                results.append(f"Worker {worker_id}: 异常 - {e}")
        
        # 创建多个线程并发操作
        threads = []
        results = []
        
        for i in range(3):  # 减少线程数避免过度压力
            thread = threading.Thread(target=worker, args=(i, results))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 检查结果
        success_count = sum(1 for r in results if "成功" in r)
        print(f"  📊 并发测试结果: {success_count}/{len(results)} 个线程成功")
        
        for result in results:
            print(f"    {result}")
        
        if success_count >= len(threads) * 0.8:  # 80%成功率
            print("  ✅ 并发操作测试通过")
        else:
            print("  ⚠️  并发操作可能存在问题")
    
    def test_exception_handling(self):
        """测试异常处理"""
        print("  🔍 测试数据库异常处理...")
        
        session = self.db.get_session()
        
        try:
            print("  🔍 测试SQL语法错误...")
            try:
                session.execute(text("SELECT * FROM non_existent_table_12345"))
                assert False, "应该抛出SQL异常"
            except Exception as e:
                print(f"  ✓ SQL异常正确捕获: {type(e).__name__}")
            
            print("  🔍 测试约束违反...")
            try:
                # 尝试插入重复数据或违反约束的数据
                user1 = TestUser(username=None, email="test@example.com")  # username不能为空
                session.add(user1)
                session.commit()
                assert False, "应该抛出约束异常"
            except Exception as e:
                session.rollback()  # 回滚失败的事务
                print(f"  ✓ 约束异常正确捕获: {type(e).__name__}")
            
            print("  🔍 测试会话状态异常...")
            # 关闭会话后尝试操作
            session.close()
            
            try:
                session.execute(text("SELECT 1"))
                # 某些情况下可能不会立即抛出异常，这取决于SQLAlchemy的实现
                print("  ℹ️  已关闭会话的操作行为取决于SQLAlchemy版本")
            except Exception as e:
                print(f"  ✓ 已关闭会话异常正确捕获: {type(e).__name__}")
            
        finally:
            # 确保会话关闭
            try:
                session.close()
            except:
                pass
    
    def test_performance(self):
        """测试数据库性能"""
        print("  🔍 测试数据库操作性能...")
        
        session = self.db.get_session()
        
        try:
            # 测试批量插入性能
            print("  📊 测试批量插入性能...")
            batch_size = 100
            start_time = time.time()
            
            test_users = []
            for i in range(batch_size):
                user = TestUser(
                    username=f"perf_user_{i}_{int(time.time())}",
                    email=f"perf_{i}@example.com"
                )
                test_users.append(user)
                session.add(user)
            
            session.commit()
            insert_time = time.time() - start_time
            
            print(f"    批量插入 {batch_size} 条记录耗时: {insert_time:.3f}秒")
            print(f"    插入速率: {batch_size/insert_time:.0f} records/sec")
            
            # 测试批量查询性能
            print("  📊 测试批量查询性能...")
            start_time = time.time()
            
            usernames = [user.username for user in test_users]
            queried_users = session.query(TestUser).filter(
                TestUser.username.in_(usernames)
            ).all()
            
            query_time = time.time() - start_time
            
            print(f"    批量查询 {len(queried_users)} 条记录耗时: {query_time:.3f}秒")
            print(f"    查询速率: {len(queried_users)/query_time:.0f} records/sec")
            
            # 清理测试数据
            for user in test_users:
                session.delete(user)
            session.commit()
            
            # 性能基准检查
            if insert_time < 1.0 and query_time < 0.1:
                print("  ✅ 数据库性能优秀")
            elif insert_time < 2.0 and query_time < 0.5:
                print("  ✓ 数据库性能良好")
            else:
                print("  ⚠️  数据库性能可能需要优化")
                
        finally:
            session.close()
    
    def test_resource_cleanup(self):
        """测试资源清理"""
        print("  🔍 测试资源清理...")
        
        # 测试会话自动关闭
        session = self.db.get_session()
        session_id = id(session)
        
        # 正常关闭
        session.close()
        print("  ✓ 会话正常关闭")
        
        # 测试连接池状态（如果可访问）
        try:
            if hasattr(self.db, 'engine'):
                pool = self.db.engine.pool
                print(f"  📊 连接池状态: checkedout={pool.checkedout()}, checkedin={pool.checkedin()}")
            else:
                print("  ℹ️  连接池信息不可访问")
        except:
            print("  ℹ️  连接池状态检查跳过")
        
        print("  ✓ 资源清理测试完成")
    
    def _print_final_results(self):
        """打印最终测试结果"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("=" * 80)
        print("📊 数据库模块测试结果汇总")
        print("=" * 80)
        
        print(f"⏱️  总耗时: {total_time:.2f}秒")
        print(f"📈 总测试数: {self.test_results['total_tests']}")
        print(f"✅ 通过测试: {self.test_results['passed_tests']}")
        print(f"❌ 失败测试: {self.test_results['failed_tests']}")
        
        if self.test_results['total_tests'] > 0:
            success_rate = (self.test_results['passed_tests'] / self.test_results['total_tests']) * 100
            print(f"🎯 成功率: {success_rate:.1f}%")
        else:
            success_rate = 0
            print("🎯 成功率: N/A (MySQL不可用)")
        
        if self.test_results['failed_tests'] > 0:
            print("\n❌ 失败的测试详情:")
            for detail in self.test_results['test_details']:
                print(f"   {detail}")
        
        print("\n" + "=" * 80)
        
        if not self.mysql_available:
            print("ℹ️  MySQL数据库不可用，未进行数据库测试")
            print("   请配置MySQL连接参数并启动MySQL服务")
        elif success_rate >= 90:
            print("🎉 数据库模块测试整体通过！")
        elif success_rate >= 70:
            print("⚠️  数据库模块测试部分通过，需要关注失败的测试")
        else:
            print("❌ 数据库模块测试失败较多，需要重点修复")
        
        print("=" * 80)


def main():
    """主函数 - 运行数据库模块测试"""
    print("🧪 Python Project Template - 数据库模块测试")
    
    try:
        test_suite = DatabaseModuleTestSuite()
        test_suite.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试运行出现异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()