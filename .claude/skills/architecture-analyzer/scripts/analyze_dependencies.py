#!/usr/bin/env python3
"""
依赖关系分析脚本
用于分析代码库中的模块/文件依赖关系

使用方式:
    python analyze_dependencies.py python  # 分析 Python 项目
    python analyze_dependencies.py js      # 分析 JavaScript/TypeScript 项目
    python analyze_dependencies.py go      # 分析 Go 项目
"""

import ast
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json


class DependencyAnalyzer:
    """基类分析器"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.dependencies = defaultdict(set)
        self.reverse_dependencies = defaultdict(set)

    def analyze(self) -> Dict:
        """执行分析"""
        raise NotImplementedError

    def get_circular_dependencies(self) -> List[List[str]]:
        """检测循环依赖"""
        visited = set()
        path = []
        cycles = []

        def dfs(node, start_node):
            if node in path:
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                cycles.append(cycle)
                return True

            if node in visited:
                return False

            visited.add(node)
            path.append(node)

            for neighbor in self.dependencies[node]:
                if dfs(neighbor, start_node):
                    return True

            path.pop()
            return False

        for node in list(self.dependencies.keys()):
            if node not in visited:
                dfs(node, node)

        return cycles

    def get_most_dependent_on(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """获取被依赖最多的模块"""
        counts = [(node, len(deps)) for node, deps in self.dependencies.items()]
        return sorted(counts, key=lambda x: x[1], reverse=True)[:top_n]

    def get_most_dependent_by(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """获取依赖其他模块最多的模块"""
        counts = [(node, len(self.dependencies[node]))
                  for node in self.dependencies]
        return sorted(counts, key=lambda x: x[1], reverse=True)[:top_n]

    def generate_mermaid_graph(self, max_nodes: int = 20) -> str:
        """生成 Mermaid 依赖图"""
        all_nodes = list(self.dependencies.keys())
        if len(all_nodes) > max_nodes:
            # 只显示核心节点
            node_scores = {}
            for node in all_nodes:
                # 计算节点重要性（被依赖 + 依赖其他）
                score = len(self.reverse_dependencies[node]) + \
                        len(self.dependencies[node])
                node_scores[node] = score

            # 选择最重要节点
            core_nodes = sorted(node_scores.items(),
                               key=lambda x: x[1],
                               reverse=True)[:max_nodes]
            core_nodes = [node for node, _ in core_nodes]
        else:
            core_nodes = all_nodes

        lines = []
        lines.append("graph TD")
        lines.append("")

        added_edges = set()
        for source in core_nodes:
            if source not in self.dependencies:
                continue

            for target in list(self.dependencies[source]):
                if target not in core_nodes:
                    continue

                edge = f"    {source} --> {target}"
                if edge not in added_edges:
                    lines.append(edge)
                    added_edges.add(edge)

        return "\n".join(lines)

    def generate_report(self) -> str:
        """生成分析报告"""
        report = []
        report.append("# 依赖关系分析报告")
        report.append("")

        # 统计信息
        total_files = len(self.dependencies)
        total_deps = sum(len(deps) for deps in self.dependencies.values())

        report.append(f"- 分析文件数: {total_files}")
        report.append(f"- 总依赖数: {total_deps}")
        report.append(f"- 平均依赖数: {total_deps / max(total_files, 1):.2f}")
        report.append("")

        # 循环依赖
        cycles = self.get_circular_dependencies()
        report.append(f"## 循环依赖")
        if cycles:
            report.append(f"- **发现 {len(cycles)} 个循环依赖** ⚠️")
            for i, cycle in enumerate(cycles, 1):
                report.append(f"\n### 循环 {i}")
                for j in range(len(cycle) - 1):
                    report.append(f"- {cycle[j]} → {cycle[j + 1]}")
        else:
            report.append("- 没有发现循环依赖 ✓")
        report.append("")

        # 被依赖最多的模块
        report.append("## 被依赖最多的模块（核心模块）")
        for module, count in self.get_most_dependent_on():
            report.append(f"- `{module}` - 被 {count} 个模块依赖")
        report.append("")

        # 依赖其他模块最多的模块
        report.append("## 依赖最多的模块（复杂模块）")
        for module, count in self.get_most_dependent_by():
            report.append(f"- `{module}` - 依赖 {count} 个模块")
        report.append("")

        # 架构建议
        report.append("## 架构建议")
        if cycles:
            report.append("\n### 循环依赖问题")
            report.append("- 考虑提取公共逻辑到第三方模块")
            report.append("- 应用依赖倒置原则（依赖抽象而非具体实现）")
            report.append("- 使用依赖注入容器管理依赖\n")

        # 高依赖模块建议
        high_dependents = self.get_most_dependent_by(3)
        if high_dependents and high_dependents[0][1] > 10:
            report.append("\n### 高度耦合模块")
            report.append(f"- `{high_dependents[0][0]}` 依赖了 {high_dependents[0][1]} 个模块")
            report.append("- 考虑模块拆分，降低耦合度")
            report.append("- 检查是否遵循单一职责原则\n")

        report.append("## 依赖关系图")
        report.append("")
        report.append("\n```mermaid")
        report.append(self.generate_mermaid_graph())
        report.append("```\n")

        return "\n".join(report)


class PythonDependencyAnalyzer(DependencyAnalyzer):
    """Python 依赖分析器"""

    def __init__(self, project_path: str):
        super().__init__(project_path)
        self.packages = set()

    def _extract_imports_from_file(self, file_path: Path) -> Set[str]:
        """从 Python 文件提取导入"""
        imports = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            for node in ast.walk(tree):
                # import module
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name.split('.')[0]
                        if self._is_internal_module(module_name, file_path):
                            imports.add(module_name)

                # from module import something
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_name = node.module.split('.')[0]
                        if self._is_internal_module(module_name, file_path):
                            imports.add(module_name)

        except SyntaxError as e:
            print(f"语法错误解析 {file_path}: {e}")
        except Exception as e:
            print(f"错误解析 {file_path}: {e}")

        return imports

    def _is_internal_module(self, module_name: str, current_file: Path) -> bool:
        """判断是否为项目内部模块"""
        # 排除标准库和第三方库
        std_libs = {
            'os', 'sys', 're', 'json', 'datetime', 'typing', 'collections',
            'pathlib', 'ast', 'abc', 'uuid', 'hashlib', 'base64', 'hmac',
            'logging', 'io', 'functools', 'itertools', 'copy', 'pickle',
            'threading', 'multiprocessing', 'asyncio', 'subprocess',
            'email', 'http', 'urllib', 'socket', 'ssl', 'mimetypes',
            'inspect', 'textwrap', 'string', 'random', 'math', 'csv',
            'html', 'xml', 'zipfile', 'tarfile', 'sqlite3', 'decimal'
        }

        third_party_libs = {
            'fastapi', 'flask', 'django', 'sqlalchemy', 'alembic',
            'pytest', 'requests', 'httpx', 'pydantic', 'jinja2',
            'redis', 'celery', 'prometheus_client', 'aioredis',
            'psycopg2', 'mysql', 'asyncpg', 'motor', 'pymongo',
            'numpy', 'pandas', 'matplotlib', 'seaborn',
            'jwt', 'cryptography', 'bcrypt', 'passlib',
            'sentry_sdk', 'structlog', 'colorlog', 'uvicorn',
            'aiofiles', 'pillow', 'opencv', 'scipy', 'sklearn'
        }

        if module_name in std_libs or module_name in third_party_libs:
            return False

        # 检查是否存在对应的目录或文件
        possible_paths = [
            self.project_path / f"{module_name.replace('.', '/')}.py",
            self.project_path / module_name.replace('.', '/') / '__init__.py',
        ]

        return any(p.exists() for p in possible_paths)

    def _module_path_to_name(self, file_path: Path) -> str:
        """将文件路径转换为模块名"""
        try:
            rel_path = file_path.relative_to(self.project_path)
            if rel_path.name == '__init__.py':
                return str(rel_path.parent).replace('/', '.')
            else:
                return str(rel_path.with_suffix('')).replace('/', '.')
        except ValueError:
            return str(file_path).replace('/', '.')

    def analyze(self) -> Dict:
        """分析 Python 项目依赖"""
        print("🔍 分析 Python 项目依赖关系...")

        # 查找所有 Python 文件
        python_files = list(self.project_path.rglob("*.py"))
        print(f"  找到 {len(python_files)} 个 Python 文件")

        # 提取每个文件的导入
        for file_path in python_files:
            module_name = self._module_path_to_name(file_path)
            imports = self._extract_imports_from_file(file_path)

            for imported in imports:
                self.dependencies[module_name].add(imported)
                self.reverse_dependencies[imported].add(module_name)

        # 统计
        self._analyze_third_party_packages()

        return {
            'dependencies': dict(self.dependencies),
            'reverse_dependencies': dict(self.reverse_dependencies),
            'packages': list(self.packages),
            'total_files': len(python_files),
        }

    def _analyze_third_party_packages(self):
        """分析第三方包依赖"""
        requirements_files = [
            self.project_path / 'requirements.txt',
            self.project_path / 'requirements' / 'base.txt',
            self.project_path / 'requirements' / 'dev.txt',
        ]

        for req_file in requirements_files:
            if req_file.exists():
                try:
                    with open(req_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # 提取包名
                                match = re.match(r'^([a-zA-Z0-9_-]+)', line)
                                if match:
                                    self.packages.add(match.group(1))
                except Exception as e:
                    print(f"读取 {req_file} 失败: {e}")


class JavaScriptDependencyAnalyzer(DependencyAnalyzer):
    """JavaScript/TypeScript 依赖分析器"""

    def __init__(self, project_path: str):
        super().__init__(project_path)
        self.packages = set()

    def _extract_imports_from_file(self, file_path: Path) -> Set[str]:
        """从 JS/TS 文件提取导入"""
        imports = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # ES6 import: import ... from '...'
            import_regex = r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"
            matches = re.findall(import_regex, content, re.MULTILINE)

            for module_path in matches:
                if self._is_internal_module(module_path, file_path):
                    imports.add(module_path)

            # CommonJS: require('...')
            require_regex = r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
            matches = re.findall(require_regex, content, re.MULTILINE)

            for module_path in matches:
                if self._is_internal_module(module_path, file_path):
                    imports.add(module_path)

            # ES6 export from: export ... from '...'
            export_from_regex = r"export\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"
            matches = re.findall(export_from_regex, content, re.MULTILINE)

            for module_path in matches:
                if self._is_internal_module(module_path, file_path):
                    imports.add(module_path)

        except Exception as e:
            print(f"错误解析 {file_path}: {e}")

        return imports

    def _is_internal_module(self, module_path: str, current_file: Path) -> bool:
        """判断是否为项目内部模块"""
        # 排除 node_modules 和外部库
        external_prefixes = [
            'react', 'react-dom', 'vue', 'angular',
            '@types/', 'typescript', '@typescript-eslint',
            'lodash', 'axios', 'moment', 'date-fns',
            'styled-components', '@emotion', '@mui',
            'react-router', 'react-query', 'swr',
            '@testing-library', 'jest', 'vitest',
            'vite', 'webpack', 'rollup', 'esbuild',
            'tailwindcss', 'postcss', 'sass', 'less',
            'zustand', 'redux', 'mobx', 'recoil',
            '@reduxjs', 'react-redux',
        ]

        for prefix in external_prefixes:
            if module_path.startswith(prefix):
                return False

        # 相对路径导入
        if module_path.startswith('.'):
            # 解析相对路径
            current_dir = current_file.parent
            target_path = (current_dir / module_path).resolve()

            # 检查是否存在
            if target_path.exists():
                return True
            if (target_path.with_suffix('.js')).exists():
                return True
            if (target_path.with_suffix('.ts')).exists():
                return True
            if (target_path.with_suffix('.tsx')).exists():
                return True
            if (target_path.with_suffix('.jsx')).exists():
                return True
            if (target_path / 'index.js').exists():
                return True
            if (target_path / 'index.ts').exists():
                return True

        return False

    def _module_path_to_name(self, file_path: Path) -> str:
        """将文件路径转换为模块名"""
        try:
            rel_path = file_path.relative_to(self.project_path)
            return str(rel_path.with_suffix(''))
        except ValueError:
            return str(file_path)

    def analyze(self) -> Dict:
        """分析 JavaScript/TypeScript 项目依赖"""
        print("🔍 分析 JavaScript/TypeScript 项目依赖关系...")

        # 查找所有 JS/TS/JSX/TSX 文件
        extensions = ['*.js', '*.ts', '*.jsx', '*.tsx']
        js_files = []
        for ext in extensions:
            js_files.extend(self.project_path.rglob(ext))

        # 排除 node_modules
        js_files = [f for f in js_files if 'node_modules' not in str(f)]

        print(f"  找到 {len(js_files)} 个 JS/TS 文件")

        # 提取每个文件的导入
        for file_path in js_files:
            module_name = self._module_path_to_name(file_path)
            imports = self._extract_imports_from_file(file_path)

            for imported in imports:
                self.dependencies[module_name].add(imported)
                self.reverse_dependencies[imported].add(module_name)

        # 分析 package.json
        self._analyze_packages()

        return {
            'dependencies': dict(self.dependencies),
            'reverse_dependencies': dict(self.reverse_dependencies),
            'packages': list(self.packages),
            'total_files': len(js_files),
        }

    def _analyze_packages(self):
        """分析 package.json"""
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)

                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})

                self.packages.update(deps.keys())
                self.packages.update(dev_deps.keys())
            except Exception as e:
                print(f"解析 package.json 失败: {e}")


class GoDependencyAnalyzer(DependencyAnalyzer):
    """Go 依赖分析器"""

    def __init__(self, project_path: str):
        super().__init__(project_path)
        self.packages = set()

    def _extract_imports_from_file(self, file_path: Path) -> Set[str]:
        """从 Go 文件提取导入"""
        imports = set()

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 匹配 import 语句
            import_regex = r'import\s+\(\s*([^)]+)\s*\)'
            block_matches = re.findall(import_regex, content, re.DOTALL)

            for block in block_matches:
                for line in block.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('//'):
                        # 处理带别名的导入: alias "package"
                        match = re.match(r'.*"([^"]+)"', line)
                        if match:
                            package = match.group(1)
                            if self._is_internal_package(package, file_path):
                                imports.add(package)

            # 单行 import
            import_regex = r'import\s+(?:\w+\s+)?"([^"]+)"'
            matches = re.findall(import_regex, content)
            for package in matches:
                if self._is_internal_package(package, file_path):
                    imports.add(package)

        except Exception as e:
            print(f"错误解析 {file_path}: {e}")

        return imports

    def _is_internal_package(self, package_path: str, current_file: Path) -> bool:
        """判断是否为项目内部包"""
        # 排除标准库和外部库
        external_packages = {
            'fmt', 'os', 'io', 'net/http', 'encoding/json',
            'database/sql', 'time', 'strconv', 'strings',
            'sync', 'context', 'log', 'errors', 'flag',
            'reflect', 'regexp', 'sort', 'math', 'bytes',
            'bufio', 'crypto', 'encoding', 'path', 'runtime',
            'testing', 'github.com', 'golang.org',
            'google.golang.org', 'go.uber.org', 'gorm.io',
            'github.com/gin-gonic', 'github.com/gorilla',
        }

        # 如果是相对导入
        if package_path.startswith('.'):
            return True

        # 检查是否为项目内部包
        internal_path = self.project_path / package_path
        if internal_path.exists():
            return True

        return False

    def _module_path_to_name(self, file_path: Path) -> str:
        """将文件路径转换为包名"""
        try:
            rel_path = file_path.parent.relative_to(self.project_path)
            module_name = str(rel_path)
            if module_name == '.':
                return 'main'
            return module_name
        except ValueError:
            return str(file_path.parent)

    def analyze(self) -> Dict:
        """分析 Go 项目依赖"""
        print("🔍 分析 Go 项目依赖关系...")

        # 查找所有 .go 文件（排除 vendor）
        go_files = list(self.project_path.rglob("*.go"))
        go_files = [f for f in go_files if 'vendor' not in str(f)]

        print(f"  找到 {len(go_files)} 个 Go 文件")

        # 提取每个文件的导入
        for file_path in go_files:
            module_name = self._module_path_to_name(file_path)
            imports = self._extract_imports_from_file(file_path)

            for imported in imports:
                self.dependencies[module_name].add(imported)
                self.reverse_dependencies[imported].add(module_name)

        # 分析 go.mod
        self._analyze_go_mod()

        return {
            'dependencies': dict(self.dependencies),
            'reverse_dependencies': dict(self.reverse_dependencies),
            'packages': list(self.packages),
            'total_files': len(go_files),
        }

    def _analyze_go_mod(self):
        """分析 go.mod"""
        go_mod = self.project_path / 'go.mod'
        if go_mod.exists():
            try:
                with open(go_mod, 'r') as f:
                    content = f.read()

                # 提取依赖包
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('module') and \
                       not line.startswith('go ') and not line.startswith('(') and \
                       not line.startswith(')') and not line.startswith('//'):
                        parts = line.split()
                        if parts:
                            self.packages.add(parts[0])
            except Exception as e:
                print(f"解析 go.mod 失败: {e}")


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_dependencies.py <language>")
        print("语言选项: python, js, go")
        sys.exit(1)

    language = sys.argv[1].lower()
    project_path = os.getcwd()

    # 选择分析器
    if language == 'python':
        analyzer = PythonDependencyAnalyzer(project_path)
    elif language in ['js', 'javascript', 'typescript', 'ts']:
        analyzer = JavaScriptDependencyAnalyzer(project_path)
    elif language == 'go':
        analyzer = GoDependencyAnalyzer(project_path)
    else:
        print(f"不支持的语言: {language}")
        print("支持的语言: python, js, typescript, go")
        sys.exit(1)

    # 执行分析
    results = analyzer.analyze()

    # 生成报告
    report = analyzer.generate_report()
    print("\n" + "=" * 80)
    print("依赖关系分析报告")
    print("=" * 80)
    print(report)

    # 保存到文件
    report_file = Path('dependency_report.md')
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"\n✅ 报告已保存到: {report_file}")

    return results


if __name__ == '__main__':
    main()
