from __future__ import annotations

from pathlib import Path
from typing import Optional
import sys

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QSplitterHandle,
    QTextEdit,
    QInputDialog,
    QSpinBox,
    QScrollArea,
    QMenuBar,
    QMenu,
)
import pymupdf
from pypdf import PdfReader, PdfWriter
from PIL import Image
import pdfplumber
import io

# When executed from a PyInstaller onefile/onedir build, __package__ can be
# None, so fall back to absolute import paths.
try:
    from .cli import parse_page_ranges
except Exception:  # noqa: BLE001 - broad on purpose for packaging edge cases
    current_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(current_dir))
    sys.path.insert(0, str(current_dir.parent))
    from cli import parse_page_ranges


class CustomSplitter(QSplitter):
    """Custom splitter with enhanced visual feedback for resizing."""
    
    def __init__(self, orientation):
        super().__init__(orientation)
        self.setChildrenCollapsible(False)  # 防止子窗口完全收起
        self.setHandleWidth(12)  # 增加分割柄宽度
        # 设置样式：深色背景 + 明亮分割柄
        self.setStyleSheet("""
            QSplitter::handle {
                background-color: #2c3e50;
                border: 1px solid #1a252f;
            }
            QSplitter::handle:hover {
                background-color: #34495e;
                border: 1px solid #1a252f;
            }
            QSplitter::handle:pressed {
                background-color: #2c3e50;
                border: 2px solid #3498db;
            }
        """)
        self.hover_handle = None
    
    def createHandle(self):
        """Create custom splitter handle."""
        return CustomSplitterHandle(self.orientation(), self)
    
    def mouseMoveEvent(self, event):
        """Show resize cursor when near splitter handle with enhanced feedback."""
        for i in range(len(self.sizes())):
            handle = self.handle(i)
            if not handle:
                continue
            handle_rect = handle.rect()
            # Map handle rect to global coordinates
            handle_pos = self.mapToGlobal(handle_rect.topLeft())
            handle_rect.moveTo(handle_pos)
            
            # Check if mouse is near the splitter handle
            if self.orientation() == Qt.Horizontal:
                if abs(event.globalPos().x() - (handle_pos.x() + 6)) < 12:
                    self.setCursor(QCursor(Qt.SplitHCursor))
                    super().mouseMoveEvent(event)
                    return
            else:
                if abs(event.globalPos().y() - (handle_pos.y() + 6)) < 12:
                    self.setCursor(QCursor(Qt.SplitVCursor))
                    super().mouseMoveEvent(event)
                    return
        
        self.setCursor(QCursor(Qt.ArrowCursor))
        super().mouseMoveEvent(event)


class CustomSplitterHandle(QSplitterHandle):
    """Custom splitter handle with enhanced visual design and hover effects."""
    
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.is_hovered = False
        self.setStyleSheet("""
            QSplitterHandle {
                background-color: #2c3e50;
            }
        """)
    
    def enterEvent(self, event):
        """Handle mouse enter event with invert effect."""
        self.is_hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave event to restore normal colors."""
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        """Paint custom splitter handle with visual indicators and hover effects."""
        from PyQt5.QtGui import QPainter, QColor, QPen
        from PyQt5.QtCore import Qt as QtCore
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 根据悬停状态选择颜色
        if self.is_hovered:
            # 反色模式：亮色背景 + 深色指示线
            bg_color = QColor(220, 221, 225)  # #dcdde1 浅灰
            line_color = QColor(44, 62, 80)   # #2c3e50 深灰蓝
        else:
            # 正常模式：深色背景 + 浅色指示线
            bg_color = QColor(44, 62, 80)     # #2c3e50 深灰蓝
            line_color = QColor(220, 221, 225)  # #dcdde1 浅灰
        
        # 绘制背景
        painter.fillRect(event.rect(), bg_color)
        
        # 绘制分割柄指示线
        if self.orientation() == QtCore.Horizontal:
            # 竖方向分割栏：绘制竖线指示
            painter.setPen(QPen(line_color, 2))
            for offset in [-4, 0, 4]:
                x = self.width() // 2 + offset
                painter.drawLine(x, self.height() // 4, x, 3 * self.height() // 4)
        else:
            # 横方向分割栏：绘制横线指示
            painter.setPen(QPen(line_color, 2))
            for offset in [-4, 0, 4]:
                y = self.height() // 2 + offset
                painter.drawLine(self.width() // 4, y, 3 * self.width() // 4, y)
        
        painter.end()


class PDFReaderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Reader")
        self.setGeometry(100, 100, 1200, 700)
        
        self.current_pdf: Optional[Path] = None
        self.current_page = 0
        self.total_pages = 0
        self.opened_pdfs: list[Path] = []
        self.zoom_level = 1.0
        self.fit_to_window = True
        self.current_pixmap: Optional[QPixmap] = None
        self.current_pdf_size: Optional[tuple] = None
        self.left_panel_collapsed = False
        
        self.create_menubar()
        self.init_ui()
        self.setAcceptDrops(True)

    def create_menubar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        file_menu.addAction("Open PDF", self.open_file)
        file_menu.addAction("Open Images", self.open_images)
        file_menu.addAction("Clear List", self.clear_list)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        edit_menu.addAction("Copy Text", self.copy_text)
        edit_menu.addAction("Select All", self.select_all)
        
        # View menu
        view_menu = menubar.addMenu("👁️ View")
        view_menu.addAction("Zoom In (Ctrl++)", self.zoom_in)
        view_menu.addAction("Zoom Out (Ctrl+-)", self.zoom_out)
        view_menu.addAction("Fit to Window (Ctrl+0)", self.zoom_fit)
        view_menu.addSeparator()
        view_menu.addAction("First Page (Home)", self.first_page)
        view_menu.addAction("Last Page (End)", self.last_page)
        
        # Operations menu
        ops_menu = menubar.addMenu("🛠️ Operations")
        ops_menu.addAction("Extract Text", self.extract_text)
        ops_menu.addAction("Split Pages", self.split_pages)
        ops_menu.addAction("Merge PDFs", self.merge_files)
        ops_menu.addSeparator()
        ops_menu.addAction("Images to PDF", self.images_to_pdf)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        help_menu.addAction("About", self.show_about)

    def init_ui(self):
        """Initialize UI components."""
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout with expand button
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Expand button (hidden initially, shown when collapsed)
        self.expand_btn = QPushButton("▶")
        self.expand_btn.setMaximumWidth(35)
        self.expand_btn.setToolTip("Expand panel")
        self.expand_btn.clicked.connect(self.toggle_left_panel)
        self.expand_btn.hide()
        main_layout.addWidget(self.expand_btn)
        
        # Left panel: File list with collapse button
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Top bar with title and collapse button
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("📁 Files:"))
        
        self.collapse_btn = QPushButton("◀")
        self.collapse_btn.setMaximumWidth(35)
        self.collapse_btn.setToolTip("Collapse panel")
        self.collapse_btn.clicked.connect(self.toggle_left_panel)
        top_bar.addWidget(self.collapse_btn)
        
        left_layout.addLayout(top_bar)
        
        # File list - support multiple selection
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(self.file_list.MultiSelection)  # 多选模式
        self.file_list.itemClicked.connect(self.on_file_selected)
        left_layout.addWidget(self.file_list)
        
        # Drag and drop hint
        info_label = QLabel("Drag & drop\nPDF files\nhere")
        info_label.setStyleSheet("color: #999; padding: 20px; text-align: center;")
        info_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(info_label, 0, Qt.AlignCenter)
        
        # Center panel: PDF Preview
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        pdf_title = QLabel("👁️ Preview")
        pdf_title.setStyleSheet("font-weight: bold; font-size: 12pt; padding: 5px;")
        center_layout.addWidget(pdf_title)
        
        upper_layout = QVBoxLayout()
        
        zoom_layout = QHBoxLayout()
        btn_zoom_out = QPushButton("🔍 −")
        btn_zoom_out.setMaximumWidth(50)
        btn_zoom_out.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(btn_zoom_out)
        
        self.zoom_label = QLabel("100%")
        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.setMaximumWidth(60)
        zoom_layout.addWidget(self.zoom_label)
        
        btn_zoom_in = QPushButton("🔍 +")
        btn_zoom_in.setMaximumWidth(50)
        btn_zoom_in.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(btn_zoom_in)
        
        btn_zoom_fit = QPushButton("Fit")
        btn_zoom_fit.setMaximumWidth(50)
        btn_zoom_fit.clicked.connect(self.zoom_fit)
        zoom_layout.addWidget(btn_zoom_fit)
        
        zoom_layout.addStretch()
        upper_layout.addLayout(zoom_layout)
        
        # Custom PDF label with mouse events
        class PDFLabel(QLabel):
            def __init__(self, parent):
                super().__init__(parent)
                self.gui = parent
            
            def enterEvent(self, event):
                self.setCursor(QCursor(Qt.OpenHandCursor))
                self.gui.on_pdf_preview_enter()
            
            def leaveEvent(self, event):
                self.setCursor(QCursor(Qt.ArrowCursor))
                self.gui.on_pdf_preview_leave()
        
        self.page_image_label = PDFLabel(self)
        self.page_image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f5f5f5;")
        # 不设置 setAlignment，改为让标签根据图像大小自动调整
        self.page_image_label.setScaledContents(False)  # 不自动缩放，保持原始大小
        # 移除固定最小尺寸，使标签能够自由调整
        
        scroll_upper = QScrollArea()
        self.scroll_area = scroll_upper
        scroll_upper.setWidget(self.page_image_label)
        scroll_upper.setWidgetResizable(True)
        # 配置滚动栏始终可见
        scroll_upper.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_upper.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 设置样式使滚动条更明显
        scroll_upper.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                border: 1px solid #ddd;
                background-color: #f5f5f5;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #999;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666;
            }
            QScrollBar:horizontal {
                border: 1px solid #ddd;
                background-color: #f5f5f5;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background-color: #999;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #666;
            }
        """)
        upper_layout.addWidget(scroll_upper, 1)
        
        upper_widget = QWidget()
        upper_widget.setLayout(upper_layout)
        
        # Text view section
        text_title = QLabel("📝 Text View")
        text_title.setStyleSheet("font-weight: bold; font-size: 12pt; padding: 5px;")
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet("font-family: monospace; font-size: 10pt;")
        
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.addWidget(text_title)
        text_layout.addWidget(self.preview_text)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        preview_splitter = CustomSplitter(Qt.Vertical)
        preview_splitter.addWidget(upper_widget)
        preview_splitter.addWidget(text_widget)
        preview_splitter.setStretchFactor(0, 2)  # PDF 预览占更多空间
        preview_splitter.setStretchFactor(1, 1)  # 文本占较少空间
        preview_splitter.setCollapsible(0, False)  # 禁止收起 PDF 预览
        preview_splitter.setCollapsible(1, False)  # 禁止收起文本预览
        preview_splitter.setHandleWidth(8)  # 增加分割柄宽度，便于拖动
        
        center_layout.addWidget(preview_splitter)
        
        # Page navigation
        nav_layout = QHBoxLayout()
        btn_prev = QPushButton("← Prev")
        btn_prev.clicked.connect(self.prev_page)
        nav_layout.addWidget(btn_prev)
        
        nav_layout.addWidget(QLabel("Page:"))
        self.page_spin = QSpinBox()
        self.page_spin.setMinimum(1)
        self.page_spin.valueChanged.connect(self.go_to_page)
        nav_layout.addWidget(self.page_spin)
        
        self.page_label = QLabel("0/0")
        nav_layout.addWidget(self.page_label)
        
        btn_next = QPushButton("Next →")
        btn_next.clicked.connect(self.next_page)
        nav_layout.addWidget(btn_next)
        nav_layout.addStretch()
        
        center_layout.addLayout(nav_layout)
        
        # Right panel: Tools
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("🛠️ Operations:"))
        
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMaximumHeight(150)
        right_layout.addWidget(self.info_display)
        
        btn_info = QPushButton("📊 Show Info")
        btn_info.clicked.connect(self.show_info)
        right_layout.addWidget(btn_info)
        
        btn_extract = QPushButton("📝 Extract Text")
        btn_extract.clicked.connect(self.extract_text)
        right_layout.addWidget(btn_extract)
        
        btn_split = QPushButton("✂️ Split Pages")
        btn_split.clicked.connect(self.split_pages)
        right_layout.addWidget(btn_split)
        
        btn_merge = QPushButton("🔀 Merge PDFs")
        btn_merge.clicked.connect(self.merge_files)
        right_layout.addWidget(btn_merge)
        
        btn_img_to_pdf = QPushButton("🖼️ Images to PDF")
        btn_img_to_pdf.clicked.connect(self.images_to_pdf)
        right_layout.addWidget(btn_img_to_pdf)
        
        right_layout.addWidget(QLabel("📝 Output:"))
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        right_layout.addWidget(self.text_display)
        
        right_layout.addStretch()
        
        # Main splitter with custom cursor feedback
        self.splitter = CustomSplitter(Qt.Horizontal)
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(center_panel)
        self.splitter.addWidget(right_panel)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 1)
        self.splitter.setCollapsible(0, False)  # 禁止收起左侧面板
        self.splitter.setCollapsible(1, False)  # 禁止收起中央面板
        self.splitter.setCollapsible(2, False)  # 禁止收起右侧面板
        self.splitter.setHandleWidth(8)  # 增加分割柄宽度
        
        main_layout.addWidget(self.splitter)
        
        # Store references for panel management
        self.left_panel_widget = left_panel
        self.center_panel_widget = center_panel
        self.right_panel_widget = right_panel

    def open_file(self):
        """Open PDF files."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Open PDF", "", "PDF Files (*.pdf)"
        )
        for file_path in file_paths:
            if file_path:
                path = Path(file_path)
                if path not in self.opened_pdfs:
                    self.opened_pdfs.append(path)
                    item = QListWidgetItem(path.name)
                    item.setData(Qt.UserRole, str(path))
                    self.file_list.addItem(item)

    def open_images(self):
        """Open image files (PNG, JPG, BMP, GIF, TIFF, etc.)."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Open Images", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
        )
        for file_path in file_paths:
            if file_path:
                path = Path(file_path)
                if path not in self.opened_pdfs:
                    self.opened_pdfs.append(path)
                    item = QListWidgetItem(f"🖼️ {path.name}")
                    item.setData(Qt.UserRole, str(path))
                    self.file_list.addItem(item)

    def toggle_left_panel(self):
        """Toggle left panel visibility with collapse/expand."""
        sizes = self.splitter.sizes()
        
        if self.left_panel_collapsed:
            # Expand: restore left panel
            self.left_panel_widget.show()
            self.collapse_btn.show()
            self.expand_btn.hide()
            
            # Restore previous widths
            new_sizes = [200, sizes[0] + sizes[1] - 200, sizes[2]]
            self.splitter.setSizes(new_sizes)
            self.left_panel_collapsed = False
        else:
            # Collapse: hide left panel
            self.left_panel_widget.hide()
            self.collapse_btn.hide()
            self.expand_btn.show()
            
            # Redistribute space to center panel
            new_sizes = [0, sizes[0] + sizes[1], sizes[2]]
            self.splitter.setSizes(new_sizes)
            self.left_panel_collapsed = True

    def clear_list(self):
        """Clear file list."""
        self.file_list.clear()
        self.opened_pdfs.clear()
        self.current_pdf = None
        self.current_page = 0
        self.total_pages = 0
        self.info_display.clear()
        self.text_display.clear()
        self.preview_text.clear()
        self.page_label.setText("0/0")

    def on_file_selected(self, item: QListWidgetItem):
        """Handle file selection (PDF or image)."""
        file_path = Path(item.data(Qt.UserRole))
        self.current_pdf = file_path
        self.current_page = 0
        
        # Check if it's an image
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
        if file_path.suffix.lower() in image_extensions:
            # Handle image file
            self.total_pages = 1
            self.page_spin.setMaximum(1)
            self.page_spin.setValue(1)
            self.page_label.setText("1/1")
            self.preview_image()
        else:
            # Handle PDF file
            try:
                reader = PdfReader(str(file_path))
                self.total_pages = len(reader.pages)
                self.page_spin.setMaximum(self.total_pages)
                self.page_spin.setValue(1)
                self.show_info()
                self.update_preview()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load PDF: {e}")

    def preview_image(self):
        """Preview image file."""
        if not self.current_pdf or not self.current_pdf.exists():
            return
        try:
            img = Image.open(str(self.current_pdf))
            
            # Convert RGBA to RGB if needed
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get preview area dimensions
            max_width = self.scroll_area.width() - 40
            max_height = self.scroll_area.height() - 40
            
            # Scale if needed
            if max_width > 0 and max_height > 0:
                img_ratio = img.width / img.height
                max_ratio = max_width / max_height
                
                if img_ratio > max_ratio:  # Image is wider
                    new_width = min(max_width, img.width)
                else:  # Image is taller
                    new_height = min(max_height, img.height)
                    new_width = int(new_height * img_ratio)
                
                if new_width < img.width:
                    new_height = int(new_width / img_ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert PIL Image to QPixmap using PPM format
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PPM')
            img_byte_arr.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr.read())
            
            self.page_image_label.setPixmap(pixmap)
            self.preview_text.setPlainText(f"Image: {self.current_pdf.name}\nSize: {pixmap.width()}x{pixmap.height()}px")
        except Exception as e:
            self.preview_text.setPlainText(f"Error loading image: {e}")
            self.page_image_label.setText(f"Error: {str(e)[:50]}")

    def update_preview(self):
        """Update PDF preview."""
        if not self.current_pdf or self.current_page >= self.total_pages:
            return
        
        try:
            doc = pymupdf.open(str(self.current_pdf))
            page = doc[self.current_page]
            
            # Get page rectangle (correct API)
            rect = page.rect
            page_width = rect.width
            page_height = rect.height
            self.current_pdf_size = (page_width, page_height)
            
            if self.fit_to_window:
                # 获取滚动区域的实际可用尺寸
                scroll_width = self.scroll_area.width() - 40  # 留出边距和滚动条
                scroll_height = self.scroll_area.height() - 40
                
                if scroll_width > 0 and scroll_height > 0:
                    width_ratio = scroll_width / page_width
                    height_ratio = scroll_height / page_height
                    # 同时适配宽和高：取较小的缩放比例，确保整个页面都能显示在窗口内
                    fit_zoom = min(width_ratio, height_ratio)
                    self.zoom_level = max(fit_zoom, 0.1)
            
            dpi_scale = 2.0 * self.zoom_level
            mat = pymupdf.Matrix(dpi_scale, dpi_scale)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            
            img = QImage()
            img.loadFromData(img_data)
            self.current_pixmap = QPixmap.fromImage(img)
            
            # 无论什么模式，都直接显示 pixmap，让滚动条根据内容大小自动出现
            if self.fit_to_window:
                # fit 模式：根据窗口宽度缩放
                target_width = self.scroll_area.width() - 20
                if target_width > 0 and self.current_pixmap.width() != target_width:
                    scaled_pixmap = self.current_pixmap.scaledToWidth(target_width, Qt.SmoothTransformation)
                    self.page_image_label.setPixmap(scaled_pixmap)
                else:
                    self.page_image_label.setPixmap(self.current_pixmap)
            else:
                # 非 fit 模式：显示原始 pixmap，根据大小自动显示滚动栏
                self.page_image_label.setPixmap(self.current_pixmap)
            
            doc.close()
            
            with pdfplumber.open(str(self.current_pdf)) as pdoc:
                text = pdoc.pages[self.current_page].extract_text() or "[No text found]"
                self.preview_text.setPlainText(text)
            
            self.page_label.setText(f"{self.current_page + 1}/{self.total_pages}")
        except Exception as e:
            self.preview_text.setPlainText(f"Error: {e}")
            self.page_image_label.setText(f"Error: {str(e)[:50]}")

    def show_info(self):
        """Show PDF info."""
        if not self.current_pdf:
            QMessageBox.warning(self, "Warning", "No PDF selected")
            return
        
        try:
            reader = PdfReader(str(self.current_pdf))
            metadata = reader.metadata or {}
            
            info_text = f"📄 {self.current_pdf.name}\n\n"
            info_text += f"Pages: {len(reader.pages)}\n"
            info_text += f"Encrypted: {reader.is_encrypted}\n"
            
            if metadata:
                info_text += "\nMetadata:\n"
                for key, value in metadata.items():
                    info_text += f"  {key.lstrip('/')}: {value}\n"
            
            self.info_display.setPlainText(info_text)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read PDF: {e}")

    def extract_text(self):
        """Extract text from PDF."""
        if not self.current_pdf:
            QMessageBox.warning(self, "Warning", "No PDF selected")
            return
        
        default_pages = f"1-{self.total_pages}" if self.total_pages > 0 else "1"
        pages_str, ok = QInputDialog.getText(
            self, 
            "Extract Text", 
            f"Page ranges (e.g., '1,3-5'):\nLeave empty for all pages (1-{self.total_pages})",
            text=default_pages
        )
        if not ok:
            return
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Text", str(self.current_pdf.stem) + ".txt", "Text Files (*.txt)"
        )
        if not output_path:
            return
        
        try:
            with pdfplumber.open(str(self.current_pdf)) as doc:
                total_pages = len(doc.pages)
                indexes = parse_page_ranges(pages_str or None, total_pages)
                texts = []
                for idx in indexes:
                    text = doc.pages[idx].extract_text() or ""
                    texts.append(text)
                
                combined = "\n\n".join(texts)
                Path(output_path).write_text(combined, encoding="utf-8")
                
                preview = combined[:5000]
                if len(combined) > 5000:
                    preview += "\n\n[Truncated... Full text saved to file]"
                self.text_display.setPlainText(preview)
                QMessageBox.information(self, "Success", f"Text saved to {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Extract failed: {e}")

    def split_pages(self):
        """Split PDF pages."""
        if not self.current_pdf:
            QMessageBox.warning(self, "Warning", "No PDF selected")
            return
        
        pages_str, ok = QInputDialog.getText(
            self, "Split Pages", "Enter page ranges (e.g., '1,3-5'):", text="1-3"
        )
        if not ok or not pages_str:
            return
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Split PDF", str(self.current_pdf.stem) + "_split.pdf", "PDF Files (*.pdf)"
        )
        if not output_path:
            return
        
        try:
            reader = PdfReader(str(self.current_pdf))
            indexes = parse_page_ranges(pages_str, len(reader.pages))
            writer = PdfWriter()
            for idx in indexes:
                writer.add_page(reader.pages[idx])
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                writer.write(f)
            QMessageBox.information(self, "Success", f"Split PDF saved to {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Split failed: {e}")

    def merge_files(self):
        """Merge PDFs."""
        if len(self.opened_pdfs) < 2:
            QMessageBox.warning(self, "Warning", "Select at least 2 PDFs to merge")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Merged PDF", "merged.pdf", "PDF Files (*.pdf)"
        )
        if not output_path:
            return
        
        try:
            writer = PdfWriter()
            for pdf_path in self.opened_pdfs:
                reader = PdfReader(str(pdf_path))
                for page in reader.pages:
                    writer.add_page(page)
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                writer.write(f)
            QMessageBox.information(self, "Success", f"Merged PDF saved to {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Merge failed: {e}")

    def images_to_pdf(self):
        """Convert selected images to PDF with consistent scaling."""
        image_files = [p for p in self.opened_pdfs if p.suffix.lower() in 
                      ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp']]
        
        if not image_files:
            QMessageBox.warning(self, "Warning", "No image files selected")
            return
        
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF from Images", "images.pdf", "PDF Files (*.pdf)"
        )
        if not output_path:
            return
        
        try:
            # First pass: convert images and collect dimensions
            images = []
            img_list = []
            for img_path in sorted(image_files):  # Sort by filename
                img = Image.open(str(img_path))
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                img_list.append(img)
                images.append((img_path.name, img.size))
            
            if not img_list:
                return
            
            # Calculate optimal target size (use max width and normalize height)
            # This maintains aspect ratio consistency
            max_width = max(img.width for img in img_list)
            max_height = max(img.height for img in img_list)
            
            # Use A4-like aspect ratio (210x297mm) for PDF
            # Standard DPI for PDF is 72, but we use 150 for better quality
            dpi = 150
            a4_width_pixels = int(210 * dpi / 25.4)  # ~1240px at 150dpi
            a4_height_pixels = int(297 * dpi / 25.4)  # ~1754px at 150dpi
            
            # Scale to fit A4 while maintaining aspect ratio
            aspect_ratio = max_width / max_height
            if aspect_ratio > (a4_width_pixels / a4_height_pixels):
                # Image is wider than A4
                target_width = a4_width_pixels
                target_height = int(a4_width_pixels / aspect_ratio)
            else:
                # Image is taller than A4
                target_height = a4_height_pixels
                target_width = int(a4_height_pixels * aspect_ratio)
            
            # Second pass: resize all images to consistent size
            resized_images = []
            for img in img_list:
                # Resize with high-quality resampling
                resized_img = img.resize(
                    (target_width, target_height),
                    Image.Resampling.LANCZOS
                )
                resized_images.append(resized_img)
            
            if resized_images:
                # Create PDF with consistent image sizes
                resized_images[0].save(
                    output_path,
                    save_all=True,
                    append_images=resized_images[1:] if len(resized_images) > 1 else [],
                    optimize=False,  # Don't compress to maintain quality
                    quality=95  # High quality
                )
                
                # Show success message with scaling info
                msg = f"✓ PDF created from {len(resized_images)} images!\n\n"
                msg += f"Original sizes: {min(img.width for img in img_list)}×{min(img.height for img in img_list)} to "
                msg += f"{max_width}×{max_height}px\n"
                msg += f"Normalized to: {target_width}×{target_height}px\n"
                msg += f"Saved to: {output_path}"
                QMessageBox.information(self, "Success", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create PDF: {e}")

    def next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.page_spin.setValue(self.current_page + 1)
            self.update_preview()

    def prev_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.page_spin.setValue(self.current_page + 1)
            self.update_preview()

    def go_to_page(self, page_num: int):
        """Jump to specific page."""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num - 1
            self.update_preview()

    def first_page(self):
        """Go to first page."""
        self.current_page = 0
        self.page_spin.setValue(1)
        self.update_preview()

    def last_page(self):
        """Go to last page."""
        self.current_page = self.total_pages - 1
        self.page_spin.setValue(self.total_pages)
        self.update_preview()

    def zoom_in(self):
        """Zoom in."""
        self.fit_to_window = False
        self.zoom_level = min(self.zoom_level + 0.25, 3.0)
        self.zoom_label.setText(f"{int(self.zoom_level * 100)}%")
        self.update_preview()

    def zoom_out(self):
        """Zoom out."""
        self.fit_to_window = False
        self.zoom_level = max(self.zoom_level - 0.25, 0.3)
        self.zoom_label.setText(f"{int(self.zoom_level * 100)}%")
        self.update_preview()

    def zoom_fit(self):
        """Fit to window."""
        self.fit_to_window = True
        self.zoom_label.setText("Fit")
        self.update_preview()

    def on_pdf_preview_enter(self):
        """Mouse enters PDF preview."""
        self.page_image_label.setStyleSheet("border: 2px solid #0066cc; background-color: #f0f8ff;")

    def on_pdf_preview_leave(self):
        """Mouse leaves PDF preview."""
        self.page_image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f5f5f5;")

    def copy_text(self):
        """Copy extracted text."""
        text = self.preview_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            QMessageBox.information(self, "Info", "Text copied to clipboard")

    def select_all(self):
        """Select all text."""
        self.preview_text.selectAll()

    def show_about(self):
        """Show about dialog."""
        QMessageBox.information(
            self,
            "About PDF Reader",
            "PDF Reader v0.1.0\n\n"
            "A lightweight PDF viewer and manager.\n\n"
            "Features:\n"
            "• PDF viewing and navigation\n"
            "• Text extraction\n"
            "• Page splitting and merging\n"
            "• Zoom and fit to window"
        )

    def dragEnterEvent(self, event):
        """Handle drag enter."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop."""
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'}
        
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            path = Path(file_path)
            
            # Check if it's a PDF or image file
            if file_path.endswith(".pdf") or path.suffix.lower() in image_extensions:
                if path not in self.opened_pdfs:
                    self.opened_pdfs.append(path)
                    # Add icon for images
                    if path.suffix.lower() in image_extensions:
                        item = QListWidgetItem(f"🖼️ {path.name}")
                    else:
                        item = QListWidgetItem(path.name)
                    item.setData(Qt.UserRole, str(path))
                    self.file_list.addItem(item)

    def resizeEvent(self, event):
        """Handle window resize."""
        super().resizeEvent(event)
        # 在 fit 模式下窗口改变大小时，立即更新预览以保证高度适配
        if self.fit_to_window and self.current_pdf and event.size() != event.oldSize():
            # 直接调用 update_preview，确保使用最新的滚动区域尺寸
            self.update_preview()


def main():
    app = QApplication([])
    window = PDFReaderGUI()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
