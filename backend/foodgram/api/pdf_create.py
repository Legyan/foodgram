from pathlib import Path
from borb.pdf import Document
from borb.pdf import Page, PageLayout
from borb.pdf import Paragraph
from borb.pdf import PDF
from borb.pdf import OrderedList
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf import Alignment
from borb.pdf.canvas.layout.annotation import square_annotation
from borb.pdf import HexColor
from borb.pdf import SingleColumnLayout
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont

from decimal import Decimal
import io


def shopping_list_pdf(lines):

    doc = Document()

    page = Page()

    doc.add_page(page)

    r = Rectangle(
        Decimal(59),
        Decimal(848 - 84 - 100),
        Decimal(595 - 59 * 2),
        Decimal(100),
    )

    page.add_annotation(
        square_annotation.SquareAnnotation(
            r, stroke_color=HexColor("#ff0000")
        )
    )
    print(Path(__file__).parent)
    font_path = Path(__file__).parent.parent / "data/fonts/Times New Roman.ttf"
    font = TrueTypeFont.true_type_font_from_file(font_path)

    Paragraph(
        "Список покупок",
        horizontal_alignment=Alignment.CENTERED,
        font=font,
        font_size=16
    ).paint(page, r)

    layout: PageLayout = SingleColumnLayout(page)

    order_list = OrderedList()

    for line in lines:
        order_list.add(Paragraph(line, font=font))

    layout.add(order_list)
    buffer = io.BytesIO()
    PDF.dumps(buffer, doc)
    buffer.seek(0)
    return buffer.getvalue()


if __name__ == "__main__":
    lines = ['Хлеб', 'Молоко', 'Чай']
    print(shopping_list_pdf(lines))
