# PyQt5 模块缺失问题 - 完全解决方案

## 📋 问题

```
ModuleNotFoundError: No module named 'PyQt5'
```

当尝试运行 `gui.py` 时出现此错误。

## ✅ 解决方案（已实施）

### 第 1 步：安装所有依赖包

所有必要的包已自动安装，包括：
- ✓ PyQt5 - GUI 框架
- ✓ pymupdf - PDF 处理
- ✓ pypdf - PDF 文档操作
- ✓ pdfplumber - PDF 内容提取
- ✓ Pillow - 图像处理
- ✓ typer - CLI 工具
- ✓ rich - 输出美化

### 第 2 步：验证安装

运行以下命令验证所有依赖是否已正确安装：

```bash
python check_dependencies.py
```

**预期输出：**
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

## 🚀 现在可以运行的方式

### 方式 1：直接运行 GUI 脚本

```bash
python src/pdf_reader/gui.py
```

### 方式 2：使用快速启动脚本（推荐）

```bash
start_gui.bat
```

此脚本会：
1. 自动检查依赖
2. 如果缺少依赖则给出提示
3. 启动 GUI 应用

### 方式 3：使用可执行程序

```bash
dist\PDFReader\PDFReader.exe
```

### 方式 4：使用启动脚本

```bash
run.bat
```

## 🛠️ 创建的辅助工具

| 文件 | 用途 |
|------|------|
| `check_dependencies.py` | 检查所有依赖是否已安装 |
| `install_dependencies.bat` | 一键安装所有依赖 |
| `start_gui.bat` | 启动 GUI 应用（检查依赖） |
| `run.bat` | 直接启动应用 |
| `DEPENDENCIES_SOLUTION.md` | 详细解决方案文档 |

## 💾 如果在新机器上使用

1. **首次安装依赖：**
   ```bash
   install_dependencies.bat
   ```

2. **日常运行应用：**
   ```bash
   start_gui.bat
   ```
   或
   ```bash
   dist\PDFReader\PDFReader.exe
   ```

## 🔄 重新安装依赖（如有问题）

如果遇到问题，可以强制重新安装：

```bash
python -m pip install --force-reinstall PyQt5 pymupdf pdfplumber pypdf Pillow typer rich
```

或使用脚本：

```bash
install_dependencies.bat
```

## 📦 从源代码开发

如果需要从 `pyproject.toml` 安装所有依赖：

```bash
pip install -e .
```

## ✨ 验证成功

已验证以下内容：
- ✓ PyQt5 已安装
- ✓ 所有 PyQt5 子模块可用（QtCore, QtGui, QtWidgets）
- ✓ 所有 PDF 处理库已安装
- ✓ GUI 主类可以正确导入
- ✓ main 函数可以正确导入
- ✓ 可执行程序已构建完成

## 🎉 现在您可以：

1. ✓ 直接双击 `PDFReader.exe` 运行应用
2. ✓ 使用 `start_gui.bat` 启动 GUI
3. ✓ 在任何 Windows 机器上运行应用
4. ✓ 继续开发和修改应用

---

**问题已完全解决！所有依赖都已正确安装。**
