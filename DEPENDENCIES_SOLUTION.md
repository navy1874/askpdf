# PyQt5 ModuleNotFoundError 解决方案

## 问题描述

```
ModuleNotFoundError: No module named 'PyQt5'
```

## 根本原因

PyQt5 和其他 GUI 相关的依赖包未在当前 Python 环境中安装。

## ✅ 解决方案

### 自动安装所有依赖

运行以下命令安装所有必需的包：

```bash
python -m pip install PyQt5 pymupdf pdfplumber pypdf Pillow typer rich
```

### 使用 pip 安装项目及其依赖

```bash
pip install -e .
```

这会根据 `pyproject.toml` 安装所有定义的依赖。

## 🔍 验证安装

运行依赖检查脚本来验证所有必要的模块是否已正确安装：

```bash
python check_dependencies.py
```

预期输出：
```
✓ PyQt5                - 已安装
✓ PyQt5.QtCore         - 已安装
✓ PyQt5.QtGui          - 已安装
✓ pymupdf              - 已安装
✓ pypdf                - 已安装
✓ pdfplumber           - 已安装
✓ Pillow               - 已安装
✓ typer                - 已安装
✓ rich                 - 已安装

✓ 所有依赖已安装 (9/9)
```

## 📦 已安装的模块详情

| 模块 | 用途 |
|------|------|
| **PyQt5** | GUI 框架 |
| **pymupdf** | PDF 读取和处理 |
| **pypdf** | PDF 文档操作 |
| **pdfplumber** | PDF 内容提取 |
| **Pillow** | 图像处理 |
| **typer** | CLI 命令行工具 |
| **rich** | 命令行输出美化 |

## 🚀 运行 GUI 应用

依赖安装完成后，可以运行 GUI 应用：

```bash
# 方法 1: 直接运行 Python 脚本
python src/pdf_reader/gui.py

# 方法 2: 使用已编译的可执行文件
dist\PDFReader\PDFReader.exe

# 方法 3: 使用启动脚本
run.bat
```

## 🛠️ 环境信息

- **Python 版本**: 3.13.1
- **操作系统**: Windows
- **包管理器**: pip

## 📋 常见问题

### Q: 为什么会出现 ModuleNotFoundError？
**A**: 可能原因：
1. 依赖包未安装
2. 使用了错误的 Python 版本
3. 虚拟环境未激活
4. 使用了不同的 Python 环境

### Q: 如何重新安装所有依赖？
**A**: 
```bash
pip install -e . --force-reinstall
```

### Q: 为什么 PyInstaller 构建成功但运行时出错？
**A**: 这通常是因为在运行源代码时缺少依赖，而 PyInstaller 构建时这些依赖已经被打包了。确保在运行 GUI 前安装了所有依赖。

---

## ✅ 现在您可以：

1. ✓ 直接运行 GUI 应用
2. ✓ 使用 CLI 工具
3. ✓ 重新构建可执行程序
4. ✓ 开发和修改应用

祝您使用愉快！
