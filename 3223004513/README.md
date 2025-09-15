论文查重系统
这是一个基于Python的论文查重系统，使用余弦相似度算法计算文本重复率。系统能够比较两篇中文论文的相似度，并输出精确的重复率百分比。

功能特点
✅ 支持中文文本处理
✅ 使用jieba分词库进行精准中文分词
✅ 基于余弦相似度算法计算文本相似度
✅ 内置停用词过滤，提高查重准确性
✅ 输出精确到小数点后两位的重复率
✅ 支持命令行参数调用
✅ 完善的异常处理和错误提示
✅ 类型注解支持，提高代码可维护性

安装说明
环境要求
Python 3.7+
pip 包管理工具

安装步骤
克隆或下载本项目到本地
安装依赖包：
bash
pip install -r requirements.txt

依赖包
jieba >= 0.42.1 (中文分词库)
其他依赖详见 requirements.txt 文件

使用方法
基本用法
bash
python main.py [原文文件] [抄袭版论文的文件] [答案文件]

使用示例
bash
# Windows 示例
python main.py C:\tests\orig.txt C:\tests\orig_add.txt C:\tests\ans.txt
# Linux/Mac 示例
python main.py /home/user/orig.txt /home/user/plagiarized.txt /home/user/result.txt

参数说明
原文文件: 原始论文的完整路径
抄袭版论文的文件: 待检测论文的完整路径
答案文件: 结果输出文件的完整路径

算法说明
本系统采用余弦相似度算法计算文本相似度，主要步骤如下：

文本预处理：使用jieba进行中文分词，并过滤停用词
向量化：将文本转换为词频向量
相似度计算：计算两个向量的余弦相似度
结果输出：将相似度转换为百分比格式输出

余弦相似度公式：
text
similarity = (A · B) / (||A|| * ||B||)
其中A和B分别是两篇文本的词频向量。

项目结构
text
paper-check/
├── main.py              # 主程序文件
├── test_main.py         # 单元测试文件
├── requirements.txt     # 项目依赖列表
├── README.md           # 项目说明文档
├── samples/            # 示例文件目录
│   ├── orig.txt        # 原文示例
│   ├── plagiarized.txt # 抄袭版示例
│   └── result.txt      # 结果输出示例
└── tests/              # 测试目录
    └── test_data/      # 测试数据

测试
运行单元测试
bash
python -m unittest discover

测试覆盖率检查
bash
coverage run -m unittest discover
coverage report

代码质量检查
bash
# 代码格式化
black main.py test_main.py
# 代码风格检查
flake8 main.py test_main.py
# 类型检查
mypy main.py test_main.py

性能分析
可以使用cProfile进行性能分析：
bash
python -m cProfile -o profile_output main.py samples/orig.txt samples/plagiarized.txt samples/result.txt

注意事项
1.系统仅支持UTF-8编码的文本文件
2.建议文本文件大小不超过10MB以保证性能
3.系统会过滤常见停用词以提高查重准确性
4.对于非常短的文本，相似度计算结果可能不够准确

作者
姓名：[]
学号：[3223004513]
