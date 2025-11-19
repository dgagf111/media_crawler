#!/usr/bin/env python3
"""
配置管理模块快速测试运行器

用法：
  python config/run_config_tests.py         # 运行所有配置测试
  python config/run_config_tests.py --env   # 只运行环境切换测试
  python config/run_config_tests.py --prod  # 只运行生产环境变量测试
"""

import os
import sys
import argparse

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入测试套件（采用直接导入方式避免包导入问题）
try:
    from pythonprojecttemplate.config.test_config_module import ConfigModuleTestSuite
except ImportError:
    # 如果包导入失败，尝试直接文件导入
    import importlib.util
    test_module_path = os.path.join(os.path.dirname(__file__), 'test_config_module.py')
    spec = importlib.util.spec_from_file_location('test_config_module', test_module_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    ConfigModuleTestSuite = test_module.ConfigModuleTestSuite


def run_environment_tests_only():
    """只运行环境切换相关测试"""
    print("🧪 Python Project Template - 配置环境切换测试")
    print("=" * 80)
    
    suite = ConfigModuleTestSuite()
    
    # 只运行环境相关的测试
    env_test_methods = [
        ('开发环境配置切换', suite.test_dev_environment_switch),
        ('测试环境配置切换', suite.test_test_environment_switch),
        ('生产环境配置切换', suite.test_prod_environment_switch),
        ('环境配置差异验证', suite.test_environment_differences)
    ]
    
    suite.start_time = __import__('time').time()
    
    for test_name, test_method in env_test_methods:
        suite._run_single_test(test_name, test_method)
    
    suite._print_final_results()


def run_prod_env_tests_only():
    """只运行生产环境变量测试"""
    print("🧪 Python Project Template - 生产环境变量测试")
    print("=" * 80)
    
    suite = ConfigModuleTestSuite()
    
    # 只运行生产环境变量测试
    prod_test_methods = [
        ('生产环境配置切换', suite.test_prod_environment_switch),
        ('生产环境变量读取', suite.test_prod_environment_variables)
    ]
    
    suite.start_time = __import__('time').time()
    
    for test_name, test_method in prod_test_methods:
        suite._run_single_test(test_name, test_method)
    
    suite._print_final_results()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='配置管理模块测试运行器')
    parser.add_argument('--env', action='store_true', help='只运行环境切换测试')
    parser.add_argument('--prod', action='store_true', help='只运行生产环境变量测试')
    parser.add_argument('--quick', action='store_true', help='运行快速测试（不包含性能测试）')
    
    args = parser.parse_args()
    
    if args.env:
        run_environment_tests_only()
    elif args.prod:
        run_prod_env_tests_only()
    else:
        # 运行完整测试
        suite = ConfigModuleTestSuite()
        suite.run_all_tests()


if __name__ == "__main__":
    main()
