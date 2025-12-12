#!/usr/bin/env python3
"""
测试 GUI 模块的各种导入方式
"""

import sys
from pathlib import Path

def test_import_method_1():
    """方法 1: 从 src.pdf_reader 导入"""
    try:
        from src.pdf_reader.gui import main
        print("✓ 方法 1 成功: from src.pdf_reader.gui import main")
        return True
    except Exception as e:
        print(f"✗ 方法 1 失败: {e}")
        return False

def test_import_method_2():
    """方法 2: 添加路径后导入"""
    try:
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root / "src" / "pdf_reader"))
        import gui
        print("✓ 方法 2 成功: 添加 src/pdf_reader 到路径后 import gui")
        return True
    except Exception as e:
        print(f"✗ 方法 2 失败: {e}")
        return False

def test_import_method_3():
    """方法 3: 直接运行 gui.py"""
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "src/pdf_reader/gui.py", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 or "PDF Reader" in result.stdout or "PDF Reader" in result.stderr:
            print("✓ 方法 3 成功: 直接运行 python src/pdf_reader/gui.py")
            return True
        else:
            print(f"✗ 方法 3 失败: 返回码 {result.returncode}")
            if result.stderr:
                print(f"  错误: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ 方法 3 失败: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("GUI 模块导入测试")
    print("=" * 60 + "\n")
    
    results = [
        test_import_method_1(),
        test_import_method_2(),
        test_import_method_3(),
    ]
    
    print("\n" + "=" * 60)
    success = sum(results)
    total = len(results)
    print(f"结果: {success}/{total} 个方法成功")
    print("=" * 60 + "\n")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
