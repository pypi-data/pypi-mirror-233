import os
from setuptools import find_packages, setup


HERE = os.path.dirname(__file__)

with open(os.path.join(HERE, "README.md"), encoding="utf8") as f:
    readme = f.read()

setup(
    author="Abirami R",
    version="0.5.1",
    description="Jupyter extension to export notebooks as PDFs",
    install_requires=["nbconvert", "pyppeteer", "PyPDF2"],
    keywords="jupyter pdf export bundler",
    license="BSD3",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="notebook-as-pdf-updated",
    packages=find_packages(),
    python_requires=">=3.7",
    url="https://github.com/betatim/notebook-as-pdf",
    entry_points={
        # One entry for nbconvert 5.x and the second one for newer releases
        "nbconvert.exporters": [
            "PDFviaHTML = notebook_as_pdf:PDFExporter",
            "pdfviahtml = notebook_as_pdf:PDFExporter",
        ]
    },
)
