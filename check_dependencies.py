#!/usr/bin/env python3
"""
PDF Reader 依赖检查脚本
验证所有必要的模块是否已正确安装
"""

import sys

def check_module(module_name, import_name=None):
    """检查模块是否已安装"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"✓ {module_name:20} - 已安装")
        return True
    except ImportError as e:
        print(f"✗ {module_name:20} - 缺失: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("PDF Reader 依赖检查")
    print("=" * 60 + "\n")
    
    modules_to_check = [
        ("PyQt5", "PyQt5.QtWidgets"),
        ("PyQt5.QtCore", "PyQt5.QtCore"),
        ("PyQt5.QtGui", "PyQt5.QtGui"),
        ("pymupdf", "fitz"),
        ("pypdf", "pypdf"),
        ("pdfplumber", "pdfplumber"),
        ("Pillow", "PIL"),
        ("typer", "typer"),
        ("rich", "rich"),
    ]
    
    results = []
    for module_name, import_name in modules_to_check:
        results.append(check_module(module_name, import_name))
    
    print("\n" + "=" * 60)
    if all(results):
        print(f"✓ 所有依赖已安装 ({len(results)}/{len(results)})")
        print("=" * 60 + "\n")
        return 0
    else:
        missing = len([r for r in results if not r])
        print(f"✗ 有 {missing} 个依赖缺失")
        print("=" * 60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
