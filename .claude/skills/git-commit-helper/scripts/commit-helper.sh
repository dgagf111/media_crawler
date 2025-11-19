#!/bin/bash

# Git 提交助手 - 智能生成中文提交信息
# 作者: Claude Code
# 使用方法: ./.claude/skills/git-commit-helper/scripts/commit-helper.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

print_header() {
    echo -e "${PURPLE}Git 提交助手${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
}

# 检查是否在 Git 仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是 Git 仓库"
        exit 1
    fi
}

# 获取 Git 状态
get_git_status() {
    print_info "检查 Git 状态..."

    # 检查是否有暂存的更改
    if git diff --staged --quiet; then
        print_warning "没有暂存的更改"

        # 检查是否有未暂存的更改
        if git diff --quiet && git ls-files --others --exclude-standard --directory | grep -q .; then
            print_info "发现未暂存的更改"
            echo -e "${CYAN}未暂存的文件:${NC}"
            git status --porcelain | grep -E '^.[^? ]' | cut -c4-
            echo
            read -p "是否要暂存所有更改? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_info "暂存所有更改..."
                git add .
                print_success "所有更改已暂存"
            else
                print_info "请先暂存要提交的文件，使用: git add <files>"
                exit 0
            fi
        else
            print_info "没有需要提交的更改"
            exit 0
        fi
    fi
}

# 分析暂存的更改
analyze_staged_changes() {
    print_info "分析暂存的更改..."
    echo

    # 显示更改统计
    echo -e "${CYAN}更改统计:${NC}"
    git diff --staged --stat

    echo
    echo -e "${CYAN}修改的文件:${NC}"
    git diff --staged --name-only | nl

    echo
    echo -e "${CYAN}详细更改:${NC}"
    git diff --staged --color=always | head -50
    if [ $(git diff --staged | wc -l) -gt 50 ]; then
        echo -e "${YELLOW}... (显示前50行，使用 'git diff --staged' 查看完整更改)${NC}"
    fi
    echo
}

# 智能分析更改类型
analyze_change_type() {
    local files=$(git diff --staged --name-only)
    local changes=$(git diff --staged)

    # 分析文件类型
    local has_py=false
    local has_js=false
    local has_ts=false
    local has_test=false
    local has_doc=false
    local has_config=false
    local has_docker=false

    for file in $files; do
        case $file in
            *.py) has_py=true ;;
            *.js|*.jsx) has_js=true ;;
            *.ts|*.tsx) has_ts=true ;;
            *test*|*spec*) has_test=true ;;
            *.md|*.rst|*.txt) has_doc=true ;;
            *.yaml|*.yml|*.json|*.toml|*.ini) has_config=true ;;
            Dockerfile*|docker-compose*) has_docker=true ;;
        esac
    done

    # 分析更改内容
    local type="feat"  # 默认类型
    local scope=""

    if echo "$changes" | grep -qi "fix\|bug\|error\|issue\|problem\|crash\|exception"; then
        type="fix"
    elif echo "$changes" | grep -qi "refactor\|重构\|优化\|improve\|enhance\|clean"; then
        type="refactor"
    elif echo "$changes" | grep -qi "test\|测试\|spec"; then
        type="test"
    elif echo "$changes" | grep -qi "doc\|文档\|readme\|注释\|comment"; then
        type="docs"
    elif echo "$changes" | grep -qi "style\|format\|lint\|代码风格\|格式化"; then
        type="style"
    elif echo "$changes" | grep -qi "chore\|维护\|depend\|version\|build\|ci"; then
        type="chore"
    fi

    # 确定范围
    if $has_test; then
        scope="test"
    elif echo "$files" | grep -q "api\|route\|endpoint\|controller"; then
        scope="api"
    elif echo "$files" | grep -q "model\|schema\|database\|db\|migration"; then
        scope="db"
    elif echo "$files" | grep -q "auth\|login\|user\|permission\|token"; then
        scope="auth"
    elif echo "$files" | grep -q "config\|setting\|environment"; then
        scope="config"
    elif echo "$files" | grep -q "core\|util\|helper\|common"; then
        scope="core"
    elif echo "$files" | grep -q "service\|business\|logic"; then
        scope="service"
    elif $has_doc; then
        scope="docs"
    elif $has_config; then
        scope="config"
    elif $has_docker; then
        scope="docker"
    else
        scope=$(echo "$files" | head -1 | cut -d'/' -f1)
    fi

    echo "$type:$scope"
}

# 生成提交信息建议
generate_commit_suggestions() {
    local analysis=$(analyze_change_type)
    local type=$(echo "$analysis" | cut -d: -f1)
    local scope=$(echo "$analysis" | cut -d: -f2)

    echo -e "${CYAN}建议的提交类型:${NC} $type"
    echo -e "${CYAN}建议的作用域:${NC} $scope"
    echo

    # 根据类型生成建议
    echo -e "${CYAN}提交信息建议:${NC}"

    case $type in
        "feat")
            echo "  • $type($scope): 添加新功能"
            echo "  • $type($scope): 实现 XXX 功能"
            echo "  • $type($scope): 新增 XXX 支持"
            ;;
        "fix")
            echo "  • $type($scope): 修复 XXX 问题"
            echo "  • $type($scope): 解决 XXX 异常"
            echo "  • $type($scope): 处理 XXX 错误"
            ;;
        "refactor")
            echo "  • $type($scope): 重构 XXX 代码"
            echo "  • $type($scope): 优化 XXX 实现"
            echo "  • $type($scope): 简化 XXX 逻辑"
            ;;
        "test")
            echo "  • $type($scope): 添加 XXX 测试"
            echo "  • $type($scope): 完善 XXX 测试覆盖"
            echo "  • $type($scope): 修复 XXX 测试问题"
            ;;
        "docs")
            echo "  • $type($scope): 更新 XXX 文档"
            echo "  • $type($scope): 完善 XXX 说明"
            echo "  • $type($scope): 添加 XXX 注释"
            ;;
        "style")
            echo "  • $type($scope): 格式化 XXX 代码"
            echo "  • $type($scope): 统一 XXX 风格"
            echo "  • $type($scope): 修复 XXX 格式问题"
            ;;
        "chore")
            echo "  • $type($scope): 更新 XXX 配置"
            echo "  • $type($scope): 升级 XXX 版本"
            echo "  • $type($scope): 清理 XXX 依赖"
            ;;
    esac
    echo
}

# 交互式输入提交信息
interactive_commit() {
    local analysis=$(analyze_change_type)
    local suggested_type=$(echo "$analysis" | cut -d: -f1)
    local suggested_scope=$(echo "$analysis" | cut -d: -f2)

    echo -e "${CYAN}请输入提交信息:${NC}"
    echo

    # 输入类型
    echo -e "可用类型: ${YELLOW}feat${NC}, ${YELLOW}fix${NC}, ${YELLOW}docs${NC}, ${YELLOW}style${NC}, ${YELLOW}refactor${NC}, ${YELLOW}test${NC}, ${YELLOW}chore${NC}"
    read -p "提交类型 [$suggested_type]: " commit_type
    commit_type=${commit_type:-$suggested_type}

    # 输入作用域
    read -p "作用域 [$suggested_scope]: " commit_scope
    commit_scope=${commit_scope:-$suggested_scope}

    # 输入描述
    echo
    echo -e "${CYAN}请输入简要描述 (使用中文，不超过50个字符):${NC}"
    read -p "描述: " commit_desc

    if [ -z "$commit_desc" ]; then
        print_error "提交描述不能为空"
        exit 1
    fi

    # 构建提交信息
    local commit_msg="$commit_type($commit_scope): $commit_desc"

    echo
    echo -e "${CYAN}是否需要添加详细描述? (y/N):${NC}"
    read -p "" -n 1 -r
    echo

    local detailed_desc=""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${CYAN}请输入详细描述 (输入 'END' 结束):${NC}"
        while IFS= read -r line; do
            if [ "$line" = "END" ]; then
                break
            fi
            detailed_desc="$detailed_desc$line\n"
        done
    fi

    # 显示最终提交信息
    echo
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}提交信息预览:${NC}"
    echo -e "${GREEN}$commit_msg${NC}"
    if [ -n "$detailed_desc" ]; then
        echo
        printf "$detailed_desc"
    fi
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo

    # 确认提交
    echo -e "${CYAN}确认提交? (y/N):${NC}"
    read -p "" -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -n "$detailed_desc" ]; then
            echo -e "$commit_msg" | git commit -F -
        else
            git commit -m "$commit_msg"
        fi
        print_success "提交成功!"

        # 显示提交信息
        echo
        echo -e "${CYAN}最新提交:${NC}"
        git log --oneline -1

    else
        print_info "提交已取消"
        exit 0
    fi
}

# 快速提交模式
quick_commit() {
    local analysis=$(analyze_change_type)
    local suggested_type=$(echo "$analysis" | cut -d: -f1)
    local suggested_scope=$(echo "$analysis" | cut -d: -f2)

    # 自动生成提交信息
    local auto_desc=""
    local changes=$(git diff --staged --name-only)

    case $suggested_type in
        "feat")
            auto_desc="添加新功能"
            ;;
        "fix")
            auto_desc="修复问题"
            ;;
        "refactor")
            auto_desc="重构代码"
            ;;
        "test")
            auto_desc="更新测试"
            ;;
        "docs")
            auto_desc="更新文档"
            ;;
        "style")
            auto_desc="调整代码格式"
            ;;
        "chore")
            auto_desc="维护性更新"
            ;;
    esac

    local commit_msg="$suggested_type($suggested_scope): $auto_desc"

    print_info "自动生成的提交信息: ${GREEN}$commit_msg${NC}"

    git commit -m "$commit_msg"
    print_success "快速提交成功!"
}

# 显示帮助信息
show_help() {
    echo -e "${CYAN}Git 提交助手使用说明:${NC}"
    echo
    echo "用法: $0 [选项]"
    echo
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -q, --quick    快速提交模式（自动生成提交信息）"
    echo "  -i, --interactive  交互式模式（默认）"
    echo
    echo "示例:"
    echo "  $0                    # 交互式模式"
    echo "  $0 --quick           # 快速提交"
    echo "  $0 -i                # 交互式模式"
    echo
}

# 主函数
main() {
    print_header

    # 解析命令行参数
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        -q|--quick)
            quick_mode=true
            ;;
        -i|--interactive|"")
            quick_mode=false
            ;;
        *)
            print_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac

    # 检查 Git 仓库
    check_git_repo

    # 检查 Git 状态
    get_git_status

    # 分析更改
    analyze_staged_changes

    # 生成建议
    generate_commit_suggestions

    # 执行提交
    if [ "$quick_mode" = true ]; then
        quick_commit
    else
        interactive_commit
    fi

    echo
    print_success "操作完成!"
}

# 运行主函数
main "$@"