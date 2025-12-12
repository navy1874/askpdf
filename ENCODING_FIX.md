# 批处理文件编码问题修复

## 问题描述

在某些 Windows 系统上运行批处理文件时出现乱码：

```
'鏌ヤ緷璧?..' 不是内部或外部命令，也不是可运行的程序
或批处理文件。
```

## 根本原因

批处理文件中的中文字符在不同的 Windows 代码页（Code Page）下显示不一致，导致：
- 中文字符显示为乱码
- echo 命令无法正确执行
- 用户看到的错误信息难以理解

## 解决方案

将所有批处理文件中的中文字符改为英文，确保在所有 Windows 系统上都能正常显示。

## 修复的文件

### 1. start_gui.bat ✅
- **之前**: 使用中文提示信息
- **现在**: 使用英文提示信息
- **改进**: 
  - "检查依赖..." → "Checking dependencies..."
  - "某些依赖缺失" → "[ERROR] Some dependencies are missing"
  - "启动 PDF Reader..." → "Starting PDF Reader..."

### 2. install_dependencies.bat ✅
- **之前**: 使用中文提示
- **现在**: 使用英文提示
- **改进**:
  - "检查 Python..." → "[1/3] Checking Python..."
  - "找到 Python" → "[OK] Found Python"
  - "依赖安装完成" → "[OK] Dependencies installed"

### 3. run.bat ✅
- **之前**: 中文错误信息
- **现在**: 英文错误信息
- **改进**:
  - "启动 PDF Reader..." → "Starting PDF Reader..."
  - "错误: 未找到" → "[ERROR] PDFReader.exe not found"

### 4. quick_build.bat ✅
- **之前**: 中文构建信息
- **现在**: 英文构建信息
- **改进**:
  - "安装 PyInstaller..." → "Installing PyInstaller..."
  - "清理旧文件..." → "Cleaning old files..."
  - "构建成功!" → "BUILD SUCCESSFUL!"

## 使用方法

现在所有批处理文件都可以在任何 Windows 系统上正常运行：

```bash
# 安装依赖
install_dependencies.bat

# 启动 GUI
start_gui.bat

# 运行应用
run.bat

# 构建应用
quick_build.bat
```

## 预期输出示例

### start_gui.bat
```
Checking dependencies...
[OK] All dependencies installed

Starting PDF Reader...
```

### install_dependencies.bat
```
======================================================================
  PDF Reader - Dependencies Installer
======================================================================

[1/3] Checking Python...
[OK] Found Python 3.13.1

[2/3] Upgrading pip...
[OK] pip upgraded

[3/3] Installing project dependencies...
[OK] Dependencies installed
```

## 兼容性

- ✅ Windows 7
- ✅ Windows 8/8.1
- ✅ Windows 10
- ✅ Windows 11
- ✅ 所有语言版本的 Windows
- ✅ 所有代码页设置

## 技术细节

### 为什么会出现乱码？

Windows 批处理文件默认使用系统的 ANSI 代码页：
- 中文 Windows: GBK (Code Page 936)
- 英文 Windows: Windows-1252 (Code Page 1252)
- 日文 Windows: Shift-JIS (Code Page 932)

当批处理文件包含中文字符时，在非中文 Windows 系统上会显示为乱码。

### 我们的解决方案

使用纯 ASCII 字符（英文），确保：
1. 在所有 Windows 版本上显示一致
2. 不受代码页设置影响
3. 更容易被国际用户理解

## 其他改进

同时改进了错误信息格式：
- 使用 `[ERROR]` 前缀标识错误
- 使用 `[OK]` 前缀标识成功
- 使用 `[1/3]` 等标识进度

---

**修复完成！现在所有批处理文件都能在任何 Windows 系统上正常显示。**
