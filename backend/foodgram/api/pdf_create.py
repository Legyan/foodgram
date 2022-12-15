from borb.pdf import (Alignment, Barcode, BarcodeType,
                      Document, Page, PageLayout, Paragraph,
                      PDF, OrderedList, SingleColumnLayout)
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont

from datetime import datetime
from decimal import Decimal
import io
from math import ceil
from pathlib import Path


def add_info(page, pages=1, page_num=1):
    font_path = Path(__file__).parent.parent / 'data/fonts/Times New Roman.ttf'
    font = TrueTypeFont.true_type_font_from_file(font_path)
    r = Rectangle(
        Decimal(50),
        Decimal(848 - 720 - 100),
        Decimal(595 - 45 * 2),
        Decimal(100),
    )
    r_text = Rectangle(
        Decimal(180),
        Decimal(848 - 680 - 100),
        Decimal(595 - 180 * 2),
        Decimal(30),
    )
    Barcode(
        "http://158.160.13.152/recipes",
        width=Decimal(96),
        height=Decimal(96),
        type=BarcodeType.QR,
        horizontal_alignment=Alignment.RIGHT,

    ).paint(page, r)
    Paragraph(
        'Список сформирован с помощью сервиса Foodgram',
        font=font,
        font_size=10,
        vertical_alignment=Alignment.TOP,
        horizontal_alignment=Alignment.CENTERED,
    ).paint(page, r_text)
    Paragraph(
        'http://158.160.13.152',
        font=font,
        font_size=10,
        vertical_alignment=Alignment.BOTTOM,
        horizontal_alignment=Alignment.CENTERED,
    ).paint(page, r_text)
    if pages > 1:
        Paragraph(
            f'{page_num} (из {pages})',
            font=font,
            font_size=10,
            vertical_alignment=Alignment.BOTTOM,
            horizontal_alignment=Alignment.CENTERED,
        ).paint(page, r)


def add_orderlist(lines, first_page, font, doc, pages=1, page_num=1):
    layout: PageLayout = SingleColumnLayout(first_page)
    order_list = OrderedList()
    if len(lines) <= 43:
        for line in lines:
            order_list.add(Paragraph(line, font=font))
        layout.add(order_list)
    else:
        for line in lines[:43]:
            order_list.add(Paragraph(line, font=font))
        page = Page()
        doc.add_page(page)
        add_orderlist(
            lines[43:], page, font, doc, pages, page_num=page_num + 1
        )
        add_info(page, pages, page_num=page_num + 1)
        layout.add(order_list)


def shopping_list_pdf(lines):
    doc = Document()
    page = Page()
    doc.add_page(page)
    r = Rectangle(
        Decimal(59),
        Decimal(848 - 60 - 100),
        Decimal(595 - 59 * 2),
        Decimal(100),
    )
    font_path = Path(__file__).parent.parent / 'data/fonts/Helvetica.ttf'
    font = TrueTypeFont.true_type_font_from_file(font_path)
    pages = ceil(len(lines) / 43)
    date = datetime.now()
    Paragraph(
        f'Список покупок от {date.day}.{date.month}.{date.year}',
        horizontal_alignment=Alignment.CENTERED,
        font=font,
        font_size=16
    ).paint(page, r)
    add_info(page, pages)
    add_orderlist(lines, page, font, doc, pages)
    buffer = io.BytesIO()
    PDF.dumps(buffer, doc)
    return buffer.getvalue()
