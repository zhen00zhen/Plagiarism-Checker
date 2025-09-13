import sys
import jieba
import math
from collections import Counter

def read_file(file_path):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件时出错：{e}")
        sys.exit(1)

def write_file(file_path, result):
    """
    将结果写入文件
    :param file_path: 输出文件路径
    :param result: 要写入的结果
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"{result:.2f}")
    except Exception as e:
        print(f"写入文件时出错：{e}")
        sys.exit(1)

def preprocess(text):
    """
    文本预处理：分词并过滤停用词
    :param text: 原始文本
    :return: 处理后的词列表
    """
    # 使用jieba分词
    words = jieba.cut(text)
    # 可以在这里添加停用词过滤等预处理步骤
    return list(words)

def calculate_cosine_similarity(text1, text2):
    """
    计算两个文本的余弦相似度
    :param text1: 文本1
    :param text2: 文本2
    :return: 相似度得分 (0-1)
    """
    # 分词并获取词频
    words1 = preprocess(text1)
    words2 = preprocess(text2)
    
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
    return dot_product / (magnitude1 * magnitude2)

def main():
    """
    主函数：处理命令行参数并执行查重
    """
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版论文的文件] [答案文件]")
        sys.exit(1)
    
    original_file = sys.argv[1]
    plagiarized_file = sys.argv[2]
    output_file = sys.argv[3]
    
    try:
        # 读取文件内容
        original_text = read_file(original_file)
        plagiarized_text = read_file(plagiarized_file)
        
        # 计算相似度
        similarity = calculate_cosine_similarity(original_text, plagiarized_text)
        
        # 将相似度转换为百分比并写入文件
        write_file(output_file, similarity * 100)
        
        print(f"查重完成！重复率: {similarity*100:.2f}%")
        
    except Exception as e:
        print(f"处理过程中出错: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
