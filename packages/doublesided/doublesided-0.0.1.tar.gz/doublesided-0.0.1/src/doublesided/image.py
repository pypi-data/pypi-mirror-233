from PIL import Image, ImageDraw


def create_image(w, h):
    image = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    return image, draw


def calculate_grid_position(canvas, border_width, layout, grid_position, is_back_page=False):
    image_width, image_height = canvas
    column_count, row_count = layout
    x, y = grid_position

    if is_back_page:
        x = column_count - x - 1

    grid_width = (image_width - (column_count - 1) * border_width) // column_count
    grid_height = (image_height - (row_count - 1) * border_width) // row_count

    # Calculate grid position
    grid_pos_x = x * (grid_width + border_width)
    grid_pos_y = y * (grid_height + border_width)

    return grid_pos_x, grid_pos_y, grid_width, grid_height


def adjust_padding(grid_pos, pt=0, pl=0, pr=0, pb=0):
    grid_pos_x, grid_pos_y, grid_width, grid_height = grid_pos
    return (
        grid_pos_x + pl,
        grid_pos_y + pt,
        grid_width - pl - pr,
        grid_height - pt - pb
    )


def create_grid(draw, paper_dim, layout, grid_color='black', grid_width=10):
    image_width, image_height = paper_dim
    (column_count, row_count) = layout
    cell_width = (image_width - (grid_width * (column_count - 1))) // column_count
    cell_height = (image_height - (grid_width * (row_count - 1))) // row_count
    for i in range(column_count - 1):
        x = grid_width * i + cell_width * (i + 1)
        draw.line([(x, 0), (x, image_height)],
                  fill=grid_color,
                  width=grid_width)

    for i in range(row_count - 1):
        y = grid_width * i + cell_height * (i + 1)
        draw.line([(0, y), (image_width, y)],
                  fill=grid_color,
                  width=grid_width)
