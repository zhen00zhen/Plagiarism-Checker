import unittest
import os
from main import read_file, write_file, calculate_cosine_similarity

class TestPaperCheck(unittest.TestCase):
    
    def setUp(self):
        """在每个测试方法前执行，用于设置测试环境"""
        # 创建测试用的临时文件
        with open('test_orig.txt', 'w', encoding='utf-8') as f:
            f.write("今天是星期天，天气晴，今天晚上我要去看电影。")
        
        with open('test_plag.txt', 'w', encoding='utf-8') as f:
            f.write("今天是周天，天气晴朗，我晚上要去看电影。")
        
        with open('empty_file.txt', 'w', encoding='utf-8') as f:
            f.write("")  # 创建空文件
    
    def tearDown(self):
        """在每个测试方法后执行，用于清理测试环境"""
        # 删除测试用的临时文件
        test_files = ['test_orig.txt', 'test_plag.txt', 'test_output.txt', 'empty_file.txt']
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
    
    def test_read_file_normal(self):
        """测试正常文件读取功能"""
        content = read_file('test_orig.txt')
        self.assertEqual(content, "今天是星期天，天气晴，今天晚上我要去看电影。")
    
    def test_read_file_nonexistent(self):
        """测试读取不存在文件时的异常处理"""
        with self.assertRaises(SystemExit):
            read_file('nonexistent_file.txt')
    
    def test_write_file_normal(self):
        """测试文件写入功能"""
        write_file('test_output.txt', 75.50)
        with open('test_output.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, "75.50")
    
    def test_cosine_similarity_identical(self):
        """测试相同文本的相似度计算"""
        text1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        text2 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        similarity = calculate_cosine_similarity(text1, text2)
        self.assertAlmostEqual(similarity, 1.0, places=2)
    
    def test_cosine_similarity_different(self):
        """测试完全不同文本的相似度计算"""
        text1 = "今天是星期天"
        text2 = "明天是星期一"
        similarity = calculate_cosine_similarity(text1, text2)
        self.assertLess(similarity, 0.5)
    
    def test_cosine_similarity_partial(self):
        """测试部分相似文本的相似度计算"""
        text1 = "今天是星期天，天气晴，今天晚上我要去看电影。"
        text2 = "今天是周天，天气晴朗，我晚上要去看电影。"
        similarity = calculate_cosine_similarity(text1, text2)
        # 预期相似度应该在0.7-0.9之间
        self.assertGreater(similarity, 0.7)
        self.assertLess(similarity, 0.9)
    
    def test_cosine_similarity_empty(self):
        """测试空文本的相似度计算"""
        text1 = ""
        text2 = "今天是星期天"
        similarity = calculate_cosine_similarity(text1, text2)
        self.assertEqual(similarity, 0.0)
    
    def test_cosine_similarity_both_empty(self):
        """测试两个空文本的相似度计算"""
        text1 = ""
        text2 = ""
        similarity = calculate_cosine_similarity(text1, text2)
        self.assertEqual(similarity, 0.0)

if __name__ == '__main__':
    unittest.main()