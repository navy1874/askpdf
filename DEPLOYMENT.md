# PDF Reader - 应用程序打包和部署完全指南

## 📋 目录

1. [快速开始](#快速开始)
2. [详细构建步骤](#详细构建步骤)
3. [运行应用](#运行应用)
4. [故障排查](#故障排查)
5. [高级配置](#高级配置)
6. [发布分发](#发布分发)

---

## 🚀 快速开始

### 最简单的方法 - 使用 Python 构建脚本

#### Windows

```bash
# 方式 1: 双击 build_executable.bat
build_executable.bat

# 方式 2: 在 PowerShell 或 CMD 中运行
python build.py
```

#### Linux/macOS

```bash
# 方式 1: 使用 Bash 脚本
chmod +x build_executable.sh
./build_executable.sh

# 方式 2: 使用 Python 脚本
python3 build.py
```

### 等待构建完成

构建时间通常为 2-5 分钟，取决于你的系统性能。

### 运行应用

构建完成后，可执行文件位置：

- **Windows**: `dist\PDFReader\PDFReader.exe`
- **Linux**: `dist/PDFReader/PDFReader`
- **macOS**: `dist/PDFReader/PDFReader`

---

## 🔧 详细构建步骤

### 前置要求

```
✓ Python 3.8 或更高版本
✓ pip 包管理器
✓ 网络连接 (用于下载依赖)
✓ 至少 2 GB 可用磁盘空间
✓ 50+ MB 的 RAM
```

### 步骤 1: 准备环境

#### Windows (PowerShell 或 CMD)

```bash
# 打开项目目录
cd C:\path\to\pdfReader

# 验证 Python 版本
python --version

# 如果版本低于 3.8，请从 https://www.python.org 下载
```

#### Linux/macOS (终端)

```bash
# 打开项目目录
cd /path/to/pdfReader

# 验证 Python 版本
python3 --version

# 如果未安装 Python，使用包管理器安装
# Ubuntu/Debian:
# sudo apt-get install python3.8 python3-pip

# macOS:
# brew install python@3.8
```

### 步骤 2: 选择构建方法

#### 方法 A: 自动构建脚本 (推荐)

最简单且最可靠的方法。

**Windows**:
```bash
# 使用批处理文件
build_executable.bat

# 或使用 Python 脚本
python build.py
```

**Linux/macOS**:
```bash
chmod +x build_executable.sh
./build_executable.sh

# 或使用 Python 脚本
python3 build.py
```

#### 方法 B: 手动步骤

对于需要完全控制的高级用户。

**Windows**:
```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate.bat

# 3. 升级 pip
python -m pip install --upgrade pip

# 4. 安装 PyInstaller
pip install PyInstaller

# 5. 安装项目依赖
pip install -e .

# 6. 构建应用
pyinstaller --name=PDFReader --onedir --windowed ^
    --hidden-import=PyQt5 ^
    --hidden-import=pymupdf ^
    --hidden-import=pdfplumber ^
    --hidden-import=PIL ^
    --hidden-import=pypdf ^
    --collect-all PyQt5 ^
    src/pdf_reader/gui.py
```

**Linux/macOS**:
```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 升级 pip
python -m pip install --upgrade pip

# 4. 安装 PyInstaller
pip install PyInstaller

# 5. 安装项目依赖
pip install -e .

# 6. 构建应用
pyinstaller --name=PDFReader --onedir --windowed \
    --hidden-import=PyQt5 \
    --hidden-import=pymupdf \
    --hidden-import=pdfplumber \
    --hidden-import=PIL \
    --hidden-import=pypdf \
    --collect-all PyQt5 \
    src/pdf_reader/gui.py
```

### 步骤 3: 验证构建结果

检查可执行文件是否生成：

**Windows**:
```bash
dir dist\PDFReader\PDFReader.exe
```

**Linux/macOS**:
```bash
ls -lh dist/PDFReader/PDFReader
```

---

## ▶️ 运行应用

### Windows

#### 方式 1: 直接双击

导航到 `dist\PDFReader\` 目录，双击 `PDFReader.exe` 文件。

#### 方式 2: 命令行

```bash
dist\PDFReader\PDFReader.exe
```

#### 方式 3: 创建桌面快捷方式

1. 打开 `dist\PDFReader\` 文件夹
2. 右键点击 `PDFReader.exe`
3. 选择 "创建快捷方式"
4. 将快捷方式移动到桌面

#### 方式 4: 添加到开始菜单

1. 右键点击 `PDFReader.exe`
2. 选择 "固定到开始菜单"

### Linux

#### 方式 1: 直接运行

```bash
./dist/PDFReader/PDFReader
```

#### 方式 2: 添加到 PATH (全局可访问)

```bash
# 创建符号链接
sudo ln -s $(pwd)/dist/PDFReader/PDFReader /usr/local/bin/pdfreader

# 然后可以在任何地方运行
pdfreader
```

#### 方式 3: 创建桌面快捷方式

```bash
# 创建 .desktop 文件
cat > ~/.local/share/applications/pdfreader.desktop << EOF
[Desktop Entry]
Type=Application
Name=PDF Reader
Comment=PDF Reading and Management Tool
Exec=$(pwd)/dist/PDFReader/PDFReader
Icon=$(pwd)/icon.png
Terminal=false
Categories=Office;Utility;
EOF

# 使其可执行
chmod +x ~/.local/share/applications/pdfreader.desktop

# 更新应用数据库
update-desktop-database ~/.local/share/applications
```

### macOS

#### 方式 1: 直接运行

```bash
./dist/PDFReader/PDFReader
```

#### 方式 2: 在 Spotlight 中搜索

```bash
# 将应用移动到 Applications 文件夹
mv dist/PDFReader/PDFReader /Applications/PDFReader.app

# 然后可以在 Spotlight 中搜索和启动
```

---

## 🐛 故障排查

### 问题 1: 构建失败 - "缺少模块"

**错误信息**:
```
ERROR: module 'PyQt5' not found
```

**解决方案**:
```bash
# 方式 1: 清理并重新构建
rm -rf build dist venv  # Linux/macOS
rmdir /s build dist venv  # Windows
python build.py  # 重新构建

# 方式 2: 手动安装缺失的模块
pip install PyQt5 pymupdf pdfplumber
```

### 问题 2: PyInstaller 未安装

**错误信息**:
```
No module named pyinstaller
```

**解决方案**:
```bash
pip install PyInstaller
python build.py
```

### 问题 3: 权限拒绝 (Linux/macOS)

**错误信息**:
```
Permission denied: './build_executable.sh'
```

**解决方案**:
```bash
chmod +x build_executable.sh
./build_executable.sh
```

### 问题 4: 应用无法启动

**症状**: 双击可执行文件无反应

**解决方案**:

1. **检查依赖库**:
```bash
# Windows
dumpbin /dependents dist\PDFReader\PDFReader.exe

# Linux
ldd dist/PDFReader/PDFReader

# macOS
otool -L dist/PDFReader/PDFReader
```

2. **从命令行运行查看错误**:
```bash
# Windows
dist\PDFReader\PDFReader.exe
# 观察输出信息

# Linux/macOS
./dist/PDFReader/PDFReader
# 观察输出信息
```

3. **重新构建**:
```bash
python build.py
```

### 问题 5: 应用启动很慢

**症状**: 点击后需要 10+ 秒才能打开

**原因**: PyInstaller 需要解压依赖库

**解决方案**:
- 这是正常行为，首次启动会较慢
- 后续启动会更快
- 可以预加载应用来改进用户体验

### 问题 6: 应用很大 (100+ MB)

**症状**: 可执行文件占用很多空间

**原因**: 包含完整的 Python 运行时和所有库

**解决方案**:
- 这是预期的大小
- 可以压缩后分发
- 或使用 `--onefile` 创建单个文件 (但启动较慢)

---

## ⚙️ 高级配置

### 自定义应用图标

1. **准备图标文件**:
   - Windows: `icon.ico` (256×256 像素)
   - macOS: `icon.icns`
   - Linux: `icon.png` (可选)

2. **放在项目根目录**:
```
pdfReader/
├── icon.ico
├── build_executable.bat
└── ...
```

3. **自动包含** (构建脚本会自动检测)
```bash
python build.py
# 脚本会自动检测 icon.ico 并包含它
```

或手动指定:
```bash
pyinstaller --icon=icon.ico ...
```

### 自定义应用名称

编辑 `build.py` 或构建脚本中的 `--name=PDFReader` 参数：

```bash
pyinstaller --name=MyCustomName ...
```

### 添加启动屏幕

可以在 `gui.py` 中的 `PDFReaderGUI.__init__()` 方法中添加：

```python
def __init__(self):
    super().__init__()
    # ... 现有代码 ...
    
    # 显示启动屏幕
    self.show_splash_screen()
```

### 包含额外数据文件

如果需要包含数据文件：

```bash
pyinstaller --add-data="path/to/data:data" ...
```

---

## 📦 发布分发

### 创建压缩包分发

```bash
# Windows
# 使用 7-Zip, WinRAR 或 Windows 内置压缩功能
# 右键 dist/PDFReader → 发送到 → 压缩文件夹

# Linux/macOS
tar -czf PDFReader-linux.tar.gz dist/PDFReader/
zip -r PDFReader-windows.zip dist/PDFReader/
```

### 创建安装程序

#### Windows NSIS 安装程序

1. 下载安装 NSIS: https://nsis.sourceforge.io
2. 创建 `installer.nsi`:

```nsis
; installer.nsi
!include "MUI2.nsh"

Name "PDF Reader"
OutFile "PDFReaderSetup.exe"
InstallDir "$PROGRAMFILES\PDFReader"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\PDFReader\*.*"
  CreateDirectory "$SMPROGRAMS\PDF Reader"
  CreateShortcut "$SMPROGRAMS\PDF Reader\PDF Reader.lnk" "$INSTDIR\PDFReader.exe"
  CreateShortcut "$DESKTOP\PDF Reader.lnk" "$INSTDIR\PDFReader.exe"
SectionEnd

Section "Uninstall"
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\PDF Reader"
  Delete "$DESKTOP\PDF Reader.lnk"
SectionEnd
```

3. 使用 NSIS 编译：
```bash
makensis installer.nsi
```

### 发布到网站

1. 创建发布页面
2. 提供下载链接
3. 包含版本信息和更新日志
4. 提供使用说明

### 版本控制

在 `pyproject.toml` 中更新版本：

```toml
[project]
name = "pdf-reader-cli"
version = "1.0.0"  # 更新此处
```

---

## ✅ 检查清单

构建可执行文件前：

- [ ] Python 版本 >= 3.8
- [ ] 所有依赖已安装
- [ ] 项目代码无误
- [ ] 可选：准备了应用图标
- [ ] 磁盘空间 >= 2 GB
- [ ] 互联网连接良好

构建后：

- [ ] 可执行文件成功生成
- [ ] 应用可以成功启动
- [ ] 所有功能正常工作
- [ ] 文件大小合理
- [ ] 可以创建快捷方式
- [ ] 在多个系统上测试过

发布前：

- [ ] 更新版本号
- [ ] 编写更新日志
- [ ] 准备安装程序
- [ ] 最终测试
- [ ] 创建发布说明
- [ ] 准备下载链接

---

## 📞 常见问题

**Q: 我需要编译 C/C++ 代码吗?**  
A: 不需要，PyInstaller 会自动处理所有依赖。

**Q: 用户需要安装 Python 吗?**  
A: 不需要，可执行文件包含完整的 Python 运行时。

**Q: 可以在不同的操作系统上运行相同的可执行文件吗?**  
A: 不可以，每个操作系统都需要单独的可执行文件。

**Q: 如何更新应用?**  
A: 重新构建新版本，用户下载新版本即可。

**Q: 可以添加自动更新功能吗?**  
A: 可以，需要在应用中实现版本检查和更新逻辑。

---

## 🎉 完成

现在你拥有一个可以在任何 PC 上运行的独立应用程序！

### 下一步

1. 分享应用给其他用户
2. 收集反馈和建议
3. 定期发布更新
4. 改进应用功能

---

**最后更新**: 2025-12-11  
**版本**: 1.0.0
