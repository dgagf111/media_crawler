import pytest
import os
import sys
import argparse
import time
import subprocess
from datetime import datetime
from typing import List

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from pythonprojecttemplate.log.logHelper import get_logger

logger = get_logger()


class UnifiedTestRunner:
    """统一测试运行器 - 支持所有类型的测试"""
    
    def __init__(self):
        self.available_modules = {
            'cache': {
                'name': '缓存系统',
                'script': 'src/pythonprojecttemplate/cache/test_cache_module.py',
                'description': '测试内存缓存、Redis缓存、缓存管理器等功能'
            },
            'config': {
                'name': '配置管理',
                'script': 'src/pythonprojecttemplate/config/test_config_module.py',
                'description': '测试配置文件加载、环境变量解析、配置获取等功能'
            },
            'database': {
                'name': '数据库系统',
                'script': 'src/pythonprojecttemplate/db/test_database_module.py',
                'description': '测试数据库连接、事务管理、CRUD操作等功能'
            },
            'scheduler': {
                'name': '任务调度',
                'script': 'src/pythonprojecttemplate/scheduler/test_scheduler_module.py',
                'description': '测试任务调度、触发器、重试机制等功能'
            },
            'monitoring': {
                'name': '监控系统',
                'script': 'src/pythonprojecttemplate/monitoring/test_monitoring_module.py',
                'description': '测试Prometheus指标、系统监控、告警等功能'
            },
            'log': {
                'name': '日志系统',
                'script': 'src/pythonprojecttemplate/log/test_log_module.py',
                'description': '测试日志记录、文件管理、异常处理等功能'
            },
            'api': {
                'name': 'API服务',
                'script': 'src/pythonprojecttemplate/api/test_api_module.py',
                'description': '测试API路由、认证系统、响应模型等功能'
            },
            'utils': {
                'name': '工具类库',
                'script': 'src/pythonprojecttemplate/utils/test_utils_module.py',
                'description': '测试加密工具、Excel处理、HTTP工具等功能'
            }
        }
        
        self.test_results = {}
        self.total_start_time = None
    
    def _run_single_module_test(self, module: str) -> bool:
        """运行单个模块测试"""
        info = self.available_modules[module]
        script_path = info['script']
        
        # 检查测试脚本是否存在
        if not os.path.exists(script_path):
            print(f"❌ 测试脚本不存在: {script_path}")
            self.test_results[module] = {
                'success': False,
                'error': f"测试脚本不存在: {script_path}",
                'duration': 0,
                'output': ''
            }
            return False
        
        # 运行测试
        start_time = time.time()
        
        try:
            print(f"📂 执行脚本: {script_path}")
            
            # 使用subprocess运行测试脚本
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                print(f"✅ {info['name']}模块测试成功")
                print(f"⏱️  耗时: {duration:.2f}秒")
                
                self.test_results[module] = {
                    'success': True,
                    'duration': duration,
                    'output': result.stdout,
                    'error': result.stderr
                }
                return True
            else:
                print(f"❌ {info['name']}模块测试失败")
                print(f"⏱️  耗时: {duration:.2f}秒")
                print(f"返回码: {result.returncode}")
                
                if result.stderr:
                    print("错误输出:")
                    print(result.stderr[:500])  # 限制错误输出长度
                
                self.test_results[module] = {
                    'success': False,
                    'duration': duration,
                    'output': result.stdout,
                    'error': result.stderr,
                    'return_code': result.returncode
                }
                return False
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            print(f"⏰ {info['name']}模块测试超时 (>300秒)")
            
            self.test_results[module] = {
                'success': False,
                'duration': duration,
                'error': '测试超时',
                'output': ''
            }
            return False
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 {info['name']}模块测试异常: {e}")
            
            self.test_results[module] = {
                'success': False,
                'duration': duration,
                'error': str(e),
                'output': ''
            }
            return False
    
    def _print_summary_results(self, modules: List[str], success_count: int):
        """打印汇总结果"""
        total_time = time.time() - self.total_start_time
        
        print("=" * 80)
        print("📊 模块测试结果汇总")
        print("=" * 80)
        
        print(f"⏱️  总耗时: {total_time:.2f}秒")
        print(f"📈 测试模块数: {len(modules)}")
        print(f"✅ 成功模块: {success_count}")
        print(f"❌ 失败模块: {len(modules) - success_count}")
        
        success_rate = (success_count / len(modules)) * 100
        print(f"🎯 成功率: {success_rate:.1f}%")
        
        if success_count < len(modules):
            print("\n❌ 失败的模块详情:")
            for module in modules:
                if module in self.test_results and not self.test_results[module]['success']:
                    info = self.available_modules[module]
                    error = self.test_results[module].get('error', '未知错误')
                    print(f"   ❌ {module} ({info['name']}): {error}")
        
        print("\n" + "=" * 80)
        
        if success_rate >= 90:
            print("🎉 模块测试整体通过！")
        elif success_rate >= 70:
            print("⚠️  模块测试部分通过，需要关注失败的测试")
        else:
            print("❌ 模块测试失败较多，需要重点修复")
        
        print("=" * 80)

def run_integration_tests():
    """运行整体框架集成测试"""
    logger.info("开始运行整体框架集成测试...")
    
    # 直接运行集成测试脚本
    integration_test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_framework_integration.py')
    
    if os.path.exists(integration_test_path):
        logger.info("执行整体框架集成测试")
        # 使用subprocess运行集成测试
        import subprocess
        result = subprocess.run([sys.executable, integration_test_path], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            logger.info("整体框架集成测试完成")
        else:
            logger.error("整体框架集成测试失败")
    else:
        logger.error("集成测试文件不存在")


def run_module_tests(modules: List[str]):
    """运行指定模块的详细测试"""
    runner = UnifiedTestRunner()
    
    print("🧪 Python Project Template - 模块测试运行器")
    print("=" * 80)
    print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    runner.total_start_time = time.time()
    
    # 验证模块名称
    if 'all' in modules:
        modules = list(runner.available_modules.keys())
    
    invalid_modules = [m for m in modules if m not in runner.available_modules]
    if invalid_modules:
        print(f"❌ 无效的模块名称: {', '.join(invalid_modules)}")
        print(f"可用模块: {', '.join(runner.available_modules.keys())}")
        return False
    
    # 显示测试计划
    print("📋 测试计划:")
    for module in modules:
        info = runner.available_modules[module]
        print(f"  🔹 {module}: {info['name']} - {info['description']}")
    print()
    
    # 运行测试
    success_count = 0
    for i, module in enumerate(modules, 1):
        print(f"[{i}/{len(modules)}] 🚀 运行{module}模块测试...")
        print("-" * 60)
        
        if runner._run_single_module_test(module):
            success_count += 1
        
        print()
    
    # 输出汇总结果
    runner._print_summary_results(modules, success_count)


def run_framework_tests(module=None):
    """运行框架测试"""
    logger.info(f"开始运行框架测试{'（' + module + '）' if module else ''}...")
    framework_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'framework')
    
    if module:
        test_path = os.path.join(framework_dir, module)
        if not os.path.exists(test_path):
            logger.error(f"指定的模块 '{module}' 不存在")
            return
    else:
        test_path = framework_dir

    pytest.main(['-v', '--tb=short', '-s', test_path])

    logger.info("框架测试运行完成")

def run_business_tests(module=None):
    """运行业务测试"""
    logger.info(f"开始运行业务测试{'（' + module + '）' if module else ''}...")
    business_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'business')
    
    if module:
        test_path = os.path.join(business_dir, module)
        if not os.path.exists(test_path):
            logger.error(f"指定的模块 '{module}' 不存在")
            return
    else:
        test_path = business_dir

    pytest.main(['-v', '--tb=short', '-s', test_path])

    logger.info("业务测试运行完成")

def run_all_tests():
    """运行所有测试"""
    logger.info("开始运行所有测试...")
    
    # 首先运行整体框架集成测试
    print("🎆 步骤1: 运行整体框架集成测试")
    print("=" * 80)
    run_integration_tests()
    print("\n")
    
    # 然后运行所有模块的详细测试
    print("🎆 步骤2: 运行所有模块详细测试")
    print("=" * 80)
    run_module_tests(['all'])
    print("\n")
    
    # 最后运行传统的框架和业务测试
    print("🎆 步骤3: 运行框架和业务测试")
    print("=" * 80)
    run_framework_tests()
    run_business_tests()
    
    logger.info("所有测试运行完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="统一测试运行器 - 支持所有类型的测试")
    parser.add_argument("test_type", 
                       choices=["all", "framework", "business", "integration", "modules"], 
                       help="指定要运行的测试类型")
    parser.add_argument("--module", 
                       help="指定要测试的模块（适用于 framework 和 business 测试类型）")
    parser.add_argument("modules", nargs="*", 
                       help="指定要运行的模块测试（适用于 modules 类型）")
    
    args = parser.parse_args()
    
    if args.test_type == "all":
        run_all_tests()
    elif args.test_type == "framework":
        run_framework_tests(args.module)
    elif args.test_type == "business":
        run_business_tests(args.module)
    elif args.test_type == "integration":
        run_integration_tests()
    elif args.test_type == "modules":
        modules_to_test = args.modules if args.modules else ['all']
        run_module_tests(modules_to_test)
    
    print("\n🎆 测试运行器使用示例:")
    print("python tests/run_tests.py all                    # 运行所有测试")
    print("python tests/run_tests.py integration           # 运行集成测试")
    print("python tests/run_tests.py modules all           # 运行所有模块测试")
    print("python tests/run_tests.py modules config cache  # 运行指定模块测试")
    print("python tests/run_tests.py framework --module api # 运行指定框架测试")
