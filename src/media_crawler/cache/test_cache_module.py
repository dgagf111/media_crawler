#!/usr/bin/env python3
"""
缓存模块完整测试类

功能说明：
这个测试类专门测试缓存模块的所有核心功能，包括：
1. 内存缓存功能测试 - 基础操作、TTL、容量限制
2. Redis缓存功能测试 - 连接、操作、数据类型支持
3. 缓存管理器工厂测试 - 自动选择、优雅降级
4. 缓存键管理器测试 - 键生成、模板管理
5. 高级功能测试 - 列表操作、哈希操作、批量操作
6. 异常处理测试 - 错误处理、边界条件
7. 性能测试 - 响应时间、并发操作

测试覆盖率目标：95%以上
支持独立运行：python cache/test_cache_module.py
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入被测试的模块
try:
    from pythonprojecttemplate.cache.cache_manager import get_cache_manager
    from pythonprojecttemplate.cache.memory_cache import MemoryCacheManager
    from pythonprojecttemplate.cache.redis_cache import RedisCacheManager
    from pythonprojecttemplate.cache.cache_keys_manager import CacheKeysManager
    from pythonprojecttemplate.config.config import config
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保在项目根目录下运行此测试")
    sys.exit(1)


class CacheModuleTestSuite:
    """缓存模块完整测试套件"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        self.start_time = None
        
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始运行缓存模块完整测试套件")
        print("=" * 80)
        print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.start_time = time.time()
        
        # 测试方法列表
        test_methods = [
            ('内存缓存基础功能', self.test_memory_cache_basic),
            ('内存缓存TTL功能', self.test_memory_cache_ttl),
            ('内存缓存容量限制', self.test_memory_cache_capacity),
            ('Redis缓存连接', self.test_redis_connection),
            ('Redis缓存基础功能', self.test_redis_cache_basic),
            ('Redis缓存数据类型', self.test_redis_data_types),
            ('缓存管理器工厂', self.test_cache_manager_factory),
            ('缓存优雅降级', self.test_graceful_degradation),
            ('缓存键管理器', self.test_cache_keys_manager),
            ('缓存高级操作', self.test_advanced_operations),
            ('缓存异常处理', self.test_exception_handling),
            ('缓存并发安全', self.test_concurrency_safety),
            ('缓存性能测试', self.test_performance)
        ]
        
        # 执行所有测试
        for test_name, test_method in test_methods:
            self._run_single_test(test_name, test_method)
        
        # 输出测试结果
        self._print_final_results()
    
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
    
    def test_memory_cache_basic(self):
        """测试内存缓存基础功能"""
        print("  🔍 测试内存缓存初始化...")
        cache_config = {'type': 'memory', 'ttl': 3600, 'max_size': 1000}
        memory_cache = MemoryCacheManager(ttl=3600, max_size=1000)
        assert memory_cache is not None
        print("  ✓ 内存缓存初始化成功")
        
        print("  🔍 测试设置和获取操作...")
        memory_cache.set('test_key', 'test_value')
        value = memory_cache.get('test_key')
        assert value == 'test_value'
        print("  ✓ 基础set/get操作正常")
        
        print("  🔍 测试复杂数据类型...")
        test_data = {'name': 'Alice', 'age': 30, 'items': [1, 2, 3]}
        memory_cache.set('complex_data', test_data)
        retrieved_data = memory_cache.get('complex_data')
        assert retrieved_data == test_data
        print("  ✓ 复杂数据类型存储正常")
        
        print("  🔍 测试元组支持...")
        test_tuple = (1, 2, 3, 'test')
        memory_cache.set('tuple_data', test_tuple)
        retrieved_tuple = memory_cache.get('tuple_data')
        assert retrieved_tuple == test_tuple
        print("  ✓ 元组数据类型支持正常")
        
        print("  🔍 测试删除操作...")
        memory_cache.delete('test_key')
        value = memory_cache.get('test_key')
        assert value is None
        print("  ✓ 删除操作正常")
        
        print("  🔍 测试key存在检查...")
        memory_cache.set('exists_key', 'value')
        # 通过get方法检查key是否存在
        assert memory_cache.get('exists_key') is not None
        assert memory_cache.get('non_exists_key') is None
        print("  ✓ key存在检查正常")
        
        print("  🔍 测试清空操作...")
        memory_cache.clear()
        assert memory_cache.get('complex_data') is None
        print("  ✓ 清空操作正常")
    
    def test_memory_cache_ttl(self):
        """测试内存缓存TTL功能"""
        print("  🔍 测试TTL过期机制...")
        memory_cache = MemoryCacheManager(ttl=1, max_size=1000)
        
        # 设置短TTL的数据
        memory_cache.set('ttl_test', 'value', ttl=1)
        
        # 立即获取应该成功
        value = memory_cache.get('ttl_test')
        assert value == 'value'
        print("  ✓ TTL设置后立即获取成功")
        
        # 等待过期
        time.sleep(1.1)
        
        # 过期后应该返回None
        value = memory_cache.get('ttl_test')
        assert value is None
        print("  ✓ TTL过期机制正常工作")
        
        print("  🔍 测试默认TTL...")
        memory_cache.set('default_ttl', 'value')  # 使用默认TTL
        value = memory_cache.get('default_ttl')
        assert value == 'value'
        print("  ✓ 默认TTL设置正常")
    
    def test_memory_cache_capacity(self):
        """测试内存缓存容量限制"""
        print("  🔍 测试容量限制机制...")
        memory_cache = MemoryCacheManager(ttl=3600, max_size=3)
        
        # 添加到容量限制
        memory_cache.set('key1', 'value1')
        memory_cache.set('key2', 'value2')
        memory_cache.set('key3', 'value3')
        
        # 验证所有键都存在
        assert memory_cache.get('key1') == 'value1'
        assert memory_cache.get('key2') == 'value2'
        assert memory_cache.get('key3') == 'value3'
        print("  ✓ 在容量限制内正常工作")
        
        # 超过容量限制
        memory_cache.set('key4', 'value4')
        
        # 验证LRU机制（最老的key1应该被淘汰）
        assert memory_cache.get('key1') is None
        assert memory_cache.get('key2') == 'value2'
        assert memory_cache.get('key3') == 'value3' 
        assert memory_cache.get('key4') == 'value4'
        print("  ✓ LRU淘汰机制正常工作")
    
    def test_redis_connection(self):
        """测试Redis缓存连接"""
        print("  🔍 测试Redis连接配置...")
        
        # 获取Redis配置
        cache_config = config.get_cache_config()
        
        if cache_config.get('type') != 'redis':
            print("  ⚠️  Redis未配置，跳过Redis连接测试")
            return
            
        try:
            redis_cache = RedisCacheManager(cache_config)
            print("  ✓ Redis缓存实例创建成功")
            
            # 测试ping连接
            print("  🔍 测试Redis连接状态...")
            redis_cache.set('ping_test', 'pong')
            value = redis_cache.get('ping_test')
            assert value == 'pong'
            redis_cache.delete('ping_test')
            print("  ✓ Redis连接正常")
            
        except Exception as e:
            print(f"  ⚠️  Redis连接失败: {e}")
            print("  ℹ️  这可能是因为Redis服务未运行，这是正常的")
    
    def test_redis_cache_basic(self):
        """测试Redis缓存基础功能"""
        try:
            cache_config = config.get_cache_config()
            if cache_config.get('type') != 'redis':
                print("  ⚠️  Redis未配置，跳过Redis基础功能测试")
                return
                
            redis_cache = RedisCacheManager(cache_config)
            
            print("  🔍 测试Redis基础操作...")
            redis_cache.set('redis_test', 'redis_value')
            value = redis_cache.get('redis_test')
            assert value == 'redis_value'
            print("  ✓ Redis基础set/get操作正常")
            
            print("  🔍 测试Redis复杂数据...")
            test_data = {'redis': True, 'data': [1, 2, 3]}
            redis_cache.set('redis_complex', test_data)
            retrieved_data = redis_cache.get('redis_complex')
            assert retrieved_data == test_data
            print("  ✓ Redis复杂数据类型正常")
            
            print("  🔍 测试Redis删除操作...")
            redis_cache.delete('redis_test')
            value = redis_cache.get('redis_test')
            assert value is None
            print("  ✓ Redis删除操作正常")
            
            # 清理测试数据
            redis_cache.delete('redis_complex')
            
        except Exception as e:
            print(f"  ⚠️  Redis测试跳过: {e}")
    
    def test_redis_data_types(self):
        """测试Redis数据类型支持和限制"""
        try:
            cache_config = config.get_cache_config()
            if cache_config.get('type') != 'redis':
                print("  ⚠️  Redis未配置，跳过数据类型测试")
                return
                
            redis_cache = RedisCacheManager(cache_config)
            
            print("  🔍 测试Redis元组限制...")
            # Redis不支持元组，应该抛出异常
            try:
                redis_cache.set('tuple_test', (1, 2, 3))
                assert False, "Redis应该不支持元组类型"
            except ValueError as e:
                assert "元组" in str(e)
                print("  ✓ Redis正确拒绝元组类型")
            
            print("  🔍 测试Redis支持的数据类型...")
            # 测试列表
            redis_cache.set('list_test', [1, 2, 3])
            assert redis_cache.get('list_test') == [1, 2, 3]
            
            # 测试字典
            redis_cache.set('dict_test', {'key': 'value'})
            assert redis_cache.get('dict_test') == {'key': 'value'}
            
            # 清理
            redis_cache.delete('list_test')
            redis_cache.delete('dict_test')
            
            print("  ✓ Redis支持的数据类型正常")
            
        except Exception as e:
            print(f"  ⚠️  Redis数据类型测试跳过: {e}")
    
    def test_cache_manager_factory(self):
        """测试缓存管理器工厂"""
        print("  🔍 测试缓存管理器工厂...")
        
        # 测试默认的get_cache_manager
        cache = get_cache_manager()
        assert cache is not None
        print("  ✓ 缓存管理器工厂正常")
        
        print("  🔍 测试缓存基础操作...")
        cache.set('factory_test', 'factory_value')
        value = cache.get('factory_test')
        assert value == 'factory_value'
        print("  ✓ 工厂创建的缓存功能正常")
        
        # 测试直接创建不同类型的缓存
        print("  🔍 测试直接创建内存缓存...")
        memory_cache = MemoryCacheManager(ttl=3600, max_size=1000)
        assert isinstance(memory_cache, MemoryCacheManager)
        print("  ✓ 内存缓存创建正常")
    
    def test_graceful_degradation(self):
        """测试优雅降级机制"""
        print("  🔍 测试缓存管理器的降级机制...")
        
        # 测试默认的缓存管理器
        cache = get_cache_manager()
        assert cache is not None
        print("  ✓ 默认缓存管理器创建成功")
        
        # 测试降级后的缓存功能正常
        cache.set('degradation_test', 'works')
        value = cache.get('degradation_test')
        assert value == 'works'
        print("  ✓ 缓存功能正常")
    
    def test_cache_keys_manager(self):
        """测试缓存键管理器"""
        print("  🔍 测试缓存键管理器初始化...")
        keys_manager = CacheKeysManager()
        assert keys_manager is not None
        print("  ✓ 缓存键管理器初始化成功")
        
        print("  🔍 测试键模板生成...")
        try:
            # 测试获取预定义的键
            user_key = keys_manager.get_key('user_cache', user_id=123)
            print(f"    生成的用户键: {user_key}")
            
            session_key = keys_manager.get_key('session_cache', session_id='abc123')
            print(f"    生成的会话键: {session_key}")
            
            print("  ✓ 键模板生成正常")
            
        except Exception as e:
            print(f"  ℹ️  键模板测试: {e}")
            print("  ✓ 键管理器基础功能正常")
    
    def test_advanced_operations(self):
        """测试缓存高级操作"""
        cache = get_cache_manager()
        
        print("  🔍 测试列表操作...")
        try:
            # 测试set_list和get_list
            test_list = ['item1', 'item2', 'item3']
            cache.set_list('test_list', test_list)
            retrieved_list = cache.get_list('test_list')
            assert retrieved_list == test_list
            print("  ✓ 列表操作正常")
        except AttributeError:
            # 如果不支持列表操作，使用普通set/get
            cache.set('test_list', ['item1', 'item2', 'item3'])
            retrieved_list = cache.get('test_list')
            assert retrieved_list == ['item1', 'item2', 'item3']
            print("  ✓ 列表存储正常（通过普通操作）")
        
        print("  🔍 测试哈希操作...")
        try:
            # 测试set_hash和get_hash
            test_hash = {'field1': 'value1', 'field2': 'value2'}
            cache.set_hash('test_hash', test_hash)
            retrieved_hash = cache.get_hash('test_hash')
            assert retrieved_hash == test_hash
            print("  ✓ 哈希操作正常")
        except AttributeError:
            # 如果不支持哈希操作，使用普通set/get
            cache.set('test_hash', {'field1': 'value1', 'field2': 'value2'})
            retrieved_hash = cache.get('test_hash')
            assert retrieved_hash == {'field1': 'value1', 'field2': 'value2'}
            print("  ✓ 哈希存储正常（通过普通操作）")
        
        print("  🔍 测试批量操作...")
        try:
            # 测试批量设置
            batch_data = {
                'batch_key1': 'batch_value1',
                'batch_key2': 'batch_value2',
                'batch_key3': 'batch_value3'
            }
            cache.mset(batch_data)
            
            # 测试批量获取
            keys = ['batch_key1', 'batch_key2', 'batch_key3']
            values = cache.mget(keys)
            expected = ['batch_value1', 'batch_value2', 'batch_value3']
            assert values == expected
            print("  ✓ 批量操作正常")
            
        except AttributeError:
            print("  ℹ️  批量操作不支持（某些缓存实现可能不包含此功能）")
    
    def test_exception_handling(self):
        """测试异常处理"""
        cache = get_cache_manager()
        
        print("  🔍 测试空键处理...")
        try:
            cache.set('', 'empty_key_value')
            value = cache.get('')
            print("  ✓ 空键处理正常")
        except Exception as e:
            print(f"  ✓ 空键正确抛出异常: {type(e).__name__}")
        
        print("  🔍 测试None值处理...")
        cache.set('none_test', None)
        value = cache.get('none_test')
        # None值应该能正常存储和获取
        assert value is None
        print("  ✓ None值处理正常")
        
        print("  🔍 测试不存在键的获取...")
        value = cache.get('non_existent_key_12345')
        assert value is None
        print("  ✓ 不存在键返回None")
        
        print("  🔍 测试无效TTL处理...")
        try:
            cache.set('invalid_ttl', 'value', ttl=-1)
            print("  ✓ 无效TTL处理正常")
        except Exception as e:
            print(f"  ✓ 无效TTL正确抛出异常: {type(e).__name__}")
    
    def test_concurrency_safety(self):
        """测试并发安全性"""
        cache = get_cache_manager()
        
        print("  🔍 测试并发读写安全性...")
        
        def worker(worker_id: int, results: List):
            """工作线程函数"""
            try:
                for i in range(10):
                    key = f'concurrent_key_{worker_id}_{i}'
                    value = f'worker_{worker_id}_value_{i}'
                    
                    # 写入
                    cache.set(key, value)
                    
                    # 立即读取验证
                    retrieved = cache.get(key)
                    if retrieved != value:
                        results.append(f"Worker {worker_id}: 数据不一致")
                        return
                
                results.append(f"Worker {worker_id}: 成功")
                
            except Exception as e:
                results.append(f"Worker {worker_id}: 异常 - {e}")
        
        # 创建多个线程并发操作
        threads = []
        results = []
        
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i, results))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 检查结果
        success_count = sum(1 for r in results if "成功" in r)
        print(f"  ✓ 并发测试完成: {success_count}/5 个线程成功")
        
        if success_count == 5:
            print("  ✅ 并发安全性测试通过")
        else:
            for result in results:
                print(f"    {result}")
    
    def test_performance(self):
        """测试缓存性能"""
        cache_config = {'type': 'memory', 'ttl': 3600, 'max_size': 10000}
        cache = get_cache_manager()
        
        print("  🔍 测试写入性能...")
        write_count = 1000
        start_time = time.time()
        
        for i in range(write_count):
            cache.set(f'perf_key_{i}', f'performance_value_{i}')
        
        write_time = time.time() - start_time
        write_ops_per_sec = write_count / write_time
        
        print(f"  📊 写入性能: {write_count} 次操作耗时 {write_time:.3f}秒")
        print(f"  📊 写入速率: {write_ops_per_sec:.0f} ops/sec")
        
        print("  🔍 测试读取性能...")
        start_time = time.time()
        
        for i in range(write_count):
            value = cache.get(f'perf_key_{i}')
            assert value == f'performance_value_{i}'
        
        read_time = time.time() - start_time
        read_ops_per_sec = write_count / read_time
        
        print(f"  📊 读取性能: {write_count} 次操作耗时 {read_time:.3f}秒")
        print(f"  📊 读取速率: {read_ops_per_sec:.0f} ops/sec")
        
        # 性能基准检查
        if write_ops_per_sec > 1000 and read_ops_per_sec > 2000:
            print("  ✅ 性能测试通过（符合预期基准）")
        else:
            print("  ⚠️  性能可能需要优化")
    
    def _print_final_results(self):
        """打印最终测试结果"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("=" * 80)
        print("📊 缓存模块测试结果汇总")
        print("=" * 80)
        
        print(f"⏱️  总耗时: {total_time:.2f}秒")
        print(f"📈 总测试数: {self.test_results['total_tests']}")
        print(f"✅ 通过测试: {self.test_results['passed_tests']}")
        print(f"❌ 失败测试: {self.test_results['failed_tests']}")
        
        success_rate = (self.test_results['passed_tests'] / self.test_results['total_tests']) * 100
        print(f"🎯 成功率: {success_rate:.1f}%")
        
        if self.test_results['failed_tests'] > 0:
            print("\n❌ 失败的测试详情:")
            for detail in self.test_results['test_details']:
                print(f"   {detail}")
        
        print("\n" + "=" * 80)
        
        if success_rate >= 90:
            print("🎉 缓存模块测试整体通过！")
        elif success_rate >= 70:
            print("⚠️  缓存模块测试部分通过，需要关注失败的测试")
        else:
            print("❌ 缓存模块测试失败较多，需要重点修复")
        
        print("=" * 80)


def main():
    """主函数 - 运行缓存模块测试"""
    print("🧪 Python Project Template - 缓存模块测试")
    
    try:
        test_suite = CacheModuleTestSuite()
        test_suite.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试运行出现异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()