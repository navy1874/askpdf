@echo off
REM GitHub Actions 快速设置脚本 (Windows 版本)
REM 自动初始化 git 仓库并推送到 GitHub

setlocal enabledelayedexpansion
chcp 65001 > nul

echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║                      GitHub Actions 快速设置助手                               ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM 步骤 1: 初始化 git
echo [1/5] 初始化 git 仓库...
if not exist ".git" (
    git init
    echo     ✅ 已初始化 git 仓库
) else (
    echo     ℹ️  git 仓库已存在
)

REM 步骤 2: 配置用户信息
echo.
echo [2/5] 配置 git 用户信息...

for /f "tokens=*" %%i in ('git config user.email') do set GIT_EMAIL=%%i
if "!GIT_EMAIL!"=="" (
    echo     请输入 git 用户邮箱 (用于 GitHub 提交):
    set /p GIT_EMAIL=     邮箱: 
    git config user.email "!GIT_EMAIL!"
) else (
    echo     已配置邮箱: !GIT_EMAIL!
)

for /f "tokens=*" %%i in ('git config user.name') do set GIT_NAME=%%i
if "!GIT_NAME!"=="" (
    echo     请输入 git 用户名:
    set /p GIT_NAME=     用户名: 
    git config user.name "!GIT_NAME!"
) else (
    echo     已配置用户名: !GIT_NAME!
)

echo     ✅ 用户信息已配置

REM 步骤 3: 创建 .gitignore
echo.
echo [3/5] 创建 .gitignore...
(
    echo # Python
    echo __pycache__/
    echo *.py[cod]
    echo *$py.class
    echo *.so
    echo .Python
    echo build/
    echo develop-eggs/
    echo dist/
    echo dist_multiplatform/
    echo downloads/
    echo eggs/
    echo .eggs/
    echo lib/
    echo lib64/
    echo parts/
    echo sdist/
    echo var/
    echo wheels/
    echo *.egg-info/
    echo .installed.cfg
    echo *.egg
    echo.
    echo # Virtual Environment
    echo venv/
    echo ENV/
    echo env/
    echo.
    echo # IDE
    echo .vscode/
    echo .idea/
    echo *.swp
    echo *.swo
    echo *~
    echo.
    echo # OS
    echo .DS_Store
    echo Thumbs.db
) > .gitignore

echo     ✅ .gitignore 已创建

REM 步骤 4: 添加文件并提交
echo.
echo [4/5] 提交文件到本地仓库...
git add .
git commit -m "Initial commit: PDF Reader application with GitHub Actions CI/CD" 2>nul || echo     ℹ️  仓库已是最新状态
echo     ✅ 文件已提交

REM 步骤 5: 显示后续步骤
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║                           下一步操作说明                                       ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.
echo 现在需要在 GitHub 上创建仓库并推送代码。请按以下步骤操作:
echo.
echo 1️⃣  在 GitHub 上创建新仓库
echo    - 访问: https://github.com/new
echo    - 填写仓库名称: PDFReader (或你想要的名称)
echo    - 勾选 'Initialize this repository with a README' (不勾选)
echo    - 点击 'Create repository'
echo.
echo 2️⃣  复制仓库 URL
echo    - 在仓库页面点击 'Code' 按钮
echo    - 选择 HTTPS (如果未配置 SSH)
echo    - 复制 URL (格式: https://github.com/YOUR_USERNAME/PDFReader.git)
echo.
echo 3️⃣  推送代码到 GitHub
echo    运行以下命令 (替换 YOUR_GITHUB_URL 为上面复制的 URL):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/PDFReader.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4️⃣  启用 GitHub Actions
echo    - 进入仓库页面
echo    - 点击 'Actions' 标签
echo    - 如果看到 'I understand my workflows' 字样，点击启用
echo.
echo 5️⃣  创建版本标签来触发自动构建
echo    运行以下命令:
echo.
echo    git tag v1.0.0
echo    git push origin v1.0.0
echo.
echo 6️⃣  查看自动构建进度
echo    - 返回仓库的 'Actions' 标签
echo    - 应该看到 'Build Executables' 工作流正在运行
echo    - 等待约 5-10 分钟，3 个平台都编译完成
echo.
echo 7️⃣  下载编译结果
echo    - 等待所有工作流完成 (绿色 ✅)
echo    - 在工作流详情页面查看 'Artifacts'
echo    - 或进入 'Releases' 页面下载完整版本
echo.
echo ════════════════════════════════════════════════════════════════════════════════
echo.
echo 💡 提示:
echo    - GitHub 免费账户每月有 2000 分钟的 Actions 免费额度
echo    - 本项目编译 3 个平台约需 20-30 分钟
echo    - 足够每个月编译多个版本
echo.
pause
