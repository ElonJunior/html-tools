#!/usr/bin/env python3
"""
HTML文件批量处理脚本
功能：
1. 在所有HTML文件的</head>标签前添加Google Ads代码
2. 替换页面中的域名 https://www.htmls.dev/ 为 https://tools.abc.com/
"""

import os
import re
import argparse
from pathlib import Path
from typing import List

# Google Ads代码模板
GOOGLE_ADS_CODE = """<!-- Google Ads -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6660718818470329" crossorigin="anonymous"></script>
<!-- End Google Ads -->"""

def process_html_files(directory: str, ads_client_id: str = None, dry_run: bool = False):
    """
    处理指定目录下的所有HTML文件

    Args:
        directory: HTML文件所在的目录
        ads_client_id: Google Ads的客户端ID（可选）
        dry_run: 试运行模式，只显示更改而不实际写入
    """
    # 如果提供了客户端ID，则替换模板中的占位符
    ads_code = GOOGLE_ADS_CODE
    # if ads_client_id:
    #     ads_code = ads_code.replace("YOUR_CLIENT_ID", ads_client_id)

    # 统计信息
    stats = {
        'total_files': 0,
        'files_modified': 0,
        'ads_added': 0,
        'links_replaced': 0
    }

    # 支持的文件扩展名
    html_extensions = {'.html', '.htm', '.json'}

    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = Path(root) / file

            # 检查是否是HTML文件
            if filepath.suffix.lower() not in html_extensions:
                continue

            stats['total_files'] += 1
            print(f"处理文件: {filepath}")

            try:
                # 读取文件内容
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content
                modified = False

                # 1. 在</head>前添加Google Ads代码
                if '</head>' in content:
                    # 检查是否已经包含Google Ads代码（避免重复添加）
                    if 'pagead2.googlesyndication.com' not in content:
                        content = content.replace('</head>', f'{ads_code}\n</head>')
                        if content != original_content:
                            modified = True
                            stats['ads_added'] += 1
                            print(f"  ✓ 已添加Google Ads代码")

                # 2. 替换域名
                REPLACE_PAIRS = {
                    'https://www.htmls.dev': 'https://tools.karing.app',
                    'https://htmls.dev' : 'https://tools.karing.app',
                    'github.com/justhtmls/html-tools' : 'github.com/ElonJunior/html-tools'
                }

                # 循环替换
                for old_domain, new_domain in REPLACE_PAIRS.items():
                    if old_domain in content:
                        # 使用正则表达式确保只替换完整的域名
                        pattern = re.compile(re.escape(old_domain), re.IGNORECASE)
                        new_content = pattern.sub(new_domain, content)

                        if new_content != content:
                            modified = True
                            # 统计替换了多少处
                            replacements = len(re.findall(re.escape(old_domain), content, re.IGNORECASE))
                            stats['links_replaced'] += replacements
                            print(f"  ✓ 已替换 {replacements} 处域名引用")

                            content = new_content
                    #END for

                # 如果文件有修改，则写入
                if modified:
                    stats['files_modified'] += 1

                    if not dry_run:
                        # 备份原文件（可选）
                        # backup_path = filepath.with_suffix(filepath.suffix + '.bak')
                        # with open(backup_path, 'w', encoding='utf-8') as f:
                        #     f.write(original_content)

                        # 写入修改后的内容
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"  ✓ 已保存修改")
                    else:
                        print(f"  ⚠ 试运行模式：文件已修改但未保存")
                else:
                    print(f"  ⓘ 文件无修改")

            except UnicodeDecodeError:
                # 尝试其他编码
                try:
                    with open(filepath, 'r', encoding='gbk') as f:
                        content = f.read()
                    print(f"  ⚠ 使用GBK编码读取文件")
                    # 这里可以添加处理逻辑，但为了简单起见，我们跳过非UTF-8文件
                    print(f"  ✗ 跳过非UTF-8编码文件")
                except:
                    print(f"  ✗ 无法读取文件编码: {filepath}")
            except Exception as e:
                print(f"  ✗ 处理文件时出错: {e}")

    # 打印统计信息
    print("\n" + "="*50)
    print("处理完成！统计信息：")
    print(f"扫描文件总数: {stats['total_files']}")
    print(f"修改文件数: {stats['files_modified']}")
    print(f"添加Google Ads代码: {stats['ads_added']} 个文件")
    print(f"替换域名引用: {stats['links_replaced']} 处")
    print("="*50)

    if dry_run:
        print("\n⚠ 注意：本次为试运行模式，未实际修改任何文件！")
        print("使用 --no-dry-run 参数实际执行修改操作。")

def main():
    parser = argparse.ArgumentParser(description='批量处理HTML文件，添加Google Ads代码和替换域名')
    parser.add_argument('directory', nargs='?', default='./html/tools',
                       help='要处理的HTML文件目录（默认: ./html/tools）')
    parser.add_argument('--client-id', '-c',
                       help='Google Ads客户端ID (ca-pub-XXXXXX)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='试运行模式，只显示更改而不实际修改文件')
    parser.add_argument('--no-dry-run', action='store_false', dest='dry_run',
                       help='实际执行修改操作（默认行为）')

    args = parser.parse_args()

    # 检查目录是否存在
    if not os.path.exists(args.directory):
        print(f"错误：目录 '{args.directory}' 不存在！")
        print("请指定正确的HTML文件目录。")
        return

    # 如果没有提供client-id，询问用户
    # if not args.client_id:
    #     use_ads = input("是否要添加Google Ads代码？(y/n): ").lower().strip()
    #     if use_ads == 'y':
    #         args.client_id = input("请输入Google Ads客户端ID (ca-pub-XXXXXX): ").strip()

    # 执行处理
    process_html_files(args.directory, args.client_id, args.dry_run)

if __name__ == "__main__":
    main()