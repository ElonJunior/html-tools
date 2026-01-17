#!/usr/bin/env python3
"""
自动更新 sitemap.xml 文件
使用说明：
1. 在更新工具后运行此脚本：python3 scripts/update_sitemap.py
2. 或者在 GitHub Actions 中设置为自动运行
"""
import json
from pathlib import Path
from datetime import datetime
import sys

BASE_URL = "https://tools.karing.app"

def generate_sitemap():
    """生成sitemap.xml"""
    # 脚本在 scripts/ 目录下，需要获取项目根目录
    base_dir = Path(__file__).parent.parent

    # 读取工具列表
    try:
        with open(base_dir / 'index.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("错误: 找不到 index.json 文件")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: index.json 格式错误: {e}")
        sys.exit(1)

    urls = []
    today = datetime.now().strftime('%Y-%m-%d')

    # 添加主页
    urls.append({
        'loc': BASE_URL + '/',
        'lastmod': today,
        'changefreq': 'daily',
        'priority': '1.0'
    })

    # 添加其他页面
    for page in ['reference.html']:
        page_path = base_dir / page
        if page_path.exists():
            # 使用文件的修改时间
            lastmod = datetime.fromtimestamp(page_path.stat().st_mtime).strftime('%Y-%m-%d')
            urls.append({
                'loc': BASE_URL + '/' + page,
                'lastmod': lastmod,
                'changefreq': 'monthly',
                'priority': '0.5'
            })

    # 添加 CONTRIBUTING.md (指向 GitHub)
    contributing_path = base_dir / 'CONTRIBUTING.md'
    if contributing_path.exists():
        lastmod = datetime.fromtimestamp(contributing_path.stat().st_mtime).strftime('%Y-%m-%d')
        urls.append({
            'loc': 'https://github.com/ElonJunior/html-tools/raw/refs/heads/prod/CONTRIBUTING.md',
            'lastmod': lastmod,
            'changefreq': 'monthly',
            'priority': '0.5'
        })

    # 添加所有工具页面
    for tool in data.get('tools', []):
        slug = tool.get('slug', '')
        if not slug:
            continue

        # 工具详情页 (index.html)
        index_path = base_dir / 'tools' / slug / 'index.html'
        app_path = base_dir / 'tools' / slug / 'app.html'

        # 使用文件的最后修改时间
        lastmod = tool.get('updatedAt', tool.get('createdAt', today))
        if index_path.exists():
            file_time = datetime.fromtimestamp(index_path.stat().st_mtime).strftime('%Y-%m-%d')
            # 如果文件修改时间更新，使用文件时间
            if file_time > lastmod:
                lastmod = file_time

        urls.append({
            'loc': BASE_URL + '/tools/' + slug + '/',
            'lastmod': lastmod,
            'changefreq': 'monthly',
            'priority': '0.8'
        })

        # 工具应用页 (app.html)
        if app_path.exists():
            app_time = datetime.fromtimestamp(app_path.stat().st_mtime).strftime('%Y-%m-%d')
            if app_time > lastmod:
                lastmod = app_time

        urls.append({
            'loc': BASE_URL + '/tools/' + slug + '/app.html',
            'lastmod': lastmod,
            'changefreq': 'monthly',
            'priority': '0.7'
        })

    # 生成XML - 使用标准格式
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += '  </url>\n'

    xml += '</urlset>\n'

    # 写入文件
    sitemap_path = base_dir / 'sitemap.xml'
    try:
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(xml)
        print(f"✓ 成功生成 sitemap.xml")
        print(f"  - 包含 {len(urls)} 个URL")
        print(f"  - 文件路径: {sitemap_path}")
        return True
    except Exception as e:
        print(f"✗ 写入文件失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    generate_sitemap()

