#!/usr/bin/env python3
"""
PDF Reader - 快速构建脚本
支持 Windows, Linux, macOS
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class PDFReaderBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.is_windows = sys.platform == "win32"
        self.is_macos = sys.platform == "darwin"
        self.is_linux = sys.platform.startswith("linux")
    
    def print_header(self, text):
        """打印格式化的标题"""
        # 计算文本显示宽度（中文字符按2计算）
        def display_width(s):
            return sum(2 if ord(c) > 127 else 1 for c in s)
        
        content_width = 78
        text_width = display_width(text)
        left_pad = (content_width - text_width) // 2
        right_pad = content_width - text_width - left_pad
        
        print("\n╔" + "═" * 80 + "╗")
        print("║ " + " " * left_pad + text + " " * right_pad + " ║")
        print("╚" + "═" * 80 + "╝\n")
    
    def print_step(self, step, text):
        """打印步骤信息"""
        print(f"\n[{step}] {text}")
    
    def run_command(self, cmd, description=None):
        """运行命令"""
        if description:
            print(f"   {description}...")
        try:
            if isinstance(cmd, str):
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"   ❌ 失败: {result.stderr}")
                return False
            print(f"   ✅ 完成")
            return True
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return False
    
    def check_python(self):
        """检查 Python 环境"""
        self.print_step("1/6", "检查 Python 环境")
        
        if sys.version_info < (3, 8):
            print(f"   ❌ Python 版本过低 (需要 3.8+)")
            return False
        
        version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"   ✅ Python {version}")
        return True
    
    def setup_venv(self):
        """设置虚拟环境"""
        self.print_step("2/6", "设置虚拟环境")
        
        if self.venv_path.exists():
            print(f"   虚拟环境已存在")
            return True
        
        print(f"   创建虚拟环境...")
        if not self.run_command([sys.executable, "-m", "venv", str(self.venv_path)]):
            return False
        
        print(f"   ✅ 虚拟环境创建完成")
        return True
    
    def get_python_exe(self):
        """获取虚拟环境中的 Python 可执行文件"""
        if self.is_windows:
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")
    
    def get_pip_exe(self):
        """获取虚拟环境中的 pip 可执行文件"""
        if self.is_windows:
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:
            return str(self.venv_path / "bin" / "pip")
    
    def install_dependencies(self):
        """安装依赖"""
        self.print_step("3/6", "安装依赖包")
        
        pip_exe = self.get_pip_exe()
        
        dependencies = [
            ("pip", "升级 pip"),
            ("setuptools", "安装 setuptools"),
            ("wheel", "安装 wheel"),
            ("PyInstaller", "安装 PyInstaller"),
        ]
        
        # 升级 pip
        print("   升级 pip...")
        self.run_command([pip_exe, "install", "--upgrade", "pip"], None)
        
        # 安装其他依赖
        for pkg, desc in dependencies:
            self.run_command([pip_exe, "install", pkg], desc)
        
        # 安装项目
        print("   安装项目...")
        self.run_command([pip_exe, "install", "-e", str(self.project_root)], None)
        
        print(f"   ✅ 依赖安装完成")
        return True
    
    def clean_build(self):
        """清理旧的构建文件"""
        self.print_step("4/6", "清理旧的构建文件")
        
        dirs_to_remove = ["build", "dist", "__pycache__"]
        for dir_name in dirs_to_remove:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"   删除 {dir_name}/...")
                shutil.rmtree(dir_path)
        
        print(f"   ✅ 清理完成")
        return True
    
    def build_executable(self):
        """构建可执行文件"""
        self.print_step("5/6", "构建可执行文件")
        
        python_exe = self.get_python_exe()
        
        # 基本参数
        pyinstaller_args = [
            python_exe, "-m", "PyInstaller",
            "--name=PDFReader",
            "--onedir",
            "--windowed",
            "--add-data=src/pdf_reader:pdf_reader",
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
        ]
        
        # 添加图标 (如果存在)
        icon_path = self.project_root / "icon.ico"
        if icon_path.exists():
            pyinstaller_args.append(f"--icon={icon_path}")
        
        # GUI 文件
        gui_path = self.project_root / "src" / "pdf_reader" / "gui.py"
        pyinstaller_args.append(str(gui_path))
        
        print("   运行 PyInstaller...")
        if not self.run_command(pyinstaller_args, None):
            print("   ❌ 构建失败")
            return False
        
        print(f"   ✅ 构建完成")
        return True
    
    def verify_build(self):
        """验证构建结果"""
        self.print_step("6/6", "验证构建结果")
        
        if self.is_windows:
            exe_path = self.project_root / "dist" / "PDFReader" / "PDFReader.exe"
        else:
            exe_path = self.project_root / "dist" / "PDFReader" / "PDFReader"
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ 可执行文件已生成")
            print(f"   📦 位置: {exe_path}")
            print(f"   📊 大小: {size_mb:.1f} MB")
            return True
        else:
            print(f"   ❌ 可执行文件未生成")
            return False
    
    def print_success(self):
        """打印成功信息"""
        self.print_header("✅ 构建成功!")
        
        if self.is_windows:
            exe_path = "dist\\PDFReader\\PDFReader.exe"
            print(f"📦 可执行文件: {exe_path}")
            print(f"\n运行方法:")
            print(f"  1. 直接双击: dist\\PDFReader\\PDFReader.exe")
            print(f"  2. 命令行: {exe_path}")
            print(f"  3. 创建快捷方式到桌面")
        else:
            exe_path = "dist/PDFReader/PDFReader"
            print(f"📦 可执行文件: {exe_path}")
            print(f"\n运行方法:")
            print(f"  1. 直接运行: ./dist/PDFReader/PDFReader")
            print(f"  2. 创建快捷方式到桌面:")
            print(f"     ln -s $(pwd)/dist/PDFReader/PDFReader ~/Desktop/PDFReader")
        
        print(f"\n更多信息请查看: BUILD_GUIDE.md")
    
    def build(self):
        """执行完整构建流程"""
        self.print_header("PDF Reader - 应用程序构建")
        
        print(f"平台: {sys.platform}")
        print(f"项目路径: {self.project_root}")
        
        steps = [
            self.check_python,
            self.setup_venv,
            self.install_dependencies,
            self.clean_build,
            self.build_executable,
            self.verify_build,
        ]
        
        for step in steps:
            if not step():
                print("\n❌ 构建失败")
                return False
        
        self.print_success()
        return True

def main():
    """主函数"""
    builder = PDFReaderBuilder()
    
    try:
        if builder.build():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ 构建已取消")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
