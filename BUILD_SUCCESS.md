# Windows 可执行应用程序构建完成

## 构建信息

**构建日期:** 2025年12月11日
**平台:** Windows
**构建工具:** PyInstaller 6.17.0
**Python 版本:** 3.13.1

## 可执行文件位置

```
d:\code\pdfReader\dist\PDFReader\PDFReader.exe
```

## 文件信息

- **文件大小:** 1.66 MB
- **文件类型:** Windows 可执行程序 (.exe)
- **版本:** 独立可执行文件，无需外部依赖

## 运行方式

### 方法 1: 直接双击
```
双击 dist\PDFReader\PDFReader.exe
```

### 方法 2: 命令行运行
```cmd
dist\PDFReader\PDFReader.exe
```

### 方法 3: 从任何位置运行
可以将 `dist\PDFReader` 整个文件夹复制到任何位置，然后运行 `PDFReader.exe`

## 文件夹结构

```
dist\PDFReader\
├── PDFReader.exe          (主执行文件)
├── _internal\             (运行库和依赖文件)
│   ├── base_library.zip
│   ├── PyQt5相关文件
│   └── 其他依赖
```

## 创建快捷方式

### Windows 快捷方式
1. 右键点击 `PDFReader.exe`
2. 选择 "创建快捷方式"
3. 将快捷方式移到桌面或开始菜单

## 部署

可以将 `dist\PDFReader` 整个文件夹压缩并分发给其他 Windows 用户，用户可以直接解压后运行 `PDFReader.exe`

## 构建命令

快速重新构建可以使用以下命令：

```cmd
# 使用我们创建的快速构建脚本
quick_build.bat

# 或者使用 Python 脚本
python build_simple.py

# 或者使用原始构建脚本
python build.py
```

## 故障排除

### 如果程序无法运行

1. 确保您的 Windows 系统是 Windows 7 及以上版本
2. 检查是否缺少必要的运行库（通常不需要，因为 PyInstaller 已包含）
3. 如果有错误消息，请查看 `dist/PDFReader/_internal/` 目录中的日志文件

### 文件关联

如果要将 PDF 文件与 PDFReader 关联，可以：
1. 右键点击任何 PDF 文件
2. 选择 "打开方式" → "选择其他应用"
3. 浏览到 `PDFReader.exe`
4. 勾选 "始终用此应用打开"

---

**成功！您现在可以在 Windows 上运行 PDF Reader 应用了。**
