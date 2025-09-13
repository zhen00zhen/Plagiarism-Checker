# 论文查重系统

这是一个基于Python的论文查重系统，使用余弦相似度算法计算文本重复率。

## 功能特点
- 支持中文文本处理
- 使用jieba分词库
- 计算余弦相似度
- 输出精确到小数点后两位的重复率

## 使用方法
1. 安装依赖：pip install -r requirements.txt
2. 运行程序：python main.py [原文文件] [抄袭版论文的文件] [答案文件]

## 项目结构
- main.py: 主程序文件
- test_main.py: 单元测试文件
- requirements.txt: 项目依赖列表
