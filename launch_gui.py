#!/usr/bin/env python3
"""
PDF Reader GUI Launcher
Handles path configuration and dependency checking
"""

import sys
from pathlib import Path

# Add necessary paths
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
pdf_reader_dir = src_dir / "pdf_reader"

# Ensure paths are in sys.path
for path in [str(pdf_reader_dir), str(src_dir), str(current_dir)]:
    if path not in sys.path:
        sys.path.insert(0, path)

def check_and_install_dependencies():
    """Check if PyQt5 is installed, offer to install if missing"""
    try:
        import PyQt5
        return True
    except ImportError:
        print()
        print("=" * 70)
        print("MISSING DEPENDENCY: PyQt5 is not installed")
        print("=" * 70)
        print()
        print("PyQt5 is required to run the GUI application.")
        print()
        
        # Try to install automatically
        try:
            import subprocess
            print("Attempting to install PyQt5 and other dependencies...")
            print("This may take a few minutes...")
            print()
            
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", 
                 "PyQt5", "pymupdf", "pdfplumber", "pypdf", "Pillow", "typer", "rich"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("[OK] Dependencies installed successfully!")
                print()
                return True
            else:
                print("[ERROR] Installation failed!")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"[ERROR] Could not install automatically: {e}")
            print()
            print("Please install manually:")
            print("  python -m pip install PyQt5 pymupdf pdfplumber pypdf Pillow")
            print("Or run:")
            print("  install_dependencies.bat")
            return False

# Import and run GUI
try:
    # First check dependencies
    if not check_and_install_dependencies():
        print()
        print("=" * 70)
        sys.exit(1)
    
    from src.pdf_reader.gui import main
    
    if __name__ == "__main__":
        print("Starting PDF Reader GUI...")
        print()
        sys.exit(main())
        
except ImportError as e:
    print()
    print("=" * 70)
    print("ERROR: Cannot import GUI module")
    print("=" * 70)
    print(f"Details: {e}")
    print()
    print("To fix this, run:")
    print("  install_dependencies.bat")
    print()
    print("=" * 70)
    sys.exit(1)
except Exception as e:
    print()
    print("=" * 70)
    print("ERROR: Unexpected error")
    print("=" * 70)
    print(f"Details: {e}")
    print()
    import traceback
    traceback.print_exc()
    print("=" * 70)
    sys.exit(1)
