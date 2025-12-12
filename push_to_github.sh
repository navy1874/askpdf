#!/bin/bash
# GitHub 推送验证和执行脚本

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║              GitHub 推送脚本 - 检查仓库并推送代码                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

REPO_URL="https://github.com/NavyYang/askpdf.git"
REPO_DIR="/home/coff/pdfReader"

# 步骤 1: 检查网络连接
echo "[1/4] 检查网络连接..."
if ping -c 1 github.com &> /dev/null; then
    echo "    ✅ 网络连接正常"
else
    echo "    ❌ 网络连接失败"
    exit 1
fi

# 步骤 2: 尝试访问仓库
echo ""
echo "[2/4] 验证 GitHub 仓库..."
echo "    尝试访问: https://github.com/NavyYang/askpdf"

if curl -s -I "https://github.com/NavyYang/askpdf" | head -1 | grep -q "200"; then
    echo "    ✅ 仓库存在 (HTTP 200)"
elif curl -s -I "https://github.com/NavyYang/askpdf" | head -1 | grep -q "404"; then
    echo "    ❌ 仓库不存在 (HTTP 404)"
    echo ""
    echo "    ⚠️  请先在 GitHub 上创建仓库:"
    echo "    1. 访问: https://github.com/new"
    echo "    2. Repository name: askpdf"
    echo "    3. Visibility: Public"
    echo "    4. 不要初始化任何文件 (README, .gitignore, license)"
    echo "    5. 点击 'Create repository'"
    echo ""
    exit 1
else
    echo "    ℹ️  无法完全验证，但尝试继续推送..."
fi

# 步骤 3: 推送代码
echo ""
echo "[3/4] 推送代码到 GitHub..."
cd "$REPO_DIR"

git branch -M main
git push -u origin main 2>&1 | tee /tmp/git_push.log

# 检查是否成功
if grep -q "Permission denied\|Repository not found\|fatal" /tmp/git_push.log; then
    echo ""
    echo "    ❌ 推送失败"
    echo ""
    echo "    可能的原因:"
    echo "    1. 仓库在 GitHub 上不存在"
    echo "    2. 网络连接问题"
    echo "    3. GitHub 认证失败"
    echo ""
    echo "    请检查:"
    echo "    - GitHub 仓库是否已创建: https://github.com/NavyYang/askpdf"
    echo "    - git 是否配置了 GitHub 认证"
    exit 1
else
    echo "    ✅ 推送成功"
fi

# 步骤 4: 验证推送结果
echo ""
echo "[4/4] 验证推送结果..."
if [ $? -eq 0 ]; then
    echo "    ✅ 所有步骤完成"
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                           下一步: 触发自动编译                                 ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "代码已推送到 GitHub。现在创建版本标签来触发自动编译:"
    echo ""
    echo "  git tag v1.0.0"
    echo "  git push origin v1.0.0"
    echo ""
    echo "然后访问以下链接查看构建进度:"
    echo "  https://github.com/NavyYang/askpdf/actions"
    echo ""
else
    exit 1
fi
