# 📄 pdf2docx-converter

`pdf2docx-converter` is a Python package that makes converting PDF files to Word documents (DOCX) a breeze. It leverages the power of PyMuPDF to extract text and images from PDFs and uses python-docx to create the resulting Word documents. Whether you need to transform research papers, reports, or any PDF document into an editable Word format, this package has you covered.

## Installation 🚀

Getting started with `pdf2docx-converter` is as easy as pie. Simply follow these steps:

1. **Install Python**: Make sure you have Python installed on your system. If not, you can download it from [python.org](https://www.python.org/downloads/) and follow the installation instructions for your operating system.

2. **Install pdf2docx-converter**: Open your terminal or command prompt and run the following command to install the package using pip:

   ```bash
   pip install pdf2docx-converter


## After installantion commands used in pyfile

from pdf2docx_converter import pdf_to_docx

pdf_file = "input.pdf"
docx_file = "output.docx"
pdf_to_docx(pdf_file, docx_file)
