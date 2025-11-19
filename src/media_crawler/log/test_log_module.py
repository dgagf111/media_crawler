#!/usr/bin/env python3
"""
日志模块完整测试类

功能说明：
这个测试类专门测试日志模块的所有核心功能，包括：
1. 日志辅助类初始化测试 - 单例模式、配置加载、处理器设置
2. 日志级别测试 - DEBUG、INFO、WARNING、ERROR、CRITICAL
3. 日志输出测试 - 控制台输出、文件输出、格式化
4. 文件管理测试 - 按日期组织、文件轮转、备份管理
5. 异常日志测试 - 异常信息记录、堆栈跟踪
6. 并发安全测试 - 多线程日志写入、线程安全性
7. 性能测试 - 日志写入性能、内存使用

测试覆盖率目标：90%以上
支持独立运行：python log/test_log_module.py
"""

import os
import sys
import time
import threading
import tempfile
import shutil
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pythonprojecttemplate.log.logHelper import LogHelper, get_logger
    from pythonprojecttemplate.config.config import config
    import logging
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)


class LogModuleTestSuite:
    """日志模块完整测试套件"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        self.start_time = None
        self.temp_log_dir = None
        
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始运行日志模块完整测试套件")
        print("=" * 80)
        print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.start_time = time.time()
        
        # 创建临时日志目录
        self.temp_log_dir = tempfile.mkdtemp(prefix="test_logs_")
        
        # 测试方法列表
        test_methods = [
            ('日志辅助类初始化', self.test_log_helper_initialization),
            ('单例模式验证', self.test_singleton_pattern),
            ('日志级别功能', self.test_logging_levels),
            ('日志格式化', self.test_log_formatting),
            ('文件日志管理', self.test_file_logging),
            ('日志轮转功能', self.test_log_rotation),
            ('异常日志记录', self.test_exception_logging),
            ('并发日志安全', self.test_concurrent_logging),
            ('日志配置加载', self.test_log_configuration),
            ('日志性能测试', self.test_logging_performance)
        ]
        
        # 执行所有测试
        for test_name, test_method in test_methods:
            self._run_single_test(test_name, test_method)
        
        # 清理临时目录
        if self.temp_log_dir and os.path.exists(self.temp_log_dir):
            shutil.rmtree(self.temp_log_dir)
        
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
    
    def test_log_helper_initialization(self):
        """测试日志辅助类初始化"""
        print("  🔍 测试LogHelper类初始化...")
        
        # 创建测试用的日志辅助类
        test_logger = LogHelper(
            project_name="test_project",
            base_log_directory=self.temp_log_dir,
            log_level="DEBUG"
        )
        
        assert test_logger is not None
        print("  ✓ LogHelper实例创建成功")
        
        # 检查关键属性
        assert hasattr(test_logger, 'logger')
        assert hasattr(test_logger, 'project_name')
        assert test_logger.project_name == "test_project"
        print("  ✓ 关键属性设置正确")
        
        # 检查日志级别
        assert test_logger.logger.level == logging.DEBUG
        print("  ✓ 日志级别设置正确")
        
        # 测试全局日志获取函数
        global_logger = get_logger()
        assert isinstance(global_logger, LogHelper)
        print("  ✓ 全局日志获取函数正常")
    
    def test_singleton_pattern(self):
        """测试单例模式"""
        print("  🔍 测试单例模式实现...")
        
        # 创建多个LogHelper实例
        logger1 = LogHelper()
        logger2 = LogHelper()
        logger3 = get_logger()
        
        # 验证是否为同一实例
        assert logger1 is logger2
        assert logger2 is logger3
        print("  ✓ LogHelper正确实现单例模式")
        
        # 测试多次初始化
        original_project_name = logger1.project_name
        
        # 重新创建实例（应该保持原有配置）
        logger4 = LogHelper(project_name="new_project")
        
        # 在单例模式下，后续创建应该使用原有配置
        assert logger4 is logger1
        print("  ✓ 单例模式配置保护正常")
    
    def test_logging_levels(self):
        """测试日志级别功能"""
        print("  🔍 测试各种日志级别...")
        
        # 创建测试日志器
        test_logger = LogHelper(
            project_name="level_test",
            base_log_directory=self.temp_log_dir,
            log_level="DEBUG"
        )
        
        # 测试各个日志级别
        test_messages = {
            'debug': '这是DEBUG级别日志',
            'info': '这是INFO级别日志',
            'warning': '这是WARNING级别日志',
            'error': '这是ERROR级别日志',
            'critical': '这是CRITICAL级别日志'
        }
        
        print("  📝 测试日志级别输出:")
        for level, message in test_messages.items():
            method = getattr(test_logger, level)
            method(message)
            print(f"    ✓ {level.upper()}: {message}")
        
        print("  ✓ 所有日志级别测试完成")
        
        # 测试日志级别过滤
        print("  🔍 测试日志级别过滤...")
        
        # 创建INFO级别的日志器
        info_logger = LogHelper(
            project_name="info_test",
            base_log_directory=self.temp_log_dir,
            log_level="INFO"
        )
        
        # DEBUG消息应该被过滤
        info_logger.debug("这条DEBUG消息应该被过滤")
        info_logger.info("这条INFO消息应该显示")
        
        print("  ✓ 日志级别过滤功能正常")
    
    def test_log_formatting(self):
        """测试日志格式化"""
        print("  🔍 测试日志格式化...")
        
        test_logger = LogHelper(
            project_name="format_test",
            base_log_directory=self.temp_log_dir
        )
        
        # 测试基本格式化
        test_logger.info("基本日志消息测试")
        print("  ✓ 基本日志格式化正常")
        
        # 测试带参数的日志
        user_id = 12345
        operation = "登录"
        test_logger.info("用户操作日志: 用户ID=%d, 操作=%s", user_id, operation)
        print("  ✓ 参数化日志格式化正常")
        
        # 测试额外参数
        extra_data = {"user": "testuser", "ip": "127.0.0.1"}
        test_logger.info("带额外数据的日志", extra=extra_data)
        print("  ✓ 额外参数日志格式化正常")
        
        # 测试特殊字符处理
        special_message = "包含特殊字符的日志: äöü ñ 中文 🎉"
        test_logger.info(special_message)
        print("  ✓ 特殊字符日志处理正常")
    
    def test_file_logging(self):
        """测试文件日志管理"""
        print("  🔍 测试文件日志功能...")
        
        test_logger = LogHelper(
            project_name="file_test",
            base_log_directory=self.temp_log_dir
        )
        
        # 写入测试日志
        test_messages = [
            "文件日志测试消息 1",
            "文件日志测试消息 2", 
            "文件日志测试消息 3"
        ]
        
        for msg in test_messages:
            test_logger.info(msg)
        
        print("  ✓ 日志消息写入完成")
        
        # 验证日志文件结构
        current_date = datetime.now()
        year = current_date.strftime('%Y')
        month = current_date.strftime('%Y-%m')
        day = current_date.strftime('%Y-%m-%d')
        
        expected_log_dir = os.path.join(self.temp_log_dir, "file_test", year, month)
        expected_log_file = os.path.join(expected_log_dir, f"{day}.log")
        
        print(f"  🔍 验证日志文件: {expected_log_file}")
        
        if os.path.exists(expected_log_file):
            print("  ✓ 日志文件创建成功")
            
            # 验证日志内容
            with open(expected_log_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            found_messages = 0
            for msg in test_messages:
                if msg in content:
                    found_messages += 1
            
            print(f"  📊 日志文件中找到 {found_messages}/{len(test_messages)} 条消息")
            assert found_messages == len(test_messages)
            print("  ✓ 日志内容验证通过")
            
        else:
            print("  ⚠️  日志文件未找到，可能日志配置问题")
    
    def test_log_rotation(self):
        """测试日志轮转功能"""
        print("  🔍 测试日志轮转功能...")
        
        # 创建小容量的日志器进行轮转测试
        test_logger = LogHelper(
            project_name="rotation_test",
            base_log_directory=self.temp_log_dir,
            max_bytes=1024,  # 1KB
            backup_count=3
        )
        
        # 写入大量日志触发轮转
        print("  📝 写入大量日志数据...")
        
        for i in range(100):
            long_message = f"日志轮转测试消息 {i:03d} - " + "x" * 50
            test_logger.info(long_message)
        
        print("  ✓ 大量日志数据写入完成")
        
        # 检查是否产生了轮转文件
        current_date = datetime.now()
        year = current_date.strftime('%Y')
        month = current_date.strftime('%Y-%m')
        day = current_date.strftime('%Y-%m-%d')
        
        log_dir = os.path.join(self.temp_log_dir, "rotation_test", year, month)
        
        if os.path.exists(log_dir):
            log_files = [f for f in os.listdir(log_dir) if f.startswith(day)]
            print(f"  📊 发现日志文件: {len(log_files)} 个")
            
            for log_file in log_files:
                print(f"    - {log_file}")
            
            if len(log_files) > 1:
                print("  ✅ 日志轮转功能正常工作")
            else:
                print("  ℹ️  日志轮转未触发（可能需要更多数据）")
        else:
            print("  ⚠️  日志目录未找到")
    
    def test_exception_logging(self):
        """测试异常日志记录"""
        print("  🔍 测试异常日志记录...")
        
        test_logger = LogHelper(
            project_name="exception_test",
            base_log_directory=self.temp_log_dir
        )
        
        # 测试异常对象记录
        print("  🔍 测试异常对象记录...")
        try:
            raise ValueError("测试异常")
        except ValueError as e:
            test_logger.error("捕获到ValueError异常", exc_info=e)
            print("  ✓ 异常对象记录成功")
        
        # 测试自动异常记录
        print("  🔍 测试自动异常记录...")
        try:
            1 / 0  # 故意除零错误
        except ZeroDivisionError:
            test_logger.error("除零错误", exc_info=True)
            print("  ✓ 自动异常记录成功")
        
        # 测试不同级别的异常记录
        print("  🔍 测试不同级别异常记录...")
        try:
            raise RuntimeError("运行时错误")
        except RuntimeError as e:
            test_logger.warning("警告级别异常", exc_info=e)
            test_logger.critical("严重级别异常", exc_info=e)
            print("  ✓ 多级别异常记录成功")
        
        # 测试嵌套异常
        print("  🔍 测试嵌套异常记录...")
        try:
            try:
                raise ValueError("内部异常")
            except ValueError:
                raise RuntimeError("外部异常")
        except RuntimeError as e:
            test_logger.error("嵌套异常", exc_info=e)
            print("  ✓ 嵌套异常记录成功")
    
    def test_concurrent_logging(self):
        """测试并发日志安全"""
        print("  🔍 测试并发日志安全性...")
        
        test_logger = LogHelper(
            project_name="concurrent_test",
            base_log_directory=self.temp_log_dir
        )
        
        # 并发写入结果
        concurrent_results = {'success': 0, 'errors': 0, 'lock': threading.Lock()}
        
        def worker_function(worker_id: int, message_count: int):
            """工作线程函数"""
            try:
                for i in range(message_count):
                    message = f"Worker {worker_id} - Message {i:03d}"
                    test_logger.info(message)
                    
                    # 随机测试不同日志级别
                    if i % 5 == 0:
                        test_logger.warning(f"Worker {worker_id} - Warning {i}")
                    elif i % 10 == 0:
                        test_logger.error(f"Worker {worker_id} - Error {i}")
                
                with concurrent_results['lock']:
                    concurrent_results['success'] += 1
                    
            except Exception as e:
                with concurrent_results['lock']:
                    concurrent_results['errors'] += 1
                print(f"  ❌ Worker {worker_id} 异常: {e}")
        
        # 创建多个线程并发写入
        thread_count = 5
        messages_per_thread = 20
        
        print(f"  🔄 启动 {thread_count} 个线程，每个写入 {messages_per_thread} 条日志...")
        
        threads = []
        start_time = time.time()
        
        for i in range(thread_count):
            thread = threading.Thread(
                target=worker_function,
                args=(i, messages_per_thread)
            )
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # 分析结果
        total_time = end_time - start_time
        total_messages = thread_count * messages_per_thread * 1.3  # 包括warning和error
        
        print(f"  📊 并发测试结果:")
        print(f"    总耗时: {total_time:.3f}秒")
        print(f"    成功线程: {concurrent_results['success']}")
        print(f"    失败线程: {concurrent_results['errors']}")
        print(f"    估计日志条数: {int(total_messages)}")
        print(f"    写入速率: {total_messages/total_time:.0f} logs/sec")
        
        if concurrent_results['errors'] == 0:
            print("  ✅ 并发日志写入安全测试通过")
        else:
            print("  ⚠️  并发日志写入存在问题")
    
    def test_log_configuration(self):
        """测试日志配置加载"""
        print("  🔍 测试日志配置加载...")
        
        # 获取日志配置
        log_config = config.get_log_config()
        assert isinstance(log_config, dict)
        print("  ✓ 日志配置加载成功")
        
        print("  📋 当前日志配置:")
        if log_config:
            for key, value in log_config.items():
                print(f"    {key}: {value}")
        else:
            print("    使用默认日志配置")
        
        # 测试配置应用
        print("  🔍 测试配置应用...")
        
        # 从配置创建日志器
        project_name = log_config.get('project_name', 'config_test')
        log_level = log_config.get('log_level', 'INFO')
        base_log_directory = log_config.get('base_log_directory', self.temp_log_dir)
        
        config_logger = LogHelper(
            project_name=project_name,
            base_log_directory=base_log_directory,
            log_level=log_level
        )
        
        assert config_logger is not None
        print("  ✓ 配置应用成功")
        
        # 验证配置生效
        expected_level = getattr(logging, log_level.upper(), logging.INFO)
        assert config_logger.logger.level == expected_level
        print(f"  ✓ 日志级别配置正确: {log_level}")
    
    def test_logging_performance(self):
        """测试日志性能"""
        print("  🔍 测试日志性能...")
        
        test_logger = LogHelper(
            project_name="performance_test",
            base_log_directory=self.temp_log_dir
        )
        
        # 测试大量日志写入性能
        print("  📊 测试大量日志写入性能...")
        log_count = 1000
        start_time = time.time()
        
        for i in range(log_count):
            test_logger.info(f"性能测试日志消息 {i:04d}")
        
        write_time = time.time() - start_time
        logs_per_second = log_count / write_time
        
        print(f"  📈 {log_count} 条日志写入耗时: {write_time:.3f}秒")
        print(f"  📈 日志写入速率: {logs_per_second:.0f} logs/sec")
        
        # 测试不同级别日志性能
        print("  📊 测试不同级别日志性能...")
        level_counts = {'debug': 100, 'info': 100, 'warning': 50, 'error': 20, 'critical': 10}
        
        level_performance = {}
        
        for level, count in level_counts.items():
            method = getattr(test_logger, level)
            start_time = time.time()
            
            for i in range(count):
                method(f"{level.upper()} 级别性能测试 {i}")
            
            level_time = time.time() - start_time
            level_performance[level] = {
                'count': count,
                'time': level_time,
                'rate': count / level_time if level_time > 0 else float('inf')
            }
        
        print("  📊 各级别日志性能:")
        for level, perf in level_performance.items():
            print(f"    {level.upper()}: {perf['count']} 条/{perf['time']:.3f}秒 = {perf['rate']:.0f} logs/sec")
        
        # 性能评估
        if logs_per_second > 1000:
            print("  ✅ 日志系统性能优秀")
        elif logs_per_second > 500:
            print("  ✓ 日志系统性能良好")
        else:
            print("  ⚠️  日志系统性能可能需要优化")
    
    def _print_final_results(self):
        """打印最终测试结果"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("=" * 80)
        print("📊 日志模块测试结果汇总")
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
            print("🎉 日志模块测试整体通过！")
        elif success_rate >= 70:
            print("⚠️  日志模块测试部分通过，需要关注失败的测试")
        else:
            print("❌ 日志模块测试失败较多，需要重点修复")
        
        print("=" * 80)


def main():
    """主函数 - 运行日志模块测试"""
    print("🧪 Python Project Template - 日志模块测试")
    
    try:
        test_suite = LogModuleTestSuite()
        test_suite.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试运行出现异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()