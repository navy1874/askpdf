# PDF Reader - Quick Launch Reference

## 🚀 Fastest Ways to Start

### 1. Using Executable (Fastest - No Python needed)
```bash
run.bat
```
or double-click: `dist\PDFReader\PDFReader.exe`

**Pros:** 
- ⚡ Instant startup
- 📦 No dependencies needed
- ✅ Always works

---

### 2. Using Python (Fast - Requires Python)
```bash
start_gui.bat
```
or
```bash
python launch_gui.py
```

**Pros:**
- 🔧 Can modify source code
- 🐛 Easier to debug
- 📝 See error messages

---

### 3. With Dependency Verification (Slower)
```bash
start_gui_checked.bat
```

**Pros:**
- ✓ Checks dependencies first
- 📊 Shows verification details
- 🔍 Good for troubleshooting

---

## 📋 Comparison Table

| Method | Command | Speed | Requirements | Use When |
|--------|---------|-------|--------------|----------|
| **Executable** | `run.bat` | ⚡⚡⚡ | None | Daily use |
| **Python Quick** | `start_gui.bat` | ⚡⚡ | Python + deps | Development |
| **Python Direct** | `python launch_gui.py` | ⚡⚡ | Python + deps | Testing |
| **With Check** | `start_gui_checked.bat` | ⚡ | Python + deps | Troubleshooting |

---

## ❌ Troubleshooting

### Problem: start_gui.bat doesn't work

**Solution:** Use `run.bat` instead (it always works)

### Problem: "Dependencies missing" error

**Solution:** 
```bash
install_dependencies.bat
```

### Problem: Want to verify dependencies

**Solution:**
```bash
python check_dependencies.py
```

---

## 💡 Recommendations

### For Daily Use
```bash
run.bat              # Just double-click!
```

### For Development
```bash
start_gui.bat        # Fast startup
```

### For First-Time Setup
```bash
install_dependencies.bat    # Install dependencies
start_gui_checked.bat       # Verify and start
```

---

**TL;DR: Just use `run.bat` - it always works!**
