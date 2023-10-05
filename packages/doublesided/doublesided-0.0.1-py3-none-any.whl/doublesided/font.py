from typing import Optional

from PIL import ImageFont
import platform
import os


def get_default_font_path():
    if platform.system() == "Windows":
        return "C:/Windows/Fonts/Arialuni.ttf"
    elif platform.system() == "Darwin":
        return "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    else:
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def find_font_path(font_name, search_path=None):
    font_exts = ['.ttf', '.otf', '.ttc']  # Supported font extensions
    if search_path is None:
        if platform.system() == "Windows":
            search_path = [
                'C:\\Windows\\Fonts'  # Windows
            ]

        elif platform.system() == "Darwin":
            search_path = [
                '/Library/Fonts',
                '/System/Library/Fonts/Supplemental',
                os.path.expanduser('~/Library/Fonts'),
            ]

        else:
            search_path = [
                '/usr/share/fonts',
                os.path.expanduser('~/.local/share/fonts'),
                os.path.expanduser('~/.fonts'),
            ]

    for font_dir in search_path:
        if not os.path.isdir(font_dir):
            continue

        for root, _, files in os.walk(font_dir):
            for font_file in files:
                font_path = os.path.join(root, font_file)
                name, ext = os.path.splitext(font_path)
                if ext.lower() in font_exts and font_name.lower() in name.lower():
                    return font_path

    return None


def get_font_or_default(font_size: int, font_path: Optional[str] = None):
    system_font_path = None
    if not font_path:
        if platform.system() == "Windows":
            system_font_path = "C:/Windows/Fonts/arial.ttf"
        elif platform.system() == "Darwin":
            system_font_path = "/Library/Fonts/Arial.ttf"
        else:
            system_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    font = None
    if font_path or system_font_path:
        font_path = font_path or system_font_path
        font = ImageFont.truetype(font_path, font_size)
    return font


def pt_to_px(pt, ppi=180):
    return int(pt * ppi / 72)


class FontSize:
    DEFAULT_PPI = 180

    @staticmethod
    def pt(_pt, ppi=180):
        return pt_to_px(_pt, ppi)

    @staticmethod
    def px(v):
        return v
