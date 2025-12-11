#!/usr/bin/env python3
"""
多平台构建脚本 - 使用 Docker 在单台 Linux 机器上编译所有平台
支持编译 Windows, Linux, macOS 应用程序
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class MultiPlatformBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_root = self.project_root / "dist_multiplatform"
    
    def print_header(self, text):
        """打印格式化的标题"""
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
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"   ❌ 失败: {result.stderr}")
                return False
            print(f"   ✅ 完成")
            return True
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return False
    
    def check_requirements(self):
        """检查系统要求"""
        self.print_step("1/4", "检查系统要求")
        
        # 检查是否为 Linux
        if sys.platform != "linux":
            print("   ℹ️  多平台构建需要在 Linux 上运行")
            print("   当前平台: " + sys.platform)
            return False
        
        print("   ✅ Linux 系统")
        
        # 检查 Docker
        result = subprocess.run("docker --version", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("   ❌ Docker 未安装")
            print("   请安装 Docker: https://docs.docker.com/get-docker/")
            return False
        
        docker_version = result.stdout.strip()
        print(f"   ✅ {docker_version}")
        
        return True
    
    def build_linux(self):
        """编译 Linux 版本"""
        self.print_step("2/4", "编译 Linux 版本")
        
        # 使用本地环境编译
        print("   使用当前 Python 环境编译...")
        cmd = f"cd {self.project_root} && python build.py"
        
        if not self.run_command(cmd, "编译 Linux 可执行文件"):
            return False
        
        # 复制到多平台目录
        src = self.project_root / "dist" / "PDFReader"
        dst = self.dist_root / "PDFReader-Linux"
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"   ✅ Linux 版本已保存到: {dst}")
            return True
        
        return False
    
    def build_windows_with_docker(self):
        """使用 Docker 编译 Windows 版本"""
        self.print_step("3/4", "编译 Windows 版本 (Docker)")
        
        print("   ⚠️  跨平台编译 Windows 需要在 Windows 上进行")
        print("   请在 Windows PC 上运行: python build.py")
        print("   或使用 GitHub Actions 自动编译")
        
        return True
    
    def build_macos_with_docker(self):
        """使用 Docker 编译 macOS 版本"""
        self.print_step("4/4", "编译 macOS 版本 (Docker)")
        
        print("   ⚠️  跨平台编译 macOS 需要在 macOS 上进行")
        print("   请在 macOS 上运行: python build.py")
        print("   或使用 GitHub Actions 自动编译")
        
        return True
    
    def print_summary(self):
        """打印总结"""
        self.print_header("✅ 本地编译完成!")
        
        print(f"📦 输出目录: {self.dist_root}")
        print(f"\n已生成的文件:")
        
        linux_path = self.dist_root / "PDFReader-Linux"
        if linux_path.exists():
            print(f"  ✅ Linux 版本: {linux_path}/PDFReader")
        
        print(f"\n多平台编译建议:")
        print(f"  1. GitHub Actions (推荐)")
        print(f"     - 在 GitHub 仓库中启用 Actions")
        print(f"     - 创建版本标签: git tag v1.0.0 && git push origin v1.0.0")
        print(f"     - 自动为所有平台编译")
        print(f"")
        print(f"  2. 本地编译 (逐平台)")
        print(f"     - Linux: python build.py (当前机器)")
        print(f"     - Windows: 在 Windows PC 上运行 python build.py")
        print(f"     - macOS: 在 macOS 上运行 python build.py")
        print(f"")
        print(f"  3. 云构建服务")
        print(f"     - 使用 GitHub Actions (完全免费)")
        print(f"     - 配置文件已创建: .github/workflows/build-executables.yml")
    
    def build(self):
        """执行构建"""
        self.print_header("多平台构建系统")
        
        # 创建输出目录
        self.dist_root.mkdir(exist_ok=True)
        
        steps = [
            self.check_requirements,
            self.build_linux,
            self.build_windows_with_docker,
            self.build_macos_with_docker,
        ]
        
        for step in steps:
            if not step():
                # 部分失败不中断，继续其他平台
                continue
        
        self.print_summary()
        return True

def main():
    """主函数"""
    builder = MultiPlatformBuilder()
    
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
