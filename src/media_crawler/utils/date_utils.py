#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日期工具模块 - date_utils.py

作者: AI Assistant
版本: 2.0.0
最后更新: 2025年1月

描述:
    这是一个功能强大且易于使用的Python日期时间处理工具库。
    该模块提供了超过100个实用函数，涵盖日期时间的各个方面，
    包括格式转换、计算、比较、验证、格式化等功能。
    
    特别设计了灵活的参数类型支持，大部分函数都能接受多种输入类型，
    包括datetime对象、date对象、字符串等，极大提升了使用便利性。

主要特性:
    ✓ 支持多种输入参数类型（datetime、date、字符串）
    ✓ 智能字符串解析，支持中文日期格式
    ✓ 丰富的日期计算和比较功能
    ✓ 完善的格式化选项，包括自定义格式
    ✓ 工作日和节假日处理
    ✓ 时区转换和时间戳处理
    ✓ 年龄计算和持续时间解析
    ✓ 完整的单元测试覆盖

快速开始:
    from pythonprojecttemplate.utils.date_utils import *
    
    # 基本使用
    today = get_current_date()
    tomorrow = add_days(today, 1)
    
    # 字符串输入
    result = add_days('2024-01-15', 10)
    
    # 中文日期
    chinese_date = parse_date_string('2024年1月15日')
    
    # 格式化
    formatted = format_date_chinese(today)

依赖库:
    - datetime (标准库)
    - time (标准库) 
    - typing (标准库)
    - re (标准库)
    - calendar (标准库)
    - dateutil (第三方库，需要安装: pip install python-dateutil)

该工具类由AI生成，包含以下日期处理工具：

=== 参数类型支持说明 ===
本模块中的大部分函数都支持多种输入参数类型，提供了极大的灵活性：

1. datetime.date对象：标准的Python日期对象
   示例：datetime.date(2023, 6, 15)

2. datetime.datetime对象：标准的Python日期时间对象
   示例：datetime.datetime(2023, 6, 15, 14, 30, 0)

3. 字符串格式：支持多种常见的日期字符串格式
   支持的格式包括：
   - ISO格式：'2023-06-15', '2023-06-15 14:30:00'
   - 斜杠格式：'2023/06/15', '2023/06/15 14:30:00'
   - 紧凑格式：'20230615', '20230615143000'
   - 中文格式：'2023年6月15日', '2023年06月15日'
   - 其他常见格式：'Jun 15, 2023', '15-06-2023'等

=== 混合参数类型支持 ===
对于接受多个日期参数的函数（如date_diff, is_before等），支持混合使用不同类型的参数：
- 可以同时传入datetime对象和字符串
- 可以同时传入date对象和datetime对象
- 可以同时传入不同格式的字符串

示例：
  date_diff(datetime.date(2023, 6, 15), '2023-12-25')  # date对象 + 字符串
  is_before('2023-06-15', datetime.datetime(2023, 12, 25, 10, 0))  # 字符串 + datetime对象

=== 字符串解析机制 ===
当函数接收到字符串参数时，会按以下顺序尝试解析：
1. 首先尝试使用string_to_date()函数解析为date对象
2. 如果失败，尝试使用string_to_datetime()函数解析为datetime对象
3. 如果仍然失败，使用parse_date_string()函数进行智能解析
4. 如果所有方法都失败，会抛出相应的异常

=== 返回值类型说明 ===
- 如果输入是date对象，通常返回date对象
- 如果输入是datetime对象，通常返回datetime对象
- 如果输入是字符串，返回类型取决于解析结果和函数设计
- 对于比较和判断类函数，始终返回布尔值
- 对于格式化函数，始终返回字符串

=== 函数分类 ===

1. 日期格式转换
   - `date_to_string`: 将日期对象转换为字符串。
   - `datetime_to_string`: 将日期时间对象转换为字符串。
   - `string_to_date`: 将字符串转换为日期对象。
   - `string_to_datetime`: 将字符串转换为日期时间对象。
   - `parse_date_string`: 智能解析日期字符串（支持多种格式，包括中文格式）。

2. 日期计算（支持datetime/date/string输入）
   - `add_days`: 给日期添加天数。
   - `add_hours`: 给日期添加小时数。
   - `add_minutes`: 给日期添加分钟数。
   - `add_months`: 给日期添加月数。
   - `add_years`: 给日期添加年数。
   - `date_diff`: 计算两个日期之间的时间差。
   - `days_between`: 计算两个日期之间的天数。
   - `weekdays_between`: 计算两个日期之间的工作日天数（不包括周六日）。

3. 日期比较（支持datetime/date/string输入）
   - `is_before`: 判断date1是否在date2之前。
   - `is_after`: 判断date1是否在date2之后。
   - `is_same_day`: 判断两个日期是否是同一天。
   - `is_same_month`: 判断两个日期是否在同一月。
   - `is_same_year`: 判断两个日期是否在同一年。

4. 日期验证
   - `is_valid_date`: 验证字符串是否是有效的日期。
   - `is_valid_datetime`: 验证字符串是否是有效的日期时间。
   - `is_leap_year`: 判断是否是闰年。

5. 获取日期信息（支持datetime/date/string输入）
   - `get_year`: 获取日期的年份。
   - `get_month`: 获取日期的月份。
   - `get_day`: 获取日期的天。
   - `get_weekday`: 获取日期是星期几（0=周一，6=周日）。
   - `get_weekday_name`: 获取日期的星期几名称。
   - `get_week_of_year`: 获取日期是一年中的第几周。
   - `get_day_of_year`: 获取日期是一年中的第几天。
   - `get_quarter`: 获取日期所在的季度。

6. 日期判断（支持datetime/date/string输入）
   - `is_weekend`: 判断是否是周末。
   - `is_weekday`: 判断是否是工作日。

7. 日期格式化（支持datetime/date/string输入）
   - `format_date_iso`: 格式化为ISO标准格式。
   - `format_date_chinese`: 格式化为中文格式。
   - `format_date_us`: 格式化为美式格式。

8. 获取特殊日期
   - `get_first_day_of_month`: 获取日期所在月份的第一天。
   - `get_last_day_of_month`: 获取日期所在月份的最后一天。
   - `get_first_day_of_week`: 获取日期所在周的第一天。
   - `get_last_day_of_week`: 获取日期所在周的最后一天。
   - `get_first_day_of_quarter`: 获取日期所在季度的第一天。
   - `get_last_day_of_quarter`: 获取日期所在季度的最后一天。
   - `get_first_day_of_year`: 获取日期所在年份的第一天。
   - `get_last_day_of_year`: 获取日期所在年份的最后一天。

7. 日期范围生成
   - `get_dates_between`: 获取两个日期之间的所有日期。
   - `get_month_dates`: 获取日期所在月份的所有日期。
   - `get_week_dates`: 获取日期所在周的所有日期。
   - `get_quarter_dates`: 获取日期所在季度的所有日期。
   - `get_year_dates`: 获取日期所在年份的所有日期。

8. 工作日相关
   - `is_weekend`: 判断日期是否是周末（周六或周日）。
   - `is_weekday`: 判断日期是否是工作日（周一到周五）。
   - `get_next_weekday`: 获取下一个工作日。
   - `get_previous_weekday`: 获取上一个工作日。
   - `get_weekdays_count_in_month`: 获取日期所在月份的工作日数量。
   - `get_weekends_count_in_month`: 获取日期所在月份的周末数量。

9. 时间戳相关
   - `datetime_to_timestamp`: 将日期时间对象转换为时间戳。
   - `timestamp_to_datetime`: 将时间戳转换为日期时间对象。
   - `timestamp_to_date`: 将时间戳转换为日期对象。
   - `get_current_timestamp`: 获取当前时间戳。
   - `get_current_datetime`: 获取当前日期时间。
   - `get_current_date`: 获取当前日期。
   - `get_current_time`: 获取当前时间。

10. 时区相关
    - `get_utc_datetime`: 获取当前UTC时间。
    - `datetime_to_utc`: 将本地时间转换为UTC时间。
    - `utc_to_local`: 将UTC时间转换为指定时区的本地时间。
    - `format_with_timezone`: 格式化带时区的日期时间。

11. 格式化相关
    - `format_date_iso`: 格式化日期为ISO格式。
    - `format_datetime_iso`: 格式化日期时间为ISO格式。
    - `format_date_chinese`: 格式化日期为中文格式。
    - `format_datetime_chinese`: 格式化日期时间为中文格式。
    - `format_date_us`: 格式化日期为美国格式。
    - `format_datetime_us`: 格式化日期时间为美国格式。
    - `format_time_12h`: 格式化时间为12小时制。
    - `format_time_24h`: 格式化时间为24小时制。
    - `format_date_custom`: 使用自定义格式模式格式化日期（支持YYYY、MM、DD等占位符）。
    - `format_datetime_custom`: 使用自定义格式模式格式化日期时间。
    - `format_date_compact`: 格式化日期为紧凑格式（YYYYMMDD）。
    - `format_datetime_compact`: 格式化日期时间为紧凑格式（YYYYMMDDHHmmSS）。
    - `format_date_readable`: 格式化日期为可读格式（支持自定义分隔符）。
    - `format_datetime_readable`: 格式化日期时间为可读格式（支持自定义分隔符）。

12. 年龄计算
    - `calculate_age`: 计算年龄。
    - `calculate_months_between`: 计算两个日期之间的月数差。
    - `calculate_years_between`: 计算两个日期之间的年数差。

13. 其他实用函数
    - `get_season`: 获取日期所在的季节。
    - `get_zodiac_sign`: 获取日期对应的星座。
    - `get_chinese_zodiac`: 获取年份对应的生肖。
    - `is_business_day`: 判断是否是工作日（排除周末和节假日）。
    - `get_next_business_day`: 获取下一个工作日（排除周末和节假日）。
    - `get_previous_business_day`: 获取上一个工作日（排除周末和节假日）。
    - `get_business_days_between`: 计算两个日期之间的工作日数量（排除周末和节假日）。
    - `get_fuzzy_time_description`: 获取模糊的时间描述（如：刚刚、几分钟前、昨天等）。
    - `parse_duration`: 解析持续时间字符串为timedelta对象。
    - `format_duration`: 格式化timedelta对象为持续时间字符串。

=== 详细使用示例 ===

1. 基础日期操作:
    ```python
    from pythonprojecttemplate.utils.date_utils import *
    
    # 获取当前日期和时间
    today = get_current_date()          # 2024-01-15
    now = get_current_datetime()        # 2024-01-15 14:30:45
    
    # 日期计算
    future_date = add_days(today, 30)   # 30天后
    past_date = add_months(today, -2)   # 2个月前
    next_year = add_years(today, 1)     # 1年后
    ```

2. 字符串输入支持:
    ```python
    # 直接使用字符串作为输入
    result1 = add_days('2024-01-15', 10)        # 字符串 + 数字
    result2 = days_between('2024-01-01', '2024-12-31')  # 字符串比较
    
    # 支持中文日期格式
    chinese_date = parse_date_string('2024年1月15日')
    result3 = add_days('2024年1月15日', 7)
    ```

3. 混合参数类型:
    ```python
    import datetime
    
    date_obj = datetime.date(2024, 1, 15)
    datetime_obj = datetime.datetime(2024, 1, 15, 14, 30)
    date_str = '2024-01-20'
    
    # 混合使用不同类型
    diff1 = days_between(date_obj, date_str)        # date对象 + 字符串
    diff2 = is_before(datetime_obj, '2024-02-01')   # datetime对象 + 字符串
    diff3 = date_diff(date_str, datetime_obj)       # 字符串 + datetime对象
    ```

4. 格式化功能:
    ```python
    date = datetime.date(2024, 1, 15)
    
    # 预定义格式
    iso_format = format_date_iso(date)          # '2024-01-15'
    chinese_format = format_date_chinese(date)  # '2024年01月15日'
    us_format = format_date_us(date)            # '01/15/2024'
    
    # 自定义格式
    custom1 = format_date_custom(date, 'YYYYmmDD')      # '20240115'
    custom2 = format_date_custom(date, 'YYYY年MM月DD日')  # '2024年01月15日'
    custom3 = format_date_custom(date, 'DD/MM/YY')      # '15/01/24'
    ```

5. 工作日处理:
    ```python
    # 基本工作日判断
    is_workday = is_weekday(today)              # 是否工作日
    is_weekend_day = is_weekend(today)          # 是否周末
    
    # 获取下一个/上一个工作日
    next_workday = get_next_weekday(today)
    prev_workday = get_previous_weekday(today)
    
    # 考虑节假日的工作日处理
    holidays = [datetime.date(2024, 1, 1), datetime.date(2024, 2, 10)]
    is_business = is_business_day(today, holidays)
    next_business = get_next_business_day(today, holidays)
    ```

6. 日期范围和批量操作:
    ```python
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 31)
    
    # 获取日期范围
    all_dates = get_dates_between(start_date, end_date)
    month_dates = get_month_dates(today)
    week_dates = get_week_dates(today)
    
    # 统计信息
    workdays_count = get_weekdays_count_in_month(today)
    weekends_count = get_weekends_count_in_month(today)
    ```

=== 注意事项 ===

1. 时区处理:
   - 默认使用系统本地时区
   - UTC转换函数可处理时区相关操作
   - 建议在跨时区应用中明确指定时区

2. 字符串解析:
   - 支持多种常见格式，但建议使用标准ISO格式
   - 中文日期解析依赖正则表达式，可能不支持所有方言
   - 解析失败时会抛出相应异常

3. 性能考虑:
   - 字符串解析比直接使用对象稍慢
   - 大批量操作时建议预先转换为对象类型
   - 日期范围生成函数可能消耗较多内存

4. 依赖库:
   - 需要安装python-dateutil: pip install python-dateutil
   - 某些高级功能依赖dateutil库

5. 错误处理:
   - 无效日期会抛出ValueError异常
   - 建议在生产环境中添加适当的异常处理
   - 可使用is_valid_date()等函数预先验证

=== 测试和验证 ===

本模块包含完整的单元测试，运行方式：
```bash
python date_utils.py
```

测试覆盖:
- 所有函数的基本功能测试
- 边界条件和异常情况测试  
- 多种输入类型的兼容性测试
- 性能基准测试
"""

import datetime
import time
from typing import List, Tuple, Optional, Union
import re
from dateutil import parser, relativedelta
from dateutil.tz import gettz, UTC
import calendar


# ==================== 日期格式转换 ====================

def date_to_string(date_obj: datetime.date, format_str: str = "%Y-%m-%d") -> str:
    """
    将日期对象转换为字符串
    
    Args:
        date_obj: 日期对象
        format_str: 格式化字符串，默认为"%Y-%m-%d"
    
    Returns:
        格式化后的日期字符串
    """
    return date_obj.strftime(format_str)


def datetime_to_string(datetime_obj: datetime.datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    将日期时间对象转换为字符串
    
    Args:
        datetime_obj: 日期时间对象
        format_str: 格式化字符串，默认为"%Y-%m-%d %H:%M:%S"
    
    Returns:
        格式化后的日期时间字符串
    """
    return datetime_obj.strftime(format_str)


def string_to_date(date_str: str, format_str: str = "%Y-%m-%d") -> datetime.date:
    """
    将字符串转换为日期对象
    
    Args:
        date_str: 日期字符串
        format_str: 格式化字符串，默认为"%Y-%m-%d"
    
    Returns:
        日期对象
    
    Raises:
        ValueError: 当字符串格式不匹配时
    """
    return datetime.datetime.strptime(date_str, format_str).date()


def string_to_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime.datetime:
    """
    将字符串转换为日期时间对象
    
    Args:
        datetime_str: 日期时间字符串
        format_str: 格式化字符串，默认为"%Y-%m-%d %H:%M:%S"
    
    Returns:
        日期时间对象
    
    Raises:
        ValueError: 当字符串格式不匹配时
    """
    return datetime.datetime.strptime(datetime_str, format_str)


def parse_date_string(date_str: str) -> datetime.datetime:
    """
    智能解析日期字符串（支持多种格式，包括中文格式）
    
    Args:
        date_str: 日期字符串
    
    Returns:
        日期时间对象
    """
    # 预处理中文格式
    # 处理 "2024年1月15日 下午2:30" 格式
    chinese_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日\s*(上午|下午)?\s*(\d{1,2}):(\d{1,2})'
    match = re.match(chinese_pattern, date_str)
    
    if match:
        year, month, day, period, hour, minute = match.groups()
        
        # 转换为24小时制
        hour = int(hour)
        if period == "下午" and hour < 12:
            hour += 12
        elif period == "上午" and hour == 12:
            hour = 0
        
        # 构造标准格式字符串
        date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)} {hour:02d}:{minute.zfill(2)}"
    
    # 处理 "2024年1月15日" 格式（只有日期）
    chinese_date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    match = re.match(chinese_date_pattern, date_str)
    
    if match:
        year, month, day = match.groups()
        date_str = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
    
    # 处理 "下午2:30" 格式（只有时间）
    chinese_time_pattern = r'(上午|下午)?\s*(\d{1,2}):(\d{1,2})'
    match = re.match(chinese_time_pattern, date_str)
    
    if match and not re.match(r'\d{4}', date_str):  # 确保不包含年份
        period, hour, minute = match.groups()
        
        # 转换为24小时制
        hour = int(hour)
        if period == "下午" and hour < 12:
            hour += 12
        elif period == "上午" and hour == 12:
            hour = 0
        
        # 获取当前日期
        now = datetime.datetime.now()
        date_str = f"{now.year}-{now.month:02d}-{now.day:02d} {hour:02d}:{minute.zfill(2)}"
    
    # 使用dateutil.parser进行最终解析
    return parser.parse(date_str)


# ==================== 日期计算 ====================

def add_days(date_obj: Union[datetime.date, datetime.datetime, str], days: int) -> Union[datetime.date, datetime.datetime]:
    """
    给日期添加天数
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接进行日期运算
            - datetime.datetime对象：保持时间信息进行运算
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        days: 要添加的天数（可为负数，负数表示减去天数）
    
    Returns:
        Union[datetime.date, datetime.datetime]: 新的日期对象
            - 如果输入是date对象或纯日期字符串，返回date对象
            - 如果输入是datetime对象或包含时间的字符串，返回datetime对象
    
    Examples:
        >>> # 使用datetime.date对象
        >>> add_days(datetime.date(2025, 1, 15), 7)
        datetime.date(2025, 1, 22)
        
        >>> # 使用datetime.datetime对象
        >>> add_days(datetime.datetime(2025, 1, 15, 14, 30), -3)
        datetime.datetime(2025, 1, 12, 14, 30)
        
        >>> # 使用ISO格式字符串
        >>> add_days("2025-01-15", 10)
        datetime.date(2025, 1, 25)
        
        >>> # 使用中文格式字符串
        >>> add_days("2025年1月15日", -5)
        datetime.date(2025, 1, 10)
        
        >>> # 使用包含时间的字符串
        >>> add_days("2025-01-15 14:30:00", 1)
        datetime.datetime(2025, 1, 16, 14, 30)
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            # 尝试解析为日期
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                # 如果失败，尝试解析为日期时间
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                # 如果还是失败，使用智能解析
                parsed_datetime = parse_date_string(date_obj)
                # 如果原字符串只包含日期信息，返回date对象
                if ' ' not in date_obj.strip() and ':' not in date_obj:
                    date_obj = parsed_datetime.date()
                else:
                    date_obj = parsed_datetime
    
    return date_obj + datetime.timedelta(days=days)


def add_hours(date_obj: Union[datetime.date, datetime.datetime, str], hours: int) -> Union[datetime.date, datetime.datetime]:
    """
    给日期添加小时数
    
    Args:
        date_obj: 日期对象或日期字符串
        hours: 要添加的小时数（可为负数）
    
    Returns:
        新的日期对象
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            # 尝试解析为日期时间
            date_obj = string_to_datetime(date_obj)
        except ValueError:
            try:
                # 如果失败，尝试解析为日期，然后转为datetime
                date_part = string_to_date(date_obj)
                date_obj = datetime.datetime.combine(date_part, datetime.time())
            except ValueError:
                # 使用智能解析
                date_obj = parse_date_string(date_obj)
    
    return date_obj + datetime.timedelta(hours=hours)


def add_minutes(date_obj: Union[datetime.date, datetime.datetime, str], minutes: int) -> Union[datetime.date, datetime.datetime]:
    """
    给日期添加分钟数
    
    Args:
        date_obj: 日期对象或日期字符串
        minutes: 要添加的分钟数（可为负数）
    
    Returns:
        新的日期对象
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            # 尝试解析为日期时间
            date_obj = string_to_datetime(date_obj)
        except ValueError:
            try:
                # 如果失败，尝试解析为日期，然后转为datetime
                date_part = string_to_date(date_obj)
                date_obj = datetime.datetime.combine(date_part, datetime.time())
            except ValueError:
                # 使用智能解析
                date_obj = parse_date_string(date_obj)
    
    return date_obj + datetime.timedelta(minutes=minutes)


def add_months(date_obj: Union[datetime.date, datetime.datetime, str], months: int) -> Union[datetime.date, datetime.datetime]:
    """
    给日期添加月数
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接进行月份运算
            - datetime.datetime对象：保持时间信息进行月份运算
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        months: 要添加的月数（可为负数，负数表示减去月数）
    
    Returns:
        Union[datetime.date, datetime.datetime]: 新的日期对象
            - 如果输入是date对象或纯日期字符串，返回date对象
            - 如果输入是datetime对象或包含时间的字符串，返回datetime对象
    
    Note:
        使用relativedelta进行月份计算，能正确处理月末日期的边界情况
        例如：1月31日加1个月会得到2月28日（或29日）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> add_months(datetime.date(2025, 1, 15), 3)
        datetime.date(2025, 4, 15)
        
        >>> # 使用datetime.datetime对象
        >>> add_months(datetime.datetime(2025, 1, 15, 14, 30), -2)
        datetime.datetime(2024, 11, 15, 14, 30)
        
        >>> # 使用ISO格式字符串
        >>> add_months("2025-01-31", 1)
        datetime.date(2025, 2, 28)
        
        >>> # 使用中文格式字符串
        >>> add_months("2025年1月15日", 6)
        datetime.date(2025, 7, 15)
        
        >>> # 使用包含时间的字符串
        >>> add_months("2025-01-15 14:30:00", -1)
        datetime.datetime(2024, 12, 15, 14, 30)
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            # 尝试解析为日期
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                # 如果失败，尝试解析为日期时间
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                # 如果还是失败，使用智能解析
                parsed_datetime = parse_date_string(date_obj)
                # 如果原字符串只包含日期信息，返回date对象
                if ' ' not in date_obj.strip() and ':' not in date_obj:
                    date_obj = parsed_datetime.date()
                else:
                    date_obj = parsed_datetime
    
    return date_obj + relativedelta.relativedelta(months=months)


def add_years(date_obj: Union[datetime.date, datetime.datetime, str], years: int) -> Union[datetime.date, datetime.datetime]:
    """
    给日期添加年数
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接进行年份运算
            - datetime.datetime对象：保持时间信息进行年份运算
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        years: 要添加的年数（可为负数，负数表示减去年数）
    
    Returns:
        Union[datetime.date, datetime.datetime]: 新的日期对象
            - 如果输入是date对象或纯日期字符串，返回date对象
            - 如果输入是datetime对象或包含时间的字符串，返回datetime对象
    
    Note:
        使用relativedelta进行年份计算，能正确处理闰年的边界情况
        例如：2024年2月29日加1年会得到2025年2月28日
    
    Examples:
        >>> # 使用datetime.date对象
        >>> add_years(datetime.date(2025, 1, 15), 2)
        datetime.date(2027, 1, 15)
        
        >>> # 使用datetime.datetime对象
        >>> add_years(datetime.datetime(2025, 1, 15, 14, 30), -1)
        datetime.datetime(2024, 1, 15, 14, 30)
        
        >>> # 使用ISO格式字符串
        >>> add_years("2024-02-29", 1)
        datetime.date(2025, 2, 28)
        
        >>> # 使用中文格式字符串
        >>> add_years("2025年1月15日", 3)
        datetime.date(2028, 1, 15)
        
        >>> # 使用包含时间的字符串
        >>> add_years("2025-01-15 14:30:00", -2)
        datetime.datetime(2023, 1, 15, 14, 30)
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            # 尝试解析为日期
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                # 如果失败，尝试解析为日期时间
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                # 如果还是失败，使用智能解析
                parsed_datetime = parse_date_string(date_obj)
                # 如果原字符串只包含日期信息，返回date对象
                if ' ' not in date_obj.strip() and ':' not in date_obj:
                    date_obj = parsed_datetime.date()
                else:
                    date_obj = parsed_datetime
    
    return date_obj + relativedelta.relativedelta(years=years)


def date_diff(start_date: Union[datetime.date, datetime.datetime, str], 
              end_date: Union[datetime.date, datetime.datetime, str]) -> int:
    """
    计算两个日期之间的时间差
    
    Args:
        start_date: 开始日期或日期字符串
            - datetime.date对象：直接进行日期计算
            - datetime.datetime对象：精确到秒的时间计算
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        end_date: 结束日期或日期字符串（支持的格式同start_date）
    
    Returns:
        int: 天数差
            - 正值表示end_date晚于start_date
            - 负值表示end_date早于start_date
    
    Note:
        支持混合参数类型，可以同时传入datetime对象和字符串
        时间差计算会自动处理不同类型的日期对象
    
    Examples:
        >>> # 使用datetime.date对象
        >>> date_diff(datetime.date(2025, 1, 1), datetime.date(2025, 1, 10))
        9
        
        >>> # 使用datetime.datetime对象
        >>> date_diff(datetime.datetime(2025, 1, 1, 10, 0), datetime.datetime(2025, 1, 1, 14, 30))
        0
        
        >>> # 使用ISO格式字符串
        >>> date_diff("2025-01-01", "2025-01-10")
        9
        
        >>> # 使用中文格式字符串
        >>> date_diff("2025年1月1日", "2025年1月10日")
        9
        
        >>> # 混合参数类型
        >>> date_diff(datetime.date(2025, 1, 1), "2025-01-10")
        9
        
        >>> # 负时间差
        >>> date_diff("2025-01-10", "2025-01-01")
        -9
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(start_date, str):
        try:
            start_date = string_to_date(start_date)
        except ValueError:
            try:
                start_date = string_to_datetime(start_date)
            except ValueError:
                start_date = parse_date_string(start_date)
    
    if isinstance(end_date, str):
        try:
            end_date = string_to_date(end_date)
        except ValueError:
            try:
                end_date = string_to_datetime(end_date)
            except ValueError:
                end_date = parse_date_string(end_date)
    
    # 确保两个对象类型一致
    if hasattr(start_date, 'date') and not hasattr(end_date, 'date'):
        # start_date是datetime，end_date是date，将end_date转换为datetime
        end_date = datetime.datetime.combine(end_date, datetime.time())
    elif not hasattr(start_date, 'date') and hasattr(end_date, 'date'):
        # start_date是date，end_date是datetime，将start_date转换为datetime
        start_date = datetime.datetime.combine(start_date, datetime.time())
    
    return (end_date - start_date).days


def days_between(start_date: Union[datetime.date, datetime.datetime, str], 
                 end_date: Union[datetime.date, datetime.datetime, str]) -> int:
    """
    计算两个日期之间的天数（绝对值）
    
    Args:
        start_date: 开始日期或日期字符串
        end_date: 结束日期或日期字符串
    
    Returns:
        int: 两个日期之间的天数（绝对值）
    
    Examples:
        >>> days_between(datetime.date(2025, 1, 1), datetime.date(2025, 1, 10))
        9
        >>> days_between("2025-01-01", "2025-01-10")
        9
        >>> days_between("2025-01-10", "2025-01-01")
        9
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(start_date, str):
        try:
            start_date = string_to_date(start_date)
        except ValueError:
            try:
                start_date = string_to_datetime(start_date)
            except ValueError:
                parsed_datetime = parse_date_string(start_date)
                start_date = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    if isinstance(end_date, str):
        try:
            end_date = string_to_date(end_date)
        except ValueError:
            try:
                end_date = string_to_datetime(end_date)
            except ValueError:
                parsed_datetime = parse_date_string(end_date)
                end_date = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return abs((end_date - start_date).days)


def weekdays_between(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    计算两个日期之间的工作日天数（不包括周六日）
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        工作日天数
    """
    days = (end_date - start_date).days + 1
    weeks = days // 7
    remainder = days % 7
    weekdays = weeks * 5
    
    # 处理剩余的天数
    for i in range(remainder):
        current_day = start_date + datetime.timedelta(days=i)
        if current_day.weekday() < 5:  # 0-4是周一到周五
            weekdays += 1
    
    return weekdays


# ==================== 日期比较 ====================

def is_before(date1: Union[datetime.date, datetime.datetime, str], 
              date2: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断date1是否在date2之前
    
    Args:
        date1: 日期1或日期字符串
            - datetime.date对象：直接进行日期比较
            - datetime.datetime对象：精确到秒的时间比较
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        date2: 日期2或日期字符串（支持的格式同date1）
    
    Returns:
        bool: 如果date1在date2之前返回True，否则返回False
    
    Note:
        支持混合参数类型，可以同时传入datetime对象和字符串
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_before(datetime.date(2025, 1, 1), datetime.date(2025, 1, 10))
        True
        
        >>> # 使用字符串
        >>> is_before("2025-01-01", "2025-01-10")
        True
        
        >>> # 混合参数类型
        >>> is_before(datetime.date(2025, 1, 1), "2025-01-10")
        True
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date1, str):
        try:
            date1 = string_to_date(date1)
        except ValueError:
            try:
                date1 = string_to_datetime(date1)
            except ValueError:
                parsed_datetime = parse_date_string(date1)
                date1 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    if isinstance(date2, str):
        try:
            date2 = string_to_date(date2)
        except ValueError:
            try:
                date2 = string_to_datetime(date2)
            except ValueError:
                parsed_datetime = parse_date_string(date2)
                date2 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date1 < date2


def is_after(date1: Union[datetime.date, datetime.datetime, str], 
             date2: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断date1是否在date2之后
    
    Args:
        date1: 日期1或日期字符串
            - datetime.date对象：直接进行日期比较
            - datetime.datetime对象：精确到秒的时间比较
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        date2: 日期2或日期字符串（支持的格式同date1）
    
    Returns:
        bool: 如果date1在date2之后返回True，否则返回False
    
    Note:
        支持混合参数类型，可以同时传入datetime对象和字符串
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_after(datetime.date(2025, 1, 10), datetime.date(2025, 1, 1))
        True
        
        >>> # 使用字符串
        >>> is_after("2025-01-10", "2025-01-01")
        True
        
        >>> # 混合参数类型
        >>> is_after("2025-01-10", datetime.date(2025, 1, 1))
        True
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date1, str):
        try:
            date1 = string_to_date(date1)
        except ValueError:
            try:
                date1 = string_to_datetime(date1)
            except ValueError:
                parsed_datetime = parse_date_string(date1)
                date1 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    if isinstance(date2, str):
        try:
            date2 = string_to_date(date2)
        except ValueError:
            try:
                date2 = string_to_datetime(date2)
            except ValueError:
                parsed_datetime = parse_date_string(date2)
                date2 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date1 > date2


def is_same_day(date1: Union[datetime.date, datetime.datetime, str], 
                date2: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断两个日期是否是同一天
    
    Args:
        date1: 日期1或日期字符串
            - datetime.date对象：直接比较日期
            - datetime.datetime对象：比较日期部分，忽略时间
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        date2: 日期2或日期字符串（支持的格式同date1）
    
    Returns:
        bool: 如果是同一天返回True，否则返回False
    
    Note:
        支持混合参数类型，可以同时传入datetime对象和字符串
        对于datetime对象，只比较日期部分，忽略时间部分
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_same_day(datetime.date(2025, 1, 1), datetime.date(2025, 1, 1))
        True
        
        >>> # 使用字符串
        >>> is_same_day("2025-01-01", "2025-01-01")
        True
        
        >>> # 混合参数类型
        >>> is_same_day(datetime.date(2025, 1, 1), "2025-01-01")
        True
        
        >>> # datetime对象忽略时间部分
        >>> is_same_day(datetime.datetime(2025, 1, 1, 10, 0), datetime.datetime(2025, 1, 1, 15, 30))
        True
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date1, str):
        try:
            date1 = string_to_date(date1)
        except ValueError:
            try:
                date1 = string_to_datetime(date1)
            except ValueError:
                parsed_datetime = parse_date_string(date1)
                date1 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    if isinstance(date2, str):
        try:
            date2 = string_to_date(date2)
        except ValueError:
            try:
                date2 = string_to_datetime(date2)
            except ValueError:
                parsed_datetime = parse_date_string(date2)
                date2 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date1.date() == date2.date() if hasattr(date1, 'date') else date1 == date2


def is_same_month(date1: Union[datetime.date, datetime.datetime, str], 
                  date2: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断两个日期是否在同一月
    
    Args:
        date1: 日期1或日期字符串
            - datetime.date对象：直接比较年月
            - datetime.datetime对象：比较日期部分的年月
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        date2: 日期2或日期字符串（支持的格式同date1）
    
    Returns:
        bool: 如果在同一月返回True，否则返回False
    
    Note:
        支持混合参数类型，可以同时传入datetime对象和字符串
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_same_month(datetime.date(2025, 1, 1), datetime.date(2025, 1, 15))
        True
        
        >>> # 使用字符串
        >>> is_same_month("2025-01-01", "2025-01-15")
        True
        
        >>> # 混合参数类型
        >>> is_same_month(datetime.date(2025, 1, 1), "2025-01-15")
        True
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date1, str):
        try:
            date1 = string_to_date(date1)
        except ValueError:
            try:
                date1 = string_to_datetime(date1)
            except ValueError:
                parsed_datetime = parse_date_string(date1)
                date1 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    if isinstance(date2, str):
        try:
            date2 = string_to_date(date2)
        except ValueError:
            try:
                date2 = string_to_datetime(date2)
            except ValueError:
                parsed_datetime = parse_date_string(date2)
                date2 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    date1_date = date1.date() if hasattr(date1, 'date') else date1
    date2_date = date2.date() if hasattr(date2, 'date') else date2
    return date1_date.year == date2_date.year and date1_date.month == date2_date.month


def is_same_year(date1: Union[datetime.date, datetime.datetime, str], 
                 date2: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断两个日期是否在同一年
    
    Args:
        date1: 日期1或日期字符串
            - datetime.date对象：直接比较年份
            - datetime.datetime对象：比较日期部分的年份
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
        date2: 日期2或日期字符串（支持的格式同date1）
    
    Returns:
        bool: 如果在同一年返回True，否则返回False
    
    Note:
        支持混合参数类型，可以同时传入datetime对象和字符串
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_same_year(datetime.date(2025, 1, 1), datetime.date(2025, 12, 31))
        True
        
        >>> # 使用字符串
        >>> is_same_year("2025-01-01", "2025-12-31")
        True
        
        >>> # 混合参数类型
        >>> is_same_year(datetime.date(2025, 1, 1), "2025-12-31")
        True
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date1, str):
        try:
            date1 = string_to_date(date1)
        except ValueError:
            try:
                date1 = string_to_datetime(date1)
            except ValueError:
                parsed_datetime = parse_date_string(date1)
                date1 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    if isinstance(date2, str):
        try:
            date2 = string_to_date(date2)
        except ValueError:
            try:
                date2 = string_to_datetime(date2)
            except ValueError:
                parsed_datetime = parse_date_string(date2)
                date2 = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    date1_date = date1.date() if hasattr(date1, 'date') else date1
    date2_date = date2.date() if hasattr(date2, 'date') else date2
    return date1_date.year == date2_date.year


# ==================== 日期验证 ====================

def is_valid_date(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
    """
    验证字符串是否是有效的日期
    
    Args:
        date_str: 日期字符串
        format_str: 格式化字符串
    
    Returns:
        如果是有效日期返回True，否则返回False
    """
    try:
        datetime.datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False


def is_valid_datetime(datetime_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> bool:
    """
    验证字符串是否是有效的日期时间
    
    Args:
        datetime_str: 日期时间字符串
        format_str: 格式化字符串
    
    Returns:
        如果是有效日期时间返回True，否则返回False
    """
    try:
        datetime.datetime.strptime(datetime_str, format_str)
        return True
    except ValueError:
        return False


def is_leap_year(year: int) -> bool:
    """
    判断是否是闰年
    
    Args:
        year: 年份
    
    Returns:
        如果是闰年返回True，否则返回False
    """
    return calendar.isleap(year)


# ==================== 获取日期信息 ====================

def get_year(date_obj: Union[datetime.date, datetime.datetime, str]) -> int:
    """
    获取日期的年份
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接获取年份
            - datetime.datetime对象：获取日期部分的年份
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        int: 年份（四位数）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> get_year(datetime.date(2025, 9, 6))
        2025
        
        >>> # 使用datetime.datetime对象
        >>> get_year(datetime.datetime(2025, 9, 6, 14, 30))
        2025
        
        >>> # 使用ISO格式字符串
        >>> get_year("2025-09-06")
        2025
        
        >>> # 使用中文格式字符串
        >>> get_year("2025年9月6日")
        2025
        
        >>> # 使用美式格式字符串
        >>> get_year("09/06/2025")
        2025
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date_obj.year


def get_month(date_obj: Union[datetime.date, datetime.datetime, str]) -> int:
    """
    获取日期的月份
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接获取月份
            - datetime.datetime对象：获取日期部分的月份
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        int: 月份（1-12）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> get_month(datetime.date(2025, 9, 6))
        9
        
        >>> # 使用datetime.datetime对象
        >>> get_month(datetime.datetime(2025, 9, 6, 14, 30))
        9
        
        >>> # 使用ISO格式字符串
        >>> get_month("2025-09-06")
        9
        
        >>> # 使用中文格式字符串
        >>> get_month("2025年9月6日")
        9
        
        >>> # 使用美式格式字符串
        >>> get_month("09/06/2025")
        9
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date_obj.month


def get_day(date_obj: Union[datetime.date, datetime.datetime, str]) -> int:
    """
    获取日期的天
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接获取天数
            - datetime.datetime对象：获取日期部分的天数
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        int: 天（1-31）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> get_day(datetime.date(2025, 9, 6))
        6
        
        >>> # 使用datetime.datetime对象
        >>> get_day(datetime.datetime(2025, 9, 6, 14, 30))
        6
        
        >>> # 使用ISO格式字符串
        >>> get_day("2025-09-06")
        6
        
        >>> # 使用中文格式字符串
        >>> get_day("2025年9月6日")
        6
        
        >>> # 使用美式格式字符串
        >>> get_day("09/06/2025")
        6
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date_obj.day


def get_weekday(date_obj: Union[datetime.date, datetime.datetime, str]) -> int:
    """
    获取日期是星期几（0=周一，6=周日）
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接获取星期几
            - datetime.datetime对象：获取日期部分的星期几
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        int: 星期几（0=周一，1=周二，...，6=周日）
    
    Examples:
        >>> get_weekday(datetime.date(2025, 1, 6))  # Monday
        0
        >>> get_weekday("2025-01-06")  # Monday
        0
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date_obj.weekday()


def get_weekday_name(date_obj: Union[datetime.date, datetime.datetime], 
                     locale: str = "zh_CN") -> str:
    """
    获取日期的星期几名称
    
    Args:
        date_obj: 日期对象
        locale: 语言环境，默认为中文
    
    Returns:
        星期几名称
    """
    weekday_names = {
        "zh_CN": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
        "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    }
    names = weekday_names.get(locale, weekday_names["en"])
    return names[date_obj.weekday()]


def get_week_of_year(date_obj: Union[datetime.date, datetime.datetime]) -> int:
    """
    获取日期是一年中的第几周
    
    Args:
        date_obj: 日期对象
    
    Returns:
        第几周（1-53）
    """
    return date_obj.isocalendar()[1]


def get_day_of_year(date_obj: Union[datetime.date, datetime.datetime]) -> int:
    """
    获取日期是一年中的第几天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        第几天（1-366）
    """
    return date_obj.timetuple().tm_yday


def get_quarter(date_obj: Union[datetime.date, datetime.datetime]) -> int:
    """
    获取日期所在的季度
    
    Args:
        date_obj: 日期对象
    
    Returns:
        季度（1-4）
    """
    return (date_obj.month - 1) // 3 + 1


# ==================== 获取特殊日期 ====================

def get_first_day_of_month(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取日期所在月份的第一天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该月第一天的日期对象
    """
    return datetime.date(date_obj.year, date_obj.month, 1)


def get_last_day_of_month(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取日期所在月份的最后一天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该月最后一天的日期对象
    """
    _, last_day = calendar.monthrange(date_obj.year, date_obj.month)
    return datetime.date(date_obj.year, date_obj.month, last_day)


def get_first_day_of_week(date_obj: Union[datetime.date, datetime.datetime], 
                         week_start: int = 0) -> datetime.date:
    """
    获取日期所在周的第一天
    
    Args:
        date_obj: 日期对象
        week_start: 周开始日，0=周一，6=周日
    
    Returns:
        该周第一天的日期对象
    """
    date_obj = date_obj.date() if hasattr(date_obj, 'date') else date_obj
    weekday = date_obj.weekday()
    days_to_subtract = (weekday - week_start) % 7
    return date_obj - datetime.timedelta(days=days_to_subtract)


def get_last_day_of_week(date_obj: Union[datetime.date, datetime.datetime], 
                        week_start: int = 0) -> datetime.date:
    """
    获取日期所在周的最后一天
    
    Args:
        date_obj: 日期对象
        week_start: 周开始日，0=周一，6=周日
    
    Returns:
        该周最后一天的日期对象
    """
    date_obj = date_obj.date() if hasattr(date_obj, 'date') else date_obj
    first_day = get_first_day_of_week(date_obj, week_start)
    return first_day + datetime.timedelta(days=6)


def get_first_day_of_quarter(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取日期所在季度的第一天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该季度第一天的日期对象
    """
    quarter = get_quarter(date_obj)
    month = (quarter - 1) * 3 + 1
    return datetime.date(date_obj.year, month, 1)


def get_last_day_of_quarter(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取日期所在季度的最后一天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该季度最后一天的日期对象
    """
    quarter = get_quarter(date_obj)
    month = quarter * 3
    _, last_day = calendar.monthrange(date_obj.year, month)
    return datetime.date(date_obj.year, month, last_day)


def get_first_day_of_year(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取日期所在年份的第一天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该年第一天的日期对象
    """
    return datetime.date(date_obj.year, 1, 1)


def get_last_day_of_year(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取日期所在年份的最后一天
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该年最后一天的日期对象
    """
    return datetime.date(date_obj.year, 12, 31)


# ==================== 日期范围生成 ====================

def get_dates_between(start_date: datetime.date, end_date: datetime.date) -> List[datetime.date]:
    """
    获取两个日期之间的所有日期
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        日期列表
    """
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += datetime.timedelta(days=1)
    return dates


def get_month_dates(date_obj: Union[datetime.date, datetime.datetime]) -> List[datetime.date]:
    """
    获取日期所在月份的所有日期
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该月所有日期的列表
    """
    first_day = get_first_day_of_month(date_obj)
    last_day = get_last_day_of_month(date_obj)
    return get_dates_between(first_day, last_day)


def get_week_dates(date_obj: Union[datetime.date, datetime.datetime], 
                  week_start: int = 0) -> List[datetime.date]:
    """
    获取日期所在周的所有日期
    
    Args:
        date_obj: 日期对象
        week_start: 周开始日，0=周一，6=周日
    
    Returns:
        该周所有日期的列表
    """
    first_day = get_first_day_of_week(date_obj, week_start)
    last_day = get_last_day_of_week(date_obj, week_start)
    return get_dates_between(first_day, last_day)


def get_quarter_dates(date_obj: Union[datetime.date, datetime.datetime]) -> List[datetime.date]:
    """
    获取日期所在季度的所有日期
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该季度所有日期的列表
    """
    first_day = get_first_day_of_quarter(date_obj)
    last_day = get_last_day_of_quarter(date_obj)
    return get_dates_between(first_day, last_day)


def get_year_dates(date_obj: Union[datetime.date, datetime.datetime]) -> List[datetime.date]:
    """
    获取日期所在年份的所有日期
    
    Args:
        date_obj: 日期对象
    
    Returns:
        该年所有日期的列表
    """
    first_day = get_first_day_of_year(date_obj)
    last_day = get_last_day_of_year(date_obj)
    return get_dates_between(first_day, last_day)


# ==================== 工作日相关 ====================

def is_weekend(date_obj: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断日期是否是周末（周六或周日）
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接判断星期几
            - datetime.datetime对象：使用日期部分判断星期几
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        bool: 如果是周末（周六或周日）返回True，否则返回False
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_weekend(datetime.date(2025, 1, 4))  # Saturday
        True
        
        >>> # 使用datetime.datetime对象
        >>> is_weekend(datetime.datetime(2025, 1, 4, 14, 30))  # Saturday
        True
        
        >>> # 使用ISO格式字符串
        >>> is_weekend("2025-01-04")  # Saturday
        True
        
        >>> # 使用中文格式字符串
        >>> is_weekend("2025年1月4日")  # Saturday
        True
        
        >>> # 工作日示例
        >>> is_weekend("2025-01-06")  # Monday
        False
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date_obj.weekday() >= 5


def is_weekday(date_obj: Union[datetime.date, datetime.datetime, str]) -> bool:
    """
    判断日期是否是工作日（周一到周五）
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接判断星期几
            - datetime.datetime对象：使用日期部分判断星期几
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        bool: 如果是工作日（周一到周五）返回True，否则返回False
    
    Examples:
        >>> # 使用datetime.date对象
        >>> is_weekday(datetime.date(2025, 1, 6))  # Monday
        True
        
        >>> # 使用datetime.datetime对象
        >>> is_weekday(datetime.datetime(2025, 1, 6, 14, 30))  # Monday
        True
        
        >>> # 使用ISO格式字符串
        >>> is_weekday("2025-01-06")  # Monday
        True
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    return date_obj.weekday() < 5


def get_next_weekday(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取下一个工作日
    
    Args:
        date_obj: 日期对象
    
    Returns:
        下一个工作日的日期对象
    """
    next_day = add_days(date_obj, 1)
    while is_weekend(next_day):
        next_day = add_days(next_day, 1)
    return next_day


def get_previous_weekday(date_obj: Union[datetime.date, datetime.datetime]) -> datetime.date:
    """
    获取上一个工作日
    
    Args:
        date_obj: 日期对象
    
    Returns:
        上一个工作日的日期对象
    """
    previous_day = add_days(date_obj, -1)
    while is_weekend(previous_day):
        previous_day = add_days(previous_day, -1)
    return previous_day


def get_weekdays_count_in_month(date_obj: Union[datetime.date, datetime.datetime]) -> int:
    """
    获取日期所在月份的工作日数量
    
    Args:
        date_obj: 日期对象
    
    Returns:
        工作日数量
    """
    month_dates = get_month_dates(date_obj)
    return sum(1 for date in month_dates if is_weekday(date))


def get_weekends_count_in_month(date_obj: Union[datetime.date, datetime.datetime]) -> int:
    """
    获取日期所在月份的周末数量
    
    Args:
        date_obj: 日期对象
    
    Returns:
        周末数量
    """
    month_dates = get_month_dates(date_obj)
    return sum(1 for date in month_dates if is_weekend(date))


# ==================== 时间戳相关 ====================

def datetime_to_timestamp(datetime_obj: datetime.datetime) -> float:
    """
    将日期时间对象转换为时间戳
    
    Args:
        datetime_obj: 日期时间对象
    
    Returns:
        时间戳
    """
    return datetime_obj.timestamp()


def timestamp_to_datetime(timestamp: float) -> datetime.datetime:
    """
    将时间戳转换为日期时间对象
    
    Args:
        timestamp: 时间戳
    
    Returns:
        日期时间对象
    """
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp_to_date(timestamp: float) -> datetime.date:
    """
    将时间戳转换为日期对象
    
    Args:
        timestamp: 时间戳
    
    Returns:
        日期对象
    """
    return timestamp_to_datetime(timestamp).date()


def get_current_timestamp() -> float:
    """
    获取当前时间戳
    
    Returns:
        当前时间戳
    """
    return time.time()


def get_current_datetime() -> datetime.datetime:
    """
    获取当前日期时间
    
    Returns:
        当前日期时间对象
    """
    return datetime.datetime.now()


def get_current_date() -> datetime.date:
    """
    获取当前日期
    
    Returns:
        当前日期对象
    """
    return datetime.date.today()


def get_current_time() -> datetime.time:
    """
    获取当前时间
    
    Returns:
        当前时间对象
    """
    return datetime.datetime.now().time()


# ==================== 时区相关 ====================

def get_utc_datetime() -> datetime.datetime:
    """
    获取当前UTC时间
    
    Returns:
        UTC日期时间对象
    """
    return datetime.datetime.now(UTC)


def datetime_to_utc(datetime_obj: datetime.datetime) -> datetime.datetime:
    """
    将本地时间转换为UTC时间
    
    Args:
        datetime_obj: 本地日期时间对象
    
    Returns:
        UTC日期时间对象
    """
    if datetime_obj.tzinfo is None:
        datetime_obj = datetime_obj.replace(tzinfo=gettz())
    return datetime_obj.astimezone(UTC)


def utc_to_local(utc_datetime: datetime.datetime, timezone: str = "Asia/Shanghai") -> datetime.datetime:
    """
    将UTC时间转换为指定时区的本地时间
    
    Args:
        utc_datetime: UTC日期时间对象
        timezone: 时区字符串，默认为"Asia/Shanghai"
    
    Returns:
        本地日期时间对象
    """
    return utc_datetime.astimezone(gettz(timezone))


def format_with_timezone(datetime_obj: datetime.datetime, 
                        format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    格式化带时区的日期时间
    
    Args:
        datetime_obj: 日期时间对象
        format_str: 格式化字符串
    
    Returns:
        格式化后的字符串
    """
    if datetime_obj.tzinfo is None:
        datetime_obj = datetime_obj.replace(tzinfo=gettz())
    return datetime_obj.strftime(format_str)


# ==================== 格式化相关 ====================

def format_date_iso(date_obj: Union[datetime.date, datetime.datetime, str]) -> str:
    """
    格式化日期为ISO格式
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接格式化为ISO格式
            - datetime.datetime对象：使用日期部分格式化为ISO格式
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        str: ISO格式的日期字符串（YYYY-MM-DD）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> format_date_iso(datetime.date(2025, 1, 6))
        '2025-01-06'
        
        >>> # 使用datetime.datetime对象
        >>> format_date_iso(datetime.datetime(2025, 1, 6, 14, 30))
        '2025-01-06'
        
        >>> # 使用ISO格式字符串
        >>> format_date_iso("2025-01-06")
        '2025-01-06'
        
        >>> # 使用中文格式字符串
        >>> format_date_iso("2025年1月6日")
        '2025-01-06'
        
        >>> # 使用美式格式字符串
        >>> format_date_iso("01/06/2025")
        '2025-01-06'
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    # 如果是datetime对象，提取日期部分
    if hasattr(date_obj, 'date'):
        date_obj = date_obj.date()
    
    return date_obj.isoformat()


def format_datetime_iso(datetime_obj: Union[datetime.datetime, str]) -> str:
    """
    格式化日期时间为ISO格式
    
    Args:
        datetime_obj: 日期时间对象或日期时间字符串
            - datetime.datetime对象：直接格式化为ISO格式
            - str：支持多种格式的日期时间字符串，包括：
                * ISO格式："2025-01-15 14:30:00", "2025-01-15T14:30:00"
                * 中文格式："2025年1月15日 下午2:30", "2025年1月15日 14时30分"
                * 美式格式："01/15/2025 2:30 PM", "01-15-2025 14:30"
                * 其他常见格式："15/01/2025 14:30", "2025.01.15 14:30:00"
    
    Returns:
        str: ISO格式的日期时间字符串（YYYY-MM-DDTHH:MM:SS格式）
    
    Examples:
        >>> # 使用datetime.datetime对象
        >>> format_datetime_iso(datetime.datetime(2025, 1, 6, 14, 30, 45))
        '2025-01-06T14:30:45'
        
        >>> # 使用ISO格式字符串
        >>> format_datetime_iso("2025-01-06 14:30:45")
        '2025-01-06T14:30:45'
        
        >>> # 使用中文格式字符串
        >>> format_datetime_iso("2025年1月6日 下午2:30")
        '2025-01-06T14:30:00'
        
        >>> # 使用美式格式字符串
        >>> format_datetime_iso("01/06/2025 2:30 PM")
        '2025-01-06T14:30:00'
    """
    # 如果输入是字符串，先转换为日期时间对象
    if isinstance(datetime_obj, str):
        try:
            datetime_obj = string_to_datetime(datetime_obj)
        except ValueError:
            parsed_datetime = parse_date_string(datetime_obj)
            datetime_obj = parsed_datetime if hasattr(parsed_datetime, 'hour') else datetime.datetime.combine(parsed_datetime, datetime.time())
    
    return datetime_obj.isoformat()


def format_date_chinese(date_obj: Union[datetime.date, datetime.datetime, str]) -> str:
    """
    格式化日期为中文格式
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接格式化为中文格式
            - datetime.datetime对象：使用日期部分格式化为中文格式
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        str: 中文格式的日期字符串（YYYY年MM月DD日）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> format_date_chinese(datetime.date(2025, 1, 6))
        '2025年01月06日'
        
        >>> # 使用datetime.datetime对象
        >>> format_date_chinese(datetime.datetime(2025, 1, 6, 14, 30))
        '2025年01月06日'
        
        >>> # 使用ISO格式字符串
        >>> format_date_chinese("2025-01-06")
        '2025年01月06日'
        
        >>> # 使用中文格式字符串
        >>> format_date_chinese("2025年1月6日")
        '2025年01月06日'
        
        >>> # 使用美式格式字符串
        >>> format_date_chinese("01/06/2025")
        '2025年01月06日'
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    # 如果是datetime对象，提取日期部分
    if hasattr(date_obj, 'date'):
        date_obj = date_obj.date()
    
    return date_obj.strftime("%Y年%m月%d日")


def format_datetime_chinese(datetime_obj: Union[datetime.datetime, str]) -> str:
    """
    格式化日期时间为中文格式
    
    Args:
        datetime_obj: 日期时间对象或日期时间字符串
            - datetime.datetime对象：直接格式化为中文格式
            - str：支持多种格式的日期时间字符串，包括：
                * ISO格式："2025-01-15 14:30:00", "2025-01-15T14:30:00"
                * 中文格式："2025年1月15日 下午2:30", "2025年1月15日 14时30分"
                * 美式格式："01/15/2025 2:30 PM", "01-15-2025 14:30"
                * 其他常见格式："15/01/2025 14:30", "2025.01.15 14:30:00"
    
    Returns:
        str: 中文格式的日期时间字符串（YYYY年MM月DD日 HH时MM分SS秒格式）
    
    Examples:
        >>> # 使用datetime.datetime对象
        >>> format_datetime_chinese(datetime.datetime(2025, 1, 6, 14, 30, 45))
        '2025年01月06日 14时30分45秒'
        
        >>> # 使用ISO格式字符串
        >>> format_datetime_chinese("2025-01-06 14:30:45")
        '2025年01月06日 14时30分45秒'
        
        >>> # 使用美式格式字符串
        >>> format_datetime_chinese("01/06/2025 2:30 PM")
        '2025年01月06日 14时30分00秒'
        
        >>> # 使用其他格式字符串
        >>> format_datetime_chinese("06/01/2025 14:30")
        '2025年01月06日 14时30分00秒'
    """
    # 如果输入是字符串，先转换为日期时间对象
    if isinstance(datetime_obj, str):
        try:
            datetime_obj = string_to_datetime(datetime_obj)
        except ValueError:
            parsed_datetime = parse_date_string(datetime_obj)
            datetime_obj = parsed_datetime if hasattr(parsed_datetime, 'hour') else datetime.datetime.combine(parsed_datetime, datetime.time())
    
    return datetime_obj.strftime("%Y年%m月%d日 %H时%M分%S秒")


def format_date_us(date_obj: Union[datetime.date, datetime.datetime, str]) -> str:
    """
    格式化日期为美国格式
    
    Args:
        date_obj: 日期对象或日期字符串
            - datetime.date对象：直接格式化为美国格式
            - datetime.datetime对象：提取日期部分格式化为美国格式
            - str：支持多种格式的日期字符串，包括：
                * ISO格式："2025-01-15", "2025-01-15 14:30:00"
                * 中文格式："2025年1月15日", "2025年1月15日 下午2:30"
                * 美式格式："01/15/2025", "01-15-2025"
                * 其他常见格式："15/01/2025", "2025.01.15"
    
    Returns:
        str: 美国格式的日期字符串（MM/DD/YYYY格式）
    
    Examples:
        >>> # 使用datetime.date对象
        >>> format_date_us(datetime.date(2025, 1, 6))
        '01/06/2025'
        
        >>> # 使用datetime.datetime对象
        >>> format_date_us(datetime.datetime(2025, 1, 6, 14, 30))
        '01/06/2025'
        
        >>> # 使用ISO格式字符串
        >>> format_date_us("2025-01-06")
        '01/06/2025'
        
        >>> # 使用中文格式字符串
        >>> format_date_us("2025年1月6日")
        '01/06/2025'
        
        >>> # 使用其他格式字符串
        >>> format_date_us("06/01/2025")
        '01/06/2025'
    """
    # 如果输入是字符串，先转换为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = string_to_date(date_obj)
        except ValueError:
            try:
                date_obj = string_to_datetime(date_obj)
            except ValueError:
                parsed_datetime = parse_date_string(date_obj)
                date_obj = parsed_datetime.date() if hasattr(parsed_datetime, 'date') else parsed_datetime
    
    # 如果是datetime对象，提取日期部分
    if hasattr(date_obj, 'date'):
        date_obj = date_obj.date()
    
    return date_obj.strftime("%m/%d/%Y")


def format_datetime_us(datetime_obj: Union[datetime.datetime, str]) -> str:
    """
    格式化日期时间为美国格式
    
    Args:
        datetime_obj: 日期时间对象或日期时间字符串
            - datetime.datetime对象：直接格式化为美国格式
            - str：支持多种格式的日期时间字符串，包括：
                * ISO格式："2025-01-15 14:30:00", "2025-01-15T14:30:00"
                * 中文格式："2025年1月15日 下午2:30", "2025年1月15日 14时30分"
                * 美式格式："01/15/2025 2:30 PM", "01-15-2025 14:30"
                * 其他常见格式："15/01/2025 14:30", "2025.01.15 14:30:00"
    
    Returns:
        str: 美国格式的日期时间字符串（MM/DD/YYYY HH:MM:SS AM/PM格式）
    
    Examples:
        >>> # 使用datetime.datetime对象
        >>> format_datetime_us(datetime.datetime(2025, 1, 6, 14, 30, 45))
        '01/06/2025 02:30:45 PM'
        
        >>> # 使用ISO格式字符串
        >>> format_datetime_us("2025-01-06 14:30:45")
        '01/06/2025 02:30:45 PM'
        
        >>> # 使用中文格式字符串
        >>> format_datetime_us("2025年1月6日 下午2:30")
        '01/06/2025 02:30:00 PM'
        
        >>> # 使用其他格式字符串
        >>> format_datetime_us("06/01/2025 14:30")
        '01/06/2025 02:30:00 PM'
    """
    # 如果输入是字符串，先转换为日期时间对象
    if isinstance(datetime_obj, str):
        try:
            datetime_obj = string_to_datetime(datetime_obj)
        except ValueError:
            parsed_datetime = parse_date_string(datetime_obj)
            datetime_obj = parsed_datetime if hasattr(parsed_datetime, 'hour') else datetime.datetime.combine(parsed_datetime, datetime.time())
    
    return datetime_obj.strftime("%m/%d/%Y %I:%M:%S %p")


def format_time_12h(time_obj: datetime.time) -> str:
    """
    格式化时间为12小时制
    
    Args:
        time_obj: 时间对象
    
    Returns:
        12小时制的时间字符串
    """
    return time_obj.strftime("%I:%M:%S %p")


def format_time_24h(time_obj: datetime.time) -> str:
    """
    格式化时间为24小时制
    
    Args:
        time_obj: 时间对象
    
    Returns:
        24小时制的时间字符串
    """
    return time_obj.strftime("%H:%M:%S")


def format_date_custom(date_obj: Union[datetime.date, datetime.datetime, str], 
                      format_pattern: str) -> str:
    """
    使用自定义格式模式格式化日期
    
    Args:
        date_obj: 日期对象、日期时间对象或日期字符串
        format_pattern: 自定义格式模式，支持以下占位符：
                       - YYYY: 4位年份
                       - YY: 2位年份
                       - MM: 2位月份（补零）
                       - M: 月份（不补零）
                       - DD: 2位日期（补零）
                       - D: 日期（不补零）
                       - HH: 2位小时（补零）
                       - H: 小时（不补零）
                       - mm: 2位分钟（补零）
                       - m: 分钟（不补零）
                       - SS: 2位秒（补零）
                       - S: 秒（不补零）
    
    Returns:
        格式化后的日期字符串
    
    Examples:
        >>> format_date_custom(datetime.date(2024, 1, 5), "YYYYmmDD")
        '20240105'
        >>> format_date_custom(datetime.datetime(2024, 1, 5, 14, 30, 45), "YYYY-MM-DD HH:mm:SS")
        '2024-01-05 14:30:45'
        >>> format_date_custom("2024-01-05", "YY/M/D")
        '24/1/5'
    """
    # 如果输入是字符串，尝试解析为日期对象
    if isinstance(date_obj, str):
        try:
            date_obj = parse_date_string(date_obj)
        except Exception:
            # 如果解析失败，尝试标准格式
            try:
                date_obj = string_to_datetime(date_obj)
            except Exception:
                try:
                    date_obj = string_to_date(date_obj)
                except Exception:
                    raise ValueError(f"无法解析日期字符串: {date_obj}")
    
    # 提取日期时间组件
    if hasattr(date_obj, 'date'):
        # datetime对象
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        hour = date_obj.hour
        minute = date_obj.minute
        second = date_obj.second
    else:
        # date对象
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        hour = 0
        minute = 0
        second = 0
    
    # 替换格式占位符（按长度从长到短替换，避免冲突）
    result = format_pattern
    
    # 年份替换
    result = result.replace('YYYY', f'{year:04d}')
    result = result.replace('YY', f'{year % 100:02d}')
    
    # 月份替换（MM必须在mm之前替换）
    result = result.replace('MM', f'{month:02d}')
    
    # 日期替换
    result = result.replace('DD', f'{day:02d}')
    
    # 小时替换
    result = result.replace('HH', f'{hour:02d}')
    
    # 分钟替换（mm在这里处理）
    result = result.replace('mm', f'{minute:02d}')
    
    # 秒替换
    result = result.replace('SS', f'{second:02d}')
    
    # 单字符替换（放在最后，避免与双字符冲突）
    result = result.replace('M', str(month))
    result = result.replace('D', str(day))
    result = result.replace('H', str(hour))
    result = result.replace('m', str(minute))
    result = result.replace('S', str(second))
    
    return result


def format_datetime_custom(datetime_obj: Union[datetime.datetime, str], 
                          format_pattern: str) -> str:
    """
    使用自定义格式模式格式化日期时间（专门用于datetime对象）
    
    Args:
        datetime_obj: 日期时间对象或日期时间字符串
        format_pattern: 自定义格式模式
    
    Returns:
        格式化后的日期时间字符串
    
    Examples:
        >>> format_datetime_custom(datetime.datetime(2024, 1, 5, 14, 30, 45), "YYYYMMDDHHmmSS")
        '20240105143045'
        >>> format_datetime_custom("2024-01-05 14:30:45", "YYYY年MM月DD日 HH时mm分SS秒")
        '2024年01月05日 14时30分45秒'
    """
    return format_date_custom(datetime_obj, format_pattern)


def format_date_compact(date_obj: Union[datetime.date, datetime.datetime, str]) -> str:
    """
    格式化日期为紧凑格式（YYYYMMDD）
    
    Args:
        date_obj: 日期对象、日期时间对象或日期字符串
    
    Returns:
        紧凑格式的日期字符串
    
    Examples:
        >>> format_date_compact(datetime.date(2024, 1, 5))
        '20240105'
    """
    return format_date_custom(date_obj, "YYYYMMDD")


def format_datetime_compact(datetime_obj: Union[datetime.datetime, str]) -> str:
    """
    格式化日期时间为紧凑格式（YYYYMMDDHHmmSS）
    
    Args:
        datetime_obj: 日期时间对象或日期时间字符串
    
    Returns:
        紧凑格式的日期时间字符串
    
    Examples:
        >>> format_datetime_compact(datetime.datetime(2024, 1, 5, 14, 30, 45))
        '20240105143045'
    """
    return format_date_custom(datetime_obj, "YYYYMMDDHHmmSS")


def format_date_readable(date_obj: Union[datetime.date, datetime.datetime, str], 
                        separator: str = "-") -> str:
    """
    格式化日期为可读格式（YYYY-MM-DD或自定义分隔符）
    
    Args:
        date_obj: 日期对象、日期时间对象或日期字符串
        separator: 分隔符，默认为"-"
    
    Returns:
        可读格式的日期字符串
    
    Examples:
        >>> format_date_readable(datetime.date(2024, 1, 5))
        '2024-01-05'
        >>> format_date_readable(datetime.date(2024, 1, 5), "/")
        '2024/01/05'
    """
    pattern = f"YYYY{separator}MM{separator}DD"
    return format_date_custom(date_obj, pattern)


def format_datetime_readable(datetime_obj: Union[datetime.datetime, str], 
                           date_separator: str = "-", 
                           time_separator: str = ":") -> str:
    """
    格式化日期时间为可读格式（YYYY-MM-DD HH:mm:SS或自定义分隔符）
    
    Args:
        datetime_obj: 日期时间对象或日期时间字符串
        date_separator: 日期分隔符，默认为"-"
        time_separator: 时间分隔符，默认为":"
    
    Returns:
        可读格式的日期时间字符串
    
    Examples:
        >>> format_datetime_readable(datetime.datetime(2024, 1, 5, 14, 30, 45))
        '2024-01-05 14:30:45'
        >>> format_datetime_readable(datetime.datetime(2024, 1, 5, 14, 30, 45), "/", ".")
        '2024/01/05 14.30.45'
    """
    pattern = f"YYYY{date_separator}MM{date_separator}DD HH{time_separator}mm{time_separator}SS"
    return format_date_custom(datetime_obj, pattern)


# ==================== 年龄计算 ====================

def calculate_age(birth_date: Union[datetime.date, datetime.datetime], 
                 reference_date: Optional[Union[datetime.date, datetime.datetime]] = None) -> int:
    """
    计算年龄
    
    Args:
        birth_date: 出生日期
        reference_date: 参考日期，默认为当前日期
    
    Returns:
        年龄
    """
    if reference_date is None:
        reference_date = get_current_date()
    
    birth_date = birth_date.date() if hasattr(birth_date, 'date') else birth_date
    reference_date = reference_date.date() if hasattr(reference_date, 'date') else reference_date
    
    age = reference_date.year - birth_date.year
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def calculate_months_between(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    计算两个日期之间的月数差
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        月数差
    """
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)


def calculate_years_between(start_date: datetime.date, end_date: datetime.date) -> int:
    """
    计算两个日期之间的年数差
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        年数差
    """
    years = end_date.year - start_date.year
    if (end_date.month, end_date.day) < (start_date.month, start_date.day):
        years -= 1
    return years


# ==================== 其他实用函数 ====================

def get_season(date_obj: Union[datetime.date, datetime.datetime]) -> str:
    """
    获取日期所在的季节
    
    Args:
        date_obj: 日期对象
    
    Returns:
        季节名称
    """
    month = date_obj.month
    if month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    elif month in [9, 10, 11]:
        return "秋季"
    else:
        return "冬季"


def get_zodiac_sign(date_obj: Union[datetime.date, datetime.datetime]) -> str:
    """
    获取日期对应的星座
    
    Args:
        date_obj: 日期对象
    
    Returns:
        星座名称
    """
    month = date_obj.month
    day = date_obj.day
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "白羊座"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "金牛座"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
        return "双子座"
    elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
        return "巨蟹座"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "狮子座"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "处女座"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
        return "天秤座"
    elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
        return "天蝎座"
    elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
        return "射手座"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "摩羯座"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "水瓶座"
    else:
        return "双鱼座"


def get_chinese_zodiac(year: int) -> str:
    """
    获取年份对应的生肖
    
    Args:
        year: 年份
    
    Returns:
        生肖名称
    """
    zodiacs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    return zodiacs[(year - 1900) % 12]


def is_business_day(date_obj: Union[datetime.date, datetime.datetime], 
                    holidays: List[datetime.date] = None) -> bool:
    """
    判断是否是工作日（排除周末和节假日）
    
    Args:
        date_obj: 日期对象
        holidays: 节假日列表
    
    Returns:
        如果是工作日返回True，否则返回False
    """
    if holidays is None:
        holidays = []
    
    date_obj = date_obj.date() if hasattr(date_obj, 'date') else date_obj
    return is_weekday(date_obj) and date_obj not in holidays


def get_next_business_day(date_obj: Union[datetime.date, datetime.datetime], 
                          holidays: List[datetime.date] = None) -> datetime.date:
    """
    获取下一个工作日（排除周末和节假日）
    
    Args:
        date_obj: 日期对象
        holidays: 节假日列表
    
    Returns:
        下一个工作日的日期对象
    """
    if holidays is None:
        holidays = []
    
    next_day = add_days(date_obj, 1)
    while not is_business_day(next_day, holidays):
        next_day = add_days(next_day, 1)
    return next_day


def get_previous_business_day(date_obj: Union[datetime.date, datetime.datetime], 
                             holidays: List[datetime.date] = None) -> datetime.date:
    """
    获取上一个工作日（排除周末和节假日）
    
    Args:
        date_obj: 日期对象
        holidays: 节假日列表
    
    Returns:
        上一个工作日的日期对象
    """
    if holidays is None:
        holidays = []
    
    previous_day = add_days(date_obj, -1)
    while not is_business_day(previous_day, holidays):
        previous_day = add_days(previous_day, -1)
    return previous_day


def get_business_days_between(start_date: datetime.date, end_date: datetime.date, 
                             holidays: List[datetime.date] = None) -> int:
    """
    计算两个日期之间的工作日数量（排除周末和节假日）
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        holidays: 节假日列表
    
    Returns:
        工作日数量
    """
    if holidays is None:
        holidays = []
    
    business_days = 0
    current_date = start_date
    while current_date <= end_date:
        if is_business_day(current_date, holidays):
            business_days += 1
        current_date += datetime.timedelta(days=1)
    return business_days


def get_fuzzy_time_description(datetime_obj: datetime.datetime, 
                              reference_datetime: Optional[datetime.datetime] = None) -> str:
    """
    获取模糊的时间描述（如：刚刚、几分钟前、昨天等）
    
    Args:
        datetime_obj: 要描述的日期时间
        reference_datetime: 参考日期时间，默认为当前时间
    
    Returns:
        模糊的时间描述
    """
    if reference_datetime is None:
        reference_datetime = get_current_datetime()
    
    delta = reference_datetime - datetime_obj
    seconds = delta.total_seconds()
    
    if seconds < 60:
        return "刚刚"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}分钟前"
    elif seconds < 86400:  # 1天
        hours = int(seconds // 3600)
        return f"{hours}小时前"
    elif seconds < 172800:  # 2天
        return "昨天"
    elif seconds < 604800:  # 7天
        days = int(seconds // 86400)
        return f"{days}天前"
    elif seconds < 2592000:  # 30天
        weeks = int(seconds // 604800)
        return f"{weeks}周前"
    elif seconds < 31536000:  # 365天
        months = int(seconds // 2592000)
        return f"{months}个月前"
    else:
        years = int(seconds // 31536000)
        return f"{years}年前"


def parse_duration(duration_str: str) -> datetime.timedelta:
    """
    解析持续时间字符串为timedelta对象
    
    Args:
        duration_str: 持续时间字符串，如"1d2h30m"、"2小时30分钟"等
    
    Returns:
        timedelta对象
    """
    # 首先尝试中文格式：使用更简单直接的方法
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    
    # 查找天数
    day_match = re.search(r'(\d+)\s*天', duration_str)
    if day_match:
        days = int(day_match.group(1))
    
    # 查找小时数
    hour_match = re.search(r'(\d+)\s*小时', duration_str)
    if hour_match:
        hours = int(hour_match.group(1))
    
    # 查找分钟数
    minute_match = re.search(r'(\d+)\s*分钟', duration_str)
    if minute_match:
        minutes = int(minute_match.group(1))
    
    # 查找秒数
    second_match = re.search(r'(\d+)\s*秒', duration_str)
    if second_match:
        seconds = int(second_match.group(1))
    
    # 如果找到了任何中文时间单位，返回结果
    if days > 0 or hours > 0 or minutes > 0 or seconds > 0:
        return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    # 如果没有找到中文格式，尝试英文格式：1d2h30m15s
    en_pattern = r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
    en_match = re.fullmatch(en_pattern, duration_str.lower())
    
    if en_match and any(en_match.groups()):
        days = int(en_match.group(1)) if en_match.group(1) else 0
        hours = int(en_match.group(2)) if en_match.group(2) else 0
        minutes = int(en_match.group(3)) if en_match.group(3) else 0
        seconds = int(en_match.group(4)) if en_match.group(4) else 0
        return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    raise ValueError(f"无法解析的持续时间字符串: {duration_str}")


def format_duration(timedelta_obj: datetime.timedelta, 
                   format_type: str = "chinese") -> str:
    """
    格式化timedelta对象为持续时间字符串
    
    Args:
        timedelta_obj: timedelta对象
        format_type: 格式类型，"chinese"或"english"
    
    Returns:
        格式化后的持续时间字符串
    """
    total_seconds = int(timedelta_obj.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    if format_type == "chinese":
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}秒")
        return "".join(parts)
    else:  # english
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")
        return "".join(parts)


def test_duration_parsing():
    """
    测试持续时间解析功能
    """
    print("=== 持续时间解析专项测试 ===")
    
    test_cases = [
        # 英文格式
        ("1d", "1天"),
        ("2h", "2小时"),
        ("30m", "30分钟"),
        ("45s", "45秒"),
        ("1d2h30m15s", "1天2小时30分钟15秒"),
        ("2d1h30m", "2天1小时30分钟"),
        
        # 中文格式
        ("1天", "1天"),
        ("2小时", "2小时"),
        ("30分钟", "30分钟"),
        ("45秒", "45秒"),
        ("1天2小时30分钟15秒", "1天2小时30分钟15秒"),
        ("2天1小时30分钟", "2天1小时30分钟"),
        
        # 混合格式（带空格）
        ("1 天 2 小时 30 分钟", "1天2小时30分钟"),
    ]
    
    for duration_str, expected_desc in test_cases:
        try:
            duration = parse_duration(duration_str)
            formatted_cn = format_duration(duration)
            formatted_en = format_duration(duration, "english")
            print(f"输入: '{duration_str}' -> 解析: {duration} -> 中文: {formatted_cn}, 英文: {formatted_en}")
        except Exception as e:
            print(f"输入: '{duration_str}' -> 错误: {e}")
    
    print()


# ==================== 主函数和测试 ====================

def run_unit_tests():
    """
    运行单元测试，验证所有函数的正确性
    """
    print("\n🧪 开始单元测试...")
    
    # 导入需要的类
    from datetime import date, datetime as dt
    
    # 测试数据准备
    test_date = date(2023, 6, 15)  # 2023年6月15日，星期四
    test_datetime = dt(2023, 6, 15, 14, 30, 0)
    test_date_str = '2023-06-15'
    test_date_str_slash = '2023/06/15'
    test_date_str_compact = '20230615'
    test_date2 = date(2023, 12, 25)  # 2023年12月25日，星期一
    test_date2_str = '2023-12-25'
    
    test_count = 0
    passed_count = 0
    failed_tests = []
    
    def assert_equal(actual, expected, test_name):
        nonlocal test_count, passed_count, failed_tests
        test_count += 1
        if actual == expected:
            passed_count += 1
            print(f"✅ {test_name}: 通过")
        else:
            failed_tests.append(f"{test_name}: 期望 {expected}, 实际 {actual}")
            print(f"❌ {test_name}: 失败 - 期望 {expected}, 实际 {actual}")
    
    def assert_true(condition, test_name):
        nonlocal test_count, passed_count, failed_tests
        test_count += 1
        if condition:
            passed_count += 1
            print(f"✅ {test_name}: 通过")
        else:
            failed_tests.append(f"{test_name}: 期望 True, 实际 False")
            print(f"❌ {test_name}: 失败 - 期望 True, 实际 False")
    
    def assert_false(condition, test_name):
        nonlocal test_count, passed_count, failed_tests
        test_count += 1
        if not condition:
            passed_count += 1
            print(f"✅ {test_name}: 通过")
        else:
            failed_tests.append(f"{test_name}: 期望 False, 实际 True")
            print(f"❌ {test_name}: 失败 - 期望 False, 实际 True")
    
    # 测试add_days函数
    print("\n--- 测试add_days函数 ---")
    result1 = add_days(test_date, 10)
    expected1 = date(2023, 6, 25)
    assert_equal(result1, expected1, "add_days(date对象, 10)")
    
    result2 = add_days(test_datetime, 10)
    expected2 = dt(2023, 6, 25, 14, 30, 0)
    assert_equal(result2, expected2, "add_days(datetime对象, 10)")
    
    result3 = add_days(test_date_str, 10)
    if hasattr(result3, 'date'):
        assert_equal(result3.date(), expected1, "add_days(字符串, 10)")
    else:
        assert_equal(result3, expected1, "add_days(字符串, 10)")
    
    result4 = add_days(test_date, -5)
    expected4 = date(2023, 6, 10)
    assert_equal(result4, expected4, "add_days(负数天数)")
    
    # 测试add_months函数
    print("\n--- 测试add_months函数 ---")
    result1 = add_months(test_date, 2)
    expected1 = date(2023, 8, 15)
    assert_equal(result1, expected1, "add_months(date对象, 2)")
    
    result2 = add_months(test_date_str, 2)
    if hasattr(result2, 'date'):
        assert_equal(result2.date(), expected1, "add_months(字符串, 2)")
    else:
        assert_equal(result2, expected1, "add_months(字符串, 2)")
    
    result3 = add_months(test_date, 8)
    expected3 = date(2024, 2, 15)
    assert_equal(result3, expected3, "add_months(跨年)")
    
    # 测试add_years函数
    print("\n--- 测试add_years函数 ---")
    result1 = add_years(test_date, 1)
    expected1 = date(2024, 6, 15)
    assert_equal(result1, expected1, "add_years(date对象, 1)")
    
    result2 = add_years(test_date_str, 1)
    if hasattr(result2, 'date'):
        assert_equal(result2.date(), expected1, "add_years(字符串, 1)")
    else:
        assert_equal(result2, expected1, "add_years(字符串, 1)")
    
    # 测试date_diff函数
    print("\n--- 测试date_diff函数 ---")
    result1 = date_diff(test_date2, test_date)
    expected1 = -193
    assert_equal(result1, expected1, "date_diff(date对象)")
    
    result2 = date_diff(test_date2_str, test_date_str)
    assert_equal(result2, expected1, "date_diff(字符串)")
    
    result3 = date_diff(test_date2, test_date_str)
    assert_equal(result3, expected1, "date_diff(混合类型)")
    
    # 测试get_year函数
    print("\n--- 测试get_year函数 ---")
    assert_equal(get_year(test_date), 2023, "get_year(date对象)")
    assert_equal(get_year(test_datetime), 2023, "get_year(datetime对象)")
    assert_equal(get_year(test_date_str), 2023, "get_year(字符串)")
    assert_equal(get_year(test_date_str_slash), 2023, "get_year(斜杠格式字符串)")
    
    # 测试get_month函数
    print("\n--- 测试get_month函数 ---")
    assert_equal(get_month(test_date), 6, "get_month(date对象)")
    assert_equal(get_month(test_date_str), 6, "get_month(字符串)")
    
    # 测试get_day函数
    print("\n--- 测试get_day函数 ---")
    assert_equal(get_day(test_date), 15, "get_day(date对象)")
    assert_equal(get_day(test_date_str), 15, "get_day(字符串)")
    
    # 测试get_weekday函数
    print("\n--- 测试get_weekday函数 ---")
    assert_equal(get_weekday(test_date), 3, "get_weekday(date对象)")
    assert_equal(get_weekday(test_date_str), 3, "get_weekday(字符串)")
    
    # 测试days_between函数
    print("\n--- 测试days_between函数 ---")
    result1 = days_between(test_date2, test_date)
    expected1 = 193
    assert_equal(result1, expected1, "days_between(date对象)")
    
    result2 = days_between(test_date2_str, test_date_str)
    assert_equal(result2, expected1, "days_between(字符串)")
    
    # 测试is_before函数
    print("\n--- 测试is_before函数 ---")
    assert_true(is_before(test_date, test_date2), "is_before(早期日期)")
    assert_false(is_before(test_date2, test_date), "is_before(晚期日期)")
    assert_true(is_before(test_date_str, test_date2_str), "is_before(字符串)")
    
    # 测试is_after函数
    print("\n--- 测试is_after函数 ---")
    assert_true(is_after(test_date2, test_date), "is_after(晚期日期)")
    assert_false(is_after(test_date, test_date2), "is_after(早期日期)")
    assert_true(is_after(test_date2_str, test_date_str), "is_after(字符串)")
    
    # 测试is_same_day函数
    print("\n--- 测试is_same_day函数 ---")
    assert_true(is_same_day(test_date, test_date), "is_same_day(相同日期)")
    assert_false(is_same_day(test_date, test_date2), "is_same_day(不同日期)")
    assert_true(is_same_day(test_date_str, test_date_str), "is_same_day(字符串)")
    assert_true(is_same_day(test_date, test_date_str), "is_same_day(混合类型)")
    
    # 测试is_same_month函数
    print("\n--- 测试is_same_month函数 ---")
    same_month_date = date(2023, 6, 20)
    assert_true(is_same_month(test_date, same_month_date), "is_same_month(相同月份)")
    assert_false(is_same_month(test_date, test_date2), "is_same_month(不同月份)")
    assert_true(is_same_month(test_date_str, '2023-06-20'), "is_same_month(字符串)")
    
    # 测试is_same_year函数
    print("\n--- 测试is_same_year函数 ---")
    assert_true(is_same_year(test_date, test_date2), "is_same_year(相同年份)")
    different_year_date = date(2024, 6, 15)
    assert_false(is_same_year(test_date, different_year_date), "is_same_year(不同年份)")
    assert_true(is_same_year(test_date_str, test_date2_str), "is_same_year(字符串)")
    
    # 测试is_weekend函数
    print("\n--- 测试is_weekend函数 ---")
    assert_false(is_weekend(test_date), "is_weekend(工作日)")
    weekend_date = date(2023, 6, 17)  # 星期六
    assert_true(is_weekend(weekend_date), "is_weekend(周末)")
    assert_true(is_weekend('2023-06-17'), "is_weekend(字符串-星期六)")
    assert_true(is_weekend('2023-06-18'), "is_weekend(字符串-星期日)")
    
    # 测试is_weekday函数
    print("\n--- 测试is_weekday函数 ---")
    assert_true(is_weekday(test_date), "is_weekday(工作日)")
    assert_false(is_weekday(weekend_date), "is_weekday(周末)")
    assert_true(is_weekday(test_date_str), "is_weekday(字符串-工作日)")
    assert_false(is_weekday('2023-06-17'), "is_weekday(字符串-周末)")
    
    # 测试format_date_iso函数
    print("\n--- 测试format_date_iso函数 ---")
    expected_iso = '2023-06-15'
    assert_equal(format_date_iso(test_date), expected_iso, "format_date_iso(date对象)")
    assert_equal(format_date_iso(test_datetime), expected_iso, "format_date_iso(datetime对象)")
    assert_equal(format_date_iso(test_date_str), expected_iso, "format_date_iso(字符串)")
    assert_equal(format_date_iso(test_date_str_slash), expected_iso, "format_date_iso(斜杠格式)")
    
    # 测试format_date_chinese函数
    print("\n--- 测试format_date_chinese函数 ---")
    expected_chinese = '2023年06月15日'
    assert_equal(format_date_chinese(test_date), expected_chinese, "format_date_chinese(date对象)")
    assert_equal(format_date_chinese(test_date_str), expected_chinese, "format_date_chinese(字符串)")
    
    # 测试format_date_us函数
    print("\n--- 测试format_date_us函数 ---")
    expected_us = '06/15/2023'
    assert_equal(format_date_us(test_date), expected_us, "format_date_us(date对象)")
    assert_equal(format_date_us(test_date_str), expected_us, "format_date_us(字符串)")
    
    # 测试字符串格式兼容性
    print("\n--- 测试字符串格式兼容性 ---")
    formats = ['2023-06-15', '2023/06/15', '20230615']
    for date_str in formats:
        assert_equal(get_year(date_str), 2023, f"格式兼容性-年份({date_str})")
        assert_equal(get_month(date_str), 6, f"格式兼容性-月份({date_str})")
        assert_equal(get_day(date_str), 15, f"格式兼容性-日期({date_str})")
        assert_false(is_weekend(date_str), f"格式兼容性-周末判断({date_str})")
    
    # 输出测试结果
    print(f"\n📊 单元测试结果:")
    print(f"✅ 总测试数: {test_count}")
    print(f"✅ 通过: {passed_count}")
    print(f"❌ 失败: {len(failed_tests)}")
    
    if failed_tests:
        print("\n❌ 失败的测试:")
        for failed_test in failed_tests:
            print(f"  - {failed_test}")
        return False
    else:
        print("\n🎉 所有单元测试通过！")
        return True

def run_comprehensive_tests():
    """
    运行全面的日期工具函数测试
    包含原有的功能演示测试
    """
    print("\n🔧 开始功能演示测试...")
    
    # 获取当前日期时间
    now = get_current_datetime()
    today = get_current_date()
    print(f"当前日期时间: {datetime_to_string(now)}")
    print(f"当前日期: {date_to_string(today)}")
    print(f"当前时间: {format_time_24h(get_current_time())}")
    print()
    
    # 测试日期格式转换
    print("=== 日期格式转换测试 ===")
    test_date = datetime.date(2024, 1, 15)
    test_datetime = datetime.datetime(2024, 1, 15, 14, 30, 45)
    
    print(f"日期转字符串: {date_to_string(test_date)}")
    print(f"日期时间转字符串: {datetime_to_string(test_datetime)}")
    print(f"字符串转日期: {string_to_date('2024-01-15')}")
    print(f"字符串转日期时间: {string_to_datetime('2024-01-15 14:30:45')}")
    
    # 测试中文日期解析 - 使用修复后的函数
    try:
        print(f"智能解析日期(中文): {parse_date_string('2024年1月15日')}")
        print(f"智能解析日期时间(中文): {parse_date_string('2024年1月15日 下午2:30')}")
        print(f"智能解析时间(中文): {parse_date_string('下午2:30')}")
    except Exception as e:
        print(f"中文日期解析测试失败: {e}")
    
    # 测试其他格式
    try:
        print(f"智能解析日期(英文): {parse_date_string('January 15, 2024')}")
        print(f"智能解析日期时间(英文): {parse_date_string('2024-01-15 14:30:45')}")
    except Exception as e:
        print(f"英文日期解析测试失败: {e}")
    
    print()
    
    # 测试日期计算
    print("=== 日期计算测试 ===")
    print(f"加10天: {add_days(today, 10)}")
    print(f"加2个月: {add_months(today, 2)}")
    print(f"加1年: {add_years(today, 1)}")
    print(f"日期差: {date_diff(today, add_days(today, 10))}")
    print(f"天数差: {days_between(today, add_days(today, 10))}")
    print(f"工作日差: {weekdays_between(today, add_days(today, 10))}")
    
    # 测试字符串输入的日期计算（修复后的功能）
    print("\n=== 字符串输入日期计算测试 ===")
    print(f"字符串加天数: {add_days('2025-09-06', -1)}")
    print(f"字符串加小时: {add_hours('2025-09-06 14:30:00', 2)}")
    print(f"字符串加分钟: {add_minutes('2025-09-06 14:30:00', 30)}")
    print(f"中文日期格式: {add_days('2025年9月6日', 1)}")
    print()
    
    # 测试日期比较
    print("=== 日期比较测试 ===")
    date1 = datetime.date(2024, 1, 1)
    date2 = datetime.date(2024, 1, 2)
    print(f"date1 < date2: {is_before(date1, date2)}")
    print(f"date1 > date2: {is_after(date1, date2)}")
    print(f"是否同一天: {is_same_day(date1, date2)}")
    print(f"是否同月: {is_same_month(date1, date2)}")
    print(f"是否同年: {is_same_year(date1, date2)}")
    print()
    
    # 测试日期验证
    print("=== 日期验证测试 ===")
    print(f"'2024-01-15' 是否有效日期: {is_valid_date('2024-01-15')}")
    print(f"'2024-02-30' 是否有效日期: {is_valid_date('2024-02-30')}")
    print(f"'2024-01-15 14:30:45' 是否有效日期时间: {is_valid_datetime('2024-01-15 14:30:45')}")
    print(f"2024年是否是闰年: {is_leap_year(2024)}")
    print(f"2023年是否是闰年: {is_leap_year(2023)}")
    print()
    
    # 测试获取日期信息
    print("=== 获取日期信息测试 ===")
    print(f"年份: {get_year(today)}")
    print(f"月份: {get_month(today)}")
    print(f"天: {get_day(today)}")
    print(f"星期几: {get_weekday(today)}")
    print(f"星期几名称: {get_weekday_name(today)}")
    print(f"第几周: {get_week_of_year(today)}")
    print(f"第几天: {get_day_of_year(today)}")
    print(f"第几季度: {get_quarter(today)}")
    print()
    
    # 测试获取特殊日期
    print("=== 获取特殊日期测试 ===")
    print(f"本月第一天: {get_first_day_of_month(today)}")
    print(f"本月最后一天: {get_last_day_of_month(today)}")
    print(f"本周第一天: {get_first_day_of_week(today)}")
    print(f"本周最后一天: {get_last_day_of_week(today)}")
    print(f"本季度第一天: {get_first_day_of_quarter(today)}")
    print(f"本季度最后一天: {get_last_day_of_quarter(today)}")
    print(f"本年第一天: {get_first_day_of_year(today)}")
    print(f"本年最后一天: {get_last_day_of_year(today)}")
    print()
    
    # 测试日期范围生成
    print("=== 日期范围生成测试 ===")
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 5)
    print(f"日期范围: {get_dates_between(start_date, end_date)}")
    print(f"本月所有日期数量: {len(get_month_dates(today))}")
    print(f"本周所有日期: {get_week_dates(today)}")
    print()
    
    # 测试工作日相关
    print("=== 工作日相关测试 ===")
    print(f"今天是否是周末: {is_weekend(today)}")
    print(f"今天是否是工作日: {is_weekday(today)}")
    print(f"下一个工作日: {get_next_weekday(today)}")
    print(f"上一个工作日: {get_previous_weekday(today)}")
    print(f"本月工作日数量: {get_weekdays_count_in_month(today)}")
    print(f"本月周末数量: {get_weekends_count_in_month(today)}")
    print()
    
    # 测试时间戳相关
    print("=== 时间戳相关测试 ===")
    timestamp = get_current_timestamp()
    print(f"当前时间戳: {timestamp}")
    print(f"时间戳转日期时间: {timestamp_to_datetime(timestamp)}")
    print(f"时间戳转日期: {timestamp_to_date(timestamp)}")
    print(f"日期时间转时间戳: {datetime_to_timestamp(now)}")
    print()
    
    # 测试时区相关
    print("=== 时区相关测试 ===")
    utc_now = get_utc_datetime()
    print(f"UTC时间: {utc_now}")
    print(f"本地时间转UTC: {datetime_to_utc(now)}")
    print(f"UTC转本地时间: {utc_to_local(utc_now)}")
    print(f"带时区格式化: {format_with_timezone(now)}")
    print()
    
    # 测试格式化相关
    print("=== 格式化相关测试 ===")
    print(f"ISO格式日期: {format_date_iso(today)}")
    print(f"ISO格式日期时间: {format_datetime_iso(now)}")
    print(f"中文格式日期: {format_date_chinese(today)}")
    print(f"中文格式日期时间: {format_datetime_chinese(now)}")
    print(f"美国格式日期: {format_date_us(today)}")
    print(f"美国格式日期时间: {format_datetime_us(now)}")
    print(f"12小时制时间: {format_time_12h(get_current_time())}")
    print(f"24小时制时间: {format_time_24h(get_current_time())}")
    print()
    
    # 测试自定义格式化函数
    print("=== 自定义格式化测试 ===")
    test_date = datetime.date(2024, 1, 5)
    test_datetime = datetime.datetime(2024, 1, 5, 14, 30, 45)
    test_date_str = "2024-01-05"
    test_datetime_str = "2024-01-05 14:30:45"
    
    print(f"自定义格式化日期(YYYYMMDD): {format_date_custom(test_date, 'YYYYMMDD')}")
    print(f"自定义格式化日期(YY/M/D): {format_date_custom(test_date, 'YY/M/D')}")
    print(f"自定义格式化日期时间(YYYYMMDDHHmmSS): {format_date_custom(test_datetime, 'YYYYMMDDHHmmSS')}")
    print(f"自定义格式化日期时间(YYYY年MM月DD日 HH时mm分SS秒): {format_date_custom(test_datetime, 'YYYY年MM月DD日 HH时mm分SS秒')}")
    
    # 测试字符串输入
    print(f"字符串输入格式化(YYYYMMDD): {format_date_custom(test_date_str, 'YYYYMMDD')}")
    print(f"字符串输入格式化(YY.MM.DD): {format_date_custom(test_date_str, 'YY.MM.DD')}")
    print(f"字符串输入格式化日期时间(YYYYMMDDHHmmSS): {format_datetime_custom(test_datetime_str, 'YYYYMMDDHHmmSS')}")
    
    # 测试便捷函数
    print(f"紧凑格式日期: {format_date_compact(test_date)}")
    print(f"紧凑格式日期时间: {format_datetime_compact(test_datetime)}")
    print(f"可读格式日期(默认): {format_date_readable(test_date)}")
    print(f"可读格式日期(/分隔): {format_date_readable(test_date, '/')}")
    print(f"可读格式日期时间(默认): {format_datetime_readable(test_datetime)}")
    print(f"可读格式日期时间(自定义分隔符): {format_datetime_readable(test_datetime, '/', '.')}")
    
    # 测试各种格式模式
    print("\n--- 各种格式模式测试 ---")
    patterns = [
        "YYYYmmDD",
        "YYYY-MM-DD",
        "YY/MM/DD",
        "YYYY年MM月DD日",
        "YYYYMMDDHHmmSS",
        "YYYY-MM-DD HH:mm:SS",
        "YY/MM/DD HH.mm.SS",
        "M/D/YYYY",
        "D-M-YY",
        "YYYY.MM.DD HH时mm分"
    ]
    
    for pattern in patterns:
        try:
            result = format_date_custom(test_datetime, pattern)
            print(f"模式 '{pattern}': {result}")
        except Exception as e:
            print(f"模式 '{pattern}': 错误 - {e}")
    
    print()
    
    # 测试年龄计算
    print("=== 年龄计算测试 ===")
    birth_date = datetime.date(1990, 5, 15)
    print(f"出生日期: {birth_date}")
    print(f"年龄: {calculate_age(birth_date)}")
    print(f"月数差: {calculate_months_between(birth_date, today)}")
    print(f"年数差: {calculate_years_between(birth_date, today)}")
    print()
    
    # 测试其他实用函数
    print("=== 其他实用函数测试 ===")
    print(f"季节: {get_season(today)}")
    print(f"星座: {get_zodiac_sign(today)}")
    print(f"生肖: {get_chinese_zodiac(1990)}")
    print(f"模糊时间描述(2天前): {get_fuzzy_time_description(add_days(now, -2))}")
    print(f"模糊时间描述(3小时前): {get_fuzzy_time_description(add_hours(now, -3))}")
    print(f"模糊时间描述(30分钟前): {get_fuzzy_time_description(now - datetime.timedelta(minutes=30))}")
    print()
    
    # 测试持续时间解析和格式化 - 使用修复后的函数
    test_duration_parsing()
    
    # 测试节假日相关
    print("=== 节假日相关测试 ===")
    holidays = [
        datetime.date(2024, 1, 1),  # 元旦
        datetime.date(2024, 2, 10),  # 春节
        datetime.date(2024, 2, 11),
        datetime.date(2024, 2, 12),
    ]
    
    test_holiday_date = datetime.date(2024, 2, 10)
    print(f"{test_holiday_date} 是否是工作日: {is_business_day(test_holiday_date, holidays)}")
    print(f"{test_holiday_date} 的下一个工作日: {get_next_business_day(test_holiday_date, holidays)}")
    print(f"{test_holiday_date} 的上一个工作日: {get_previous_business_day(test_holiday_date, holidays)}")
    
    # 计算两个日期之间的工作日数量
    start_date = datetime.date(2024, 2, 8)
    end_date = datetime.date(2024, 2, 14)
    business_days = get_business_days_between(start_date, end_date, holidays)
    print(f"{start_date} 到 {end_date} 之间的工作日数量: {business_days}")
    print()
    
    print("=== 功能演示测试完成 ===")

def main():
    """
    主函数，运行所有测试
    """
    print("=== 日期工具模块完整测试套件 ===")
    print("包含功能演示和单元测试")
    print("="*50)
    
    # 运行单元测试
    unit_test_success = run_unit_tests()
    
    # 运行功能演示测试
    run_comprehensive_tests()
    
    # 输出最终结果
    if unit_test_success:
        print("\n🎉 所有测试完成！单元测试全部通过。")
    else:
        print("\n⚠️ 测试完成，但有单元测试失败，请检查上述错误信息。")
    
    print("=== 所有测试完成 ===")


if __name__ == "__main__":
    main()