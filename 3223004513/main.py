#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
论文查重系统
基于余弦相似度算法计算文本重复率
"""
import re
import sys
import jieba  # type: ignore
import math
from collections import Counter
from typing import List, Set

# 同义词词典 - 提高查重准确性
SYNONYMS = {
    "周天": "星期天",
    "礼拜天": "星期天",
    "星期日": "星期天",
    "周末": "星期天",
    "晴朗": "晴",
    "阳光明媚": "晴",
    "好天气": "晴",
    "明日": "明天",
    "影片": "电影",
    "电影院": "电影",
    "观影": "电影",
    "我要": "我",
    "我想要": "我",
    "我打算": "我",
    "晚上": "晚间",
    "夜晚": "晚间",
    "今夜": "晚间",
    "天气晴朗": "天气晴",  # 添加复合词同义词
    "晴朗天气": "晴好天气",
    # 可以根据需要继续添加更多同义词
}

# 停用词列表 - 减少常见词对相似度计算的影响
STOPWORDS: Set[str] = {
    "的",
    "了",
    "在",
    "是",
    "我",
    "有",
    "和",
    "就",
    "不",
    "人",
    "都",
    "一",
    "一个",
    "上",
    "也",
    "很",
    "到",
    "说",
    "要",
    "去",
    "你",
    "会",
    "着",
    "没有",
    "看",
    "好",
    "自己",
    "这",
    "那",
    "他",
    "她",
    "它",
    "我们",
    "你们",
    "他们",
    "她们",
    "它们",
    "这",
    "那",
    "哪",
    "谁",
    "什么",
    "怎么",
    "为什么",
    "可以",
    "可能",
    "能够",
    "应该",
    "必须",
    "需要",
    "想要",
    "希望",
    "喜欢",
    "认为",
    "觉得",
    "知道",
    "理解",
    "明白",
    "发现",
    "看到",
    "听到",
    "感到",
    "因为",
    "所以",
    "但是",
    "然而",
    "虽然",
    "尽管",
    "如果",
    "只要",
    "只有",
    "除非",
    "无论",
    "不管",
    "即使",
    "既然",
    "为了",
    "关于",
    "对于",
    "根据",
    "按照",
    "通过",
    "随着",
    "作为",
    "以及",
    "及其",
    "及其",
    "其他",
    "另外",
    "此外",
    "同时",
    "同样",
    "例如",
    "比如",
    "尤其",
    "特别",
    "非常",
    "相当",
    "十分",
    "极其",
    "最",
    "更",
    "较",
    "越",
    "挺",
    "好",
    "太",
    "真",
    "还",
    "再",
    "又",
    "也",
    "都",
    "总",
    "共",
    "全",
    "所有",
    "每个",
    "任何",
    "一些",
    "几个",
    "许多",
    "不少",
    "大量",
    "少量",
    "个",
    "件",
    "条",
    "种",
    "类",
    "样",
    "些",
    "点",
    "部分",
    "整体",
    "全部",
    "完全",
    "彻底",
    "绝对",
    "相对",
    "比较",
    "非常",
    "极其",
    "特别",
    "最",
    "顶",
    "极",
    "超",
    "巨",
    "忒",
    "贼",
    "死",
    "狂",
    "爆",
    "绝",
    "顶",
    "极",
    "超",
    "巨",
    "忒",
    "贼",
    "死",
    "狂",
    "爆",
    "绝",
}


def read_file(file_path: str) -> str:
    """
    读取文件内容

    Args:
        file_path: 文件路径

    Returns:
        文件内容字符串

    Raises:
        SystemExit: 当文件不存在或读取失败时退出程序
    """
    try:
        with open(
            file_path, "r", encoding="utf-8-sig"
        ) as f:  # 使用 utf-8-sig 编码去除 BOM
            content = f.read().strip()
            # 进一步确保去除 BOM
            if content.startswith("\ufeff"):
                content = content[1:]
            return content
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
        sys.exit(1)
    except PermissionError:
        print(f"错误：没有权限读取文件 '{file_path}'")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"错误：文件 '{file_path}' 编码不是UTF-8")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件 '{file_path}' 时出错：{e}")
        sys.exit(1)


def write_file(file_path: str, result: float) -> None:
    """
    将结果写入文件

    Args:
        file_path: 输出文件路径
        result: 要写入的结果（浮点数）

    Raises:
        SystemExit: 当写入失败时退出程序
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{result:.2f}")
    except PermissionError:
        print(f"错误：没有权限写入文件 '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"写入文件 '{file_path}' 时出错：{e}")
        sys.exit(1)


def normalize_words(words: List[str]) -> List[str]:
    """
    将同义词转换为统一形式

    Args:
        words: 分词后的词列表

    Returns:
        标准化后的词列表
    """
    normalized = []
    i = 0
    while i < len(words):
        matched = False
        # 检查2-gram和3-gram
        for n in range(3, 0, -1):
            if i + n <= len(words):
                phrase = "".join(words[i:i+n])
                if phrase in SYNONYMS:
                    normalized.append(SYNONYMS[phrase])
                    i += n
                    matched = True
                    break
        if not matched:
            normalized.append(words[i])
            i += 1
    return normalized


def preprocess(text: str) -> List[str]:
    """
    文本预处理：分词并过滤停用词和标点符号

    Args:
        text: 原始文本

    Returns:
        处理后的词列表
    """
    # 移除标点符号
    text = re.sub(r"[^\w\s]", "", text)

    # 使用jieba分词，并转换为列表
    words = list(jieba.cut(text))

    # 过滤停用词、空字符和单个字符
    words = [word for word in words if word not in STOPWORDS and len(word) > 1]

    # 同义词标准化
    words = normalize_words(words)

    return words


def calculate_cosine_similarity(text1: str, text2: str) -> float:
    """
    计算两个文本的余弦相似度

    Args:
        text1: 文本1
        text2: 文本2

    Returns:
        相似度得分 (0-1)
    """
    # 空文本处理
    if not text1 and not text2:
        return 1.0  # 两个空文本视为相同
    elif not text1 or not text2:
        return 0.0

    # 分词并获取词频
    words1 = preprocess(text1)
    words2 = preprocess(text2)

    # 如果预处理后两个文本都为空，返回1
    if not words1 and not words2:
        return 1.0
    elif not words1 or not words2:
        return 0.0

    # 获取所有词汇
    vocab = set(words1) | set(words2)

    # 构建词频向量
    vec1 = Counter(words1)
    vec2 = Counter(words2)

    vector1 = [vec1.get(word, 0) for word in vocab]
    vector2 = [vec2.get(word, 0) for word in vocab]

    # 计算点积
    dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))

    # 计算模长
    magnitude1 = math.sqrt(sum(v * v for v in vector1))
    magnitude2 = math.sqrt(sum(v * v for v in vector2))

    # 避免除零错误
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # 计算余弦相似度
    similarity = dot_product / (magnitude1 * magnitude2)

    return similarity


def main() -> None:
    """
    主函数：处理命令行参数并执行查重
    """
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版论文的文件] [答案文件]")
        print("示例: python main.py orig.txt plagiarized.txt result.txt")
        sys.exit(1)

    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]

    try:
        # 读取文件内容
        print("正在读取文件...")
        original_text = read_file(original_file)
        plagiarized_text = read_file(plagiarized_file)

        # 计算相似度
        print("正在计算相似度...")
        similarity = calculate_cosine_similarity(original_text, plagiarized_text)

        # 将相似度转换为百分比并写入文件
        result = similarity * 100
        write_file(output_file, result)

        print(f"查重完成！重复率: {result:.2f}%")

    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"处理过程中出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
