import os
import re

def count_chinese_characters_in_file(file_path):
    """ 计算指定文件中的中文字符数 """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 使用正则表达式匹配中文字符
            chinese_characters = re.findall(r'[\u4e00-\u9fff]', content)
            return len(chinese_characters)
    except Exception as e:
        print(f'Error reading {file_path}: {e}')
        return 0

def main():
    """ 统计当前目录下所有 .txt 文件的总中文字数 """
    total_chinese_count = 0
    
    for filename in os.listdir('.'):
        if filename.endswith('.txt'):
            file_path = os.path.join('.', filename)
            chinese_count = count_chinese_characters_in_file(file_path)
            total_chinese_count += chinese_count
            print(f'{filename}: {chinese_count} Chinese characters')
    
    print(f'Total Chinese characters in all .txt files: {total_chinese_count}')

if __name__ == '__main__':
    main()
