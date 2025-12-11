import streamlit as st
from pathlib import Path
import tempfile
from pypdf import PdfReader, PdfWriter
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import io

from .cli import parse_page_ranges

st.set_page_config(page_title="PDF Reader", layout="wide", initial_sidebar_state="expanded")

st.title("📄 PDF Reader & Manager")

# Sidebar for file upload
with st.sidebar:
    st.header("📁 File Management")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type="pdf",
        accept_multiple_files=True,
        help="Select one or more PDF files"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        
        # Store uploaded files in session state
        if "pdf_files" not in st.session_state:
            st.session_state.pdf_files = {}
        
        for file in uploaded_files:
            if file.name not in st.session_state.pdf_files:
                st.session_state.pdf_files[file.name] = file.getvalue()

# Tabs for different operations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📖 View & Preview",
    "📝 Extract Text",
    "✂️ Split Pages",
    "🔀 Merge PDFs",
    "ℹ️ Info & Metadata"
])

# Tab 1: View & Preview
with tab1:
    st.header("PDF Preview")
    
    if st.session_state.get("pdf_files"):
        col1, col2 = st.columns([3, 1])
        
        with col2:
            selected_pdf = st.selectbox(
                "Select PDF:",
                list(st.session_state.pdf_files.keys()),
                key="preview_pdf"
            )
        
        if selected_pdf:
            pdf_bytes = st.session_state.pdf_files[selected_pdf]
            
            # Read PDF info
            reader = PdfReader(io.BytesIO(pdf_bytes))
            total_pages = len(reader.pages)
            
            with col2:
                page_num = st.number_input(
                    "Page number:",
                    min_value=1,
                    max_value=total_pages,
                    value=1,
                    key="page_input"
                )
            
            st.info(f"Total pages: {total_pages}")
            
            # Generate preview image
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(pdf_bytes)
                tmp_path = tmp.name
            
            try:
                images = convert_from_path(tmp_path, first_page=page_num, last_page=page_num, dpi=150)
                if images:
                    st.image(images[0], caption=f"Page {page_num}/{total_pages}", use_column_width=True)
            except Exception as e:
                st.error(f"Preview error: {e}")
            finally:
                Path(tmp_path).unlink(missing_ok=True)
    else:
        st.info("📤 Upload a PDF file to preview")

# Tab 2: Extract Text
with tab2:
    st.header("Extract Text from PDF")
    
    if st.session_state.get("pdf_files"):
        selected_pdf = st.selectbox(
            "Select PDF:",
            list(st.session_state.pdf_files.keys()),
            key="extract_pdf"
        )
        
        pdf_bytes = st.session_state.pdf_files[selected_pdf]
        reader = PdfReader(io.BytesIO(pdf_bytes))
        total_pages = len(reader.pages)
        
        col1, col2 = st.columns(2)
        with col1:
            page_range = st.text_input(
                "Page ranges (e.g., '1,3-5'):",
                value="1-3",
                help="Leave empty to extract all pages"
            )
        
        with col2:
            if st.button("🔄 Extract", key="extract_btn"):
                try:
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp.write(pdf_bytes)
                        tmp_path = tmp.name
                    
                    with pdfplumber.open(tmp_path) as doc:
                        indexes = parse_page_ranges(page_range or None, len(doc.pages))
                        texts = []
                        for idx in indexes:
                            text = doc.pages[idx].extract_text() or ""
                            texts.append(text)
                    
                    combined_text = "\n\n".join(texts)
                    
                    st.text_area("Extracted Text:", value=combined_text, height=400)
                    
                    st.download_button(
                        label="💾 Download as TXT",
                        data=combined_text,
                        file_name=f"{Path(selected_pdf).stem}_extracted.txt",
                        mime="text/plain"
                    )
                    
                    Path(tmp_path).unlink(missing_ok=True)
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("📤 Upload a PDF file to extract text")

# Tab 3: Split Pages
with tab3:
    st.header("Split PDF Pages")
    
    if st.session_state.get("pdf_files"):
        selected_pdf = st.selectbox(
            "Select PDF:",
            list(st.session_state.pdf_files.keys()),
            key="split_pdf"
        )
        
        pdf_bytes = st.session_state.pdf_files[selected_pdf]
        reader = PdfReader(io.BytesIO(pdf_bytes))
        total_pages = len(reader.pages)
        
        page_range = st.text_input(
            "Page ranges to keep (e.g., '1,3-5'):",
            value="1-2",
            help=f"Total pages: {total_pages}"
        )
        
        if st.button("✂️ Split PDF", key="split_btn"):
            try:
                indexes = parse_page_ranges(page_range, total_pages)
                writer = PdfWriter()
                for idx in indexes:
                    writer.add_page(reader.pages[idx])
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                st.success(f"✅ Split {len(indexes)} page(s)")
                st.download_button(
                    label="💾 Download Split PDF",
                    data=output.getvalue(),
                    file_name=f"{Path(selected_pdf).stem}_split.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("📤 Upload a PDF file to split")

# Tab 4: Merge PDFs
with tab4:
    st.header("Merge Multiple PDFs")
    
    if st.session_state.get("pdf_files") and len(st.session_state.pdf_files) > 1:
        st.write("Select PDFs in order to merge:")
        
        pdf_names = list(st.session_state.pdf_files.keys())
        selected_pdfs = st.multiselect(
            "PDFs to merge:",
            pdf_names,
            default=pdf_names[:min(2, len(pdf_names))],
            key="merge_pdfs"
        )
        
        # Reorder PDFs using drag-friendly interface
        if selected_pdfs:
            st.write("Merge order (top to bottom):")
            merge_order = st.column_config.CheckboxColumn(
                "Include"
            )
            
            ordered_pdfs = st.multiselect(
                "Final merge order:",
                selected_pdfs,
                default=selected_pdfs,
                help="Reorder if needed"
            )
            
            if st.button("🔀 Merge PDFs", key="merge_btn"):
                try:
                    writer = PdfWriter()
                    for pdf_name in ordered_pdfs:
                        pdf_bytes = st.session_state.pdf_files[pdf_name]
                        reader = PdfReader(io.BytesIO(pdf_bytes))
                        for page in reader.pages:
                            writer.add_page(page)
                    
                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    
                    st.success(f"✅ Merged {len(ordered_pdfs)} PDF(s)")
                    st.download_button(
                        label="💾 Download Merged PDF",
                        data=output.getvalue(),
                        file_name="merged_output.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
    elif len(st.session_state.get("pdf_files", {})) == 1:
        st.warning("⚠️ Upload at least 2 PDFs to merge")
    else:
        st.info("📤 Upload multiple PDF files to merge")

# Tab 5: Info & Metadata
with tab5:
    st.header("PDF Information")
    
    if st.session_state.get("pdf_files"):
        selected_pdf = st.selectbox(
            "Select PDF:",
            list(st.session_state.pdf_files.keys()),
            key="info_pdf"
        )
        
        pdf_bytes = st.session_state.pdf_files[selected_pdf]
        reader = PdfReader(io.BytesIO(pdf_bytes))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pages", len(reader.pages))
        with col2:
            st.metric("Encrypted", reader.is_encrypted)
        with col3:
            file_size_kb = len(pdf_bytes) / 1024
            st.metric("File Size", f"{file_size_kb:.1f} KB")
        
        st.subheader("Metadata")
        if reader.metadata:
            for key, value in reader.metadata.items():
                st.write(f"**{key.lstrip('/')}:** {value}")
        else:
            st.info("No metadata found")
    else:
        st.info("📤 Upload a PDF file to view information")

# Footer
st.divider()
st.caption("PDF Reader CLI • Powered by Streamlit, PyPDF, and pdfplumber")
