#!/usr/bin/env python3
"""
验证 GUI 导入修复
测试从不同位置运行 gui.py 时的导入是否正常
"""

import sys
import subprocess
from pathlib import Path

def test_direct_run():
    """测试：直接运行 gui.py（用户最常见的错误场景）"""
    print("\n[测试] 直接从 src/pdf_reader 目录运行 gui.py")
    print("-" * 60)
    
    # 切换到 gui.py 所在目录并运行
    gui_dir = Path("src/pdf_reader")
    gui_file = gui_dir / "gui.py"
    
    if not gui_file.exists():
        print("✗ 找不到 gui.py")
        return False
    
    # 尝试导入测试（不启动 GUI）
    code = """
import sys
from pathlib import Path

# 模拟直接运行 gui.py 的环境
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    # 尝试导入 gui 模块的关键部分
    from PyQt5.QtWidgets import QApplication
    import pymupdf
    from pypdf import PdfReader
    import pdfplumber
    
    # 测试 cli 导入（这是之前失败的部分）
    try:
        from cli import parse_page_ranges
        print("✓ 使用 'from cli import' 成功")
    except ImportError:
        try:
            from pdf_reader.cli import parse_page_ranges
            print("✓ 使用 'from pdf_reader.cli import' 成功")
        except ImportError as e:
            print(f"✗ 导入 cli 失败: {e}")
            sys.exit(1)
    
    print("✓ 所有导入成功")
    sys.exit(0)
except Exception as e:
    print(f"✗ 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
    
    # 在 gui.py 所在目录执行测试
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(gui_dir),
        capture_output=True,
        text=True,
        timeout=5
    )
    
    print(result.stdout)
    if result.stderr:
        print("错误输出:", result.stderr)
    
    if result.returncode == 0:
        print("✓ 测试通过")
        return True
    else:
        print(f"✗ 测试失败（返回码: {result.returncode}）")
        return False

def test_module_import():
    """测试：作为模块导入"""
    print("\n[测试] 作为模块导入 (from src.pdf_reader.gui import main)")
    print("-" * 60)
    
    try:
        from src.pdf_reader.gui import main, PDFReaderGUI
        print("✓ 导入 main 和 PDFReaderGUI 成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_sys_path_import():
    """测试：添加到 sys.path 后导入"""
    print("\n[测试] 添加到 sys.path 后导入")
    print("-" * 60)
    
    try:
        import sys
        from pathlib import Path
        
        gui_dir = Path("src/pdf_reader").resolve()
        if str(gui_dir) not in sys.path:
            sys.path.insert(0, str(gui_dir))
        
        import gui
        print("✓ 导入 gui 模块成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def main():
    print("=" * 60)
    print("GUI 导入修复验证")
    print("=" * 60)
    
    results = []
    
    # 测试 1: 最常见的错误场景
    results.append(("直接运行 gui.py", test_direct_run()))
    
    # 测试 2: 模块导入
    results.append(("模块导入", test_module_import()))
    
    # 测试 3: sys.path 导入
    results.append(("sys.path 导入", test_sys_path_import()))
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    success_count = sum(1 for _, r in results if r)
    total_count = len(results)
    
    print(f"\n通过: {success_count}/{total_count}")
    print("=" * 60)
    
    return 0 if all(r for _, r in results) else 1

if __name__ == "__main__":
    sys.exit(main())
