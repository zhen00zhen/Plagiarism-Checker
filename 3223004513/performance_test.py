#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
性能测试脚本
用于测试论文查重系统的性能
"""

from main import calculate_cosine_similarity
import time

def test_performance():
    """性能测试函数"""
    # 生成长文本进行性能测试
    long_text = "文本查重测试。" * 1000
    
    # 预热：先运行一次让Jieba加载模型
    calculate_cosine_similarity("预热文本", "预热文本")
    
    start_time = time.time()
    
    # 运行性能测试
    similarity = calculate_cosine_similarity(long_text, long_text)
    
    end_time = time.time()
    print(f"执行时间: {end_time - start_time:.4f}秒")
    print(f"相似度: {similarity:.4f}")

if __name__ == "__main__":
    test_performance()
