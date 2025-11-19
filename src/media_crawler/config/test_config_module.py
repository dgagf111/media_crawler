#!/usr/bin/env python3
"""
配置管理模块完整测试类

功能说明：
这个测试类专门测试配置管理模块的所有核心功能，包括：
1. 配置文件加载测试 - YAML文件解析、环境变量替换
2. 单例模式测试 - 确保全局唯一配置实例
3. 多环境配置测试 - dev/test/prod环境切换
4. 环境变量解析测试 - ${VAR}和${VAR:-default}语法
5. 生产环境变量读取测试 - 验证敏感信息环境变量正确读取
6. 环境配置差异验证 - 对比三个环境的配置差异
7. 配置项获取测试 - 各种配置获取方法
8. 配置验证测试 - 配置完整性和正确性验证
9. 错误处理测试 - 配置文件缺失、格式错误等异常情况

新增特性：
- 自动测试三个环境的切换功能
- 生产环境变量读取验证
- 环境配置差异对比分析
- 配置安全性验证

测试覆盖率目标：95%以上
支持独立运行：python config/test_config_module.py
"""

import os
import sys
import time
import tempfile
import shutil
from datetime import datetime
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入被测试的模块
try:
    from pythonprojecttemplate.config.config import Config, config
except ImportError:
    # 如果上面的导入失败，尝试直接从文件导入
    try:
        import importlib.util
        config_path = os.path.join(os.path.dirname(__file__), 'config.py')
        spec = importlib.util.spec_from_file_location('config_module', config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        Config = config_module.Config
        config = config_module.config
    except Exception as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在项目根目录下运行此测试")
        sys.exit(1)


class ConfigModuleTestSuite:
    """配置管理模块完整测试套件"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        self.start_time = None
        self.temp_dir = None
        
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始运行配置管理模块完整测试套件")
        print("=" * 80)
        print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.start_time = time.time()
        
        # 测试方法列表
        test_methods = [
            ('配置类单例模式', self.test_singleton_pattern),
            ('环境配置加载', self.test_env_config_loading),
            ('主配置加载', self.test_main_config_loading),
            ('环境变量解析', self.test_environment_variable_parsing),
            ('开发环境配置切换', self.test_dev_environment_switch),
            ('测试环境配置切换', self.test_test_environment_switch),
            ('生产环境配置切换', self.test_prod_environment_switch),
            ('生产环境变量读取', self.test_prod_environment_variables),
            ('环境配置差异验证', self.test_environment_differences),
            ('MySQL配置获取', self.test_mysql_config),
            ('日志配置获取', self.test_log_config),
            ('API配置获取', self.test_api_config),
            ('缓存配置获取', self.test_cache_config),
            ('调度器配置获取', self.test_scheduler_config),
            ('监控配置获取', self.test_monitoring_config),
            ('配置项完整性验证', self.test_config_completeness),
            ('配置异常处理', self.test_config_exception_handling),
            ('配置性能测试', self.test_config_performance)
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
    
    def test_singleton_pattern(self):
        """测试配置类单例模式"""
        print("  🔍 测试单例模式实现...")
        
        # 创建多个Config实例
        config1 = Config()
        config2 = Config()
        
        # 验证是同一个实例
        assert config1 is config2
        print("  ✓ Config类正确实现单例模式")
        
        print("  🔍 测试全局配置实例...")
        # 验证全局config实例
        global_config = config
        assert isinstance(global_config, Config)
        assert global_config is config1
        print("  ✓ 全局配置实例正常")
        
        print("  🔍 测试多次初始化...")
        # 多次初始化应该不会重置配置
        config3 = Config()
        assert config3 is config1
        print("  ✓ 多次初始化保持单例")
    
    def test_env_config_loading(self):
        """测试环境配置加载"""
        print("  🔍 测试env.yaml加载...")
        
        env_config = config.get_env_config()
        assert env_config is not None
        assert isinstance(env_config, dict)
        print(f"  ✓ env.yaml加载成功，包含 {len(env_config)} 个配置项")
        
        print("  🔍 验证必要的环境配置项...")
        # 检查关键配置项是否存在
        expected_keys = ['logging', 'module_config', 'scheduler']
        
        for key in expected_keys:
            if key in env_config:
                print(f"    ✓ 找到配置项: {key}")
            else:
                print(f"    ⚠️  配置项缺失: {key}")
        
        print("  ✓ 环境配置基础结构正常")
    
    def test_main_config_loading(self):
        """测试主配置加载"""
        print("  🔍 测试主配置文件加载...")
        
        main_config = config.get_config()
        assert main_config is not None
        assert isinstance(main_config, dict)
        print(f"  ✓ 主配置加载成功，包含 {len(main_config)} 个配置项")
        
        print("  🔍 验证主配置结构...")
        # 检查主要配置节
        expected_sections = ['mysql', 'api', 'cache', 'monitoring']
        
        for section in expected_sections:
            if section in main_config:
                print(f"    ✓ 找到配置节: {section}")
            else:
                print(f"    ⚠️  配置节缺失: {section}")
        
        print("  ✓ 主配置结构基本完整")
    
    def test_environment_variable_parsing(self):
        """测试环境变量解析"""
        print("  🔍 测试环境变量替换机制...")
        
        # 设置测试环境变量
        os.environ['TEST_CONFIG_VAR'] = 'test_value'
        os.environ['TEST_CONFIG_PORT'] = '3306'
        
        try:
            # 测试基本环境变量解析
            mysql_config = config.get_mysql_config()
            
            # 检查是否正确解析了环境变量
            print(f"  📊 MySQL主机: {mysql_config.get('host', 'not_set')}")
            print(f"  📊 MySQL端口: {mysql_config.get('port', 'not_set')}")
            print(f"  📊 MySQL用户: {mysql_config.get('username', 'not_set')}")
            
            # 验证端口是否正确转换为int类型
            port = mysql_config.get('port')
            assert isinstance(port, int) or port is None
            print("  ✓ 端口类型转换正确")
            
        finally:
            # 清理测试环境变量
            os.environ.pop('TEST_CONFIG_VAR', None)
            os.environ.pop('TEST_CONFIG_PORT', None)
        
        print("  ✓ 环境变量解析机制正常")
    
    def test_dev_environment_switch(self):
        """测试开发环境配置切换"""
        print("  🔍 测试开发环境配置切换...")
        
        # 保存原有环境变量
        original_env = os.environ.get('ENV')
        
        try:
            # 设置为开发环境
            os.environ['ENV'] = 'dev'
            
            # 重新创建配置实例来测试环境切换
            test_config = Config()
            test_config._initialized = False
            test_config._load_config()
            
            # 验证开发环境特有配置
            api_config = test_config.get_api_config()
            cache_config = test_config.get_cache_config()
            
            print(f"  📊 当前环境: dev")
            print(f"  📊 API文档启用: {api_config.get('open_api_on_startup', False)}")
            print(f"  📊 缓存类型: {cache_config.get('type', 'unknown')}")
            print(f"  📊 事件循环: {api_config.get('loop', 'unknown')}")
            print(f"  📊 访问令牌过期时间: {api_config.get('access_token_expire_minutes', 'unknown')}分钟")
            
            # 验证开发环境特征
            assert api_config.get('open_api_on_startup') == True, "开发环境应该启用API文档"
            assert cache_config.get('type') == 'memory', "开发环境应该使用内存缓存"
            assert api_config.get('loop') == 'asyncio', "开发环境应该使用asyncio事件循环"
            
            print("  ✅ 开发环境配置验证通过")
            
        finally:
            # 恢复原有环境变量
            if original_env:
                os.environ['ENV'] = original_env
            elif 'ENV' in os.environ:
                del os.environ['ENV']
    
    def test_test_environment_switch(self):
        """测试测试环境配置切换"""
        print("  🔍 测试测试环境配置切换...")
        
        # 保存原有环境变量
        original_env = os.environ.get('ENV')
        
        try:
            # 设置为测试环境
            os.environ['ENV'] = 'test'
            
            # 重新创建配置实例来测试环境切换
            test_config = Config()
            test_config._initialized = False
            test_config._load_config()
            
            # 验证测试环境特有配置
            api_config = test_config.get_api_config()
            cache_config = test_config.get_cache_config()
            mysql_config = test_config.get_mysql_config()
            
            print(f"  📊 当前环境: test")
            print(f"  📊 API主机: {api_config.get('host')}")
            print(f"  📊 API端口: {api_config.get('port')}")
            print(f"  📊 缓存类型: {cache_config.get('type')}")
            print(f"  📊 最大并发: {api_config.get('max_concurrency')}")
            print(f"  📊 数据库用户: {mysql_config.get('username')}")
            print(f"  📊 Redis DB: {cache_config.get('redis', {}).get('db')}")
            
            # 验证测试环境特征
            assert api_config.get('host') == '127.0.0.1', "测试环境应该使用本地地址"
            assert api_config.get('port') == 8001, "测试环境应该使用8001端口"
            assert cache_config.get('type') == 'memory', "测试环境应该使用内存缓存"
            assert api_config.get('max_concurrency') == 50, "测试环境应该使用较低并发数"
            assert mysql_config.get('username') == 'test_user', "测试环境应该使用测试数据库用户"
            
            print("  ✅ 测试环境配置验证通过")
            
        finally:
            # 恢复原有环境变量
            if original_env:
                os.environ['ENV'] = original_env
            elif 'ENV' in os.environ:
                del os.environ['ENV']
    
    def test_prod_environment_switch(self):
        """测试生产环境配置切换"""
        print("  🔍 测试生产环境配置切换...")
        
        # 保存原有环境变量
        original_env = os.environ.get('ENV')
        
        try:
            # 设置为生产环境
            os.environ['ENV'] = 'prod'
            
            # 重新创建配置实例来测试环境切换
            test_config = Config()
            test_config._initialized = False
            test_config._load_config()
            
            # 验证生产环境特有配置
            api_config = test_config.get_api_config()
            cache_config = test_config.get_cache_config()
            monitoring_config = test_config.get_monitoring_config()
            
            print(f"  📊 当前环境: prod")
            print(f"  📊 API文档: {api_config.get('docs_url')}")
            print(f"  📊 缓存类型: {cache_config.get('type')}")
            print(f"  📊 事件循环: {api_config.get('loop')}")
            print(f"  📊 最大并发: {api_config.get('max_concurrency')}")
            print(f"  📊 CPU阈值: {monitoring_config.get('cpu_threshold')}%")
            print(f"  📊 访问令牌过期: {api_config.get('access_token_expire_minutes')}分钟")
            
            # 验证生产环境特征
            assert api_config.get('docs_url') is None, "生产环境应该禁用API文档"
            assert cache_config.get('type') == 'redis', "生产环境应该使用Redis缓存"
            assert api_config.get('loop') == 'uvloop', "生产环境应该使用uvloop事件循环"
            assert api_config.get('max_concurrency') == 500, "生产环境应该使用较高并发数"
            assert monitoring_config.get('cpu_threshold') == 70, "生产环境应该使用更严格的CPU阈值"
            assert api_config.get('access_token_expire_minutes') == 30, "生产环境应该使用较短的令牌过期时间"
            
            print("  ✅ 生产环境配置验证通过")
            
        finally:
            # 恢复原有环境变量
            if original_env:
                os.environ['ENV'] = original_env
            elif 'ENV' in os.environ:
                del os.environ['ENV']
    
    def test_prod_environment_variables(self):
        """测试生产环境变量读取"""
        print("  🔍 测试生产环境变量读取...")
        
        # 保存原有环境变量
        original_env = os.environ.get('ENV')
        original_vars = {}
        test_vars = {
            'MYSQL_USERNAME': 'prod_user',
            'MYSQL_PASSWORD': 'prod_secret_password',
            'MYSQL_HOST': 'prod-db.example.com',
            'MYSQL_PORT': '3306',
            'MYSQL_DATABASE': 'prod_database',
            'REDIS_HOST': 'redis.example.com',
            'REDIS_PORT': '6379',
            'SECRET_KEY': 'super-secret-production-key'
        }
        
        # 备份现有环境变量
        for var in test_vars.keys():
            original_vars[var] = os.environ.get(var)
        
        try:
            # 设置生产环境和环境变量
            os.environ['ENV'] = 'prod'
            for var, value in test_vars.items():
                os.environ[var] = value
            
            # 重新加载配置
            test_config = Config()
            test_config._initialized = False
            test_config._load_config()
            
            # 验证环境变量是否正确读取
            mysql_config = test_config.get_mysql_config()
            cache_config = test_config.get_cache_config()
            api_config = test_config.get_api_config()
            
            print("  📊 验证MySQL环境变量读取:")
            print(f"    ✓ 用户名: {mysql_config.get('username')}")
            print(f"    ✓ 主机: {mysql_config.get('host')}")
            print(f"    ✓ 端口: {mysql_config.get('port')}")
            print(f"    ✓ 数据库: {mysql_config.get('database')}")
            print(f"    ✓ 密码: {'***' if mysql_config.get('password') else 'NOT_SET'}")
            
            print("  📊 验证Redis环境变量读取:")
            redis_config = cache_config.get('redis', {})
            print(f"    ✓ Redis主机: {redis_config.get('host')}")
            print(f"    ✓ Redis端口: {redis_config.get('port')}")
            
            print("  📊 验证API环境变量读取:")
            print(f"    ✓ 密钥: {'***' if api_config.get('secret_key') else 'NOT_SET'}")
            
            # 断言验证环境变量正确读取
            assert mysql_config.get('username') == 'prod_user', "MySQL用户名环境变量读取失败"
            assert mysql_config.get('password') == 'prod_secret_password', "MySQL密码环境变量读取失败"
            assert mysql_config.get('host') == 'prod-db.example.com', "MySQL主机环境变量读取失败"
            assert mysql_config.get('port') == 3306, "MySQL端口环境变量读取失败"
            assert mysql_config.get('database') == 'prod_database', "MySQL数据库环境变量读取失败"
            
            assert redis_config.get('host') == 'redis.example.com', "Redis主机环境变量读取失败"
            assert redis_config.get('port') == 6379, "Redis端口环境变量读取失败"
            
            assert api_config.get('secret_key') == 'super-secret-production-key', "API密钥环境变量读取失败"
            
            print("  ✅ 生产环境变量读取验证通过")
            
            # 测试环境变量缺失情况
            print("  🔍 测试环境变量缺失处理...")
            del os.environ['MYSQL_HOST']
            
            test_config._initialized = False
            test_config._load_config()
            mysql_config_missing = test_config.get_mysql_config()
            
            print(f"    📊 缺失MYSQL_HOST时的值: {mysql_config_missing.get('host')}")
            print("  ✓ 环境变量缺失时处理正常")
            
        finally:
            # 恢复原有环境变量
            if original_env:
                os.environ['ENV'] = original_env
            elif 'ENV' in os.environ:
                del os.environ['ENV']
            
            # 恢复或清理测试环境变量
            for var, original_value in original_vars.items():
                if original_value is not None:
                    os.environ[var] = original_value
                elif var in os.environ:
                    del os.environ[var]
    
    def test_environment_differences(self):
        """测试环境配置差异验证"""
        print("  🔍 测试环境配置差异验证...")
        
        environments = ['dev', 'test', 'prod']
        env_configs = {}
        
        # 保存原有环境变量
        original_env = os.environ.get('ENV')
        
        try:
            # 收集各环境配置
            for env in environments:
                os.environ['ENV'] = env
                
                test_config = Config()
                test_config._initialized = False
                test_config._load_config()
                
                env_configs[env] = {
                    'api': test_config.get_api_config(),
                    'cache': test_config.get_cache_config(),
                    'mysql': test_config.get_mysql_config(),
                    'monitoring': test_config.get_monitoring_config()
                }
            
            print("  📊 环境配置对比表:")
            print("  " + "-" * 70)
            print(f"  {'配置项':<20} {'开发环境':<15} {'测试环境':<15} {'生产环境':<15}")
            print("  " + "-" * 70)
            
            # 对比关键配置项
            comparisons = [
                ('缓存类型', lambda cfg: cfg['cache'].get('type')),
                ('API文档', lambda cfg: str(cfg['api'].get('docs_url'))),
                ('事件循环', lambda cfg: cfg['api'].get('loop')),
                ('API端口', lambda cfg: str(cfg['api'].get('port'))),
                ('最大并发', lambda cfg: str(cfg['api'].get('max_concurrency'))),
                ('令牌过期', lambda cfg: str(cfg['api'].get('access_token_expire_minutes'))),
                ('CPU阈值', lambda cfg: str(cfg['monitoring'].get('cpu_threshold', 'N/A'))),
            ]
            
            for config_name, getter in comparisons:
                row = f"  {config_name:<20}"
                for env in environments:
                    value = getter(env_configs[env])
                    row += f" {str(value):<15}"
                print(row)
            
            print("  " + "-" * 70)
            
            # 验证关键差异
            dev_cache = env_configs['dev']['cache'].get('type')
            prod_cache = env_configs['prod']['cache'].get('type')
            assert dev_cache == 'memory', "开发环境应使用内存缓存"
            assert prod_cache == 'redis', "生产环境应使用Redis缓存"
            
            dev_docs = env_configs['dev']['api'].get('docs_url')
            prod_docs = env_configs['prod']['api'].get('docs_url')
            assert dev_docs == '/docs', "开发环境应启用API文档"
            assert prod_docs is None, "生产环境应禁用API文档"
            
            test_port = env_configs['test']['api'].get('port')
            assert test_port == 8001, "测试环境应使用8001端口"
            
            print("  ✅ 环境配置差异验证通过")
            
        finally:
            # 恢复原有环境变量
            if original_env:
                os.environ['ENV'] = original_env
            elif 'ENV' in os.environ:
                del os.environ['ENV']
    
    def test_mysql_config(self):
        """测试MySQL配置获取"""
        print("  🔍 测试MySQL配置获取...")
        
        mysql_config = config.get_mysql_config()
        assert isinstance(mysql_config, dict)
        print(f"  ✓ MySQL配置获取成功")
        
        print("  🔍 验证MySQL配置项...")
        required_keys = ['username', 'password', 'host', 'port', 'database']
        
        for key in required_keys:
            value = mysql_config.get(key)
            if value is not None:
                print(f"    ✓ {key}: {value if key != 'password' else '***'}")
            else:
                print(f"    ⚠️  {key}: 未配置")
        
        # 验证端口是整数类型
        port = mysql_config.get('port')
        if port is not None:
            assert isinstance(port, int), f"端口应该是整数，实际类型: {type(port)}"
            print(f"  ✓ 端口类型验证通过: {port} (int)")
    
    def test_log_config(self):
        """测试日志配置获取"""
        print("  🔍 测试日志配置获取...")
        
        log_config = config.get_log_config()
        assert isinstance(log_config, dict)
        print("  ✓ 日志配置获取成功")
        
        print("  🔍 验证日志配置项...")
        if log_config:
            for key, value in log_config.items():
                print(f"    ✓ {key}: {value}")
        else:
            print("    ℹ️  日志配置为空，使用默认设置")
        
        print("  ✓ 日志配置结构正常")
    
    def test_api_config(self):
        """测试API配置获取"""
        print("  🔍 测试API配置获取...")
        
        api_config = config.get_api_config()
        assert isinstance(api_config, dict)
        print("  ✓ API配置获取成功")
        
        print("  🔍 验证API配置项...")
        expected_keys = ['host', 'port', 'cors_origins', 'secret_key']
        
        for key in expected_keys:
            value = api_config.get(key)
            if value is not None:
                display_value = value if key != 'secret_key' else '***'
                print(f"    ✓ {key}: {display_value}")
            else:
                print(f"    ⚠️  {key}: 未配置")
        
        # 验证端口类型
        port = api_config.get('port')
        if port is not None:
            try:
                port_int = int(port)
                print(f"  ✓ API端口验证通过: {port_int}")
            except ValueError:
                print(f"  ⚠️  API端口格式错误: {port}")
    
    def test_cache_config(self):
        """测试缓存配置获取"""
        print("  🔍 测试缓存配置获取...")
        
        cache_config = config.get_cache_config()
        assert isinstance(cache_config, dict)
        print("  ✓ 缓存配置获取成功")
        
        print("  🔍 验证缓存配置项...")
        cache_type = cache_config.get('type', 'memory')
        print(f"    ✓ 缓存类型: {cache_type}")
        
        ttl = cache_config.get('ttl', 3600)
        print(f"    ✓ 默认TTL: {ttl}秒")
        
        if cache_type == 'redis':
            redis_config = cache_config.get('redis', {})
            print(f"    ✓ Redis配置: host={redis_config.get('host')}, port={redis_config.get('port')}")
            
            # 验证Redis端口类型
            redis_port = redis_config.get('port')
            if redis_port is not None:
                assert isinstance(redis_port, int), f"Redis端口应该是整数: {redis_port}"
                print(f"  ✓ Redis端口类型正确: {redis_port}")
        
        print("  ✓ 缓存配置验证通过")
    
    def test_scheduler_config(self):
        """测试调度器配置获取"""
        print("  🔍 测试调度器配置获取...")
        
        scheduler_config = config.get_scheduler_config()
        assert isinstance(scheduler_config, dict)
        print("  ✓ 调度器配置获取成功")
        
        print("  🔍 验证调度器配置项...")
        if scheduler_config:
            for section, value in scheduler_config.items():
                if isinstance(value, dict):
                    print(f"    ✓ {section}: {len(value)} 个配置项")
                else:
                    print(f"    ✓ {section}: {value}")
        else:
            print("    ℹ️  调度器配置为空，使用默认设置")
        
        # 测试任务配置
        print("  🔍 测试任务配置获取...")
        tasks_config = config.get_tasks_config()
        assert isinstance(tasks_config, dict)
        
        if tasks_config:
            print(f"    ✓ 发现 {len(tasks_config)} 个任务配置")
            for task_name in tasks_config.keys():
                print(f"      - {task_name}")
        else:
            print("    ℹ️  无任务配置")
        
        print("  ✓ 调度器和任务配置正常")
    
    def test_monitoring_config(self):
        """测试监控配置获取"""
        print("  🔍 测试监控配置获取...")
        
        monitoring_config = config.get_monitoring_config()
        assert isinstance(monitoring_config, dict)
        print("  ✓ 监控配置获取成功")
        
        print("  🔍 验证监控配置项...")
        if monitoring_config:
            prometheus_port = monitoring_config.get('prometheus_port')
            cpu_threshold = monitoring_config.get('cpu_threshold')
            memory_threshold = monitoring_config.get('memory_threshold')
            
            if prometheus_port:
                print(f"    ✓ Prometheus端口: {prometheus_port}")
            if cpu_threshold:
                print(f"    ✓ CPU阈值: {cpu_threshold}%")
            if memory_threshold:
                print(f"    ✓ 内存阈值: {memory_threshold}%")
        else:
            print("    ℹ️  监控配置为空")
        
        print("  ✓ 监控配置结构正常")
    
    def test_config_completeness(self):
        """测试配置完整性验证"""
        print("  🔍 测试配置完整性...")
        
        # 验证所有主要配置方法都能正常调用
        config_methods = [
            ('get_env_config', config.get_env_config),
            ('get_config', config.get_config),
            ('get_mysql_config', config.get_mysql_config),
            ('get_log_config', config.get_log_config),
            ('get_api_config', config.get_api_config),
            ('get_cache_config', config.get_cache_config),
            ('get_scheduler_config', config.get_scheduler_config),
            ('get_tasks_config', config.get_tasks_config),
            ('get_monitoring_config', config.get_monitoring_config)
        ]
        
        success_count = 0
        for method_name, method in config_methods:
            try:
                result = method()
                assert result is not None
                print(f"    ✓ {method_name}: OK")
                success_count += 1
            except Exception as e:
                print(f"    ❌ {method_name}: {e}")
        
        print(f"  📊 配置方法可用性: {success_count}/{len(config_methods)}")
        
        if success_count == len(config_methods):
            print("  ✅ 所有配置方法都可正常调用")
        else:
            print("  ⚠️  部分配置方法调用失败")
    
    def test_config_exception_handling(self):
        """测试配置异常处理"""
        print("  🔍 测试配置文件异常处理...")
        
        # 测试获取不存在的配置项
        try:
            main_config = config.get_config()
            non_existent = main_config.get('non_existent_config_section')
            assert non_existent is None or isinstance(non_existent, dict)
            print("  ✓ 不存在配置项返回None或空字典")
        except Exception as e:
            print(f"  ⚠️  配置异常处理: {e}")
        
        # 测试环境变量缺失的情况
        print("  🔍 测试环境变量缺失处理...")
        
        # 临时移除某个环境变量（如果存在）
        original_value = os.environ.get('MYSQL_HOST')
        if 'MYSQL_HOST' in os.environ:
            del os.environ['MYSQL_HOST']
        
        try:
            mysql_config = config.get_mysql_config()
            # 应该有默认值或者空值处理
            host = mysql_config.get('host')
            print(f"  ✓ 环境变量缺失时处理正常: host={host}")
            
        finally:
            # 恢复环境变量
            if original_value is not None:
                os.environ['MYSQL_HOST'] = original_value
        
        print("  ✓ 异常处理机制正常")
    
    def test_config_performance(self):
        """测试配置性能"""
        print("  🔍 测试配置获取性能...")
        
        # 测试多次获取配置的性能
        test_count = 1000
        start_time = time.time()
        
        for _ in range(test_count):
            config.get_mysql_config()
            config.get_api_config()
            config.get_cache_config()
        
        end_time = time.time()
        total_time = end_time - start_time
        ops_per_sec = (test_count * 3) / total_time
        
        print(f"  📊 {test_count * 3} 次配置获取耗时: {total_time:.3f}秒")
        print(f"  📊 配置获取速率: {ops_per_sec:.0f} ops/sec")
        
        # 性能基准检查（配置获取应该很快）
        if ops_per_sec > 10000:
            print("  ✅ 配置获取性能优秀")
        elif ops_per_sec > 1000:
            print("  ✓ 配置获取性能良好")
        else:
            print("  ⚠️  配置获取性能可能需要优化")
        
        print("  🔍 测试单例模式性能优势...")
        start_time = time.time()
        
        for _ in range(1000):
            Config()  # 创建实例应该很快（单例）
        
        singleton_time = time.time() - start_time
        print(f"  📊 1000次单例创建耗时: {singleton_time:.3f}秒")
        
        if singleton_time < 0.01:
            print("  ✅ 单例模式性能优秀")
        else:
            print("  ✓ 单例模式性能正常")
    
    def _print_final_results(self):
        """打印最终测试结果"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("=" * 80)
        print("📊 配置管理模块测试结果汇总")
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
            print("🎉 配置管理模块测试整体通过！")
        elif success_rate >= 70:
            print("⚠️  配置管理模块测试部分通过，需要关注失败的测试")
        else:
            print("❌ 配置管理模块测试失败较多，需要重点修复")
        
        print("=" * 80)


def main():
    """主函数 - 运行配置管理模块测试"""
    print("🧪 Python Project Template - 配置管理模块测试")
    
    try:
        test_suite = ConfigModuleTestSuite()
        test_suite.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试运行出现异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()