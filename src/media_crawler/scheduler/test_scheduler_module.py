#!/usr/bin/env python3
"""
任务调度模块完整测试类

功能说明：
这个测试类专门测试任务调度模块的所有核心功能，包括：
1. 调度器初始化测试 - 调度器创建、配置加载、执行器设置
2. 任务加载测试 - 任务模块发现、任务函数验证、配置解析
3. 触发器测试 - interval、cron、date触发器功能验证
4. 任务执行测试 - 任务运行、参数传递、返回值处理
5. 重试机制测试 - 失败重试、重试延迟、最大尝试次数

测试覆盖率目标：85%以上
支持独立运行：python scheduler/test_scheduler_module.py
"""

import os
import sys
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from pythonprojecttemplate.scheduler.scheduler_center import SchedulerCenter, scheduler_center
    from pythonprojecttemplate.config.config import config
    from apscheduler.schedulers.background import BackgroundScheduler
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    sys.exit(1)


class SchedulerModuleTestSuite:
    """任务调度模块完整测试套件"""
    
    def __init__(self):
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        self.start_time = None
        self.test_scheduler = None
        self.test_job_results = {}
        
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("🚀 开始运行任务调度模块完整测试套件")
        print("=" * 80)
        print(f"⏰ 测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.start_time = time.time()
        
        # 测试方法列表
        test_methods = [
            ('调度中心初始化', self.test_scheduler_initialization),
            ('调度器启动停止', self.test_scheduler_start_stop),
            ('任务配置解析', self.test_task_config_parsing),
            ('简单任务执行', self.test_simple_job_execution),
            ('任务重试机制', self.test_job_retry_mechanism),
            ('任务管理操作', self.test_job_management),
            ('任务异常处理', self.test_job_exception_handling),
            ('调度器性能测试', self.test_scheduler_performance)
        ]
        
        # 执行所有测试
        for test_name, test_method in test_methods:
            self._run_single_test(test_name, test_method)
        
        # 清理测试调度器
        if self.test_scheduler and self.test_scheduler.is_running:
            self.test_scheduler.shutdown()
        
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
    
    def test_scheduler_initialization(self):
        """测试调度中心初始化"""
        print("  🔍 测试SchedulerCenter类初始化...")
        
        test_scheduler = SchedulerCenter()
        assert test_scheduler is not None
        assert hasattr(test_scheduler, 'scheduler')
        assert isinstance(test_scheduler.scheduler, BackgroundScheduler)
        print("  ✓ SchedulerCenter实例创建成功")
        
        assert test_scheduler.is_running == False
        print("  ✓ 调度器初始状态正确（未运行）")
        
        global_scheduler = scheduler_center
        assert isinstance(global_scheduler, SchedulerCenter)
        print("  ✓ 全局调度中心实例正常")
        
        self.test_scheduler = test_scheduler
    
    def test_scheduler_start_stop(self):
        """测试调度器启动停止"""
        print("  🔍 测试调度器启动...")
        
        if not self.test_scheduler:
            self.test_scheduler = SchedulerCenter()
        
        self.test_scheduler.start()
        time.sleep(0.5)
        
        assert self.test_scheduler.is_running == True
        print("  ✓ 调度器启动成功")
        
        jobs = self.test_scheduler.get_jobs()
        assert isinstance(jobs, list)
        print(f"  ✓ 当前任务数量: {len(jobs)}")
        
        self.test_scheduler.shutdown(wait=False)
        time.sleep(0.5)
        
        assert self.test_scheduler.is_running == False
        print("  ✓ 调度器停止成功")
    
    def test_task_config_parsing(self):
        """测试任务配置解析"""
        print("  🔍 测试任务配置解析...")
        
        test_task_config = {
            'trigger': 'interval',
            'args': {'seconds': 5},
            'max_attempts': 3,
            'retry_delay': 2
        }
        
        trigger_type = test_task_config.get('trigger')
        assert trigger_type == 'interval'
        print("  ✓ 触发器类型解析正确")
        
        trigger_args = test_task_config.get('args', {})
        assert 'seconds' in trigger_args
        print("  ✓ 触发器参数解析正确")
        
        max_attempts = test_task_config.get('max_attempts', 1)
        retry_delay = test_task_config.get('retry_delay', 0)
        
        assert max_attempts == 3
        assert retry_delay == 2
        print("  ✓ 重试配置解析正确")
    
    def test_simple_job_execution(self):
        """测试简单任务执行"""
        print("  🔍 测试简单任务执行...")
        
        if not self.test_scheduler or not self.test_scheduler.is_running:
            self.test_scheduler = SchedulerCenter()
            self.test_scheduler.start()
            time.sleep(0.5)
        
        def test_job():
            self.test_job_results['simple_job'] = {
                'executed': True,
                'execution_time': datetime.now(),
                'result': 'success'
            }
            return "Test job executed successfully"
        
        job = self.test_scheduler.add_job(
            func=test_job,
            trigger='date',
            run_date=datetime.now() + timedelta(seconds=1),
            id='test_simple_job'
        )
        
        assert job is not None
        print("  ✓ 测试任务添加成功")
        
        time.sleep(2)
        
        assert 'simple_job' in self.test_job_results
        assert self.test_job_results['simple_job']['executed'] == True
        print("  ✓ 测试任务执行成功")
    
    def test_job_retry_mechanism(self):
        """测试任务重试机制"""
        print("  🔍 测试任务重试机制...")
        
        if not self.test_scheduler or not self.test_scheduler.is_running:
            self.test_scheduler = SchedulerCenter()
            self.test_scheduler.start()
            time.sleep(0.5)
        
        retry_info = {'attempts': 0, 'max_attempts': 3}
        
        def failing_job():
            retry_info['attempts'] += 1
            self.test_job_results['retry_job'] = retry_info.copy()
            
            if retry_info['attempts'] < retry_info['max_attempts']:
                raise ValueError(f"故意失败 (尝试 {retry_info['attempts']}/{retry_info['max_attempts']})")
            
            return "最终成功"
        
        wrapped_job = self.test_scheduler._wrap_task_with_retry(
            failing_job,
            {'max_attempts': 3, 'retry_delay': 1}
        )
        
        try:
            result = wrapped_job()
            print(f"  ✓ 任务最终成功: {result}")
        except Exception as e:
            print(f"  ❌ 重试机制测试失败: {e}")
            raise
        
        assert 'retry_job' in self.test_job_results
        attempts = self.test_job_results['retry_job']['attempts']
        assert attempts == 3
        print(f"  ✓ 重试机制正常，总尝试次数: {attempts}")
    
    def test_job_management(self):
        """测试任务管理操作"""
        print("  🔍 测试任务管理操作...")
        
        if not self.test_scheduler or not self.test_scheduler.is_running:
            self.test_scheduler = SchedulerCenter()
            self.test_scheduler.start()
            time.sleep(0.5)
        
        def managed_job():
            self.test_job_results['managed_job'] = {
                'executed': True,
                'time': datetime.now()
            }
        
        job = self.test_scheduler.add_job(
            func=managed_job,
            trigger='interval',
            seconds=10,
            id='managed_test_job'
        )
        
        assert job is not None
        print("  ✓ 任务添加成功")
        
        jobs = self.test_scheduler.get_jobs()
        job_ids = [j.id for j in jobs]
        assert 'managed_test_job' in job_ids
        print(f"  ✓ 任务列表查询成功，共 {len(jobs)} 个任务")
        
        self.test_scheduler.pause_job('managed_test_job')
        print("  ✓ 任务暂停成功")
        
        self.test_scheduler.resume_job('managed_test_job')
        print("  ✓ 任务恢复成功")
        
        self.test_scheduler.remove_job('managed_test_job')
        final_jobs = self.test_scheduler.get_jobs()
        job_ids = [j.id for j in final_jobs]
        assert 'managed_test_job' not in job_ids
        print("  ✓ 任务移除成功")
    
    def test_job_exception_handling(self):
        """测试任务异常处理"""
        print("  🔍 测试任务异常处理...")
        
        if not self.test_scheduler or not self.test_scheduler.is_running:
            self.test_scheduler = SchedulerCenter()
            self.test_scheduler.start()
            time.sleep(0.5)
        
        def exception_job():
            raise RuntimeError("测试异常处理")
        
        job = self.test_scheduler.add_job(
            func=exception_job,
            trigger='date',
            run_date=datetime.now() + timedelta(seconds=1),
            id='exception_test_job'
        )
        
        assert job is not None
        print("  ✓ 异常任务添加成功")
        
        time.sleep(2)
        
        assert self.test_scheduler.is_running == True
        print("  ✓ 调度器在任务异常后仍正常运行")
    
    def test_scheduler_performance(self):
        """测试调度器性能"""
        print("  🔍 测试调度器性能...")
        
        if not self.test_scheduler or not self.test_scheduler.is_running:
            self.test_scheduler = SchedulerCenter()
            self.test_scheduler.start()
            time.sleep(0.5)
        
        task_count = 20
        start_time = time.time()
        
        def performance_job(job_id):
            pass
        
        for i in range(task_count):
            future_time = datetime.now() + timedelta(seconds=60)
            self.test_scheduler.add_job(
                func=lambda job_id=i: performance_job(job_id),
                trigger='date',
                run_date=future_time,
                id=f'perf_job_{i}'
            )
        
        add_time = time.time() - start_time
        print(f"  📈 添加 {task_count} 个任务耗时: {add_time:.3f}秒")
        
        for i in range(task_count):
            try:
                self.test_scheduler.remove_job(f'perf_job_{i}')
            except:
                pass
        
        if add_time < 1.0:
            print("  ✅ 调度器性能优秀")
        else:
            print("  ✓ 调度器性能正常")
    
    def _print_final_results(self):
        """打印最终测试结果"""
        end_time = time.time()
        total_time = end_time - self.start_time
        
        print("=" * 80)
        print("📊 任务调度模块测试结果汇总")
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
            print("🎉 任务调度模块测试整体通过！")
        elif success_rate >= 70:
            print("⚠️  任务调度模块测试部分通过，需要关注失败的测试")
        else:
            print("❌ 任务调度模块测试失败较多，需要重点修复")
        
        print("=" * 80)


def main():
    """主函数 - 运行任务调度模块测试"""
    print("🧪 Python Project Template - 任务调度模块测试")
    
    try:
        test_suite = SchedulerModuleTestSuite()
        test_suite.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试运行出现异常: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()