# GitHub Actions 快速参考

## 🚀 5 分钟快速设置

### Linux/macOS

```bash
# 1. 运行自动化设置脚本
cd /home/coff/pdfReader
./setup_github_actions.sh

# 2. 在 GitHub 创建新仓库 (https://github.com/new)

# 3. 推送代码到 GitHub
git remote add origin https://github.com/YOUR_USERNAME/PDFReader.git
git branch -M main
git push -u origin main

# 4. 创建版本标签来触发自动编译
git tag v1.0.0
git push origin v1.0.0

# 5. 查看构建进度
# 进入: https://github.com/YOUR_USERNAME/PDFReader/actions
```

### Windows

```cmd
REM 1. 运行自动化设置脚本
cd /path/to/pdfReader
setup_github_actions.bat

REM 2. 在 GitHub 创建新仓库 (https://github.com/new)

REM 3. 推送代码到 GitHub
git remote add origin https://github.com/YOUR_USERNAME/PDFReader.git
git branch -M main
git push -u origin main

REM 4. 创建版本标签来触发自动编译
git tag v1.0.0
git push origin v1.0.0

REM 5. 查看构建进度
REM 进入: https://github.com/YOUR_USERNAME/PDFReader/actions
```

---

## 📋 完整步骤说明

### 步骤 1: 初始化 git 仓库

**自动化方式 (推荐):**
```bash
# Linux/macOS
./setup_github_actions.sh

# Windows
setup_github_actions.bat
```

**手动方式:**
```bash
cd /home/coff/pdfReader
git init
git config user.email "your_email@gmail.com"
git config user.name "Your Name"
git add .
git commit -m "Initial commit"
```

### 步骤 2: 在 GitHub 上创建仓库

1. 访问 [https://github.com/new](https://github.com/new)
2. 填写仓库详情:
   - **Repository name**: `PDFReader`
   - **Description**: `A versatile PDF and image viewer with conversion capabilities`
   - **Visibility**: `Public` (免费) 或 `Private` (需要账户)
   - **Initialize this repository**: 不勾选
3. 点击 "Create repository"

### 步骤 3: 连接本地仓库到 GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/PDFReader.git
git branch -M main
git push -u origin main
```

**获取 URL 的方法:**
1. 进入刚创建的 GitHub 仓库
2. 点击绿色 "Code" 按钮
3. 选择 "HTTPS" 标签页
4. 复制 URL (格式: `https://github.com/YOUR_USERNAME/PDFReader.git`)

### 步骤 4: 启用 GitHub Actions

1. 进入仓库首页: `https://github.com/YOUR_USERNAME/PDFReader`
2. 点击顶部 "Actions" 标签
3. 如果看到提示，点击 "I understand my workflows, go ahead and enable them"
4. 或者直接点击 "set up a workflow yourself"

### 步骤 5: 触发自动构建

创建版本标签来触发自动编译工作流:

```bash
git tag v1.0.0
git push origin v1.0.0
```

**可选:** 更新版本号:
```bash
git tag v1.0.1
git push origin v1.0.1
```

### 步骤 6: 监控构建进度

1. 打开 Actions 页面: `https://github.com/YOUR_USERNAME/PDFReader/actions`
2. 查看 "Build Executables" 工作流的运行状态
3. 每个平台的编译进度:
   - 🟠 Running - 正在编译
   - 🟢 Completed - 已完成
   - 🔴 Failed - 失败

### 步骤 7: 下载编译结果

**方式 1: 从 Artifacts 下载 (临时, 30 天后删除)**
1. 进入 Actions 页面找到完成的工作流
2. 向下滚动查看 "Artifacts" 部分
3. 下载所需的平台版本

**方式 2: 从 Releases 下载 (永久)**
1. 进入仓库首页
2. 点击右侧 "Releases"
3. 找到对应版本
4. 下载发布的文件

---

## ⚙️ 工作流说明

### Build Executables 工作流包含:

| 平台 | 运行时间 | 输出 |
|------|--------|------|
| Windows | 5-7 分钟 | `PDFReader-Windows-v*.zip` |
| Linux | 5-7 分钟 | `PDFReader-Linux-v*.tar.gz` |
| macOS | 5-7 分钟 | `PDFReader-macOS-v*.zip` |

**总耗时:** 约 5-10 分钟

### 工作流触发条件

目前配置为以下两种方式触发:

1. **创建版本标签** (推荐)
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **手动触发**
   - 进入 Actions 页面
   - 点击 "Build Executables"
   - 点击 "Run workflow"

### 工作流文件位置

`.github/workflows/build-executables.yml`

---

## 🐛 故障排除

### 工作流未出现

**解决方案:**
1. 确保 `.github/workflows/` 目录存在
2. 确保 `build-executables.yml` 文件在正确位置
3. 刷新 GitHub 页面 (Ctrl+F5)
4. 如果仍未显示，手动推送 workflow 文件:
   ```bash
   git add .github/
   git commit -m "Add GitHub Actions workflow"
   git push
   ```

### 构建失败

**检查构建日志:**
1. 进入 Actions 页面
2. 点击失败的工作流
3. 查看失败的工作任务日志
4. 常见原因:
   - 缺少 Python 依赖
   - PyInstaller 版本不兼容
   - GUI 库缺失

**解决方法:**
- 检查 `pyproject.toml` 中的依赖版本
- 更新 workflow 文件中的依赖安装命令
- 在本地测试: `python build.py`

### 下载的文件过大

**原因:** 包含所有运行时库 (正常)

**大小参考:**
- Windows: 200-300 MB
- Linux: 200-300 MB
- macOS: 200-300 MB

---

## 💡 进阶用法

### 自定义工作流

编辑 `.github/workflows/build-executables.yml`:

```yaml
# 修改触发条件
on:
  push:
    branches:
      - main
    paths:
      - 'src/**'
      - 'build.py'

# 修改 Python 版本
with:
  python-version: '3.11'

# 修改构建命令
run: python build_multiplatform.py
```

### 添加自动发布

在 workflow 中启用 Release 创建:

```yaml
- name: Create Release
  uses: softprops/action-gh-release@v1
  with:
    files: dist/**
```

### 设置通知

GitHub Actions 默认会在以下时刻发送通知:
- 工作流完成
- 构建失败

在仓库设置中可以配置通知偏好。

---

## 📚 相关文件

- `setup_github_actions.sh` - Linux/macOS 自动化设置脚本
- `setup_github_actions.bat` - Windows 自动化设置脚本
- `.github/workflows/build-executables.yml` - GitHub Actions 工作流配置
- `build.py` - 本地构建脚本
- `pyproject.toml` - 项目配置和依赖

---

## 🎯 完整工作流示例

```
开发代码
  ↓
git commit "添加新功能"
  ↓
git tag v1.1.0
  ↓
git push origin main
git push origin v1.1.0
  ↓
GitHub Actions 自动编译所有平台 (约 10 分钟)
  ↓
下载编译结果
  ↓
测试各平台版本
  ↓
发布到网站或分享给用户
```

---

## ✅ 检查清单

- [ ] git 仓库已初始化
- [ ] GitHub 账户已创建
- [ ] 在 GitHub 上创建了新仓库
- [ ] 本地代码已推送到 GitHub
- [ ] Actions 已启用
- [ ] 创建了版本标签 (v1.0.0)
- [ ] Actions 工作流已完成
- [ ] 已下载编译结果
- [ ] 在各平台测试了可执行文件

---

**需要帮助?** 查看: [GitHub Actions 官方文档](https://docs.github.com/actions)
