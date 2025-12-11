# PDF Reader - 可执行应用程序构建指南

> 将 Python GUI 应用打包成可在 Windows、Linux 和 macOS 上双击运行的独立应用

## 📋 项目概况

本项目提供了完整的工具和脚本，将 PDF Reader GUI 应用转换为可执行程序。

### 支持平台

| 平台 | 支持 | 方式 |
|------|------|------|
| Windows 7/10/11 | ✅ | 双击 `.exe` |
| Linux (Ubuntu/Debian/Fedora) | ✅ | 直接运行 |
| macOS (10.13+) | ✅ | 直接运行 |

### 文件大小

| 平台 | 大小 | 说明 |
|------|------|------|
| Windows | 100-150 MB | 包含 Python 和 PyQt5 |
| Linux | 80-120 MB | 较小的运行时 |
| macOS | 90-130 MB | 包含框架库 |

---

## 🚀 快速开始 (3 分钟)

### Windows

```bash
# 方式 1: 双击脚本
build_executable.bat

# 方式 2: 命令行
python build.py
```

### Linux/macOS

```bash
chmod +x build_executable.sh
./build_executable.sh

# 或
python3 build.py
```

**等待 2-5 分钟构建完成，然后运行:**

- Windows: `dist\PDFReader\PDFReader.exe`
- Linux: `dist/PDFReader/PDFReader`
- macOS: `dist/PDFReader/PDFReader`

---

## 📚 详细文档

| 文档 | 内容 |
|------|------|
| [BUILD_GUIDE.md](BUILD_GUIDE.md) | 完整的构建配置指南 |
| [DEPLOYMENT.md](DEPLOYMENT.md) | 部署和发布指南 |

---

## 🛠️ 可用工具

### 1. 自动构建脚本 (推荐)

#### Windows
```bash
build_executable.bat
```
- 自动处理所有步骤
- 中文提示信息
- 包括进度显示

#### Linux/macOS
```bash
chmod +x build_executable.sh
./build_executable.sh
```
- 自动化构建流程
- 清晰的步骤提示
- 错误检查

### 2. Python 构建脚本

```bash
python build.py  # Windows
python3 build.py  # Linux/macOS
```

功能：
- ✅ 自动创建虚拟环境
- ✅ 自动安装依赖
- ✅ 自动清理旧文件
- ✅ 自动构建
- ✅ 结果验证
- ✅ 详细的进度报告

### 3. PyInstaller 直接使用

高级用户可以直接使用 PyInstaller：

```bash
pyinstaller --name=PDFReader --onedir --windowed \
    --hidden-import=PyQt5 \
    --hidden-import=pymupdf \
    --hidden-import=pdfplumber \
    --hidden-import=PIL \
    --hidden-import=pypdf \
    --collect-all PyQt5 \
    src/pdf_reader/gui.py
```

---

## 📁 项目结构

```
pdfReader/
├── src/
│   └── pdf_reader/
│       ├── gui.py              # 主 GUI 程序
│       ├── cli.py              # CLI 程序
│       └── __init__.py
├── build.py                     # Python 构建脚本
├── build_executable.bat         # Windows 构建脚本
├── build_executable.sh          # Linux/macOS 构建脚本
├── pdf_reader_gui.spec          # PyInstaller 配置文件
├── BUILD_GUIDE.md               # 构建指南
├── DEPLOYMENT.md                # 部署指南
├── pyproject.toml               # 项目配置
└── dist/                        # 构建输出
    └── PDFReader/
        ├── PDFReader.exe        # (Windows)
        ├── PDFReader            # (Linux/macOS)
        └── ... (依赖库)
```

---

## ⚙️ 系统要求

### 构建时需要

```
✓ Python 3.8 或更高
✓ pip 包管理器
✓ 2+ GB 空闲磁盘空间
✓ 网络连接 (下载依赖)
```

### 运行时需要

```
✓ 无需 Python
✓ 无需其他库
✓ 完全独立
```

---

## 🔧 如何使用

### 第一次构建

1. **准备环境**:
```bash
cd /path/to/pdfReader
```

2. **运行构建脚本**:
   - Windows: 双击 `build_executable.bat`
   - Linux/macOS: `./build_executable.sh`

3. **等待完成** (2-5 分钟)

4. **测试应用**:
   - Windows: 双击 `dist\PDFReader\PDFReader.exe`
   - Linux/macOS: `./dist/PDFReader/PDFReader`

### 后续构建

修改代码后只需重新运行构建脚本即可。

### 创建快捷方式

#### Windows
1. 右键 `dist\PDFReader\PDFReader.exe`
2. 选择"创建快捷方式"
3. 移动到桌面或开始菜单

#### Linux
```bash
# 创建桌面快捷方式
ln -s $(pwd)/dist/PDFReader/PDFReader ~/Desktop/PDFReader

# 或添加到应用菜单
cat > ~/.local/share/applications/pdfreader.desktop << EOF
[Desktop Entry]
Type=Application
Name=PDF Reader
Exec=$(pwd)/dist/PDFReader/PDFReader
Terminal=false
Categories=Office;
EOF
```

#### macOS
```bash
# 移动到应用程序文件夹
cp -r dist/PDFReader/PDFReader /Applications/PDFReader.app
```

---

## 📊 构建输出

成功构建后的目录结构：

```
dist/
└── PDFReader/
    ├── PDFReader.exe            (Windows)
    ├── PDFReader                (Linux/macOS)
    ├── _internal/               (依赖库目录)
    │   ├── PyQt5/
    │   ├── PIL/
    │   ├── pymupdf/
    │   └── ... (其他库)
    └── ... (其他文件)
```

### 文件大小

- `PDFReader.exe` (Windows): ~5-10 MB
- `PDFReader` (Linux/macOS): ~5-10 MB
- `_internal/` 目录: ~90-140 MB
- **总大小**: 100-150 MB

---

## 🐛 故障排查

### 最常见的问题

| 问题 | 解决方案 |
|------|--------|
| 找不到 Python | 检查 Python 是否已安装，使用 `python --version` 验证 |
| 权限拒绝 | 运行 `chmod +x build_executable.sh` |
| 缺少模块 | 删除 `venv` 文件夹，重新运行脚本 |
| 构建失败 | 检查网络连接，删除 `build`、`dist` 文件夹，重试 |

更详细的故障排查见 [DEPLOYMENT.md](DEPLOYMENT.md#-故障排查)

---

## ✨ 特性

### 构建脚本特性

- ✅ **完全自动化** - 一键构建
- ✅ **跨平台** - Windows、Linux、macOS
- ✅ **进度显示** - 清晰的步骤提示
- ✅ **错误检查** - 自动验证结果
- ✅ **虚拟环境** - 隔离的 Python 环境
- ✅ **依赖管理** - 自动安装所有依赖
- ✅ **清理机制** - 自动清理旧文件
- ✅ **优化输出** - 小文件大小，快速启动

### 应用特性

- 📱 **跨平台 GUI** - 基于 PyQt5
- 🎨 **现代界面** - 美观的分割面板
- ⚡ **高效性能** - 快速加载和响应
- 🔧 **完整功能** - PDF 阅读、管理、分析
- 🖼️ **图片支持** - 多种图片格式
- 📊 **智能缩放** - 智能的图片到 PDF 转换

---

## 📖 进阶配置

### 自定义应用图标

在项目根目录放置 `icon.ico` 文件：

```
pdfReader/
├── icon.ico              # 256×256 像素
└── build_executable.bat
```

脚本会自动检测并包含。

### 自定义应用名称

编辑构建脚本中的 `--name` 参数：

```bash
# 在 build_executable.bat 中修改
pyinstaller --name="MyCustomName" ...
```

### 单个文件可执行文件

使用 `--onefile` 而不是 `--onedir`：

```bash
pyinstaller --name=PDFReader --onefile ...
```

优缺点：
- ✅ 单个文件，易于分发
- ❌ 启动较慢
- ❌ 文件更大

---

## 📦 分发和发布

### 创建压缩包

```bash
# Windows
7z a PDFReader-win64.7z dist\PDFReader\

# Linux
tar -czf PDFReader-linux.tar.gz dist/PDFReader/

# macOS
zip -r PDFReader-macos.zip dist/PDFReader/
```

### 创建安装程序

- **Windows**: 使用 NSIS (见 [DEPLOYMENT.md](DEPLOYMENT.md))
- **Linux**: 创建 deb/rpm 包
- **macOS**: 创建 DMG 文件

### 发布到网站

提供下载链接，包括：
- 应用版本号
- 发布日期
- 更新说明
- 系统要求
- 使用说明

---

## 🎯 最佳实践

### 开发流程

1. 在源代码中测试
2. 确认功能无误
3. 更新版本号
4. 运行构建脚本
5. 测试可执行文件
6. 创建发布包
7. 发布到网站

### 版本管理

在 `pyproject.toml` 中维护版本：

```toml
[project]
version = "1.0.0"
```

### 更新日志

维护 `CHANGELOG.md` 记录所有更改。

---

## 💡 常见问题

**Q: 为什么文件这么大 (100+ MB)?**  
A: 包含完整的 Python 运行时和所有依赖库。

**Q: 能否在 USB 上运行?**  
A: 可以，复制整个 `dist/PDFReader/` 目录即可。

**Q: 如何自动检查更新?**  
A: 可以在应用中添加版本检查机制。

**Q: 可以修改源代码后立即测试?**  
A: 可以，重新运行构建脚本即可。

**Q: 是否安全?**  
A: 代码完全开源，可以添加数字签名增强安全性。

---

## 📞 获取帮助

### 常见问题

详见 [DEPLOYMENT.md - 常见问题](DEPLOYMENT.md#-常见问题) 部分

### 错误排查

详见 [DEPLOYMENT.md - 故障排查](DEPLOYMENT.md#-故障排查) 部分

### 高级配置

详见 [BUILD_GUIDE.md - 高级配置](BUILD_GUIDE.md#-高级配置) 部分

---

## 📋 检查清单

### 构建前

- [ ] Python 版本 >= 3.8
- [ ] 网络连接正常
- [ ] 磁盘空间 >= 2 GB
- [ ] 代码测试无误

### 构建中

- [ ] 运行构建脚本
- [ ] 等待完成
- [ ] 检查输出

### 构建后

- [ ] 可执行文件存在
- [ ] 应用可以启动
- [ ] 所有功能正常
- [ ] 可以创建快捷方式

### 发布前

- [ ] 在多个系统上测试
- [ ] 更新版本号
- [ ] 编写更新说明
- [ ] 准备安装程序
- [ ] 创建快速启动指南

---

## 🎉 完成

现在你拥有一个可以在任何 PC 上运行的独立应用程序！

### 下一步

1. 分享应用给其他用户
2. 收集用户反馈
3. 定期发布更新
4. 不断改进功能

---

**最后更新**: 2025-12-11  
**支持平台**: Windows | Linux | macOS  
**版本**: 1.0.0
