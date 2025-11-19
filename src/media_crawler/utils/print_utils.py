import pandas as pd
import numpy as np
from typing import Any, Dict, List, Union, Optional, Tuple
import json
from datetime import datetime
import sys
from collections.abc import Iterable
import textwrap

# =============================================================================
# 核心格式化打印函数
# =============================================================================


def pprint_data(
    data: Any,
    title: str = None,
    max_width: int = 80,
    max_rows: int = 20,  # 默认打印20行
    max_col_width: int = 15,
    show_index: bool = True,
    show_types: bool = False,
    show_stats: bool = False,
    use_colors: bool = True,
    compact: bool = False,
    columns: List[str] = None,  # 自定义需要打印的表头
    exclude_columns: List[str] = None,
    max_depth: int = 3,
    debug_mode: bool = False,
    compare_with: Any = None,
    compare_titles: Tuple[str, str] = ("数据1", "数据2"),
    enable_header_wrap: bool = True,
    header_wrap_width: int = None,
    sync_header_width: bool = True,
) -> None:
    """
    统一的数据格式化打印函数

    支持多种数据类型的智能格式化打印，特别适用于调试场景

    Args:
        data: 要打印的数据（支持任意类型）
        title: 自定义标题
        max_width: 最大显示宽度
        max_rows: 最大显示行数，默认为20行
        max_col_width: 列最大宽度（包括表头）
        show_index: 是否显示索引
        show_types: 是否显示数据类型信息
        show_stats: 是否显示统计信息
        use_colors: 是否使用颜色输出
        compact: 是否使用紧凑格式
        columns: 自定义需要打印的表头（列名列表）
        exclude_columns: 排除的列（列名列表）
        max_depth: 字典和列表的最大递归深度
        debug_mode: 是否显示详细调试信息
        compare_with: 要比较的数据（如果提供，会并排显示比较）
        compare_titles: 比较时两个数据的标题
        enable_header_wrap: 是否启用表头换行
        header_wrap_width: 表头换行宽度，None表示使用max_col_width
        sync_header_width: 是否同步表头宽度与内容宽度

    使用示例:
        # 默认打印前20行，所有列
        pprint_data(data)

        # 自定义打印行数和表头
        pprint_data(data, max_rows=10, columns=['name', 'age'])

        # 只打印特定列，默认行数
        pprint_data(data, columns=['name', 'age', 'city'])
    """
    # 检查颜色支持
    colors = _get_colors(use_colors)

    # 如果是比较模式
    if compare_with is not None:
        _print_comparison(
            data,
            compare_with,
            compare_titles,
            colors,
            max_width,
            show_types,
            show_stats,
        )
        return

    # 如果是调试模式
    if debug_mode:
        _print_debug_info(data, title or "数据", colors, show_stats)
        return

    # 设置表头换行宽度
    if header_wrap_width is None:
        header_wrap_width = max_col_width

    # 智能识别数据类型并打印
    if isinstance(data, pd.DataFrame):
        _print_dataframe(
            data,
            title,
            colors,
            max_width,
            max_rows,
            max_col_width,
            show_index,
            show_types,
            show_stats,
            columns,
            exclude_columns,
            enable_header_wrap,
            header_wrap_width,
            sync_header_width,
        )
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        _print_dict_array(
            data,
            title,
            colors,
            max_width,
            max_rows,
            max_col_width,
            show_index,
            show_types,
            show_stats,
            columns,
            exclude_columns,
            enable_header_wrap,
            header_wrap_width,
            sync_header_width,
        )
    elif isinstance(data, dict):
        _print_dict(
            data,
            title,
            colors,
            max_width,
            max_col_width,
            show_types,
            show_stats,
            max_depth,
            max_rows,
            columns,
            exclude_columns,
            enable_header_wrap,
            header_wrap_width,
            sync_header_width,
        )
    elif isinstance(data, (list, tuple, set)):
        _print_list(data, title, colors, max_rows, show_types, show_stats)
    elif isinstance(data, pd.Series):
        _print_dataframe(
            data.to_frame(),
            title,
            colors,
            max_width,
            max_rows,
            max_col_width,
            show_index,
            show_types,
            show_stats,
            columns,
            exclude_columns,
            enable_header_wrap,
            header_wrap_width,
            sync_header_width,
        )
    elif isinstance(data, np.ndarray):
        _print_numpy_array(data, title, colors, max_rows, show_stats)
    else:
        _print_simple_data(data, title, colors, show_types)


# =============================================================================
# 辅助函数
# =============================================================================


def _get_colors(use_colors: bool) -> Dict[str, str]:
    """获取颜色配置"""
    if use_colors and _supports_color():
        return {
            "header": "\033[1;36m",  # 青色加粗
            "key": "\033[1;33m",  # 黄色加粗
            "value": "\033[0;37m",  # 白色
            "type": "\033[0;35m",  # 紫色
            "stats": "\033[0;32m",  # 绿色
            "border": "\033[0;34m",  # 蓝色
            "reset": "\033[0m",  # 重置
        }
    else:
        return {
            "header": "",
            "key": "",
            "value": "",
            "type": "",
            "stats": "",
            "border": "",
            "reset": "",
        }


def _supports_color() -> bool:
    """检查终端是否支持颜色"""
    try:
        return sys.stdout.isatty()
    except:
        return False


def _color_text(text: str, colors: Dict[str, str], color_type: str) -> str:
    """给文本添加颜色"""
    return f"{colors[color_type]}{text}{colors['reset']}"


def _truncate_text(text: str, max_len: int) -> str:
    """截断文本"""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _wrap_text(text: str, width: int) -> List[str]:
    """将文本按指定宽度换行"""
    if width <= 0:
        return [text]

    # 使用textwrap进行智能换行
    wrapped = textwrap.wrap(
        text, width=width, break_long_words=True, break_on_hyphens=False
    )

    # 如果只有一行且长度超过宽度，强制截断
    if len(wrapped) == 1 and len(wrapped[0]) > width:
        wrapped = [_truncate_text(wrapped[0], width)]

    return wrapped


def _calculate_optimal_width(text: str, max_width: int, min_width: int = 5) -> int:
    """计算最优的显示宽度"""
    # 如果文本长度小于等于最大宽度，直接使用文本长度
    if len(text) <= max_width:
        return len(text)

    # 计算换行后的最小所需宽度
    wrapped = _wrap_text(text, max_width)
    max_line_width = max(len(line) for line in wrapped)

    # 如果最大行宽小于最小宽度，使用最小宽度
    if max_line_width < min_width:
        return min_width

    # 如果最大行宽小于等于最大宽度，使用最大行宽
    if max_line_width <= max_width:
        return max_line_width

    # 否则使用最大宽度
    return max_width


def _format_value(value: Any, max_len: int = 20, colors: Dict[str, str] = None) -> str:
    """格式化单个值"""
    if colors is None:
        colors = _get_colors(False)

    if value is None:
        return _color_text("None", colors, "type")
    elif isinstance(value, (int, float)):
        if isinstance(value, float):
            return f"{value:.4f}"
        return str(value)
    elif isinstance(value, str):
        return _truncate_text(value, max_len)
    elif isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, (list, tuple, set, dict)):
        return f"{type(value).__name__}({len(value)})"
    elif isinstance(value, (pd.DataFrame, pd.Series)):
        return f"{type(value).__name__}({value.shape})"
    elif isinstance(value, np.ndarray):
        return f"ndarray{value.shape}"
    else:
        return _truncate_text(str(value), max_len)


# =============================================================================
# 具体类型的打印函数
# =============================================================================


def _print_dict_array(
    data: List[Dict[str, Any]],
    title: str,
    colors: Dict[str, str],
    max_width: int,
    max_rows: int,
    max_col_width: int,
    show_index: bool,
    show_types: bool,
    show_stats: bool,
    columns: List[str] = None,
    exclude_columns: List[str] = None,
    enable_header_wrap: bool = True,
    header_wrap_width: int = None,
    sync_header_width: bool = True,
) -> None:
    """打印字典数组"""
    if not data:
        print(_color_text("字典数组为空", colors, "stats"))
        return

    # 获取所有列名
    all_columns = set()
    for item in data:
        all_columns.update(item.keys())
    all_columns = sorted(all_columns)

    # 处理列选择 - 支持自定义表头
    if columns:
        # 验证请求的列是否存在
        available_columns = [col for col in columns if col in all_columns]
        missing_columns = [col for col in columns if col not in all_columns]

        if missing_columns:
            print(
                _color_text(f"警告：以下列不存在: {missing_columns}", colors, "stats")
            )

        if not available_columns:
            print(_color_text("错误：请求的列都不存在", colors, "stats"))
            return

        display_columns = available_columns
    else:
        display_columns = all_columns

    # 处理排除列
    if exclude_columns:
        display_columns = [col for col in display_columns if col not in exclude_columns]

    if not display_columns:
        print(_color_text("没有可显示的列", colors, "stats"))
        return

    # 计算列宽和表头换行
    col_widths = {}
    header_lines = {}  # 存储每列的表头行数
    header_wrapped = {}  # 存储换行后的表头

    for col in display_columns:
        # 处理表头换行
        if enable_header_wrap and header_wrap_width > 0:
            wrapped_headers = _wrap_text(col, header_wrap_width)
            header_wrapped[col] = wrapped_headers
            header_lines[col] = len(wrapped_headers)

            # 计算表头所需的最小宽度
            if sync_header_width:
                # 计算表头最优宽度
                header_optimal_width = _calculate_optimal_width(
                    col, header_wrap_width, 5
                )
            else:
                # 使用表头最宽的一行
                header_optimal_width = max(len(line) for line in wrapped_headers)
        else:
            # 不换行，直接截断
            header_display = _truncate_text(col, max_col_width)
            header_wrapped[col] = [header_display]
            header_lines[col] = 1
            header_optimal_width = len(header_display)

        # 计算数据内容的最大宽度
        data_max_width = 5  # 最小宽度
        for item in data[:max_rows]:  # 只计算要显示的行
            value = item.get(col, "")
            formatted = _format_value(value, max_col_width, colors)
            data_max_width = max(data_max_width, len(formatted))

        # 确定最终列宽
        if sync_header_width:
            # 同步表头和数据宽度，取两者中的较大值
            final_width = min(max(header_optimal_width, data_max_width), max_col_width)
        else:
            # 不同步，使用数据宽度和表头宽度的较大值
            final_width = min(max(header_optimal_width, data_max_width), max_col_width)

        col_widths[col] = final_width

    # 打印标题
    if title:
        print(
            f"\n{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}"
        )
        print(f"{_color_text(title, colors, 'header')}")
        print(f"{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}\n")

    # 显示列信息（如果指定了自定义列）
    if columns:
        total_cols = len(all_columns)
        displayed_cols = len(display_columns)
        print(_color_text(f"显示列: {displayed_cols}/{total_cols}", colors, "stats"))
        if missing_columns:
            print(_color_text(f"缺失列: {missing_columns}", colors, "stats"))
        print()

    # 计算表头总行数
    max_header_lines = max(header_lines.values()) if header_lines else 1

    # 打印表头（支持多行）
    for line_num in range(max_header_lines):
        header_parts = []

        # 添加索引列的表头
        if show_index:
            if line_num == 0:
                header_parts.append(_color_text("Index".ljust(5), colors, "header"))
            else:
                header_parts.append("".ljust(5))

        # 添加各列的表头行
        for col in display_columns:
            if line_num < header_lines[col]:
                header_line = header_wrapped[col][line_num]
                header_parts.append(
                    _color_text(header_line.ljust(col_widths[col]), colors, "header")
                )
            else:
                header_parts.append("".ljust(col_widths[col]))

        print(" | ".join(header_parts))

    # 打印分隔线
    separator_parts = []
    if show_index:
        separator_parts.append(_color_text("-" * 5, colors, "border"))

    for col in display_columns:
        separator_parts.append(_color_text("-" * col_widths[col], colors, "border"))

    separator = "-+-".join(separator_parts)
    print(separator)

    # 打印数据 - 使用自定义行数
    display_data = data[:max_rows]
    for i, item in enumerate(display_data):
        row_parts = []
        if show_index:
            row_parts.append(_color_text(str(i).rjust(5), colors, "type"))

        for col in display_columns:
            value = item.get(col, "")
            formatted = _format_value(value, col_widths[col], colors)
            row_parts.append(formatted.ljust(col_widths[col]))

        print(" | ".join(row_parts))

    # 显示截断信息
    total_rows = len(data)
    displayed_rows = len(display_data)
    if total_rows > displayed_rows:
        print(
            f"\n{_color_text(f'... 显示了前 {displayed_rows} 行，共 {total_rows} 行', colors, 'stats')}"
        )

    # 显示统计信息
    if show_stats:
        _print_dict_array_stats(data, display_columns, colors)

    # 显示类型信息
    if show_types:
        print(f"\n{_color_text('数据类型:', colors, 'type')} List[Dict]")
        print(f"{_color_text('总行数:', colors, 'type')} {total_rows}")
        print(f"{_color_text('显示行数:', colors, 'type')} {displayed_rows}")
        print(f"{_color_text('列数:', colors, 'type')} {len(display_columns)}")


def _print_dict_array_stats(
    data: List[Dict[str, Any]], columns: List[str], colors: Dict[str, str]
) -> None:
    """打印字典数组的统计信息"""
    print(f"\n{_color_text('统计信息:', colors, 'stats')}")

    for col in columns:
        values = [
            item.get(col) for item in data if col in item and item.get(col) is not None
        ]
        if not values:
            continue

        print(f"  {_color_text(col, colors, 'key')}:")

        # 数值统计
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        if numeric_values:
            print(
                f"    数值: {_color_text(f'count={len(numeric_values)}, min={min(numeric_values)}, max={max(numeric_values)}, avg={sum(numeric_values)/len(numeric_values):.2f}', colors, 'stats')}"
            )

        # 字符串统计
        string_values = [v for v in values if isinstance(v, str)]
        if string_values:
            unique_count = len(set(string_values))
            print(
                f"    字符串: {_color_text(f'count={len(string_values)}, unique={unique_count}', colors, 'stats')}"
            )


def _print_dataframe(
    df: pd.DataFrame,
    title: str,
    colors: Dict[str, str],
    max_width: int,
    max_rows: int,
    max_col_width: int,
    show_index: bool,
    show_types: bool,
    show_stats: bool,
    columns: List[str] = None,
    exclude_columns: List[str] = None,
    enable_header_wrap: bool = True,
    header_wrap_width: int = None,
    sync_header_width: bool = True,
) -> None:
    """打印DataFrame"""
    if df.empty:
        print(_color_text("DataFrame为空", colors, "stats"))
        return

    # 处理列选择 - 支持自定义表头
    display_df = df.copy()

    if columns:
        # 验证请求的列是否存在
        available_columns = [col for col in columns if col in df.columns]
        missing_columns = [col for col in columns if col not in df.columns]

        if missing_columns:
            print(
                _color_text(f"警告：以下列不存在: {missing_columns}", colors, "stats")
            )

        if not available_columns:
            print(_color_text("错误：请求的列都不存在", colors, "stats"))
            return

        display_df = display_df[available_columns]
    else:
        available_columns = list(df.columns)

    if exclude_columns:
        display_df = display_df.drop(columns=exclude_columns, errors="ignore")

    if display_df.empty:
        print(_color_text("没有可显示的列", colors, "stats"))
        return

    # 处理表头换行和列宽计算
    col_widths = {}
    header_lines_map = {}  # 记录每列的表头行数
    header_wrapped_map = {}  # 记录换行后的表头
    original_to_display = {}  # 原始列名到显示列名的映射

    for col in display_df.columns:
        # 处理表头换行
        if enable_header_wrap and header_wrap_width > 0:
            wrapped_headers = _wrap_text(col, header_wrap_width)
            header_wrapped_map[col] = wrapped_headers
            header_lines_map[col] = len(wrapped_headers)

            # 计算表头所需的最小宽度
            if sync_header_width:
                # 计算表头最优宽度
                header_optimal_width = _calculate_optimal_width(
                    col, header_wrap_width, 5
                )
            else:
                # 使用表头最宽的一行
                header_optimal_width = max(len(line) for line in wrapped_headers)
        else:
            # 不换行，直接截断
            header_display = _truncate_text(col, max_col_width)
            header_wrapped_map[col] = [header_display]
            header_lines_map[col] = 1
            header_optimal_width = len(header_display)

        # 计算数据内容的最大宽度 - 只计算要显示的行
        data_max_width = 5  # 最小宽度
        display_rows = min(max_rows, len(display_df))
        for i in range(display_rows):
            val = str(display_df.iloc[i][col])
            data_max_width = max(data_max_width, len(val))

        # 确定最终列宽
        if sync_header_width:
            # 同步表头和数据宽度，取两者中的较大值
            final_width = min(max(header_optimal_width, data_max_width), max_col_width)
        else:
            # 不同步，使用数据宽度和表头宽度的较大值
            final_width = min(max(header_optimal_width, data_max_width), max_col_width)

        col_widths[col] = final_width

        # 创建显示列名（使用表头第一行）
        display_col = header_wrapped_map[col][0] if header_wrapped_map[col] else col
        original_to_display[col] = display_col

    # 重命名列以适应显示
    display_df = display_df.rename(columns=original_to_display)

    # 打印标题
    if title:
        print(
            f"\n{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}"
        )
        print(f"{_color_text(title, colors, 'header')}")
        print(
            f"{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}\n"
        )

    # 显示列信息（如果指定了自定义列）
    if columns:
        total_cols = len(df.columns)
        displayed_cols = len(display_df.columns)
        print(_color_text(f"显示列: {displayed_cols}/{total_cols}", colors, "stats"))
        if missing_columns:
            print(_color_text(f"缺失列: {missing_columns}", colors, "stats"))
        print()

    # 计算表头总行数
    max_header_lines = max(header_lines_map.values()) if header_lines_map else 1

    # 打印表头（支持多行）
    for line_num in range(max_header_lines):
        header_parts = []

        # 添加索引列的表头
        if show_index:
            if line_num == 0:
                header_parts.append(_color_text("Index".ljust(5), colors, "header"))
            else:
                header_parts.append("".ljust(5))

        # 添加各列的表头行
        for col in display_df.columns:
            # 找到原始列名
            original_col = next(
                (orig for orig, disp in original_to_display.items() if disp == col), col
            )

            if line_num < header_lines_map[original_col]:
                header_line = header_wrapped_map[original_col][line_num]
                header_parts.append(
                    _color_text(
                        header_line.ljust(col_widths[original_col]), colors, "header"
                    )
                )
            else:
                header_parts.append("".ljust(col_widths[original_col]))

        print(" | ".join(header_parts))

    # 打印分隔线
    separator_parts = []
    if show_index:
        separator_parts.append(_color_text("-" * 5, colors, "border"))

    for col in display_df.columns:
        # 找到原始列名
        original_col = next(
            (orig for orig, disp in original_to_display.items() if disp == col), col
        )
        separator_parts.append(
            _color_text("-" * col_widths[original_col], colors, "border")
        )

    separator = "-+-".join(separator_parts)
    print(separator)

    # 打印数据 - 使用自定义行数
    display_rows = min(max_rows, len(display_df))
    for i in range(display_rows):
        row_parts = []
        if show_index:
            row_parts.append(_color_text(str(i).rjust(5), colors, "type"))

        for col in display_df.columns:
            # 找到原始列名
            original_col = next(
                (orig for orig, disp in original_to_display.items() if disp == col), col
            )

            val = str(display_df.iloc[i][col])
            formatted = _truncate_text(val, col_widths[original_col])
            row_parts.append(formatted.ljust(col_widths[original_col]))

        print(" | ".join(row_parts))

    # 显示截断信息
    total_rows = len(df)
    displayed_rows = display_rows
    if total_rows > displayed_rows:
        print(
            f"\n{_color_text(f'... 显示了前 {displayed_rows} 行，共 {total_rows} 行', colors, 'stats')}"
        )

    # 显示统计信息
    if show_stats:
        _print_dataframe_stats(display_df, colors)

    # 显示类型信息
    if show_types:
        print(f"\n{_color_text('DataFrame信息:', colors, 'type')}")
        print(f"  形状: {df.shape}")
        print(f"  总行数: {total_rows}")
        print(f"  显示行数: {displayed_rows}")
        print(f"  总列数: {len(df.columns)}")
        print(f"  显示列数: {len(display_df.columns)}")
        print(f"  数据类型:")
        for col, dtype in df.dtypes.items():
            if col in display_df.columns:
                print(f"    {col}: {dtype}")


def _print_dataframe_stats(df: pd.DataFrame, colors: Dict[str, str]) -> None:
    """打印DataFrame的统计信息"""
    print(f"\n{_color_text('统计信息:', colors, 'stats')}")

    # 数值列统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"  数值列统计:")
        print(df[numeric_cols].describe().to_string())

    # 分类列统计
    categorical_cols = df.select_dtypes(include=["object"]).columns
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        print(f"  {_color_text(col, colors, 'key')}:")
        for val, count in value_counts.head(5).items():
            print(f"    {val}: {count}")
        if len(value_counts) > 5:
            print(f"    ... 还有 {len(value_counts) - 5} 个唯一值")


def _print_dict(
    data: Dict[str, Any],
    title: str,
    colors: Dict[str, str],
    max_width: int,
    max_col_width: int,
    show_types: bool,
    show_stats: bool,
    max_depth: int,
    max_rows: int,
    columns: List[str] = None,
    exclude_columns: List[str] = None,
    current_depth: int = 0,
    enable_header_wrap: bool = True,
    header_wrap_width: int = None,
    sync_header_width: bool = True,
) -> None:
    """打印字典（支持列筛选与条数限制）"""
    if current_depth >= max_depth:
        print(_color_text("{...}", colors, "type"))
        return

    # 打印标题（仅顶层）
    if title and current_depth == 0:
        print(
            f"\n{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}"
        )
        print(f"{_color_text(title, colors, 'header')}")
        print(
            f"{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}\n"
        )

    if not data:
        print(_color_text("字典为空", colors, "stats"))
        return

    # 计算要显示的键集合（按插入顺序）
    all_keys = list(data.keys())

    display_keys: List[str]
    missing_columns: List[str] = []

    if columns:
        display_keys = [k for k in columns if k in data]
        missing_columns = [k for k in columns if k not in data]
        if missing_columns:
            print(_color_text(f"警告：以下键不存在: {missing_columns}", colors, "stats"))
        if not display_keys:
            print(_color_text("错误：请求的键都不存在", colors, "stats"))
            return
    else:
        display_keys = all_keys

    if exclude_columns:
        display_keys = [k for k in display_keys if k not in set(exclude_columns)]

    if not display_keys:
        print(_color_text("没有可显示的键", colors, "stats"))
        return

    total_items = len(display_keys)
    # 限制显示条数
    display_keys = display_keys[: max_rows if max_rows is not None else len(display_keys)]
    displayed_items = len(display_keys)

    # 预处理键的换行与宽度，确定统一的键列宽度
    if header_wrap_width is None:
        header_wrap_width = max_col_width

    wrapped_keys_map: Dict[str, List[str]] = {}
    key_width_candidates: List[int] = []

    for key in display_keys:
        key_str_full = str(key)
        if enable_header_wrap and header_wrap_width and header_wrap_width > 0:
            wrapped = _wrap_text(key_str_full, header_wrap_width)
            wrapped_keys_map[key] = wrapped
            if sync_header_width:
                width_i = _calculate_optimal_width(key_str_full, header_wrap_width, 5)
            else:
                width_i = max(len(line) for line in wrapped)
        else:
            display = _truncate_text(key_str_full, max_col_width)
            wrapped_keys_map[key] = [display]
            width_i = len(display)
        key_width_candidates.append(width_i)

    key_col_width = min(max(key_width_candidates) if key_width_candidates else 5, max_col_width)

    # 按序打印键值
    for key in display_keys:
        value = data.get(key)
        wrapped_keys = wrapped_keys_map.get(key, [str(key)])
        key_display = wrapped_keys[0]
        key_optimal_width = min(max(len(key_display), key_col_width), max_col_width)
        key_str = _color_text(key_display.ljust(key_optimal_width), colors, "key")

        if isinstance(value, dict):
            print(f"{key_str}: {{")
            _print_dict(
                value,
                None,
                colors,
                max_width,
                max_col_width,
                show_types,
                show_stats,
                max_depth,
                max_rows,
                None,
                None,
                current_depth + 1,
                enable_header_wrap,
                header_wrap_width,
                sync_header_width,
            )
            print("  " * (current_depth + 1) + "}")
        elif isinstance(value, (list, tuple)):
            if len(value) == 0:
                print(f"{key_str}: []")
            elif len(value) <= 5 and all(not isinstance(item, (dict, list, tuple)) for item in value):
                values_str = ", ".join([_format_value(v, max_col_width, colors) for v in value])
                print(f"{key_str}: [{values_str}]")
            else:
                print(f"{key_str}: [")
                indent = "  " * (current_depth + 1)
                for i, item in enumerate(value[:5]):
                    item_str = _format_value(item, max_col_width, colors)
                    print(f"{indent}{i}: {item_str}")
                if len(value) > 5:
                    print(f"{indent}{_color_text(f'... 还有 {len(value) - 5} 项', colors, 'stats')}")
                print(f"  " * current_depth + "]")
        else:
            value_str = _format_value(value, max_col_width, colors)
            print(f"{key_str}: {value_str}")

        # 打印键的剩余行（如果有）
        for i in range(1, len(wrapped_keys)):
            indent = " " * (min(key_optimal_width, max_col_width) + 2)  # 键的宽度 + ": "
            print(f"{indent}{wrapped_keys[i]}")

    # 显示截断信息
    if total_items > displayed_items and current_depth == 0:
        print(f"\n{_color_text(f'... 显示了前 {displayed_items} 项，共 {total_items} 项', colors, 'stats')}")

    # 显示统计信息
    if show_stats and current_depth == 0:
        # 简单统计：各类型计数
        type_counts: Dict[str, int] = {}
        for k in (display_keys if displayed_items == total_items else list(data.keys())):
            v = data.get(k)
            t = type(v).__name__
            type_counts[t] = type_counts.get(t, 0) + 1
        print(f"\n{_color_text('统计信息:', colors, 'stats')}")
        for t, cnt in type_counts.items():
            print(f"  {t}: {cnt}")

    # 显示类型信息
    if show_types and current_depth == 0:
        print(f"\n{_color_text('字典信息:', colors, 'type')}")
        print(f"  键数: {len(data)}")
        print(f"  类型: Dict[str, Any]")


def _print_list(
    data: List[Any],
    title: str,
    colors: Dict[str, str],
    max_rows: int,
    show_types: bool,
    show_stats: bool,
) -> None:
    """打印列表"""
    # 打印标题
    if title:
        print(f"\n{_color_text('=' * min(80, len(title) + 4), colors, 'border')}")
        print(f"{_color_text(title, colors, 'header')}")
        print(f"{_color_text('=' * min(80, len(title) + 4), colors, 'border')}\n")

    if not data:
        print(_color_text("列表为空", colors, "stats"))
        return

    # 使用自定义行数
    display_data = data[:max_rows]
    for i, item in enumerate(display_data):
        item_str = _format_value(item, 20, colors)
        print(f"{_color_text(str(i).rjust(5), colors, 'type')}: {item_str}")

    # 显示截断信息
    total_items = len(data)
    displayed_items = len(display_data)
    if total_items > displayed_items:
        print(
            f"\n{_color_text(f'... 显示了前 {displayed_items} 项，共 {total_items} 项', colors, 'stats')}"
        )

    # 显示类型信息
    if show_types:
        print(f"\n{_color_text('列表信息:', colors, 'type')}")
        print(f"  总长度: {total_items}")
        print(f"  显示长度: {displayed_items}")
        if data:
            print(f"  元素类型: {type(data[0]).__name__}")


def _print_numpy_array(
    arr: np.ndarray, title: str, colors: Dict[str, str], max_rows: int, show_stats: bool
) -> None:
    """打印NumPy数组"""
    if title is None:
        title = f"NumPy数组 {arr.shape}"

    print(f"\n{_color_text(title, colors, 'header')}")
    print(f"{_color_text('=' * len(title), colors, 'border')}")

    # 显示基本信息
    print(f"{_color_text('形状:', colors, 'type')} {arr.shape}")
    print(f"{_color_text('数据类型:', colors, 'type')} {arr.dtype}")

    if arr.size <= max_rows:
        # 小数组直接显示
        print(f"{_color_text('数组内容:', colors, 'type')}")
        print(arr)
    else:
        # 大数组显示部分内容
        print(f"{_color_text('前几个元素:', colors, 'type')}")
        if arr.ndim == 1:
            print(arr[:max_rows])
            print(
                f"{_color_text(f'... 还有 {arr.size - max_rows} 个元素', colors, 'stats')}"
            )
        else:
            # 多维数组显示第一维的前几个元素
            for i in range(min(3, arr.shape[0])):
                print(f"  维度 {i}: {arr[i]}")
            if arr.shape[0] > 3:
                print(
                    f"{_color_text(f'... 还有 {arr.shape[0] - 3} 个维度', colors, 'stats')}"
                )

    # 显示统计信息
    if show_stats and np.issubdtype(arr.dtype, np.number):
        print(f"\n{_color_text('统计信息:', colors, 'stats')}")
        print(f"  最小值: {np.min(arr)}")
        print(f"  最大值: {np.max(arr)}")
        print(f"  平均值: {np.mean(arr):.4f}")
        print(f"  标准差: {np.std(arr):.4f}")


def _print_simple_data(
    data: Any, title: str, colors: Dict[str, str], show_types: bool
) -> None:
    """打印简单数据类型"""
    if title:
        print(f"\n{_color_text(title, colors, 'header')}")
        print(f"{_color_text('=' * len(title), colors, 'border')}")

    print(f"{_color_text('值:', colors, 'type')} {_format_value(data, 50, colors)}")

    if show_types:
        print(f"{_color_text('类型:', colors, 'type')} {type(data).__name__}")


def _print_comparison(
    data1: Any,
    data2: Any,
    titles: Tuple[str, str],
    colors: Dict[str, str],
    max_width: int,
    show_types: bool,
    show_stats: bool,
) -> None:
    """打印数据比较"""
    print(f"\n{_color_text('数据比较', colors, 'header')}")
    print(f"{_color_text('=' * 50, colors, 'border')}")

    # 左侧显示data1，右侧显示data2
    title1, title2 = titles
    print(
        f"{_color_text(title1.ljust(25), colors, 'key')} | {_color_text(title2, colors, 'key')}"
    )
    print(
        f"{_color_text('-' * 25, colors, 'border')}+{_color_text('-' * 25, colors, 'border')}"
    )

    # 比较基本信息
    info1 = _get_data_info(data1, colors)
    info2 = _get_data_info(data2, colors)

    for key in ["类型", "形状/长度", "数据类型"]:
        val1 = info1.get(key, "N/A")
        val2 = info2.get(key, "N/A")
        print(
            f"{_color_text(str(val1).ljust(25), colors, 'type')} | {_color_text(str(val2), colors, 'type')}"
        )


def _get_data_info(data: Any, colors: Dict[str, str]) -> Dict[str, str]:
    """获取数据的基本信息"""
    info = {"类型": type(data).__name__}

    if isinstance(data, (pd.DataFrame, pd.Series)):
        info["形状/长度"] = str(data.shape)
        info["数据类型"] = (
            str(data.dtypes) if hasattr(data, "dtypes") else str(data.dtype)
        )
    elif isinstance(data, (list, tuple, set)):
        info["形状/长度"] = str(len(data))
        if data:
            info["数据类型"] = type(data[0]).__name__
    elif isinstance(data, dict):
        info["形状/长度"] = f"{len(data)} 键"
    elif isinstance(data, np.ndarray):
        info["形状/长度"] = str(data.shape)
        info["数据类型"] = str(data.dtype)

    return info


def _print_debug_info(
    data: Any, title: str, colors: Dict[str, str], show_stats: bool
) -> None:
    """打印调试信息"""
    print(f"\n{_color_text('=== 调试信息 ===', colors, 'header')}")
    print(f"{_color_text('变量名:', colors, 'key')} {title}")
    print(f"{_color_text('类型:', colors, 'type')} {type(data).__name__}")
    print(f"{_color_text('内存地址:', colors, 'type')} {hex(id(data))}")

    # 根据类型显示特定信息
    if isinstance(data, (pd.DataFrame, pd.Series)):
        print(f"{_color_text('形状:', colors, 'type')} {data.shape}")
        if show_stats:
            print(
                f"{_color_text('内存使用:', colors, 'type')} {data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
            )
        if hasattr(data, "dtypes"):
            print(f"{_color_text('列数据类型:', colors, 'type')}")
            for col, dtype in data.dtypes.items():
                print(f"  {col}: {dtype}")
    elif isinstance(data, (list, tuple, set)):
        print(f"{_color_text('长度:', colors, 'type')} {len(data)}")
        if data:
            print(
                f"{_color_text('元素类型:', colors, 'type')} {type(data[0]).__name__}"
            )
    elif isinstance(data, dict):
        print(f"{_color_text('键数:', colors, 'type')} {len(data)}")
        print(f"{_color_text('键:', colors, 'type')} {list(data.keys())}")
    elif isinstance(data, np.ndarray):
        print(f"{_color_text('形状:', colors, 'type')} {data.shape}")
        print(f"{_color_text('数据类型:', colors, 'type')} {data.dtype}")
        if show_stats:
            print(
                f"{_color_text('大小:', colors, 'type')} {data.nbytes / 1024 / 1024:.2f} MB"
            )

    # 显示数据内容预览
    print(f"\n{_color_text('数据预览:', colors, 'stats')}")
    pprint_data(data, max_rows=5, use_colors=False)


# =============================================================================
# 便捷函数
# =============================================================================


def pprint(data: Any, **kwargs) -> None:
    """简洁的格式化打印函数

    增强：当输入为字典或DataFrame的字典格式（例如 list[dict]、dict of list 等）时，
    自动按JSON标准（indent=2, ensure_ascii=False）格式化打印。
    """
    # 判定是否为“字典格式”的数据（纯dict，或list/tuple且元素为dict）
    is_dict_like = isinstance(data, dict) or (
        isinstance(data, (list, tuple)) and len(data) > 0 and isinstance(next(iter(data)), dict)
    )

    if is_dict_like:
        # 打印标题（保持与其它打印风格一致）
        title = kwargs.get("title")
        use_colors = kwargs.get("use_colors", True)
        max_width = kwargs.get("max_width", 80)
        colors = _get_colors(use_colors)
        if title:
            print(f"\n{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}")
            print(f"{_color_text(title, colors, 'header')}")
            print(f"{_color_text('=' * min(max_width, len(title) + 4), colors, 'border')}\n")

        def _default(o: Any):
            # datetime 与 pandas 时间戳
            if isinstance(o, datetime):
                return o.isoformat()
            try:
                import pandas as _pd  # 局部导入以避免循环引用问题
            except Exception:
                _pd = None
            if _pd is not None:
                try:
                    from pandas import Timestamp as _PdTimestamp  # type: ignore
                except Exception:
                    _PdTimestamp = None
                if _PdTimestamp is not None and isinstance(o, _PdTimestamp):
                    return o.isoformat()
                if isinstance(o, _pd.Series):
                    return o.to_dict()
                if isinstance(o, _pd.DataFrame):
                    # DataFrame 若混入字典中，转换为 records 形式
                    return o.to_dict(orient="records")
            # numpy 类型
            if isinstance(o, (np.integer,)):
                return int(o)
            if isinstance(o, (np.floating,)):
                return float(o)
            if isinstance(o, np.ndarray):
                return o.tolist()
            # 其它不可序列化对象，退化为字符串
            return str(o)

        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=2, default=_default)
            print(json_str)
            return
        except Exception:
            # 若JSON序列化失败，回退到通用打印
            pass

    # 其他情况使用原有的通用格式化打印
    pprint_data(data, **kwargs)


def debug(data: Any, var_name: str = "variable") -> None:
    """调试打印函数"""
    pprint_data(data, debug_mode=True, title=var_name)


def compare(
    data1: Any, data2: Any, title1: str = "数据1", title2: str = "数据2"
) -> None:
    """比较两个数据"""
    pprint_data(data1, compare_with=data2, compare_titles=(title1, title2))


# =============================================================================
# 使用示例
# =============================================================================

if __name__ == "__main__":
    # 创建示例数据
    sample_dict_array = [
        {
            "name": "Alice",
            "age": 25,
            "city": "New York",
            "salary": 50000.0,
            "department": "Engineering",
        },
        {
            "name": "Bob",
            "age": 30,
            "city": "London",
            "salary": 60000.0,
            "department": "Marketing",
        },
        {
            "name": "Charlie",
            "age": 35,
            "city": "Paris",
            "salary": 70000.0,
            "department": "Engineering",
        },
        {
            "name": "Diana",
            "age": 28,
            "city": "Tokyo",
            "salary": 55000.0,
            "department": "Sales",
        },
        {
            "name": "Eve",
            "age": 32,
            "city": "Berlin",
            "salary": 65000.0,
            "department": "Marketing",
        },
        {
            "name": "Frank",
            "age": 29,
            "city": "Sydney",
            "salary": 58000.0,
            "department": "Engineering",
        },
        {
            "name": "Grace",
            "age": 31,
            "city": "Toronto",
            "salary": 62000.0,
            "department": "Marketing",
        },
        {
            "name": "Henry",
            "age": 27,
            "city": "Mumbai",
            "salary": 52000.0,
            "department": "Sales",
        },
        {
            "name": "Ivy",
            "age": 33,
            "city": "Singapore",
            "salary": 68000.0,
            "department": "Engineering",
        },
        {
            "name": "Jack",
            "age": 26,
            "city": "Dubai",
            "salary": 54000.0,
            "department": "Marketing",
        },
        {
            "name": "Kate",
            "age": 34,
            "city": "Hong Kong",
            "salary": 71000.0,
            "department": "Engineering",
        },
        {
            "name": "Liam",
            "age": 28,
            "city": "Mumbai",
            "salary": 56000.0,
            "department": "Sales",
        },
        {
            "name": "Mia",
            "age": 30,
            "city": "Sydney",
            "salary": 61000.0,
            "department": "Marketing",
        },
        {
            "name": "Noah",
            "age": 32,
            "city": "Toronto",
            "salary": 66000.0,
            "department": "Engineering",
        },
        {
            "name": "Olivia",
            "age": 29,
            "city": "Singapore",
            "salary": 59000.0,
            "department": "Marketing",
        },
        {
            "name": "Peter",
            "age": 27,
            "city": "Dubai",
            "salary": 53000.0,
            "department": "Sales",
        },
        {
            "name": "Quinn",
            "age": 35,
            "city": "Hong Kong",
            "salary": 72000.0,
            "department": "Engineering",
        },
        {
            "name": "Ruby",
            "age": 31,
            "city": "Mumbai",
            "salary": 63000.0,
            "department": "Marketing",
        },
        {
            "name": "Sam",
            "age": 28,
            "city": "Sydney",
            "salary": 57000.0,
            "department": "Sales",
        },
        {
            "name": "Tina",
            "age": 33,
            "city": "Toronto",
            "salary": 69000.0,
            "department": "Engineering",
        },
        {
            "name": "Uma",
            "age": 30,
            "city": "Singapore",
            "salary": 62000.0,
            "department": "Marketing",
        },
        {
            "name": "Victor",
            "age": 29,
            "city": "Dubai",
            "salary": 58000.0,
            "department": "Sales",
        },
        {
            "name": "Wendy",
            "age": 34,
            "city": "Hong Kong",
            "salary": 70000.0,
            "department": "Engineering",
        },
        {
            "name": "Xavier",
            "age": 32,
            "city": "Mumbai",
            "salary": 64000.0,
            "department": "Marketing",
        },
        {
            "name": "Yara",
            "age": 28,
            "city": "Sydney",
            "salary": 55000.0,
            "department": "Sales",
        },
        {
            "name": "Zane",
            "age": 35,
            "city": "Toronto",
            "salary": 73000.0,
            "department": "Engineering",
        },
    ]

    sample_df = pd.DataFrame(sample_dict_array)

    sample_dict = {
        "user_info": {
            "name": "Alice",
            "age": 25,
            "contact": {"email": "alice@example.com", "phone": "123-456-7890"},
        },
        "preferences": ["reading", "music", "sports"],
        "metadata": {"created_at": datetime.now(), "version": 1.0},
    }

    sample_list = list(range(30))  # 30个元素的列表

    sample_array = np.random.randn(25, 3)  # 25行的数组

    # 演示各种打印功能
    print("=== 演示 pprint_data 功能 ===")

    # 1. 默认打印（前20行，所有列）
    print("\n1. 默认打印（前20行，所有列）:")
    pprint_data(sample_dict_array, title="默认打印")

    # 2. 自定义打印行数
    print("\n2. 自定义打印行数（前5行）:")
    pprint_data(sample_dict_array, title="前5行", max_rows=5)

    # 3. 自定义打印行数（前10行）
    print("\n3. 自定义打印行数（前10行）:")
    pprint_data(sample_dict_array, title="前10行", max_rows=10)

    # 4. 自定义表头（只打印特定列）
    print("\n4. 自定义表头（只打印name和age列）:")
    pprint_data(sample_dict_array, title="只打印name和age", columns=["name", "age"])

    # 5. 自定义表头和行数
    print("\n5. 自定义表头和行数（前3行，只打印name, city, salary）:")
    pprint_data(
        sample_dict_array,
        title="自定义表头和行数",
        max_rows=3,
        columns=["name", "city", "salary"],
    )

    # 6. DataFrame测试
    print("\n6. DataFrame默认打印（前20行）:")
    pprint_data(sample_df, title="DataFrame默认打印")

    # 7. DataFrame自定义行数和表头
    print("\n7. DataFrame自定义行数和表头（前8行，特定列）:")
    pprint_data(
        sample_df,
        title="DataFrame自定义",
        max_rows=8,
        columns=["name", "age", "department", "salary"],
    )

    # 8. 列表测试
    print("\n8. 列表默认打印（前20项）:")
    pprint_data(sample_list, title="列表默认打印")

    # 9. 列表自定义行数
    print("\n9. 列表自定义行数（前15项）:")
    pprint_data(sample_list, title="列表前15项", max_rows=15)

    # 10. NumPy数组测试
    print("\n10. NumPy数组默认打印（前20行）:")
    pprint_data(sample_array, title="NumPy数组默认打印")

    # 11. NumPy数组自定义行数
    print("\n11. NumPy数组自定义行数（前12行）:")
    pprint_data(sample_array, title="NumPy数组前12行", max_rows=12)

    # 12. 测试不存在的列
    print("\n12. 测试不存在的列:")
    pprint_data(
        sample_dict_array,
        title="测试不存在的列",
        columns=["name", "nonexistent_column", "age"],
    )

    # 13. 使用便捷函数
    print("\n13. 使用便捷函数:")
    pprint(sample_dict_array, title="便捷函数默认打印")
    pprint(
        sample_dict_array, title="便捷函数自定义", max_rows=7, columns=["name", "city"]
    )
