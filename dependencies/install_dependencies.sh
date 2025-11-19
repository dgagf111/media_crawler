#!/bin/bash

# =============================================================================
# Python Project Template - 依赖安装脚本
# =============================================================================
# 这个脚本帮助您快速安装项目依赖，支持多种安装模式
# 使用方法：
#   chmod +x install_dependencies.sh
#   ./install_dependencies.sh [模式]
#
# 模式选项：
#   prod    - 仅安装生产依赖 (默认)
#   dev     - 安装开发依赖 (包含生产依赖)
#   check   - 检查依赖状态
#   clean   - 清理并重新安装
# =============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Python 版本
check_python_version() {
    log_info "检查 Python 版本..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装！请先安装 Python 3.8+"
        exit 1
    fi
    
    python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    required_version="3.8"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
        log_success "Python $python_version 版本检查通过"
    else
        log_error "Python 版本 $python_version 过低，需要 $required_version 或更高版本"
        exit 1
    fi
}

# 检查虚拟环境
check_virtual_env() {
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        log_success "检测到虚拟环境: $VIRTUAL_ENV"
    else
        log_warning "未检测到虚拟环境"
        log_info "建议创建虚拟环境："
        echo "  python3 -m venv .venv"
        echo "  source .venv/bin/activate  # Linux/macOS"
        echo "  .venv\\Scripts\\activate     # Windows"
        echo ""
        
        read -p "是否继续在全局环境中安装? (y/N): " confirm
        if [[ $confirm != [yY] ]]; then
            log_info "安装已取消"
            exit 0
        fi
    fi
}

# 升级 pip
upgrade_pip() {
    log_info "升级 pip 到最新版本..."
    python3 -m pip install --upgrade pip
    log_success "pip 已升级"
}

# 安装生产依赖
install_production_deps() {
    log_info "安装生产环境依赖..."
    
    if [ ! -f "dependencies/requirements.txt" ]; then
        log_error "requirements.txt 文件不存在！"
        exit 1
    fi
    
    python3 -m pip install -r dependencies/requirements.txt
    log_success "生产依赖安装完成"
}

# 安装开发依赖
install_development_deps() {
    log_info "安装开发环境依赖..."
    
    # 先安装生产依赖
    install_production_deps
    
    if [ ! -f "dependencies/requirements-dev-only.txt" ]; then
        log_error "requirements-dev-only.txt 文件不存在！"
        exit 1
    fi
    
    log_info "安装开发专用工具..."
    python3 -m pip install -r dependencies/requirements-dev-only.txt
    log_success "开发依赖安装完成"
}

# 验证安装
verify_installation() {
    log_info "验证关键依赖安装..."
    
    # 检查核心依赖
    core_packages=("fastapi" "uvicorn" "sqlalchemy" "redis" "pytest")
    
    for package in "${core_packages[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            version=$(python3 -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
            log_success "$package ($version) ✓"
        else
            log_error "$package 未正确安装 ✗"
        fi
    done
}

# 显示依赖信息
show_dependency_info() {
    log_info "显示已安装的依赖信息..."
    echo ""
    echo "=== 核心依赖 ==="
    python3 -m pip list | grep -E "(fastapi|uvicorn|sqlalchemy|redis|pytest)" || echo "未找到核心依赖"
    
    echo ""
    echo "=== 开发工具 ==="
    python3 -m pip list | grep -E "(black|mypy|flake8|pytest-cov)" || echo "未找到开发工具"
    
    echo ""
    echo "=== 总依赖数量 ==="
    total_packages=$(python3 -m pip list | wc -l)
    log_info "共安装 $total_packages 个包"
}

# 检查依赖状态
check_dependencies() {
    log_info "检查依赖状态..."
    
    echo ""
    echo "=== 依赖健康检查 ==="
    if python3 -m pip check; then
        log_success "所有依赖兼容性检查通过"
    else
        log_warning "发现依赖兼容性问题"
    fi
    
    echo ""
    echo "=== 过期依赖检查 ==="
    outdated=$(python3 -m pip list --outdated)
    if [ -z "$outdated" ]; then
        log_success "所有依赖都是最新版本"
    else
        log_warning "发现过期依赖："
        echo "$outdated"
    fi
    
    show_dependency_info
}

# 清理并重新安装
clean_and_reinstall() {
    log_warning "这将清理所有已安装的包并重新安装"
    read -p "确认继续? (y/N): " confirm
    if [[ $confirm != [yY] ]]; then
        log_info "操作已取消"
        exit 0
    fi
    
    log_info "清理现有依赖..."
    python3 -m pip freeze | xargs python3 -m pip uninstall -y || true
    
    log_info "重新安装依赖..."
    install_production_deps
}

# 显示帮助信息
show_help() {
    echo "Python Project Template - 依赖安装脚本"
    echo ""
    echo "用法: $0 [模式]"
    echo ""
    echo "模式选项:"
    echo "  prod     - 仅安装生产依赖 (默认)"
    echo "  dev      - 安装开发依赖 (包含生产依赖)"
    echo "  check    - 检查依赖状态"
    echo "  clean    - 清理并重新安装"
    echo "  help     - 显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0          # 安装生产依赖"
    echo "  $0 dev      # 安装开发依赖"
    echo "  $0 check    # 检查依赖状态"
    echo ""
}

# 主函数
main() {
    echo "🚀 Python Project Template - 依赖安装脚本"
    echo "============================================="
    
    mode=${1:-prod}  # 默认生产模式
    
    case $mode in
        "prod")
            check_python_version
            check_virtual_env
            upgrade_pip
            install_production_deps
            verify_installation
            log_success "生产环境依赖安装完成！"
            ;;
        "dev")
            check_python_version
            check_virtual_env
            upgrade_pip
            install_development_deps
            verify_installation
            log_success "开发环境依赖安装完成！"
            ;;
        "check")
            check_dependencies
            ;;
        "clean")
            check_python_version
            check_virtual_env
            clean_and_reinstall
            verify_installation
            log_success "依赖清理并重新安装完成！"
            ;;
        "help")
            show_help
            ;;
        *)
            log_error "未知模式: $mode"
            show_help
            exit 1
            ;;
    esac
    
    echo ""
    echo "🎉 操作完成！"
    echo ""
    echo "📚 更多信息："
    echo "  - 完整安装指南: docs/guides/installation-guide.md"
    echo "  - 依赖管理指南: docs/DEPENDENCY_MANAGEMENT.md"
    echo "  - 项目架构文档: docs/PROJECT_ARCHITECTURE.md"
    echo ""
    echo "▶️  下一步："
    echo "  python main.py          # 启动应用"
    echo "  python tests/run_tests.py all  # 运行测试"
}

# 脚本入口
main "$@"