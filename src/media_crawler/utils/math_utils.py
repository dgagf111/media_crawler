"""
数值类型转换与运算工具模块（扩展版）
提供安全的类型转换、运算、比较、保留小数位、常用计算等功能
"""

from decimal import (
    Decimal,
    getcontext,
    ROUND_DOWN,
    ROUND_UP,
    ROUND_FLOOR,
    ROUND_CEILING,
    ROUND_HALF_UP,
)
from typing import Union, Any, Optional, List
import numbers
import math

# 设置Decimal的精度
getcontext().prec = 28


def to_decimal(value: Any, precision: Optional[int] = None) -> Decimal:
    """
    安全地将各种类型转换为Decimal

    Args:
        value: 要转换的值 (int, float, str, Decimal等)
        precision: 可选，设置Decimal精度

    Returns:
        Decimal: 转换后的Decimal对象
    """
    if precision is not None:
        original_prec = getcontext().prec
        getcontext().prec = precision

    try:
        if value is None:
            return Decimal("0")
        elif isinstance(value, Decimal):
            return value
        elif isinstance(value, (int, numbers.Integral)):
            return Decimal(str(value))
        elif isinstance(value, (float, numbers.Real)):
            # 避免直接传递float给Decimal，先转换为字符串
            return Decimal(str(value))
        elif isinstance(value, str):
            # 处理字符串中的空格和特殊字符
            value = value.strip()
            if not value:
                return Decimal("0")
            return Decimal(value)
        elif isinstance(value, bool):
            return Decimal("1") if value else Decimal("0")
        else:
            # 尝试转换为字符串再处理
            return Decimal(str(value))
    except (ValueError, TypeError, ArithmeticError) as e:
        raise ValueError(f"无法将值 {value} 转换为Decimal: {e}")
    finally:
        if precision is not None:
            getcontext().prec = original_prec


def to_float(value: Any) -> float:
    """
    安全地将各种类型转换为float

    Args:
        value: 要转换的值

    Returns:
        float: 转换后的float值
    """
    try:
        if value is None:
            return 0.0
        elif isinstance(value, float):
            return value
        elif isinstance(value, (int, numbers.Integral)):
            return float(value)
        elif isinstance(value, Decimal):
            return float(value)
        elif isinstance(value, str):
            value = value.strip()
            if not value:
                return 0.0
            return float(value)
        elif isinstance(value, bool):
            return 1.0 if value else 0.0
        else:
            return float(str(value))
    except (ValueError, TypeError) as e:
        raise ValueError(f"无法将值 {value} 转换为float: {e}")


def to_int(value: Any) -> int:
    """
    安全地将各种类型转换为int

    Args:
        value: 要转换的值

    Returns:
        int: 转换后的int值
    """
    try:
        if value is None:
            return 0
        elif isinstance(value, int):
            return value
        elif isinstance(value, (float, Decimal)):
            return int(value)
        elif isinstance(value, str):
            value = value.strip()
            if not value:
                return 0
            return int(float(value))
        elif isinstance(value, bool):
            return 1 if value else 0
        else:
            return int(str(value))
    except (ValueError, TypeError) as e:
        raise ValueError(f"无法将值 {value} 转换为int: {e}")


def to_str(value: Any, decimal_places: Optional[int] = None) -> str:
    """
    安全地将各种类型转换为字符串

    Args:
        value: 要转换的值
        decimal_places: 可选，小数位数

    Returns:
        str: 转换后的字符串
    """
    try:
        if value is None:
            return "0"
        elif isinstance(value, str):
            return value.strip()
        elif isinstance(value, (int, float)):
            if decimal_places is not None:
                return f"{value:.{decimal_places}f}"
            return str(value)
        elif isinstance(value, Decimal):
            if decimal_places is not None:
                return f"{float(value):.{decimal_places}f}"
            return str(value)
        elif isinstance(value, bool):
            return "1" if value else "0"
        else:
            return str(value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"无法将值 {value} 转换为字符串: {e}")


# ==================== 保留小数位和舍位进位方法 ====================


def round_number(
    value: Any, decimal_places: int = 2, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    四舍五入保留指定小数位数

    Args:
        value: 要处理的值
        decimal_places: 保留的小数位数
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        处理后的值

    Examples:
        >>> round_number('123.456', 2)
        Decimal('123.46')
        >>> round_number('123.454', 2)
        Decimal('123.45')
    """
    try:
        dec_value = to_decimal(value)

        if decimal_places < 0:
            # 负的小数位数表示对整数部分进行舍入
            multiplier = Decimal("10") ** abs(decimal_places)
            rounded = (dec_value / multiplier).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            ) * multiplier
        else:
            # 正的小数位数
            quant_str = "0." + "0" * decimal_places if decimal_places > 0 else "0"
            rounded = dec_value.quantize(Decimal(quant_str), rounding=ROUND_HALF_UP)

        if return_type == "decimal":
            return rounded
        elif return_type == "float":
            return to_float(rounded)
        elif return_type == "int":
            return to_int(rounded)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"四舍五入失败: {e}")


def floor_number(
    value: Any, decimal_places: int = 0, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    向下取整（地板函数）

    Args:
        value: 要处理的值
        decimal_places: 保留的小数位数
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        处理后的值

    Examples:
        >>> floor_number('123.456', 2)
        Decimal('123.45')
        >>> floor_number('123.999', 0)
        Decimal('123')
    """
    try:
        dec_value = to_decimal(value)

        if decimal_places == 0:
            # 对整数部分向下取整
            floored = dec_value.to_integral_value(rounding=ROUND_FLOOR)
        else:
            # 对指定小数位数向下取整
            multiplier = Decimal("10") ** decimal_places
            floored = (dec_value * multiplier).to_integral_value(
                rounding=ROUND_FLOOR
            ) / multiplier

        if return_type == "decimal":
            return floored
        elif return_type == "float":
            return to_float(floored)
        elif return_type == "int":
            return to_int(floored)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"向下取整失败: {e}")


def ceil_number(
    value: Any, decimal_places: int = 0, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    向上取整（天花板函数）

    Args:
        value: 要处理的值
        decimal_places: 保留的小数位数
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        处理后的值

    Examples:
        >>> ceil_number('123.451', 2)
        Decimal('123.46')
        >>> ceil_number('123.001', 0)
        Decimal('124')
    """
    try:
        dec_value = to_decimal(value)

        if decimal_places == 0:
            # 对整数部分向上取整
            ceiled = dec_value.to_integral_value(rounding=ROUND_CEILING)
        else:
            # 对指定小数位数向上取整
            multiplier = Decimal("10") ** decimal_places
            ceiled = (dec_value * multiplier).to_integral_value(
                rounding=ROUND_CEILING
            ) / multiplier

        if return_type == "decimal":
            return ceiled
        elif return_type == "float":
            return to_float(ceiled)
        elif return_type == "int":
            return to_int(ceiled)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"向上取整失败: {e}")


def truncate_number(
    value: Any, decimal_places: int = 0, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    直接截断（不进行四舍五入）

    Args:
        value: 要处理的值
        decimal_places: 保留的小数位数
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        处理后的值

    Examples:
        >>> truncate_number('123.456', 2)
        Decimal('123.45')
        >>> truncate_number('123.999', 0)
        Decimal('123')
    """
    try:
        dec_value = to_decimal(value)

        if decimal_places == 0:
            # 截断小数部分
            truncated = dec_value.to_integral_value(rounding=ROUND_DOWN)
        else:
            # 截断到指定小数位数
            multiplier = Decimal("10") ** decimal_places
            truncated = (dec_value * multiplier).to_integral_value(
                rounding=ROUND_DOWN
            ) / multiplier

        if return_type == "decimal":
            return truncated
        elif return_type == "float":
            return to_float(truncated)
        elif return_type == "int":
            return to_int(truncated)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"截断失败: {e}")


# ==================== 常用数字转换方法 ====================


def to_percentage(
    value: Any, decimal_places: int = 2, multiply_by_100: bool = True
) -> str:
    """
    转换为百分比字符串

    Args:
        value: 要转换的值
        decimal_places: 保留的小数位数
        multiply_by_100: 是否乘以100

    Returns:
        str: 百分比字符串

    Examples:
        >>> to_percentage('0.1234')
        '12.34%'
        >>> to_percentage('12.34', multiply_by_100=False)
        '12.34%'
    """
    try:
        dec_value = to_decimal(value)

        if multiply_by_100:
            dec_value = dec_value * Decimal("100")

        # 格式化为字符串
        if decimal_places == 0:
            formatted = f"{int(dec_value)}%"
        else:
            formatted = f"{float(dec_value):.{decimal_places}f}%"

        return formatted
    except Exception as e:
        raise ValueError(f"百分比转换失败: {e}")


def from_percentage(
    percentage_str: str, return_type: str = "decimal"
) -> Union[Decimal, float]:
    """
    从百分比字符串转换为数值

    Args:
        percentage_str: 百分比字符串（如 "12.34%"）
        return_type: 返回类型 ('decimal', 'float')

    Returns:
        转换后的数值

    Examples:
        >>> from_percentage('12.34%')
        Decimal('0.1234')
    """
    try:
        # 移除百分号并转换为数值
        clean_str = percentage_str.strip().replace("%", "")
        dec_value = to_decimal(clean_str) / Decimal("100")

        if return_type == "decimal":
            return dec_value
        elif return_type == "float":
            return to_float(dec_value)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"从百分比转换失败: {e}")


def to_fraction(value: Any, max_denominator: int = 1000) -> tuple:
    """
    转换为分数（分子, 分母）

    Args:
        value: 要转换的值
        max_denominator: 最大分母

    Returns:
        tuple: (分子, 分母)

    Examples:
        >>> to_fraction('0.75')
        (3, 4)
    """
    try:
        dec_value = to_decimal(value)
        float_value = float(dec_value)

        # 使用Fraction来获取最简分数
        from fractions import Fraction

        fraction = Fraction(float_value).limit_denominator(max_denominator)

        return (fraction.numerator, fraction.denominator)
    except Exception as e:
        raise ValueError(f"分数转换失败: {e}")


def to_scientific_notation(value: Any, decimal_places: int = 2) -> str:
    """
    转换为科学计数法字符串

    Args:
        value: 要转换的值
        decimal_places: 保留的小数位数

    Returns:
        str: 科学计数法字符串

    Examples:
        >>> to_scientific_notation('1234.56')
        '1.23e+03'
    """
    try:
        dec_value = to_decimal(value)
        float_value = float(dec_value)

        # 格式化为科学计数法
        if decimal_places == 0:
            formatted = f"{float_value:.0e}"
        else:
            formatted = f"{float_value:.{decimal_places}e}"

        # 标准化格式
        formatted = formatted.replace("e+0", "e+").replace("e-0", "e-")
        if "e+" in formatted and formatted.split("e+")[1].startswith("0"):
            formatted = formatted.replace("e+0", "e+")

        return formatted
    except Exception as e:
        raise ValueError(f"科学计数法转换失败: {e}")


# ==================== 常用计算方法 ====================


def calculate_average(
    values: List[Any], return_type: str = "decimal"
) -> Union[Decimal, float]:
    """
    计算平均值

    Args:
        values: 数值列表
        return_type: 返回类型 ('decimal', 'float')

    Returns:
        平均值

    Examples:
        >>> calculate_average(['1', '2.5', '3.5'])
        Decimal('2.333333333333333333333333333')
    """
    try:
        if not values:
            raise ValueError("数值列表不能为空")

        decimal_values = [to_decimal(v) for v in values]
        total = sum(decimal_values, Decimal("0"))
        average = total / Decimal(str(len(values)))

        if return_type == "decimal":
            return average
        elif return_type == "float":
            return to_float(average)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"计算平均值失败: {e}")


def calculate_sum(
    values: List[Any], return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    计算总和

    Args:
        values: 数值列表
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        总和

    Examples:
        >>> calculate_sum(['1', '2.5', '3.5'])
        Decimal('7.0')
    """
    try:
        if not values:
            raise ValueError("数值列表不能为空")

        decimal_values = [to_decimal(v) for v in values]
        total = sum(decimal_values, Decimal("0"))

        if return_type == "decimal":
            return total
        elif return_type == "float":
            return to_float(total)
        elif return_type == "int":
            return to_int(total)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"计算总和失败: {e}")


def calculate_max(
    values: List[Any], return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    计算最大值

    Args:
        values: 数值列表
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        最大值
    """
    try:
        if not values:
            raise ValueError("数值列表不能为空")

        decimal_values = [to_decimal(v) for v in values]
        max_value = max(decimal_values)

        if return_type == "decimal":
            return max_value
        elif return_type == "float":
            return to_float(max_value)
        elif return_type == "int":
            return to_int(max_value)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"计算最大值失败: {e}")


def calculate_min(
    values: List[Any], return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    计算最小值

    Args:
        values: 数值列表
        return_type: 返回类型 ('decimal', 'float', 'int')

    Returns:
        最小值
    """
    try:
        if not values:
            raise ValueError("数值列表不能为空")

        decimal_values = [to_decimal(v) for v in values]
        min_value = min(decimal_values)

        if return_type == "decimal":
            return min_value
        elif return_type == "float":
            return to_float(min_value)
        elif return_type == "int":
            return to_int(min_value)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"计算最小值失败: {e}")


def calculate_std_dev(
    values: List[Any], return_type: str = "decimal"
) -> Union[Decimal, float]:
    """
    计算标准差

    Args:
        values: 数值列表
        return_type: 返回类型 ('decimal', 'float')

    Returns:
        标准差
    """
    try:
        if len(values) < 2:
            raise ValueError("计算标准差至少需要2个数值")

        decimal_values = [to_decimal(v) for v in values]
        average = calculate_average(decimal_values, return_type="decimal")

        # 计算方差
        variance = sum((x - average) ** 2 for x in decimal_values) / Decimal(
            str(len(values) - 1)
        )
        std_dev = variance ** Decimal("0.5")

        if return_type == "decimal":
            return std_dev
        elif return_type == "float":
            return to_float(std_dev)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"计算标准差失败: {e}")


def calculate_percent_change(
    old_value: Any, new_value: Any, return_type: str = "decimal"
) -> Union[Decimal, float]:
    """
    计算百分比变化

    Args:
        old_value: 原始值
        new_value: 新值
        return_type: 返回类型 ('decimal', 'float')

    Returns:
        百分比变化

    Examples:
        >>> calculate_percent_change('100', '120')
        Decimal('0.2')
    """
    try:
        dec_old = to_decimal(old_value)
        dec_new = to_decimal(new_value)

        if dec_old == Decimal("0"):
            raise ValueError("原始值不能为零")

        change = (dec_new - dec_old) / dec_old

        if return_type == "decimal":
            return change
        elif return_type == "float":
            return to_float(change)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"计算百分比变化失败: {e}")


def calculate_gcd(a: Any, b: Any) -> int:
    """
    计算最大公约数（GCD）

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        最大公约数

    Examples:
        >>> calculate_gcd('12', '18')
        6
    """
    try:
        int_a = to_int(a)
        int_b = to_int(b)

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        return gcd(abs(int_a), abs(int_b))
    except Exception as e:
        raise ValueError(f"计算最大公约数失败: {e}")


def calculate_lcm(a: Any, b: Any) -> int:
    """
    计算最小公倍数（LCM）

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        最小公倍数

    Examples:
        >>> calculate_lcm('12', '18')
        36
    """
    try:
        int_a = to_int(a)
        int_b = to_int(b)

        gcd = calculate_gcd(int_a, int_b)
        lcm = abs(int_a * int_b) // gcd

        return lcm
    except Exception as e:
        raise ValueError(f"计算最小公倍数失败: {e}")


# ==================== 基础运算方法 ====================


def safe_add(
    a: Any, b: Any, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    安全加法运算
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)
        result = dec_a + dec_b

        if return_type == "decimal":
            return result
        elif return_type == "float":
            return to_float(result)
        elif return_type == "int":
            return to_int(result)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"加法运算失败: {e}")


def safe_subtract(
    a: Any, b: Any, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    安全减法运算
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)
        result = dec_a - dec_b

        if return_type == "decimal":
            return result
        elif return_type == "float":
            return to_float(result)
        elif return_type == "int":
            return to_int(result)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"减法运算失败: {e}")


def safe_multiply(
    a: Any, b: Any, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    安全乘法运算
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)
        result = dec_a * dec_b

        if return_type == "decimal":
            return result
        elif return_type == "float":
            return to_float(result)
        elif return_type == "int":
            return to_int(result)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"乘法运算失败: {e}")


def safe_divide(
    a: Any, b: Any, return_type: str = "decimal"
) -> Union[Decimal, float, int]:
    """
    安全除法运算
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)

        if dec_b == Decimal("0"):
            raise ZeroDivisionError("除数不能为零")

        result = dec_a / dec_b

        if return_type == "decimal":
            return result
        elif return_type == "float":
            return to_float(result)
        elif return_type == "int":
            return to_int(result)
        else:
            raise ValueError(f"不支持的返回类型: {return_type}")
    except Exception as e:
        raise ValueError(f"除法运算失败: {e}")


# ==================== 比较方法 ====================


def safe_equal(a: Any, b: Any, tolerance: Optional[Any] = None) -> bool:
    """
    安全相等比较
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)

        if tolerance is not None:
            dec_tolerance = to_decimal(tolerance)
            return abs(dec_a - dec_b) <= dec_tolerance
        else:
            return dec_a == dec_b
    except Exception as e:
        raise ValueError(f"相等比较失败: {e}")


def safe_greater_than(a: Any, b: Any) -> bool:
    """
    安全大于比较
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)
        return dec_a > dec_b
    except Exception as e:
        raise ValueError(f"大于比较失败: {e}")


def safe_less_than(a: Any, b: Any) -> bool:
    """
    安全小于比较
    """
    try:
        dec_a = to_decimal(a)
        dec_b = to_decimal(b)
        return dec_a < dec_b
    except Exception as e:
        raise ValueError(f"小于比较失败: {e}")


# ==================== 辅助方法 ====================


def is_numeric(value: Any) -> bool:
    """
    判断值是否为数值类型
    """
    try:
        to_decimal(value)
        return True
    except (ValueError, TypeError):
        return False


def get_type_info(value: Any) -> dict:
    """
    获取值的类型信息
    """
    return {
        "type": type(value).__name__,
        "is_numeric": is_numeric(value),
        "value": value,
        "decimal_representation": str(to_decimal(value)) if is_numeric(value) else None,
        "float_representation": str(to_float(value)) if is_numeric(value) else None,
    }


# ==================== 演示和测试 ====================


def demo_extended_usage():
    """
    演示扩展工具模块的使用方法
    """
    print("=== 扩展数值工具模块演示 ===\n")

    # 1. 保留小数位和舍位进位方法
    print("1. 保留小数位和舍位进位方法:")
    test_value = "123.456"
    print(f"原始值: {test_value}")
    print(f"四舍五入(2位): {round_number(test_value, 2)}")
    print(f"向下取整(2位): {floor_number(test_value, 2)}")
    print(f"向上取整(2位): {ceil_number(test_value, 2)}")
    print(f"直接截断(2位): {truncate_number(test_value, 2)}")
    print()

    # 2. 常用数字转换方法
    print("2. 常用数字转换方法:")
    print(f"转换为百分比: {to_percentage('0.1234')}")
    print(f"从百分比转换: {from_percentage('12.34%')}")
    print(f"转换为分数: {to_fraction('0.75')}")
    print(f"转换为科学计数法: {to_scientific_notation('1234.56')}")
    print()

    # 3. 常用计算方法
    print("3. 常用计算方法:")
    test_values = ["1", "2.5", "3.5", "4.2", "5.8"]
    print(f"测试数据: {test_values}")
    print(f"平均值: {calculate_average(test_values)}")
    print(f"总和: {calculate_sum(test_values)}")
    print(f"最大值: {calculate_max(test_values)}")
    print(f"最小值: {calculate_min(test_values)}")
    print(f"标准差: {calculate_std_dev(test_values)}")
    print(f"百分比变化(100->120): {calculate_percent_change('100', '120')}")
    print(f"最大公约数(12,18): {calculate_gcd('12', '18')}")
    print(f"最小公倍数(12,18): {calculate_lcm('12', '18')}")
    print()


if __name__ == "__main__":
    demo_extended_usage()
