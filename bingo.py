import os
import re

def convert_crlf_to_lf(file_path):
    """ 将 TXT 或 LRC 文件中的 CRLF 换行符转换为 LF """
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as file:
            content = file.read()
        
        # 替换 CRLF（\r\n）为 LF（\n）
        new_content = content.replace('\r\n', '\n')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8', newline='') as file:
                file.write(new_content)
            print(f"已将文件 {file_path} 中的 CRLF 换行符转换为 LF")
        else:
            print(f"文件 {file_path} 中无需要转换的换行符")
    except UnicodeDecodeError as e:
        print(f"无法读取文件 {file_path}: {e}")

def remove_trailing_newline(file_path):
    """ 删除 TXT 或 LRC 文件末尾的多余换行符 """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 使用 rstrip() 去除结尾的换行符
        new_content = content.rstrip()
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"已删除文件 {file_path} 中末尾的多余换行符")
        else:
            print(f"文件 {file_path} 中无多余换行符")
    except UnicodeDecodeError as e:
        print(f"无法读取文件 {file_path}: {e}")

def remove_lines_with_colons(file_path):
    """ 删除含有中文或英文冒号的行，并返回删除的内容 """
    deleted_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 匹配含有中文冒号或英文冒号的行
        colon_pattern = re.compile(r'[：:]')
        
        # 过滤出不包含冒号的行，并记录被删除的行
        new_lines = []
        for line in lines:
            if colon_pattern.search(line):
                deleted_lines.append(line.strip())
            else:
                new_lines.append(line)
        
        # 如果有行被删除，更新文件内容
        if len(deleted_lines) > 0:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(new_lines)
            print(f"已删除文件 {file_path} 中包含冒号的行: {deleted_lines}")
        else:
            print(f"文件 {file_path} 中没有包含冒号的行")
    except UnicodeDecodeError as e:
        print(f"无法读取文件 {file_path}: {e}")
    
    return deleted_lines

def process_lrc_file(input_file):
    """ 处理 LRC 文件，删除时间戳，并将歌词保存到 TXT 文件 """
    output_file = f'{os.path.splitext(input_file)[0]}.txt'
    
    if not os.path.exists(input_file):
        print(f'输入文件 {input_file} 不存在。')
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # 正则表达式匹配时间戳（[00:00.000]）
        timestamp_pattern = re.compile(r'\[\d{2}:\d{2}\.\d{3}\]')
        
        with open(output_file, 'w', encoding='utf-8') as file:
            for line in lines:
                # 删除时间戳
                cleaned_line = timestamp_pattern.sub('', line).strip()
                if cleaned_line:
                    file.write(cleaned_line + '\n')
        
        print(f'已处理 LRC 文件: {input_file}，歌词保存到: {output_file}')
        
        # 删除原始 .lrc 文件
        os.remove(input_file)
        print(f'已删除原始 LRC 文件: {input_file}')
    
    except UnicodeDecodeError as e:
        print(f"无法读取文件 {input_file}: {e}")

def remove_empty_txt_files(directory):
    """ 删除空白的 TXT 文件 """
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                print(f"已删除空白文件: {file_path}")

def process_files_in_directory(directory):
    """ 处理指定目录下的所有 .txt 和 .lrc 文件 """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if filename.endswith('.txt'):
            # 1. 将 CRLF 换行符转换为 LF
            convert_crlf_to_lf(file_path)
            
            # 2. 删除文件末尾的多余换行符
            remove_trailing_newline(file_path)
            
            # 3. 删除包含中文或英文冒号的行
            deleted_lines = remove_lines_with_colons(file_path)
            if deleted_lines:
                print(f"从文件 {file_path} 中删除的行: {deleted_lines}")
        
        elif filename.endswith('.lrc'):
            # 处理 .lrc 文件
            process_lrc_file(file_path)
    
    # 删除空白的 TXT 文件
    remove_empty_txt_files(directory)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    process_files_in_directory(current_directory)
