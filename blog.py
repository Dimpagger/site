#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简博客转换脚本
将 Markdown 文件转换为 HTML，参考 ESR 网站风格
"""

import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

# 尝试导入 markdown 库
try:
    import markdown
except ImportError:
    print("错误: 需要安装 markdown 库")
    print("请运行: venv/bin/pip install markdown")
    sys.exit(1)


class BlogConverter:
    def __init__(self, template_path=None, style_path=None):
        # 设置默认路径
        self.script_dir = Path(__file__).parent
        self.template_path = template_path or self.script_dir / "templates" / "page.html"
        self.style_path = style_path or self.script_dir / "static" / "style.css"
        self.output_dir = self.script_dir / "docs"

        # 加载模板
        self.template = self.load_template()

        # 配置 markdown - 使用真正的 markdown 库
        self.md = markdown.Markdown(
            extensions=[
                'extra',       # 包含 tables, fenced_code, etc.
                'codehilite',  # 代码高亮
                'toc',         # 目录
                'nl2br',       # 换行转 <br>
            ]
        )

    def load_template(self):
        """加载 HTML 模板"""
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def read_markdown(self, filepath):
        """读取 Markdown 文件"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_frontmatter(self, content):
        """
        提取 YAML 格式的前置元数据
        格式:
        ---
        title: 标题
        date: 2024-01-01
        ---
        """
        frontmatter = {}
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm_text = parts[1].strip()
                content = parts[2].strip()

                # 解析简单的 key: value 格式
                for line in fm_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()

        return frontmatter, content

    def convert_to_html(self, markdown_content):
        """将 Markdown 转换为 HTML"""
        self.md.reset()  # 重置状态
        return self.md.convert(markdown_content)

    def generate_menu(self, posts):
        """生成侧边栏菜单"""
        menu_items = []
        for post in posts:
            title = post.get('title', '无标题')
            filename = post.get('filename', 'index.html')
            menu_items.append(
                f'<a class="MenuLink" href="{filename}">{title}</a>'
            )
        return '\n        '.join(menu_items)

    def render_template(self, title, content, menu=''):
        """渲染 HTML 模板"""
        site_name = "我的博客"
        return (
            self.template
            .replace('{{title}}', title)
            .replace('{{content}}', content)
            .replace('{{menu}}', menu)
            .replace('{{site_name}}', site_name)
        )

    def convert_file(self, input_path, output_path=None):
        """转换单个 Markdown 文件"""
        # 读取文件
        content = self.read_markdown(input_path)

        # 提取前置元数据
        frontmatter, md_content = self.extract_frontmatter(content)

        # 转换为 HTML
        html_content = self.convert_to_html(md_content)

        # 获取标题
        title = frontmatter.get('title', Path(input_path).stem)

        # 生成输出路径
        if output_path is None:
            output_name = Path(input_path).stem + '.html'
            output_path = self.output_dir / output_name

        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)

        # 渲染模板
        final_html = self.render_template(title, html_content)

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"✓ 已转换: {input_path} -> {output_path}")
        return {'title': title, 'filename': output_path.name}

    def convert_directory(self, input_dir):
        """转换目录下所有 Markdown 文件"""
        input_path = Path(input_dir)
        posts = []

        # 查找所有 .md 文件
        md_files = list(input_path.glob('*.md'))

        if not md_files:
            print(f"警告: 在 {input_dir} 中没有找到 Markdown 文件")
            return []

        # 转换每个文件
        for md_file in sorted(md_files):
            result = self.convert_file(md_file)
            posts.append(result)

        # 生成索引页（可选）
        if posts:
            self.generate_index(posts)

        return posts

    def generate_index(self, posts):
        """生成索引页面"""
        # 生成菜单链接
        menu_html = self.generate_menu(posts)

        # 生成文章列表
        posts_html = '<h2>文章列表</h2>\n<ul>\n'
        for post in posts:
            posts_html += f'    <li><a href="{post["filename"]}">{post["title"]}</a></li>\n'
        posts_html += '</ul>'

        # 渲染模板
        final_html = self.render_template('文章索引', posts_html, menu_html)

        # 写入索引页
        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"✓ 已生成索引: {index_path}")


def main():
    parser = argparse.ArgumentParser(
        description='极简博客转换器 - 将 Markdown 转换为 HTML'
    )
    parser.add_argument(
        'input',
        help='输入的 Markdown 文件或目录'
    )
    parser.add_argument(
        '-o', '--output',
        help='输出目录 (默认: output/)'
    )
    parser.add_argument(
        '-t', '--template',
        help='自定义模板文件'
    )

    args = parser.parse_args()

    # 创建转换器
    converter = BlogConverter(template_path=args.template)

    # 如果指定了输出目录
    if args.output:
        converter.output_dir = Path(args.output)
        converter.output_dir.mkdir(exist_ok=True)

    # 执行转换
    input_path = Path(args.input)

    if input_path.is_file():
        converter.convert_file(input_path)
    elif input_path.is_dir():
        converter.convert_directory(input_path)
    else:
        print(f"错误: 输入路径不存在: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
