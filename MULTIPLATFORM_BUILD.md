# 多平台编译指南

本项目支持为 Windows、Linux 和 macOS 生成可执行文件。

## 方案对比

### 方案 1: GitHub Actions (推荐 ⭐⭐⭐)

**优点：**
- 完全自动化，一键生成所有平台版本
- 免费使用 GitHub 的构建资源
- 支持自动上传到 Release
- 适合持续集成和发布

**步骤：**

1. **推送项目到 GitHub**
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/YOUR_USERNAME/PDFReader.git
git push -u origin main
```

2. **启用 Actions**
   - 进入 GitHub 仓库设置
   - Actions → 启用

3. **创建发布版本**
```bash
git tag v1.0.0
git push origin v1.0.0
```

4. **自动构建**
   - GitHub Actions 会自动为 Windows、Linux、macOS 编译
   - 编译完成后自动上传到 Release

### 方案 2: 本地逐平台编译 (灵活)

**优点：**
- 完全本地控制
- 可定制编译选项
- 支持测试后再发布

**步骤：**

#### 在 Linux 上编译 Linux 版本
```bash
python build.py
# 输出: dist/PDFReader/PDFReader
```

#### 在 Windows 上编译 Windows 版本
```cmd
python build.py
REM 输出: dist\PDFReader\PDFReader.exe
```

#### 在 macOS 上编译 macOS 版本
```bash
python build.py
# 输出: dist/PDFReader/PDFReader
```

### 方案 3: Docker 多平台构建

**优点：**
- 不需要多台机器
- 隔离的构建环境
- 可重复的构建结果

**步骤：**

```bash
# 需要先安装 Docker
python build_multiplatform.py
```

**限制：**
- Windows 和 macOS 跨平台编译比较复杂，仍建议使用 GitHub Actions

---

## 详细步骤

### GitHub Actions 详细配置

1. **检查工作流文件**
```bash
ls -la .github/workflows/
# 应该看到: build-executables.yml
```

2. **推送更改到 GitHub**
```bash
git add .
git commit -m "Add GitHub Actions CI/CD"
git push
```

3. **在 GitHub 网页上验证**
   - 进入你的仓库
   - 点击 Actions 标签
   - 应该看到 "Build Executables" 工作流

4. **创建 Release 并触发构建**
```bash
# 方式1: 通过 git 标签
git tag v1.0.0
git push origin v1.0.0

# 方式2: 手动在 GitHub 网页上创建 Release
# Releases → Create a new release → 填写版本号和说明
```

5. **等待构建完成**
   - 查看 Actions 标签下的运行状态
   - 每个平台的构建大约需要 5-10 分钟

6. **下载编译结果**
   - 方式1: 从 Artifacts 下载 (临时，30天后删除)
   - 方式2: 从 Release 下载 (永久)

---

### 本地编译详细步骤

#### 编译 Linux 版本（在 Linux 上）

```bash
# 检查环境
python3 quick_test.py

# 编译
python build.py

# 输出位置
ls -la dist/PDFReader/

# 运行测试
./dist/PDFReader/PDFReader
```

#### 编译 Windows 版本（在 Windows 上）

```cmd
REM 检查环境
python quick_test.py

REM 编译
python build.py

REM 输出位置
dir dist\PDFReader\

REM 运行测试
dist\PDFReader\PDFReader.exe
```

#### 编译 macOS 版本（在 macOS 上）

```bash
# 检查环境
python3 quick_test.py

# 编译
python build.py

# 输出位置
ls -la dist/PDFReader/

# 运行测试
./dist/PDFReader/PDFReader
```

---

## 文件分发

### 分发格式

编译完成后，为不同平台创建独立的压缩包：

```bash
# Linux 版本
tar -czf PDFReader-Linux-v1.0.0.tar.gz dist/PDFReader/

# 或 zip 格式 (通用)
zip -r PDFReader-Linux-v1.0.0.zip dist/PDFReader/
```

### 版本管理

建议的文件命名规则：
```
PDFReader-Windows-v1.0.0.zip      # Windows 64-bit
PDFReader-Linux-v1.0.0.tar.gz     # Linux 64-bit
PDFReader-macOS-v1.0.0.zip        # macOS (Intel + Apple Silicon)
```

---

## 故障排除

### 编译失败

1. **检查依赖**
```bash
python3 quick_test.py
```

2. **清理旧编译**
```bash
rm -rf build dist venv __pycache__
```

3. **重新编译**
```bash
python build.py
```

### 跨平台兼容性问题

- **Linux 可执行文件在其他 Linux 发行版无法运行**
  - 原因: 系统库版本不同
  - 解决: 在目标 Linux 发行版上重新编译

- **Windows 可执行文件在其他 Windows 上无法运行**
  - 原因: 缺少必要的运行时库
  - 解决: 在目标 Windows 版本上重新编译，或安装 VC++ 运行时

---

## 高级选项

### 自定义 PyInstaller 配置

编辑 `pdf_reader_gui.spec` 文件：

```python
# 修改应用程序名称
a = Analysis(
    ...
    name='MyPDFReader',  # 改这里
    ...
)
```

### 添加应用图标

```bash
# 将图标文件放在项目根目录
cp /path/to/icon.ico ./

# 编译时会自动使用
python build.py
```

### 自定义版本信息 (Windows)

在 `build.py` 中修改：

```python
pyinstaller_args = [
    ...
    f"--version-file=version.txt",  # 需要创建 version.txt
    ...
]
```

---

## 相关文件

- `build.py` - 单平台编译脚本
- `build_multiplatform.py` - 多平台编译协调脚本
- `.github/workflows/build-executables.yml` - GitHub Actions 工作流
- `pdf_reader_gui.spec` - PyInstaller 配置
- `BUILD_GUIDE.md` - 构建配置详解
- `DEPLOYMENT.md` - 部署指南

---

## 推荐工作流

```
开发 → 测试 → 创建 git 标签
        ↓
    GitHub Actions 自动为所有平台编译
        ↓
    下载编译结果
        ↓
    验证功能
        ↓
    上传到 Release 或网站
```

这样可以确保所有平台版本的一致性，同时减少手动编译的工作量。
