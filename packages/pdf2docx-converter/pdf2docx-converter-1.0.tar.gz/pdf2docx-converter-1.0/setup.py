from setuptools import setup, find_packages

setup(
    name='pdf2docx-converter',
    version='1.0',
    description='A Python package to convert PDFs to Word documents (DOCX).',
    author='Vasudev Jaiswal',
    author_email='vasujaiswal00@gmail.com',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',
        'python-docx',
    ],
)
