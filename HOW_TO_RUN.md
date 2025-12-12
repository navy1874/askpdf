# How to Run PDF Reader GUI - Complete Guide

## ✅ RECOMMENDED METHODS (No Import Errors)

### Method 1: Use start_gui.bat (Easiest)
```bash
# Double-click or run:
start_gui.bat
```
- Checks dependencies automatically
- Handles all path configurations
- **Most user-friendly option**

### Method 2: Use launch_gui.py
```bash
python launch_gui.py
```
- Sets up paths correctly
- Provides helpful error messages
- Works from project root

### Method 3: Run as module
```bash
cd d:\code\pdfReader
python -m src.pdf_reader.gui
```
- Standard Python module execution
- Clean and reliable

### Method 4: Use executable
```bash
dist\PDFReader\PDFReader.exe
```
- No Python needed
- Standalone application

---

## ❌ COMMON MISTAKES (Causes Import Errors)

### ❌ DON'T: Run gui.py directly from its directory
```bash
# This will cause import errors:
cd src/pdf_reader
python gui.py      # ❌ WRONG
```

**Why it fails:**
- Relative imports don't work when running scripts directly
- Python can't find the `cli` module

### ❌ DON'T: Run without proper path setup
```bash
# This will also fail:
python src/pdf_reader/gui.py    # ❌ WRONG (from wrong directory)
```

---

## 🔧 FIXES APPLIED

### What We Fixed

1. **Added robust path initialization** in `gui.py`:
   ```python
   # Ensures module can be found from any location
   _current_file = Path(__file__).resolve()
   _current_dir = _current_file.parent
   _src_dir = _current_dir.parent
   _project_root = _src_dir.parent
   
   for _path in [str(_current_dir), str(_src_dir), str(_project_root)]:
       if _path not in sys.path:
           sys.path.insert(0, _path)
   ```

2. **Improved import fallback mechanism**:
   ```python
   try:
       from .cli import parse_page_ranges      # Try relative
   except Exception:
       sys.path.insert(0, str(current_dir))
       try:
           from cli import parse_page_ranges    # Try direct
       except ImportError:
           from pdf_reader.cli import parse_page_ranges  # Try package
   ```

3. **Created launch_gui.py launcher**:
   - Automatically configures paths
   - Provides user-friendly error messages

---

## 📋 Quick Reference

| Method | Command | Difficulty | Recommended |
|--------|---------|------------|-------------|
| Batch file | `start_gui.bat` | ⭐ Easy | ✅ YES |
| Launcher | `python launch_gui.py` | ⭐ Easy | ✅ YES |
| Module | `python -m src.pdf_reader.gui` | ⭐⭐ Medium | ✅ YES |
| Executable | `dist\PDFReader\PDFReader.exe` | ⭐ Easy | ✅ YES |
| Direct run | `python gui.py` | ⭐⭐⭐ Hard | ❌ NO |

---

## 🧪 Testing

Run the import test to verify everything works:
```bash
test_gui_import.bat
```

Expected output:
```
[Test 1] Import from project root...
[OK] Test 1 passed

[Test 2] Import after adding path...
[OK] Test 2 passed

[Test 3] Import cli module...
[OK] Test 3 passed

ALL TESTS PASSED!
```

---

## 💡 Understanding the Error

When you see:
```
ImportError: attempted relative import with no known parent package
ModuleNotFoundError: No module named 'cli'
```

**This means:**
- You're running `gui.py` directly as a script
- Python doesn't recognize it as part of a package
- The `cli` module can't be found

**Solution:**
- Use one of the recommended methods above
- Don't run `gui.py` directly from `src/pdf_reader/` directory

---

## 📁 Project Structure Understanding

```
pdfReader/                    ← Run commands from here
├── launch_gui.py            ← ✅ Use this
├── start_gui.bat            ← ✅ Use this
└── src/
    └── pdf_reader/
        ├── gui.py           ← ❌ Don't run directly
        └── cli.py
```

---

## 🎯 Summary

**To avoid import errors:**

1. ✅ Always use `start_gui.bat` or `launch_gui.py`
2. ✅ Or run from project root: `python -m src.pdf_reader.gui`
3. ❌ Never `cd` into `src/pdf_reader` and run `python gui.py`

---

**All import issues are now fixed! Just use the recommended methods.**
