#!/usr/bin/env python3
"""
简化版本的 PDF Reader 构建脚本 - Windows 快速构建
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("\n" + "=" * 80)
    print("PDF Reader - Windows 可执行文件构建")
    print("=" * 80 + "\n")
    
    # 步骤 1: 安装必要的构建工具
    print("[1/4] 安装构建工具...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "PyInstaller"],
            capture_output=True,
            check=True
        )
        print("✓ 构建工具安装完成\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ 安装失败: {e}\n")
        return False
    
    # 步骤 2: 安装项目依赖
    print("[2/4] 安装项目依赖...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            capture_output=True,
            check=True
        )
        print("✓ 依赖安装完成\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败: {e}\n")
        return False
    
    # 步骤 3: 清理旧的构建
    print("[3/4] 清理旧的构建文件...")
    for dir_name in ["build", "dist"]:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
    print("✓ 清理完成\n")
    
    # 步骤 4: 运行 PyInstaller
    print("[4/4] 构建可执行文件...")
    
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--name=PDFReader",
        "--onedir",
        "--windowed",
        "--add-data", "src/pdf_reader:pdf_reader",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=pymupdf",
        "--hidden-import=pdfplumber",
        "--hidden-import=PIL",
        "--hidden-import=pypdf",
        "--collect-all=PyQt5",
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=pandas",
        "--exclude-module=scipy",
        "src/pdf_reader/gui.py"
    ]
    
    # 添加图标 (如果存在)
    icon_path = project_root / "icon.ico"
    if icon_path.exists():
        pyinstaller_args.insert(3, "--icon=" + str(icon_path))
    
    try:
        result = subprocess.run(pyinstaller_args, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"✗ 构建失败:\n{result.stderr}\n")
            return False
    except Exception as e:
        print(f"✗ 错误: {e}\n")
        return False
    
    # 验证构建结果
    exe_path = project_root / "dist" / "PDFReader" / "PDFReader.exe"
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ 构建完成\n")
        print("=" * 80)
        print("✓ 构建成功!")
        print("=" * 80)
        print(f"\n📦 可执行文件: dist\\PDFReader\\PDFReader.exe")
        print(f"📊 文件大小: {size_mb:.1f} MB")
        print(f"\n运行方式:")
        print(f"  1. 双击: dist\\PDFReader\\PDFReader.exe")
        print(f"  2. 命令行: dist\\PDFReader\\PDFReader.exe")
        print()
        return True
    else:
        print(f"✗ 可执行文件未生成\n")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
