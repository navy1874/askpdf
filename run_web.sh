#!/usr/bin/env bash
# Streamlit 启动脚本
/home/coff/.virtualenvs/py3/bin/streamlit run /home/coff/pdfReader/src/pdf_reader/app.py \
    --logger.level=error \
    --server.headless=false
