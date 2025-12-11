# PDF Reader - 可执行应用程序构建指南

## 📋 概述

本指南将帮助你将 PDF Reader GUI 应用打包成可在 PC 上双击运行的可执行文件，支持 Windows、Linux 和 macOS。

## 🎯 支持的平台

- ✅ **Windows 7/10/11** (32-bit 和 64-bit)
- ✅ **Linux** (Ubuntu, Debian, Fedora, etc.)
- ✅ **macOS** (10.13+)

## 📦 打包工具

### 使用的工具

| 工具 | 版本 | 用途 |
|------|------|------|
| **PyInstaller** | 6.0+ | 将 Python 代码转换为可执行文件 |
| **PyQt5** | 5.15+ | GUI 框架 |
| **Python** | 3.8+ | 运行时环境 |

### 工作原理

```
Python 源代码
    ↓
PyInstaller 分析依赖
    ↓
编译字节码
    ↓
收集所有依赖库
    ↓
打包为独立可执行文件
    ↓
可直接运行的应用 (无需 Python 安装)
```

## 🚀 快速开始

### Windows 用户

#### 方法 1: 使用批处理文件 (推荐)

```bash
# 在项目根目录打开 PowerShell 或 CMD
cd C:\path\to\pdfReader
build_executable.bat
```

**步骤**:
1. 双击 `build_executable.bat`
2. 等待构建完成 (通常 2-5 分钟)
3. 可执行文件将生成在 `dist\PDFReader\PDFReader.exe`

#### 方法 2: 手动构建

```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate.bat

# 2. 安装依赖
pip install PyInstaller
pip install -e .

# 3. 构建
pyinstaller --name="PDFReader" --onedir --windowed ^
    --hidden-import=PyQt5 ^
    --hidden-import=pymupdf ^
    --hidden-import=pdfplumber ^
    --hidden-import=PIL ^
    --hidden-import=pypdf ^
    --collect-all PyQt5 ^
    src/pdf_reader/gui.py
```

### Linux/macOS 用户

```bash
# 1. 进入项目目录
cd /path/to/pdfReader

# 2. 赋予执行权限
chmod +x build_executable.sh

# 3. 运行构建脚本
./build_executable.sh
```

**步骤**:
1. 终端运行脚本
2. 等待构建完成
3. 可执行文件将生成在 `dist/PDFReader/PDFReader`

## 📂 构建后的文件结构

```
pdfReader/
├── dist/
│   └── PDFReader/
│       ├── PDFReader.exe          (Windows)
│       ├── PDFReader              (Linux/macOS)
│       ├── PyQt5/
│       ├── PIL/
│       ├── pymupdf/
│       └── ... (所有依赖库)
└── build/
    └── (构建临时文件)
```

## 🔧 配置选项

### PyInstaller 参数说明

| 参数 | 说明 | 值 |
|------|------|-----|
| `--name` | 应用名称 | PDFReader |
| `--onedir` | 生成单独目录 | (推荐) |
| `--windowed` | 隐藏控制台窗口 | (GUI 应用) |
| `--icon` | 应用图标文件 | icon.ico |
| `--hidden-import` | 隐藏导入的模块 | PyQt5, pymupdf 等 |
| `--collect-all` | 收集所有子模块 | PyQt5 |

### 自定义选项

#### 添加应用图标

```bash
# 1. 准备 icon.ico 文件 (Windows)
#    或 icon.icns 文件 (macOS)

# 2. 将图标放在项目根目录

# 3. 构建时自动包含:
pyinstaller --icon=icon.ico ...
```

#### 改变应用名称

```bash
# 修改 --name 参数
pyinstaller --name="MyPDFReader" ...
```

#### 单个可执行文件 (不推荐)

```bash
# 使用 --onefile 而不是 --onedir
# 优点: 单个文件
# 缺点: 启动慢，首次运行需要解压
pyinstaller --onefile ...
```

## ⚙️ 高级配置

### 创建自定义 spec 文件

```python
# pdf_reader_gui.spec

from PyInstaller.utils.hooks import get_module_collection_mode
import sys
import os

block_cipher = None

a = Analysis(
    ['src/pdf_reader/gui.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
        'pymupdf', 'pdfplumber', 'PIL', 'pypdf'
    ],
    # ... 更多配置
)
```

使用 spec 文件构建:

```bash
pyinstaller pdf_reader_gui.spec
```

### 代码签名 (可选)

#### Windows

```bash
# 使用 Microsoft Authenticode 签名
signtool sign /f certificate.pfx /p password /tr http://timestamp.server.com ^
    dist\PDFReader\PDFReader.exe
```

#### macOS

```bash
# 使用 Apple 开发证书签名
codesign --deep --force --verify --verbose --sign "Developer ID Application" \
    dist/PDFReader/PDFReader
```

## 🚀 运行应用

### Windows

#### 方式 1: 直接双击

```
dist\PDFReader\PDFReader.exe
```

#### 方式 2: 命令行运行

```bash
dist\PDFReader\PDFReader.exe
```

#### 方式 3: 创建桌面快捷方式

1. 右键 `dist\PDFReader\PDFReader.exe`
2. 选择 "创建快捷方式"
3. 移动快捷方式到桌面
4. 双击快捷方式运行

### Linux

#### 方式 1: 直接运行

```bash
./dist/PDFReader/PDFReader
```

#### 方式 2: 创建桌面快捷方式

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

# 使桌面快捷方式可执行
chmod +x ~/.local/share/applications/pdfreader.desktop
```

或在文件管理器中创建快捷方式：
1. 打开文件管理器
2. 导航到 `dist/PDFReader/`
3. 右键 `PDFReader` → 创建链接
4. 移动链接到桌面

### macOS

#### 方式 1: 直接运行

```bash
./dist/PDFReader/PDFReader
```

#### 方式 2: 创建应用包 (可选)

```bash
# 创建 macOS 应用包结构
mkdir -p PDFReader.app/Contents/{MacOS,Resources}
cp dist/PDFReader/PDFReader PDFReader.app/Contents/MacOS/
cp icon.icns PDFReader.app/Contents/Resources/
```

然后在 Spotlight 中搜索 "PDFReader" 运行。

## 📊 文件大小

| 平台 | 大小 | 说明 |
|------|------|------|
| Windows | 100-150 MB | 包含所有 Python 和库文件 |
| Linux | 80-120 MB | 较小的 Python 运行时 |
| macOS | 90-130 MB | 包含框架和库 |

**优化方法**:
- 使用 `--onedir` 而不是 `--onefile` 可减小启动时间
- 移除不必要的模块可减小大小
- 使用 UPX 压缩可进一步减小 (可选)

## 🔍 故障排查

### 问题 1: "缺少依赖模块" 错误

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
# 添加到 hidden-import
pyinstaller --hidden-import=module_name ...
```

### 问题 2: PyQt5 相关错误

**症状**: `ImportError: cannot import name 'QApplication'`

**解决**:
```bash
# 确保收集了完整的 PyQt5
pyinstaller --collect-all PyQt5 ...
```

### 问题 3: 应用无法找到数据文件

**症状**: 图标或资源文件加载失败

**解决**:
```bash
# 添加数据文件
pyinstaller --add-data="src/pdf_reader:pdf_reader" ...
```

### 问题 4: 在某些 Windows 版本上运行失败

**症状**: "应用无法启动" 或依赖库加载错误

**解决**:
```bash
# 1. 更新 Python 到最新版本
# 2. 重新安装所有依赖
pip install --upgrade PyQt5 pymupdf pdfplumber

# 3. 重新构建
pyinstaller ...
```

### 问题 5: 性能问题 (启动慢)

**症状**: 应用启动需要 10+ 秒

**解决**:
- 使用 `--onedir` (已默认)
- 移除不必要的模块
- 增加可用 RAM
- 检查磁盘 I/O

## 📝 最佳实践

### 1. 定期更新依赖

```bash
pip install --upgrade PyQt5 pymupdf pdfplumber pypdf
```

### 2. 在多个系统上测试

- Windows 7/10/11
- Linux (Ubuntu, Fedora)
- macOS 10.13+

### 3. 版本控制

```bash
# 在 pyproject.toml 中维护版本
[project]
version = "1.0.0"
```

### 4. 发布检查清单

- [ ] 在目标平台上测试
- [ ] 检查文件大小合理
- [ ] 验证所有功能正常
- [ ] 更新版本号
- [ ] 准备更新日志

## 📦 发布和分发

### 创建安装程序 (Windows)

使用 NSIS 创建 Windows 安装程序:

```bash
# 1. 安装 NSIS
# 2. 创建 installer.nsi
# 3. 运行 NSIS 生成 .exe 安装程序
```

### 创建 DMG 包 (macOS)

```bash
hdiutil create -volname "PDF Reader" -srcfolder dist/PDFReader \
    -ov -format UDZO pdfreader.dmg
```

### 创建 deb 包 (Linux)

```bash
# 使用 fpm 工具
fpm -s dir -t deb -n pdfreader -v 1.0.0 \
    -C dist/PDFReader -a x86_64
```

## 🎉 完成!

现在你已经拥有一个可以在任何 PC 上运行的独立应用程序，无需安装 Python 或任何依赖库。

### 下一步

1. **创建快捷方式** - 放在桌面或开始菜单
2. **分享应用** - 分发给其他用户
3. **收集反馈** - 改进应用功能
4. **定期更新** - 修复 bug，添加新功能

---

## 📞 常见问题

**Q: 为什么可执行文件这么大?**  
A: 包含了完整的 Python 运行时和所有依赖库。使用 `--onedir` 可以部分共享库文件。

**Q: 能否进一步减小文件大小?**  
A: 可以移除不必要的依赖，如 matplotlib、numpy 等。

**Q: 我能否修改源代码后重新构建?**  
A: 可以，直接运行构建脚本即可。

**Q: 可执行文件安全吗?**  
A: 可以添加代码签名以增加安全性。

**Q: 如何自动检查更新?**  
A: 可以添加版本检查机制，定期提示用户更新。

---

**版本**: 1.0.0  
**最后更新**: 2025-12-11
