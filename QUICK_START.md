# PDF Reader - 完整使用指南

## ✅ 当前状态

- ✓ **所有依赖已安装**
- ✓ **Python 环境正常** (3.13.1)
- ✓ **可执行程序已构建** (1.66 MB)
- ✓ **GUI 应用可运行**

## 🚀 快速开始

### 最简单的方式：双击运行

```
dist\PDFReader\PDFReader.exe
```

### 或使用脚本启动

```
run.bat          (最小化启动)
start_gui.bat    (检查依赖后启动)
```

## 📋 文件说明

### 可执行程序
- `dist\PDFReader\PDFReader.exe` - 主应用程序 (1.66 MB)
- `dist\PDFReader\_internal\` - 运行库和依赖

### 启动脚本
| 脚本 | 用途 |
|------|------|
| `run.bat` | 直接启动可执行程序 |
| `start_gui.bat` | 启动 GUI（检查依赖） |
| `quick_build.bat` | 重新构建可执行程序 |
| `install_dependencies.bat` | 安装/重装依赖 |

### Python 脚本
| 脚本 | 用途 |
|------|------|
| `check_dependencies.py` | 检查依赖安装情况 |
| `build_simple.py` | 简化的构建脚本 |
| `build.py` | 完整的构建脚本 |

### 文档
| 文档 | 内容 |
|------|------|
| `PYQT5_FIXED.md` | PyQt5 问题解决方案 |
| `BUILD_REPORT.md` | 构建完成报告 |
| `BUILD_SUCCESS.md` | 构建成功说明 |
| `DEPENDENCIES_SOLUTION.md` | 依赖问题详解 |

## 🔍 问题诊断

### 检查依赖是否安装

```bash
python check_dependencies.py
```

### 如果依赖缺失

```bash
install_dependencies.bat
```

或手动安装：

```bash
python -m pip install PyQt5 pymupdf pdfplumber pypdf Pillow typer rich
```

## 💡 不同场景的使用

### 场景 1: 日常使用（推荐）
```
双击 dist\PDFReader\PDFReader.exe
```
或
```
双击 run.bat
```

### 场景 2: 开发调试
```bash
python src/pdf_reader/gui.py
```

### 场景 3: 命令行使用
```bash
python -m pdf_reader.cli --help
```

### 场景 4: 分发给其他用户
1. 复制整个 `dist\PDFReader` 文件夹
2. 用户可以直接双击 `PDFReader.exe` 运行
3. 无需安装 Python，无需任何额外配置

## 🛠️ 开发流程

### 修改源代码后

1. **测试代码：**
   ```bash
   python src/pdf_reader/gui.py
   ```

2. **重新构建可执行程序：**
   ```bash
   quick_build.bat
   ```

3. **验证构建结果：**
   ```bash
   dist\PDFReader\PDFReader.exe
   ```

## 📦 项目结构

```
pdfReader/
├── dist/
│   └── PDFReader/
│       ├── PDFReader.exe          ← 可执行程序
│       └── _internal/             ← 依赖库
├── src/
│   └── pdf_reader/
│       ├── gui.py                 ← GUI 应用
│       ├── cli.py                 ← CLI 工具
│       └── app.py                 ← 核心逻辑
├── build/                         ← 构建临时文件
├── run.bat                        ← 快速启动
├── start_gui.bat                  ← GUI 启动
├── quick_build.bat                ← 快速构建
├── check_dependencies.py          ← 依赖检查
└── ...
```

## ✨ 系统要求

| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 7 及以上 |
| **Python** | 3.8 或更高版本 |
| **磁盘空间** | 200 MB（完整程序）|
| **依赖** | PyQt5, pymupdf, pypdf, pdfplumber, Pillow, typer, rich |

## 🔐 故障排除

### 问题：应用无法启动

**解决方案：**
```bash
python check_dependencies.py
```

如果有缺失的模块：
```bash
install_dependencies.bat
```

### 问题：构建失败

**解决方案：**
1. 清理旧文件：
   ```bash
   rmdir /s dist build
   ```
2. 重新构建：
   ```bash
   quick_build.bat
   ```

### 问题：导入错误

**解决方案：**
```bash
python -m pip install --upgrade PyQt5 pymupdf pdfplumber pypdf Pillow
```

## 📞 支持信息

- **项目仓库**: https://github.com/navy1874/askpdf
- **构建工具**: PyInstaller 6.17.0
- **GUI 框架**: PyQt5
- **PDF 库**: pymupdf, pypdf, pdfplumber

---

## 🎉 总结

PDF Reader 已完全准备就绪：
1. ✓ 所有依赖已安装
2. ✓ 可执行程序已生成
3. ✓ 启动脚本已创建
4. ✓ 诊断工具已提供

**现在就可以使用了！双击 `PDFReader.exe` 或 `run.bat` 开始！**

---

*最后更新: 2025年12月11日*
