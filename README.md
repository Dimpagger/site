# 极简博客

一个将 Markdown 文件转换为 HTML 的极简博客系统，参考 ESR (Eric S. Raymond) 网站风格设计。

## 特性

- 极简设计 - 纯文本优先，无多余装饰
- 中文支持 - 完美支持中文字体显示
- 易于使用 - 简单的命令行工具
- 响应式布局 - 支持移动端浏览
- 无需外部依赖 - 使用 Python 标准库和 markdown 库

## 项目结构

```
site/
├── blog.py           # 主转换脚本
├── posts/            # Markdown 源文件目录
│   └── *.md
├── templates/
│   └── page.html     # HTML 模板
├── static/
│   └── style.css     # 样式表
├── output/           # 生成的 HTML 输出
└── venv/             # Python 虚拟环境
```

## 安装

1. 创建虚拟环境（如需要）:
   ```bash
   python3.13 -m venv venv
   ```

2. 激活虚拟环境:
   ```bash
   source venv/bin/activate
   ```

3. 安装依赖:
   ```bash
   venv/bin/pip install markdown
   ```

## 使用方法

### 转换目录下所有 Markdown 文件

```bash
venv/bin/python blog.py posts/
```

### 转换单个文件

```bash
venv/bin/python blog.py posts/hello-world.md
```

### 指定输出目录

```bash
venv/bin/python blog.py posts/ -o my-output/
```

## Markdown 文件格式

支持标准的 Markdown 语法，并可以通过前置元数据添加标题和日期：

```markdown
---
title: 文章标题
date: 2024-01-01
---

# 正文内容

这里是正文内容...
```

## 生成的 HTML

生成的 HTML 文件保存在 `output/` 目录，包含：

- `index.html` - 文章索引页
- `*.html` - 各篇文章的 HTML 文件

## 样式说明

样式表参考 ESR 网站风格，主要特点：

- 字体: Helvetica, PingFang SC, Microsoft YaHei
- 配色: 灰白标题栏，黑色文字，白色背景
- 布局: 顶部标题栏 + 左侧菜单 + 右侧内容区

## 依赖

- Python 3.13+
- markdown 库

## 许可

MIT License
