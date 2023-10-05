import logging
import os
import textwrap
from dataclasses import dataclass, field
from typing import Optional

from PIL import ImageFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from .font import get_default_font_path
from .image import adjust_padding, create_image, calculate_grid_position, create_grid


@dataclass
class BoxStyle:
    pt: int = 0
    px: int = 0


@dataclass
class CardStyle:
    pt: int = 0
    pb: int = 0
    pl: int = 0
    pr: int = 0
    spacing: int = 0


@dataclass
class PageStyle:
    grid_border_width: int = 1


@dataclass
class CardContentBox:
    content: str
    font_size_px: int
    color: str = 'black'
    font_path: Optional[str] = field(default_factory=get_default_font_path)
    style: BoxStyle = field(default_factory=BoxStyle)

    @property
    def font(self):
        return ImageFont.truetype(self.font_path, self.font_size_px)

    def render(self, draw, placement):
        font = self.font
        box_x, box_y, box_w, box_h = placement
        max_chars_horizontally = box_w // font.getsize('x')[0]
        wrapped_text = textwrap.wrap(self.content, max_chars_horizontally)
        text_x = box_x + self.style.px
        text_y = box_y + self.style.pt

        lines = '\n'.join(wrapped_text).strip()
        draw.multiline_text(
            (text_x, text_y),
            lines,
            font=font,
            spacing=1,
            fill=self.color
        )

    def render_size(self, draw, placement):
        font = self.font
        box_x, box_y, box_w, box_h = placement
        max_chars_horizontally = box_w // font.getsize('x')[0]
        wrapped_text = textwrap.wrap(self.content, max_chars_horizontally)
        text_x = box_x + self.style.px
        text_y = box_y + self.style.pt

        lines = '\n'.join(wrapped_text).strip()
        return draw.multiline_textbbox(
            (text_x, text_y),
            lines,
            font=font,
            spacing=1,
        )


@dataclass
class CardContent:
    boxes: list[CardContentBox] = field(default_factory=list)
    style: CardStyle = field(default_factory=CardStyle)

    def render_to_grid(self, draw, draw_region):
        x, y, w, h = draw_region

        x, y, w, h = adjust_padding(
            draw_region,
            pt=self.style.pt,
            pl=self.style.pl,
            pr=self.style.pr,
            pb=self.style.pb,
        )

        most_right = x + w
        most_bottom = y + h

        cx = x
        cy = y
        for i, box in enumerate(self.boxes):
            left, top, right, bottom = box.render_size(draw, (cx, cy, w, h - cy))
            bh = bottom - top
            cy += bh
            if i != len(self.boxes) - 1:
                cy += self.style.spacing
            if cy > most_bottom:
                logging.warning('Context out of bound')

        total_height = cy - y

        cx = x
        cy = y + (h - total_height) / 2

        for i, box in enumerate(self.boxes):
            left, top, right, bottom = box.render_size(draw, (cx, cy, w, h - cy))
            box.render(draw, (cx, cy, w, h - cy))
            bh = bottom - top
            cy += bh
            if i != len(self.boxes) - 1:
                cy += self.style.spacing


@dataclass
class Card:
    front: CardContent
    back: CardContent


def divide_list(lst, k):
    return [lst[i:i + k] for i in range(0, len(lst), k)]


@dataclass
class DeckBuilder:
    dest: str
    cards: list[Card] = field(default_factory=list)
    ppi: int = 180
    row: int = 5
    col: int = 2
    paper_size: tuple[int, int] = (8.5, 11)
    style: PageStyle = field(default_factory=PageStyle)

    @property
    def png_folder(self):
        return os.path.join(self.dest, 'png')

    def front_png_file(self, page):
        return os.path.join(self.dest, 'png', f'front-{page}.png')

    def back_png_file(self, page):
        return os.path.join(self.dest, 'png', f'back-{page}.png')

    @property
    def pdf_file(self):
        return os.path.join(self.dest, 'out.pdf')

    def build(self):
        os.makedirs(self.dest, exist_ok=True)
        os.makedirs(self.png_folder, exist_ok=True)
        front_pages = []
        back_pages = []
        w, h = self.paper_size
        pw, ph = int(w * self.ppi), int(h * self.ppi)
        card_count_per_page = self.row * self.col
        total_page = 0
        for i, cards_per_page in enumerate(divide_list(self.cards, card_count_per_page)):
            total_page += 1
            front_page, front_page_draw = create_image(pw, ph)
            back_page, back_page_draw = create_image(pw, ph)
            for x in range(self.col):
                for y in range(self.row):
                    idx = self.col * y + x
                    card = cards_per_page[idx]
                    grid_pos_x, grid_pos_y, grid_width, grid_height = calculate_grid_position(
                        (pw, ph),
                        self.style.grid_border_width,
                        (self.col, self.row),
                        (x, y)
                    )
                    card.front.render_to_grid(front_page_draw, (
                        grid_pos_x, grid_pos_y, grid_width, grid_height
                    ))

                    grid_pos_x, grid_pos_y, grid_width, grid_height = calculate_grid_position(
                        (pw, ph),
                        self.style.grid_border_width,
                        (self.col, self.row),
                        (x, y),
                        is_back_page=True
                    )

                    card.back.render_to_grid(back_page_draw, (
                        grid_pos_x, grid_pos_y, grid_width, grid_height
                    ))

            # draw grid on page
            create_grid(
                front_page_draw,
                (pw, ph),
                (self.col, self.row),
                grid_width=self.style.grid_border_width
            )

            create_grid(
                back_page_draw,
                (pw, ph),
                (self.col, self.row),
                grid_width=self.style.grid_border_width
            )

            front_page.save(self.front_png_file(i))
            front_pages.append(i)
            back_page.save(self.back_png_file(i))
            back_pages.append(i)
        w_inch, h_inch = self.paper_size
        paper_size = (w_inch * inch, h_inch * inch)
        c = canvas.Canvas(
            self.pdf_file,
            pagesize=paper_size
        )
        for i in range(total_page):
            c.drawImage(self.front_png_file(i), 0, 0, paper_size[0], paper_size[1])
            c.showPage()
            c.drawImage(self.back_png_file(i), 0, 0, paper_size[0], paper_size[1])
            c.showPage()
        c.save()
