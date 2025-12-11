#!/bin/bash
# PDF Reader - Build executable for Linux/Windows/macOS
# Usage: bash build_executable.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════════════════════════╗"
echo "║           PDF Reader - 应用程序打包脚本                                      ║"
echo "╚════════════════════════════════════════════════════════════════════════════════╝"
echo ""

# 检查 Python 环境
echo "[1/5] 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✅ 找到 Python $PYTHON_VERSION"
echo ""

# 检查/创建虚拟环境
echo "[2/5] 检查虚拟环境..."
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "✅ 虚拟环境激活完成"
echo ""

# 安装依赖
echo "[3/5] 安装依赖包..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install PyInstaller > /dev/null 2>&1
pip install -e . > /dev/null 2>&1
echo "✅ 依赖安装完成"
echo ""

# 清理旧的构建
echo "[4/5] 清理旧的构建文件..."
rm -rf build dist *.spec __pycache__ 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# 使用 PyInstaller 构建
echo "[5/5] 构建可执行文件..."
echo "运行 PyInstaller..."

pyinstaller \
    --name="PDFReader" \
    --onedir \
    --windowed \
    --icon=icon.ico \
    --add-data="src/pdf_reader:pdf_reader" \
    --hidden-import=PyQt5 \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --hidden-import=pymupdf \
    --hidden-import=pdfplumber \
    --hidden-import=PIL \
    --hidden-import=pypdf \
    --collect-all PyQt5 \
    --exclude-module=matplotlib \
    --exclude-module=numpy \
    --exclude-module=pandas \
    --exclude-module=scipy \
    src/pdf_reader/gui.py 2>&1

echo "✅ 构建完成"
echo ""

# 检查结果
if [ -f "dist/PDFReader/PDFReader" ] || [ -f "dist/PDFReader/PDFReader.exe" ]; then
    echo "╔════════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          ✅ 构建成功!                                         ║"
    echo "╚════════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📦 可执行文件位置:"
    if [ -f "dist/PDFReader/PDFReader" ]; then
        echo "   Linux:   dist/PDFReader/PDFReader"
        echo ""
        echo "运行方式:"
        echo "   ./dist/PDFReader/PDFReader"
        ls -lh dist/PDFReader/PDFReader
    fi
    if [ -f "dist/PDFReader/PDFReader.exe" ]; then
        echo "   Windows: dist/PDFReader/PDFReader.exe"
        echo ""
        echo "运行方式:"
        echo "   dist\\PDFReader\\PDFReader.exe"
        ls -lh dist/PDFReader/PDFReader.exe
    fi
    echo ""
    echo "快捷方式创建:"
    echo "   • Linux:   ln -s \$(pwd)/dist/PDFReader/PDFReader ~/Desktop/PDFReader"
    echo "   • Windows: 右键 PDFReader.exe → 创建快捷方式 → 移动到桌面"
    echo ""
else
    echo "❌ 构建失败"
    exit 1
fi
