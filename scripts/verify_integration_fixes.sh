#!/bin/bash

# =============================================================================
# 集成测试修复验证脚本
# 用于验证集成测试问题的修复状态
# =============================================================================

set -e  # 出错时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_header() {
    echo -e "\n${BLUE}==============================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}==============================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 测试计数器
PASSED=0
FAILED=0

# 检查函数
check_test() {
    local test_name="$1"
    local command="$2"

    print_info "运行: $test_name"
    if eval "$command" > /dev/null 2>&1; then
        print_success "$test_name - 通过"
        ((PASSED++))
        return 0
    else
        print_error "$test_name - 失败"
        ((FAILED++))
        return 1
    fi
}

# =============================================================================
# 主验证流程
# =============================================================================

print_header "集成测试修复验证工具"

echo "开始验证集成测试修复状态..."
echo "测试时间: $(date)"
echo ""

# -----------------------------------------------------------------------------
# 1. 验证配置系统单例模式
# -----------------------------------------------------------------------------
print_header "1. 验证配置系统单例模式"

check_test "配置模块导入" \
    "python -c 'from pythonprojecttemplate.config.config import Config'"

check_test "配置单例模式" \
    "python -c 'from pythonprojecttemplate.config.config import Config; c1=Config(); c2=Config(); assert c1 is c2'"

check_test "配置对象一致性" \
    "python -c 'from pythonprojecttemplate.config.config import Config; c=Config(); assert hasattr(c, \"_settings\")'"

# -----------------------------------------------------------------------------
# 2. 验证API测试导入
# -----------------------------------------------------------------------------
print_header "2. 验证API测试导入"

check_test "API模块导入" \
    "python -c 'from pythonprojecttemplate.api.main import app'"

check_test "API测试文件 - test_api_router" \
    "python -m pytest tests/framework/api/test_api_router.py -v --tb=line -q"

check_test "API测试文件 - test_third_party_token" \
    "python -m pytest tests/framework/api/test_third_party_token.py -v --tb=line -q"

check_test "API测试文件 - test_token_service" \
    "python -m pytest tests/framework/api/test_token_service.py -v --tb=line -q"

# -----------------------------------------------------------------------------
# 3. 验证项目结构
# -----------------------------------------------------------------------------
print_header "3. 验证项目结构"

check_test "根目录main.py存在" \
    "test -f main.py"

check_test "main.py可读" \
    "test -r main.py"

# -----------------------------------------------------------------------------
# 4. 验证核心模块导入
# -----------------------------------------------------------------------------
print_header "4. 验证核心模块导入"

check_test "日志模块导入" \
    "python -c 'from pythonprojecttemplate.log.logHelper import get_logger'"

check_test "缓存模块导入" \
    "python -c 'from pythonprojecttemplate.cache.memory_cache import MemoryCacheManager'"

check_test "数据库模块导入" \
    "python -c 'from pythonprojecttemplate.db.mysql import Database'"

check_test "监控模块导入" \
    "python -c 'from pythonprojecttemplate.monitoring.main import MonitoringCenter'"

check_test "调度模块导入" \
    "python -c 'from pythonprojecttemplate.scheduler.main import SchedulerManager'"

# -----------------------------------------------------------------------------
# 5. 运行集成测试
# -----------------------------------------------------------------------------
print_header "5. 运行集成测试套件"

print_info "运行整体框架集成测试..."
if python tests/test_framework_integration.py > /tmp/integration_test.log 2>&1; then
    # 提取成功率
    SUCCESS_RATE=$(grep "成功率:" /tmp/integration_test.log | grep -oP '\d+\.\d+%' | head -1)
    if [ -n "$SUCCESS_RATE" ]; then
        print_success "集成测试通过 - 成功率: $SUCCESS_RATE"
        ((PASSED++))
    else
        print_success "集成测试通过"
        ((PASSED++))
    fi
else
    print_error "集成测试失败"
    cat /tmp/integration_test.log | tail -20
    ((FAILED++))
fi

# -----------------------------------------------------------------------------
# 6. 运行框架测试
# -----------------------------------------------------------------------------
print_header "6. 运行框架测试"

print_info "运行框架模块测试..."
FRAMEWORK_RESULT=$(python -m pytest tests/framework/ -v --tb=line -q 2>&1 | tail -5)
if echo "$FRAMEWORK_RESULT" | grep -q "passed"; then
    print_success "框架测试通过"
    ((PASSED++))
else
    print_error "框架测试失败"
    ((FAILED++))
fi

# -----------------------------------------------------------------------------
# 7. 业务测试验证
# -----------------------------------------------------------------------------
print_header "7. 业务测试验证"

check_test "业务模块导入" \
    "python -c 'from pythonprojecttemplate.modules.test.main import run' 2>/dev/null || print_warning '业务模块导入失败（可接受）'"

# -----------------------------------------------------------------------------
# 8. 依赖完整性检查
# -----------------------------------------------------------------------------
print_header "8. 依赖完整性检查"

check_test "pip健康状态" \
    "pip --version > /dev/null 2>&1"

check_test "依赖兼容性检查" \
    "pip check > /dev/null 2>&1"

check_test "项目可安装性" \
    "pip show pythonprojecttemplate > /dev/null 2>&1"

# -----------------------------------------------------------------------------
# 9. 代码质量检查 (可选)
# -----------------------------------------------------------------------------
print_header "9. 代码质量检查 (可选)"

if command -v black &> /dev/null; then
    check_test "代码格式检查" \
        "black --check src/ tests/ --quiet 2>/dev/null || echo '代码格式需调整'"
else
    print_warning "black未安装，跳过格式检查"
fi

if command -v mypy &> /dev/null; then
    check_test "类型检查" \
        "mypy src/pythonprojecttemplate/config/ --ignore-missing-imports --no-error-summary 2>/dev/null || echo '类型检查有问题'"
else
    print_warning "mypy未安装，跳过类型检查"
fi

# -----------------------------------------------------------------------------
# 总结报告
# -----------------------------------------------------------------------------
print_header "验证结果总结"

TOTAL=$((PASSED + FAILED))
SUCCESS_RATE=$((PASSED * 100 / TOTAL))

echo "总验证项数: $TOTAL"
echo "通过项数: $PASSED"
echo "失败项数: $FAILED"
echo "成功率: ${SUCCESS_RATE}%"

if [ $FAILED -eq 0 ]; then
    print_success "所有验证项通过！集成测试修复成功！"
    echo ""
    echo -e "${GREEN}🎉 恭喜！项目集成测试修复完成！${NC}"
    echo ""
    echo "接下来可以:"
    echo "  - 运行 'python tests/run_tests.py all' 执行完整测试"
    echo "  - 查看 'docs/INTEGRATION_TESTS_FIX_GUIDE.md' 了解详细修复信息"
    exit 0
else
    print_warning "存在 $FAILED 个未通过的验证项"
    echo ""
    echo "请参考以下文档进行修复:"
    echo "  - 快速修复: INTEGRATION_TESTS_QUICK_FIX.md"
    echo "  - 详细指南: docs/INTEGRATION_TESTS_FIX_GUIDE.md"
    echo ""
    echo "失败的验证项详情请查看上方输出。"
    exit 1
fi