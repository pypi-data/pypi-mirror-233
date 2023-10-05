from PIL import Image, ImageDraw
from .font import get_font_or_default


def suggest_layout(paper_size):
    pass


def layout_text_list(canvas, text_list, font_size, align='center', spacing_between_text=1.0, font_path=None, spacing=4,
                     text_width=50, colors=None, padding=0):
    # image, draw = create_draw(canvas)

    font = get_font_or_default(font_path, font_size)
    # boxes_size = compute_text_box_sizes(draw, text_list, font, text_width)
    #
    # sep_height = font_size * spacing_between_text
    # it_y = padding
    # for box in boxes_size:
    #     if not can_box_fit(canvas, box, it_y, padding):
    #         raise ValueError('Text cannot fit')
    #     it_y += box[1]
    #     it_y += spacing_between_text * font_size
    #
    # it_y = padding
    # for idx, (box, text) in enumerate(zip(boxes_size, text_list)):
    #     color = colors[idx] if colors is not None else 'black'
    #     if align == 'center':
    #         bx0 = centering_x_position(canvas, box, padding)
    #         print(canvas, box, bx0)
    #     elif align == 'right':
    #         bx0 = canvas[0] - box[0] - padding
    #     elif align == 'left':
    #         bx0 = padding
    #     lines = textwrap.wrap(text, width=text_width)
    #     lines = '\n'.join(lines)
    #     draw.multiline_text((bx0, it_y), lines, font=font, spacing=spacing, fill=color)
    #     it_y += box[1]
    #     it_y += spacing_between_text * font_size
    # return image, draw


def create_stacked_image(width, height, string_list):
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font_size = 1
    font_path = None

    success_font = None

    while True:
        font = get_font_or_default(font_path, font_size)

        lines = []
        for string in string_list:
            text_bbox = draw.multiline_textbbox((0, 0), string, font=font, spacing=4)
            left, top, right, bottom = text_bbox
            if text_bbox[3] <= height:
                lines.append(string)

        if len(lines) == len(string_list):
            success_font = font
        else:
            break

        font_size += 1

    line_height = draw.multiline_textsize("\n".join(lines), font=font, spacing=4)[1]
    total_height = len(lines) * line_height

    y = (height - total_height) // 2
    for line in lines:
        text_width, text_height = draw.multiline_textsize(line, font=font, spacing=4)
        x = (width - text_width) // 2
        draw.multiline_text((x, y), line, font=font, fill=(0, 0, 0), spacing=4, align="center")
        y += line_height

    return image
