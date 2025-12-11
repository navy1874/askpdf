#!/usr/bin/env python3
"""
快速测试脚本 - 验证构建环境
"""

import sys
import subprocess
from pathlib import Path

def check_python():
    """检查 Python 版本"""
    print("✓ Python 版本:", sys.version.split()[0])
    if sys.version_info < (3, 8):
        print("✗ 需要 Python 3.8 或更高")
        return False
    return True

def check_package(package_name):
    """检查包是否已安装"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name} 未安装")
        return False

def main():
    print("╔" + "═" * 50 + "╗")
    print("║  PDF Reader - 构建环境快速检查")
    print("╚" + "═" * 50 + "╝\n")
    
    print("1. 检查 Python 环境")
    print("-" * 50)
    if not check_python():
        return False
    
    print("\n2. 检查必需的包")
    print("-" * 50)
    
    packages = [
        'PyQt5',
        'pymupdf',
        'pdfplumber',
        'PIL',
        'pypdf',
        'typer',
        'rich',
    ]
    
    missing = []
    for pkg in packages:
        if not check_package(pkg):
            missing.append(pkg)
    
    print("\n3. 检查构建工具")
    print("-" * 50)
    
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
    except ImportError:
        print("✗ PyInstaller 未安装")
        missing.append('PyInstaller')
    
    print("\n4. 检查项目文件")
    print("-" * 50)
    
    project_root = Path(__file__).parent
    required_files = [
        'src/pdf_reader/gui.py',
        'pyproject.toml',
        'build.py',
        'build_executable.sh',
        'build_executable.bat',
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 不存在")
            missing.append(file_path)
    
    print("\n" + "═" * 50)
    
    if missing:
        print(f"\n❌ 缺失的内容:")
        for item in missing:
            print(f"  - {item}")
        print("\n请安装缺失的包:")
        pkg_list = [m for m in missing if m != 'PyInstaller']
        if pkg_list:
            print(f"  pip install {' '.join(pkg_list)}")
        if 'PyInstaller' in missing:
            print(f"  pip install PyInstaller")
        return False
    else:
        print("\n✅ 环境检查完成，所有必需组件已就位！")
        print("\n可以开始构建:")
        print("  Windows: python build.py")
        print("  Linux/macOS: python3 build.py")
        return True

if __name__ == '__main__':
    sys.exit(0 if main() else 1)
