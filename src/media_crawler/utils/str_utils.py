import re
import random
import string
import hashlib
import base64
import html
import urllib.parse
from typing import List, Union, Optional, Any, Callable
from datetime import datetime
import unicodedata

# =============================================================================
# 字符串拼接操作
# =============================================================================


def join_strings(*args, separator: str = "_") -> str:
    """
    拼接多个字符串

    Args:
        *args: 要拼接的参数
        separator: 拼接分隔符，默认为下划线

    Returns:
        拼接后的字符串
    """
    return separator.join(str(arg) for arg in args)


def concatenate_strings(*args) -> str:
    """
    连接多个字符串（无分隔符）

    Args:
        *args: 要连接的参数

    Returns:
        连接后的字符串
    """
    return "".join(str(arg) for arg in args)


def repeat_string(text: str, times: int, separator: str = "") -> str:
    """
    重复字符串

    Args:
        text: 要重复的字符串
        times: 重复次数
        separator: 重复之间的分隔符

    Returns:
        重复后的字符串
    """
    return separator.join([text] * times)


# =============================================================================
# 字符串分割操作
# =============================================================================


def split_string(text: str, separator: str = None, max_split: int = -1) -> List[str]:
    """
    分割字符串

    Args:
        text: 要分割的字符串
        separator: 分隔符，None表示按空白字符分割
        max_split: 最大分割次数，-1表示无限制

    Returns:
        分割后的字符串列表
    """
    return text.split(separator, max_split) if separator else text.split()


def split_lines(text: str, keepends: bool = False) -> List[str]:
    """
    按行分割字符串

    Args:
        text: 要分割的字符串
        keepends: 是否保留行尾换行符

    Returns:
        分割后的行列表
    """
    return text.splitlines(keepends)


def split_by_length(text: str, length: int) -> List[str]:
    """
    按长度分割字符串

    Args:
        text: 要分割的字符串
        length: 每段的长度

    Returns:
        分割后的字符串列表
    """
    return [text[i : i + length] for i in range(0, len(text), length)]


def partition_string(text: str, separator: str) -> tuple:
    """
    分割字符串为三部分（分隔符前、分隔符、分隔符后）

    Args:
        text: 要分割的字符串
        separator: 分隔符

    Returns:
        (head, separator, tail) 三元组
    """
    return text.partition(separator)


def rpartition_string(text: str, separator: str) -> tuple:
    """
    从右边分割字符串为三部分

    Args:
        text: 要分割的字符串
        separator: 分隔符

    Returns:
        (head, separator, tail) 三元组
    """
    return text.rpartition(separator)


# =============================================================================
# 字符串查找操作
# =============================================================================


def find_string(text: str, substring: str, start: int = 0, end: int = -1) -> int:
    """
    查找子字符串位置

    Args:
        text: 要搜索的字符串
        substring: 要查找的子字符串
        start: 开始位置
        end: 结束位置

    Returns:
        找到的位置，未找到返回-1
    """
    return text.find(substring, start, end)


def rfind_string(text: str, substring: str, start: int = 0, end: int = -1) -> int:
    """
    从右边查找子字符串位置

    Args:
        text: 要搜索的字符串
        substring: 要查找的子字符串
        start: 开始位置
        end: 结束位置

    Returns:
        找到的位置，未找到返回-1
    """
    return text.rfind(substring, start, end)


def index_string(text: str, substring: str, start: int = 0, end: int = -1) -> int:
    """
    查找子字符串位置（找不到会抛出异常）

    Args:
        text: 要搜索的字符串
        substring: 要查找的子字符串
        start: 开始位置
        end: 结束位置

    Returns:
        找到的位置
    """
    return text.index(substring, start, end)


def count_substring(text: str, substring: str, start: int = 0, end: int = -1) -> int:
    """
    统计子字符串出现次数

    Args:
        text: 要搜索的字符串
        substring: 要统计的子字符串
        start: 开始位置
        end: 结束位置

    Returns:
        出现次数
    """
    return text.count(substring, start, end)


def find_all_occurrences(text: str, substring: str) -> List[int]:
    """
    查找所有出现位置

    Args:
        text: 要搜索的字符串
        substring: 要查找的子字符串

    Returns:
        所有出现位置的列表
    """
    positions = []
    start = 0
    while True:
        pos = text.find(substring, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions


# =============================================================================
# 字符串替换操作
# =============================================================================


def replace_string(text: str, old: str, new: str, count: int = -1) -> str:
    """
    替换字符串中的子字符串

    Args:
        text: 原字符串
        old: 要替换的旧字符串
        new: 替换的新字符串
        count: 替换次数，-1表示全部替换

    Returns:
        替换后的字符串
    """
    return text.replace(old, new, count)


def replace_multiple(text: str, replacements: dict) -> str:
    """
    批量替换字符串

    Args:
        text: 原字符串
        replacements: 替换字典 {old: new}

    Returns:
        替换后的字符串
    """
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def remove_chars(text: str, chars: str) -> str:
    """
    移除指定字符

    Args:
        text: 原字符串
        chars: 要移除的字符集合

    Returns:
        处理后的字符串
    """
    return text.translate(str.maketrans("", "", chars))


def remove_duplicates(text: str) -> str:
    """
    移除重复字符（保持顺序）

    Args:
        text: 原字符串

    Returns:
        去重后的字符串
    """
    seen = set()
    return "".join(seen.add(c) or c for c in text if c not in seen)


# =============================================================================
# 字符串格式化操作
# =============================================================================


def format_string(template: str, *args, **kwargs) -> str:
    """
    格式化字符串

    Args:
        template: 格式化模板
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        格式化后的字符串
    """
    return template.format(*args, **kwargs)


def pad_string(text: str, width: int, fill_char: str = " ", align: str = "left") -> str:
    """
    填充字符串到指定宽度

    Args:
        text: 原字符串
        width: 目标宽度
        fill_char: 填充字符
        align: 对齐方式 ('left', 'right', 'center')

    Returns:
        填充后的字符串
    """
    if align == "left":
        return text.ljust(width, fill_char)
    elif align == "right":
        return text.rjust(width, fill_char)
    elif align == "center":
        return text.center(width, fill_char)
    else:
        raise ValueError("align参数必须是 'left', 'right' 或 'center'")


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    截断字符串到指定长度

    Args:
        text: 原字符串
        max_length: 最大长度
        suffix: 后缀

    Returns:
        截断后的字符串
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def wrap_text(text: str, width: int = 70, **kwargs) -> List[str]:
    """
    文本自动换行

    Args:
        text: 要换行的文本
        width: 每行宽度
        **kwargs: textwrap.wrap的额外参数

    Returns:
        换行后的文本列表
    """
    import textwrap

    return textwrap.wrap(text, width, **kwargs)


# =============================================================================
# 字符串大小写操作
# =============================================================================


def to_uppercase(text: str) -> str:
    """转换为大写"""
    return text.upper()


def to_lowercase(text: str) -> str:
    """转换为小写"""
    return text.lower()


def to_title_case(text: str) -> str:
    """转换为标题格式（每个单词首字母大写）"""
    return text.title()


def to_sentence_case(text: str) -> str:
    """转换为句子格式（首字母大写）"""
    return text.capitalize()


def swap_case(text: str) -> str:
    """大小写互换"""
    return text.swapcase()


def to_camel_case(text: str, separator: str = "_") -> str:
    """
    转换为驼峰命名

    Args:
        text: 原字符串
        separator: 分隔符

    Returns:
        驼峰命名字符串
    """
    parts = text.split(separator)
    return parts[0].lower() + "".join(word.capitalize() for word in parts[1:])


def to_snake_case(text: str) -> str:
    """
    转换为蛇形命名

    Args:
        text: 原字符串

    Returns:
        蛇形命名字符串
    """
    # 处理驼峰命名
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


# =============================================================================
# 字符串空白处理
# =============================================================================


def strip_string(text: str, chars: str = None) -> str:
    """
    去除首尾空白字符

    Args:
        text: 原字符串
        chars: 要去除的字符集合

    Returns:
        处理后的字符串
    """
    return text.strip(chars)


def lstrip_string(text: str, chars: str = None) -> str:
    """
    去除左边空白字符

    Args:
        text: 原字符串
        chars: 要去除的字符集合

    Returns:
        处理后的字符串
    """
    return text.lstrip(chars)


def rstrip_string(text: str, chars: str = None) -> str:
    """
    去除右边空白字符

    Args:
        text: 原字符串
        chars: 要去除的字符集合

    Returns:
        处理后的字符串
    """
    return text.rstrip(chars)


def remove_extra_spaces(text: str) -> str:
    """
    移除多余的空白字符（多个空格合并为一个）

    Args:
        text: 原字符串

    Returns:
        处理后的字符串
    """
    return " ".join(text.split())


def normalize_whitespace(text: str) -> str:
    """
    标准化空白字符（统一为单个空格）

    Args:
        text: 原字符串

    Returns:
        处理后的字符串
    """
    import re

    return re.sub(r"\s+", " ", text).strip()


# =============================================================================
# 字符串验证操作
# =============================================================================


def is_empty(text: str) -> bool:
    """检查字符串是否为空"""
    return not text.strip()


def is_numeric(text: str) -> bool:
    """检查字符串是否为数字"""
    try:
        float(text)
        return True
    except ValueError:
        return False


def is_integer(text: str) -> bool:
    """检查字符串是否为整数"""
    try:
        int(text)
        return True
    except ValueError:
        return False


def is_alphabetic(text: str) -> bool:
    """检查字符串是否只包含字母"""
    return text.isalpha()


def is_alphanumeric(text: str) -> bool:
    """检查字符串是否只包含字母和数字"""
    return text.isalnum()


def is_email(text: str) -> bool:
    """检查字符串是否为邮箱格式"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, text))


def is_url(text: str) -> bool:
    """检查字符串是否为URL格式"""
    try:
        result = urllib.parse.urlparse(text)
        return all([result.scheme, result.netloc])
    except:
        return False


def is_phone(text: str) -> bool:
    """检查字符串是否为手机号格式"""
    pattern = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, text))


def is_chinese(text: str) -> bool:
    """检查字符串是否只包含中文字符"""
    return all("\u4e00" <= char <= "\u9fff" for char in text)


def contains_chinese(text: str) -> bool:
    """检查字符串是否包含中文字符"""
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def is_valid_json(text: str) -> bool:
    """检查字符串是否为有效JSON"""
    try:
        import json

        json.loads(text)
        return True
    except:
        return False


# =============================================================================
# 字符串编码解码操作
# =============================================================================


def encode_base64(text: str, encoding: str = "utf-8") -> str:
    """
    Base64编码

    Args:
        text: 要编码的字符串
        encoding: 字符串编码

    Returns:
        Base64编码后的字符串
    """
    return base64.b64encode(text.encode(encoding)).decode("ascii")


def decode_base64(text: str, encoding: str = "utf-8") -> str:
    """
    Base64解码

    Args:
        text: 要解码的Base64字符串
        encoding: 目标编码

    Returns:
        解码后的字符串
    """
    return base64.b64decode(text.encode("ascii")).decode(encoding)


def encode_url(text: str) -> str:
    """URL编码"""
    return urllib.parse.quote_plus(text)


def decode_url(text: str) -> str:
    """URL解码"""
    return urllib.parse.unquote_plus(text)


def encode_html(text: str) -> str:
    """HTML编码"""
    return html.escape(text)


def decode_html(text: str) -> str:
    """HTML解码"""
    return html.unescape(text)


def encode_unicode(text: str, encoding: str = "utf-8") -> bytes:
    """
    Unicode编码

    Args:
        text: 要编码的字符串
        encoding: 目标编码

    Returns:
        编码后的字节串
    """
    return text.encode(encoding)


def decode_unicode(data: bytes, encoding: str = "utf-8") -> str:
    """
    Unicode解码

    Args:
        data: 要解码的字节串
        encoding: 编码格式

    Returns:
        解码后的字符串
    """
    return data.decode(encoding)


# =============================================================================
# 正则表达式相关操作
# =============================================================================


def regex_match(pattern: str, text: str, flags: int = 0) -> bool:
    """
    正则表达式匹配

    Args:
        pattern: 正则表达式模式
        text: 要匹配的文本
        flags: 正则表达式标志

    Returns:
        是否匹配
    """
    return bool(re.match(pattern, text, flags))


def regex_search(pattern: str, text: str, flags: int = 0) -> Optional[str]:
    """
    正则表达式搜索

    Args:
        pattern: 正则表达式模式
        text: 要搜索的文本
        flags: 正则表达式标志

    Returns:
        找到的第一个匹配，未找到返回None
    """
    match = re.search(pattern, text, flags)
    return match.group() if match else None


def regex_findall(pattern: str, text: str, flags: int = 0) -> List[str]:
    """
    正则表达式查找所有匹配

    Args:
        pattern: 正则表达式模式
        text: 要搜索的文本
        flags: 正则表达式标志

    Returns:
        所有匹配的列表
    """
    return re.findall(pattern, text, flags)


def regex_sub(pattern: str, replacement: str, text: str, flags: int = 0) -> str:
    """
    正则表达式替换

    Args:
        pattern: 正则表达式模式
        replacement: 替换字符串
        text: 原文本
        flags: 正则表达式标志

    Returns:
        替换后的文本
    """
    return re.sub(pattern, replacement, text, flags)


def regex_split(pattern: str, text: str, flags: int = 0) -> List[str]:
    """
    正则表达式分割

    Args:
        pattern: 正则表达式模式
        text: 要分割的文本
        flags: 正则表达式标志

    Returns:
        分割后的列表
    """
    return re.split(pattern, text, flags)


# =============================================================================
# 字符串清理操作
# =============================================================================


def remove_special_chars(text: str, keep_chars: str = "") -> str:
    """
    移除特殊字符

    Args:
        text: 原字符串
        keep_chars: 要保留的特殊字符

    Returns:
        清理后的字符串
    """
    # 保留字母、数字、空格和指定的特殊字符
    pattern = f"[^a-zA-Z0-9\s{re.escape(keep_chars)}]"
    return re.sub(pattern, "", text)


def remove_html_tags(text: str) -> str:
    """
    移除HTML标签

    Args:
        text: 包含HTML标签的文本

    Returns:
        清理后的文本
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def remove_emojis(text: str) -> str:
    """
    移除表情符号

    Args:
        text: 包含表情符号的文本

    Returns:
        清理后的文本
    """
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags (iOS)
        "\U00002702-\U000027b0"
        "\U000024c2-\U0001f251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def normalize_accents(text: str) -> str:
    """
    标准化重音字符

    Args:
        text: 包含重音字符的文本

    Returns:
        标准化后的文本
    """
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def sanitize_filename(text: str) -> str:
    """
    清理文件名（移除非法字符）

    Args:
        text: 原文件名

    Returns:
        清理后的文件名
    """
    # 移除或替换非法文件名字符
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        text = text.replace(char, "_")

    # 移除控制字符
    text = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)

    # 移除首尾点和空格
    text = text.strip(". ")

    # 确保不为空
    if not text:
        text = "unnamed"

    return text


# =============================================================================
# 字符串比较操作
# =============================================================================


def similarity_ratio(text1: str, text2: str) -> float:
    """
    计算字符串相似度（基于Levenshtein距离）

    Args:
        text1: 第一个字符串
        text2: 第二个字符串

    Returns:
        相似度（0-1）
    """
    import difflib

    return difflib.SequenceMatcher(None, text1, text2).ratio()


def fuzzy_match(text: str, choices: List[str], threshold: float = 0.6) -> Optional[str]:
    """
    模糊匹配

    Args:
        text: 要匹配的文本
        choices: 候选列表
        threshold: 相似度阈值

    Returns:
        最佳匹配，未找到返回None
    """
    best_match = None
    best_ratio = 0

    for choice in choices:
        ratio = similarity_ratio(text, choice)
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = choice

    return best_match


def startswith_ignore_case(text: str, prefix: str) -> bool:
    """
    忽略大小写检查前缀

    Args:
        text: 要检查的字符串
        prefix: 前缀

    Returns:
        是否匹配
    """
    return text.lower().startswith(prefix.lower())


def endswith_ignore_case(text: str, suffix: str) -> bool:
    """
    忽略大小写检查后缀

    Args:
        text: 要检查的字符串
        suffix: 后缀

    Returns:
        是否匹配
    """
    return text.lower().endswith(suffix.lower())


def contains_ignore_case(text: str, substring: str) -> bool:
    """
    忽略大小写检查包含

    Args:
        text: 要检查的字符串
        substring: 子字符串

    Returns:
        是否包含
    """
    return substring.lower() in text.lower()


# =============================================================================
# 字符串统计操作
# =============================================================================


def string_length(text: str) -> int:
    """获取字符串长度"""
    return len(text)


def word_count(text: str) -> int:
    """统计单词数量"""
    return len(text.split())


def char_frequency(text: str) -> dict:
    """
    统计字符频率

    Args:
        text: 要统计的文本

    Returns:
        字符频率字典
    """
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1
    return frequency


def word_frequency(text: str) -> dict:
    """
    统计单词频率

    Args:
        text: 要统计的文本

    Returns:
        单词频率字典
    """
    words = text.lower().split()
    frequency = {}
    for word in words:
        # 移除标点符号
        clean_word = word.strip(".,!?;:\"'")
        frequency[clean_word] = frequency.get(clean_word, 0) + 1
    return frequency


def most_common_chars(text: str, n: int = 10) -> List[tuple]:
    """
    获取最常见的字符

    Args:
        text: 要分析的文本
        n: 返回的数量

    Returns:
        (字符, 频率) 元组列表
    """
    frequency = char_frequency(text)
    return sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:n]


def most_common_words(text: str, n: int = 10) -> List[tuple]:
    """
    获取最常见的单词

    Args:
        text: 要分析的文本
        n: 返回的数量

    Returns:
        (单词, 频率) 元组列表
    """
    frequency = word_frequency(text)
    return sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:n]


# =============================================================================
# 字符串转换操作
# =============================================================================


def int_to_string(number: int) -> str:
    """整数转字符串"""
    return str(number)


def float_to_string(number: float, precision: int = 2) -> str:
    """
    浮点数转字符串

    Args:
        number: 浮点数
        precision: 小数位数

    Returns:
        字符串
    """
    return f"{number:.{precision}f}"


def bool_to_string(value: bool) -> str:
    """布尔值转字符串"""
    return str(value).lower()


def list_to_string(lst: List[Any], separator: str = ", ") -> str:
    """
    列表转字符串

    Args:
        lst: 列表
        separator: 分隔符

    Returns:
        字符串
    """
    return separator.join(str(item) for item in lst)


def dict_to_string(d: dict, separator: str = ", ", pair_separator: str = "=") -> str:
    """
    字典转字符串

    Args:
        d: 字典
        separator: 键值对之间的分隔符
        pair_separator: 键和值之间的分隔符

    Returns:
        字符串
    """
    return separator.join(f"{k}{pair_separator}{v}" for k, v in d.items())


def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    日期格式化

    Args:
        date: 日期对象
        format_str: 格式字符串

    Returns:
        格式化后的日期字符串
    """
    return date.strftime(format_str)


def format_number(number: Union[int, float], locale: str = "en_US") -> str:
    """
    数字格式化（添加千位分隔符）

    Args:
        number: 数字
        locale: 语言环境

    Returns:
        格式化后的数字字符串
    """
    try:
        import locale

        locale.setlocale(locale.LC_ALL, locale)
        return locale.format_string("%d", number, grouping=True)
    except:
        # 如果locale设置失败，使用简单格式化
        return format(number, ",").replace(",", " ")


# =============================================================================
# 字符串加密解密操作
# =============================================================================


def md5_hash(text: str) -> str:
    """
    MD5哈希

    Args:
        text: 要哈希的文本

    Returns:
        MD5哈希值
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sha1_hash(text: str) -> str:
    """
    SHA1哈希

    Args:
        text: 要哈希的文本

    Returns:
        SHA1哈希值
    """
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def sha256_hash(text: str) -> str:
    """
    SHA256哈希

    Args:
        text: 要哈希的文本

    Returns:
        SHA256哈希值
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def simple_encrypt(text: str, key: str) -> str:
    """
    简单加密（异或加密）

    Args:
        text: 要加密的文本
        key: 加密密钥

    Returns:
        加密后的字符串
    """
    encrypted = []
    for i, char in enumerate(text):
        key_char = key[i % len(key)]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted.append(encrypted_char)
    return base64.b64encode("".join(encrypted).encode()).decode()


def simple_decrypt(encrypted_text: str, key: str) -> str:
    """
    简单解密（异或解密）

    Args:
        encrypted_text: 加密文本
        key: 解密密钥

    Returns:
        解密后的字符串
    """
    decoded = base64.b64decode(encrypted_text.encode()).decode()
    decrypted = []
    for i, char in enumerate(decoded):
        key_char = key[i % len(key)]
        decrypted_char = chr(ord(char) ^ ord(key_char))
        decrypted.append(decrypted_char)
    return "".join(decrypted)


# =============================================================================
# 字符串生成操作
# =============================================================================


def generate_random_string(length: int, chars: str = None) -> str:
    """
    生成随机字符串

    Args:
        length: 字符串长度
        chars: 字符集合，None表示使用字母数字

    Returns:
        随机字符串
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def generate_uuid() -> str:
    """生成UUID"""
    import uuid

    return str(uuid.uuid4())


def generate_timestamp() -> str:
    """生成时间戳字符串"""
    return str(int(datetime.now().timestamp()))


def generate_date_string(format_str: str = "%Y-%m-%d") -> str:
    """
    生成日期字符串

    Args:
        format_str: 日期格式

    Returns:
        日期字符串
    """
    return datetime.now().strftime(format_str)


def generate_slug(text: str, max_length: int = 50) -> str:
    """
    生成URL友好的slug

    Args:
        text: 原文本
        max_length: 最大长度

    Returns:
        slug字符串
    """
    # 转换为小写
    slug = text.lower()

    # 移除特殊字符
    slug = re.sub(r"[^\w\s-]", "", slug)

    # 替换空格为连字符
    slug = re.sub(r"[\s-]+", "-", slug)

    # 移除首尾连字符
    slug = slug.strip("-")

    # 截断到指定长度
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")

    return slug


# =============================================================================
# 字符串反转操作
# =============================================================================


def reverse_string(text: str) -> str:
    """反转字符串"""
    return text[::-1]


def reverse_words(text: str) -> str:
    """反转单词顺序"""
    words = text.split()
    return " ".join(words[::-1])


def reverse_words_in_place(text: str) -> str:
    """反转每个单词（保持单词顺序）"""
    words = text.split()
    reversed_words = [word[::-1] for word in words]
    return " ".join(reversed_words)


# =============================================================================
# 字符串提取操作
# =============================================================================


def extract_numbers(text: str) -> List[str]:
    """
    提取所有数字

    Args:
        text: 原文本

    Returns:
        数字列表
    """
    return re.findall(r"\d+", text)


def extract_emails(text: str) -> List[str]:
    """
    提取所有邮箱地址

    Args:
        text: 原文本

    Returns:
        邮箱地址列表
    """
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """
    提取所有URL

    Args:
        text: 原文本

    Returns:
        URL列表
    """
    pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.findall(pattern, text)


def extract_phone_numbers(text: str) -> List[str]:
    """
    提取所有手机号

    Args:
        text: 原文本

    Returns:
        手机号列表
    """
    pattern = r"1[3-9]\d{9}"
    return re.findall(pattern, text)


def extract_chinese(text: str) -> str:
    """
    提取中文字符

    Args:
        text: 原文本

    Returns:
        中文字符串
    """
    return "".join(re.findall(r"[\u4e00-\u9fff]", text))


# =============================================================================
# 字符串验证和检查操作
# =============================================================================


def has_whitespace(text: str) -> bool:
    """检查是否包含空白字符"""
    return any(char.isspace() for char in text)


def has_digits(text: str) -> bool:
    """检查是否包含数字"""
    return any(char.isdigit() for char in text)


def has_letters(text: str) -> bool:
    """检查是否包含字母"""
    return any(char.isalpha() for char in text)


def has_uppercase(text: str) -> bool:
    """检查是否包含大写字母"""
    return any(char.isupper() for char in text)


def has_lowercase(text: str) -> bool:
    """检查是否包含小写字母"""
    return any(char.islower() for char in text)


def has_special_chars(text: str) -> bool:
    """检查是否包含特殊字符"""
    return any(not char.isalnum() and not char.isspace() for char in text)


def count_vowels(text: str) -> int:
    """统计元音字母数量"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)


def count_consonants(text: str) -> int:
    """统计辅音字母数量"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char.isalpha() and char not in vowels)


# =============================================================================
# 便捷函数和组合操作
# =============================================================================


def clean_and_normalize(text: str) -> str:
    """
    清理和标准化字符串

    Args:
        text: 原文本

    Returns:
        清理后的字符串
    """
    # 移除多余空白
    text = normalize_whitespace(text)

    # 标准化重音字符
    text = normalize_accents(text)

    # 转换为小写
    text = text.lower()

    # 移除特殊字符（可选）
    # text = remove_special_chars(text)

    return text


def format_for_display(text: str, max_length: int = 100) -> str:
    """
    格式化用于显示的字符串

    Args:
        text: 原文本
        max_length: 最大显示长度

    Returns:
        格式化后的字符串
    """
    if len(text) <= max_length:
        return text

    # 尝试在单词边界截断
    truncated = text[: max_length - 3]
    last_space = truncated.rfind(" ")

    if last_space > max_length // 2:
        return truncated[:last_space] + "..."
    else:
        return truncated + "..."


def safe_string_conversion(value: Any) -> str:
    """
    安全的字符串转换

    Args:
        value: 任意值

    Returns:
        字符串
    """
    if value is None:
        return ""
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def truncate_middle(text: str, max_length: int = 30) -> str:
    """
    从中间截断字符串

    Args:
        text: 原文本
        max_length: 最大长度

    Returns:
        截断后的字符串
    """
    if len(text) <= max_length:
        return text

    half = (max_length - 3) // 2
    return text[:half] + "..." + text[-half:]


# =============================================================================
# 使用示例和测试
# =============================================================================

if __name__ == "__main__":
    # 基本操作示例
    print("=== 基本操作示例 ===")

    # 拼接操作
    result1 = join_strings("hello", "world", 123, separator=" ")
    print(f"拼接: {result1}")

    # 分割操作
    result2 = split_string("hello world python", " ")
    print(f"分割: {result2}")

    # 查找操作
    result3 = find_string("hello world", "world")
    print(f"查找: {result3}")

    # 替换操作
    result4 = replace_string("hello world", "world", "python")
    print(f"替换: {result4}")

    # 格式化操作
    result5 = pad_string("hello", 10, "*", "center")
    print(f"格式化: {result5}")

    # 大小写操作
    result6 = to_uppercase("Hello World")
    print(f"大写: {result6}")

    # 空白处理
    result7 = strip_string("  hello  ")
    print(f"去空白: '{result7}'")

    print("\n=== 验证操作示例 ===")

    # 验证操作
    print(f"是否为数字: {is_numeric('123')}")
    print(f"是否为邮箱: {is_email('test@example.com')}")
    print(f"是否为URL: {is_url('https://example.com')}")
    print(f"是否包含中文: {contains_chinese('hello 世界')}")

    print("\n=== 编码解码示例 ===")

    # 编码解码
    encoded = encode_base64("hello world")
    decoded = decode_base64(encoded)
    print(f"Base64编码: {encoded}")
    print(f"Base64解码: {decoded}")

    print("\n=== 正则表达式示例 ===")

    # 正则表达式
    text = "Contact us at info@example.com or support@example.com"
    emails = extract_emails(text)
    print(f"提取邮箱: {emails}")

    print("\n=== 字符串统计示例 ===")

    # 统计操作
    text = "hello world hello python"
    print(f"字符频率: {char_frequency(text)}")
    print(f"单词频率: {word_frequency(text)}")

    print("\n=== 字符串生成示例 ===")

    # 生成操作
    print(f"随机字符串: {generate_random_string(10)}")
    print(f"UUID: {generate_uuid()}")
    print(f"时间戳: {generate_timestamp()}")

    print("\n=== 字符串反转示例 ===")

    # 反转操作
    text = "hello world"
    print(f"反转: {reverse_string(text)}")
    print(f"反转单词: {reverse_words(text)}")

    print("\n=== 提取操作示例 ===")

    # 提取操作
    text = "Contact: 123-456-7890 or email me at test@example.com"
    print(f"提取数字: {extract_numbers(text)}")
    print(f"提取邮箱: {extract_emails(text)}")

    print("\n=== 组合操作示例 ===")

    # 组合操作
    messy_text = "  Héllo Wörld! 123  "
    clean_text = clean_and_normalize(messy_text)
    print(f"清理前: '{messy_text}'")
    print(f"清理后: '{clean_text}'")

    # 显示格式化
    long_text = (
        "This is a very long text that needs to be truncated for display purposes"
    )
    display_text = format_for_display(long_text, 30)
    print(f"显示格式化: {display_text}")

    # 安全转换
    values = [None, 123, "hello", True, [1, 2, 3]]
    for value in values:
        print(f"安全转换 {type(value).__name__}: '{safe_string_conversion(value)}'")
