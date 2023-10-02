import asyncio
import os
import tempfile

import concurrent.futures

import nbformat
import nbconvert

from pyppeteer import launch

from traitlets import Bool, default

import PyPDF2

from nbconvert.exporters import HTMLExporter
from nbconvert.exporters import TemplateExporter


async def html_to_pdf(html_file, pdf_file, pyppeteer_args=None):
    browser = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        args=pyppeteer_args or [],
    )
    page = await browser.newPage()
    await page.setViewport(dict(width=994, height=768))
    await page.emulateMedia("screen")

    await page.goto(f"file:///{html_file}", {"waitUntil": ["networkidle2"]})

    page_margins = {
        "left": "0px",
        "right": "0px",
        "top": "0px",
        "bottom": "0px",
    }

    dimensions = await page.evaluate(
        """() => {
        return {
            width: document.body.scrollWidth,
            height: document.body.scrollHeight,
            offsetWidth: document.body.offsetWidth,
            offsetHeight: document.body.offsetHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }"""
    )
    width = dimensions["width"]
    height = dimensions["height"]

    await page.evaluate(
        """
    function getOffset( el ) {
        var _x = 0;
        var _y = 0;
        while( el && !isNaN( el.offsetLeft ) && !isNaN( el.offsetTop ) ) {
            _x += el.offsetLeft - el.scrollLeft;
            _y += el.offsetTop - el.scrollTop;
            el = el.offsetParent;
        }
        return { top: _y, left: _x };
        }
    """,
        force_expr=True,
    )

    await page.addStyleTag(
        {
            "content": """
                #notebook-container {
                    box-shadow: none;
                    padding: unset
                }
                div.cell {
                    page-break-inside: avoid;
                }
                div.output_wrapper {
                    page-break-inside: avoid;
                }
                div.output {
                    page-break-inside: avoid;
                }
                /* Jupyterlab based HTML uses these classes */
                .jp-Cell-inputWrapper {
                    page-break-inside: avoid;
                }
                .jp-Cell-outputWrapper {
                    page-break-inside: avoid;
                }
                .jp-Notebook {
                    margin: 0px;
                }
                /* Hide the message box used by MathJax */
                #MathJax_Message {
                    display: none;
                }
         """
        }
    )

    await page.pdf(
        {
            "path": pdf_file,
            # Adobe can not display pages longer than 200 inches. So we limit
            # ourselves to that and start a new page if needed.
            "width": min(width + 2, 200 * 72),
            "height": min(height + 2, 200 * 72),
            "printBackground": True,
            "margin": page_margins,
        }
    )

    headings = await page.evaluate(
        """() => {
        var vals = []
        for (const elem of document.getElementsByTagName("h1")) {
            vals.push({ top: getOffset(elem).top * (1-72/288), text: elem.innerText })
        }
        for (const elem of document.getElementsByTagName("h2")) {
            vals.push({ top: getOffset(elem).top * (1-72/288), text: "∙ " + elem.innerText })
        }
        return vals
    }"""
    )

    await browser.close()

    return headings


def finish_pdf(pdf_in, pdf_out, notebook, headings):
    pdf = PyPDF2.PdfWriter()
    pdf.append_pages_from_reader(PyPDF2.PdfReader(pdf_in))
    pdf.add_attachment(notebook["file_name"], notebook["contents"])

    for heading in sorted(headings, key=lambda x: x["top"]):
        page_num = int(heading["top"]) // (200 * 72)

        pdf.add_outline_item(
            heading["text"],
            page_number=page_num
        )

    with open(pdf_out, "wb") as fp:
        pdf.write(fp)


async def notebook_to_pdf(
    html_notebook, pdf_path, pyppeteer_args=None,
):
    with tempfile.NamedTemporaryFile(suffix=".html") as f:
        f.write(html_notebook.encode())
        f.flush()
        heading_positions = await html_to_pdf(f.name, pdf_path, pyppeteer_args)

    return heading_positions


class PDFExporter(TemplateExporter):
    enabled = True
    pool = concurrent.futures.ThreadPoolExecutor()
    export_from_notebook = "PDF via HTML"

    @default("file_extension")
    def _file_extension_default(self):
        return ".pdf"

    template_extension = ".html.j2"
    output_mimetype = "application/pdf"

    no_sandbox = Bool(True, help=("Disable chrome sandboxing."),).tag(config=True)

    def from_notebook_node(self, notebook, resources=None, **kwargs):
        notebook_copy = notebook.copy()
        for cell in notebook_copy.cells:
            if cell.cell_type == 'code':
                cell.outputs = []

        html_exporter = HTMLExporter(config=self.config, parent=self)
        html_notebook, resources = html_exporter.from_notebook_node(
            notebook_copy, resources=resources, **kwargs
        )

        if resources.get("ipywidgets_base_url", "") == "":
            resources["ipywidgets_base_url"] = "https://unpkg.com/"

        with tempfile.TemporaryDirectory(suffix="nb-as-pdf") as name:
            pdf_fname = os.path.join(name, "output.pdf")
            pdf_fname2 = os.path.join(name, "output-with-attachment.pdf")
            pyppeteer_args = ["--no-sandbox"] if self.no_sandbox else None

            heading_positions = self.pool.submit(
                asyncio.run,
                notebook_to_pdf(
                    html_notebook, pdf_fname, pyppeteer_args=pyppeteer_args,
                ),
            ).result()
            resources["output_extension"] = ".pdf"

            finish_pdf(
                pdf_fname,
                pdf_fname2,
                {
                    "file_name": f"{resources['metadata']['name']}.ipynb",
                    "contents": nbformat.writes(notebook_copy).encode("utf-8"),
                },
                heading_positions,
            )

            with open(pdf_fname2, "rb") as f:
                pdf_bytes = f.read()

        self.output_mimetype = "application/pdf"

        return (pdf_bytes, resources)
