import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black

from PIL import Image


def draw_wrapped_text(
    c,
    text,
    x,
    y,
    max_width,
    font="Helvetica",
    font_size=12,
    line_height=18
):

    c.setFont(
        font,
        font_size
    )

    words = text.split()

    line = ""

    lines = []

    for word in words:

        test_line = (
            line + " " + word
        ).strip()

        if c.stringWidth(
            test_line,
            font,
            font_size
        ) <= max_width:

            line = test_line

        else:

            if line:
                lines.append(line)

            line = word

    if line:
        lines.append(line)

    current_y = y

    for line in lines:

        c.drawString(
            x,
            current_y,
            line
        )

        current_y -= line_height

    return current_y


def create_storybook_pdf(
    title,
    pages,
    output_path,
    character_name,
    moral
):

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    c = canvas.Canvas(
        output_path,
        pagesize=A4
    )

    width, height = A4

    # =====================================
    # COVER
    # =====================================

    c.setFillColorRGB(
        0.92,
        0.95,
        1.0
    )

    c.rect(
        0,
        0,
        width,
        height,
        fill=1,
        stroke=0
    )

    c.setFillColor(
        black
    )

    c.setFont(
        "Helvetica-Bold",
        28
    )

    c.drawCentredString(
        width / 2,
        height - 150,
        title
    )

    c.setFont(
        "Helvetica",
        14
    )

    c.drawCentredString(
        width / 2,
        height - 190,
        "An AI-Generated Children's Storybook"
    )

    c.setFont(
        "Helvetica",
        12
    )

    c.drawCentredString(
        width / 2,
        100,
        f"Main Character: {character_name}"
    )

    c.showPage()

    # =====================================
    # STORY PAGES
    # =====================================

    for page in pages:

        image_path = page.get(
            "image_path"
        )

        text = page.get(
            "text",
            ""
        )

        page_number = page.get(
            "page_number"
        )

        c.setFillColor(
            black
        )

        c.setFont(
            "Helvetica-Bold",
            18
        )

        c.drawString(
            50,
            height - 50,
            f"Page {page_number}"
        )

        # -------------------------------
        # IMAGE
        # -------------------------------

        if image_path and os.path.exists(
            image_path
        ):

            try:

                img = Image.open(
                    image_path
                )

                img_width, img_height = (
                    img.size
                )

                max_width = width - 80
                max_height = 360

                scale = min(
                    max_width / img_width,
                    max_height / img_height
                )

                display_width = (
                    img_width * scale
                )

                display_height = (
                    img_height * scale
                )

                x = (
                    width - display_width
                ) / 2

                y = (
                    height
                    - display_height
                    - 80
                )

                c.drawImage(
                    ImageReader(img),
                    x,
                    y,
                    width=display_width,
                    height=display_height,
                    preserveAspectRatio=True,
                    mask="auto"
                )

            except Exception:
                pass

        # -------------------------------
        # STORY TEXT
        # -------------------------------

        draw_wrapped_text(
            c,
            text,
            50,
            130,
            width - 100,
            font="Helvetica",
            font_size=12,
            line_height=18
        )

        c.showPage()

    # =====================================
    # FINAL MORAL PAGE
    # =====================================

    c.setFont(
        "Helvetica-Bold",
        22
    )

    c.drawCentredString(
        width / 2,
        height - 150,
        "🌟 Moral of the Story"
    )

    draw_wrapped_text(
        c,
        moral,
        70,
        height - 220,
        width - 140,
        font="Helvetica",
        font_size=14,
        line_height=22
    )

    c.showPage()

    c.save()

    return output_path