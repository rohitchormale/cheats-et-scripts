"""
pip install pdf2docx
"""


from pdf2docx import Converter


pdf_file = "foo.pdf"
docx_file = "foo.docx"

cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close()