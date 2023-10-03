import os
import PIL
from PIL import ImageFont

from viso_sdk.constants import FONTS_DIR
from viso_sdk.logging import get_logger
from viso_sdk.visualize.palette import get_rgba_color

pil_version = PIL.__version__

logger = get_logger("vis-font")

DEFAULT_FONT_SIZE = 15
# DEFAULT_THICKNESS = 1
DEFAULT_TXT_COLOR = (255, 255, 255, 1.0)
DEFAULT_SHADOW_COLOR = (0, 0, 0, 1.0)


def get_text_size(draw, text, font, xy=(10, 10)):
    # calculate area to put text
    if pil_version < "10.0.0":
        text_width, text_height = draw.textsize(text, font)
    else:
        # Get the bounding box of the text
        bbox = draw.textbbox(xy, text, font=font)

        # Calculate the dimensions of the bounding box
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    return text_width, text_height


def get_supported_fonts(fonts_dir=FONTS_DIR):
    font_names = [os.path.splitext(fn)[0] for fn in os.listdir(fonts_dir) if os.path.splitext(fn)[1] == '.ttf']
    return font_names


class VizTextDraw:
    def __init__(self,
                 font: str = None,
                 font_size: int = DEFAULT_FONT_SIZE,
                 # thickness: int = DEFAULT_THICKNESS,
                 font_color=DEFAULT_TXT_COLOR,
                 shadow_color=DEFAULT_SHADOW_COLOR,
                 verbose=False):

        self.verbose = verbose

        if font_size is None:
            font_size = DEFAULT_FONT_SIZE
        self.font = self.init_font(font_name=font,
                                   font_size=font_size)
        if font_color is None:
            font_color = DEFAULT_TXT_COLOR
        self.default_txt_color = get_rgba_color(font_color)

        if shadow_color is None:
            shadow_color = DEFAULT_SHADOW_COLOR
        self.default_shadow_color = get_rgba_color(shadow_color)

    def init_font(self, font_name, font_size):
        fonts = get_supported_fonts(FONTS_DIR)
        if font_name is None:
            if self.verbose:
                logger.warning(f"font_name is not specified, use default {fonts[0]}")
            font_name = fonts[0]
            font_file = os.path.join(FONTS_DIR, f"{font_name}.ttf")
        elif os.path.isabs(font_name) and os.path.exists(font_name):
            font_file = font_name
        elif font_name not in fonts:
            if self.verbose:
                logger.warning(f"can not fine such font file {font_name}, use default {fonts[0]}")
            font_name = fonts[0]
            font_file = os.path.join(FONTS_DIR, f"{font_name}.ttf")
        else:
            if self.verbose:
                logger.warning(f"Use default {fonts[0]}")
            font_name = fonts[0]
            font_file = os.path.join(FONTS_DIR, f"{font_name}.ttf")

        if self.verbose:
            logger.info(f"load font {font_name}")
        font = ImageFont.truetype(font_file, font_size)
        return font

    def draw_texts(
            self,
            draw,
            text,
            txt_color=None,
            pos=(50, 50),  # left-lower
            large_padding=False,
            fill_rectangle=False, fill_rectangle_color=None,
            show_shadow=False, shadow_color=None):

        text_width, text_height = get_text_size(draw=draw, text=text, font=self.font, xy=pos)

        padding = max(int(text_height // 4), 2)
        padding_left = padding
        if large_padding:
            padding_top = padding * 2
        else:
            padding_top = padding // 2

        x, y = pos  # bottom left of text = top left of bbox
        x0 = x
        y0 = y - text_height - padding_top
        y1 = y
        x1 = x + text_width + padding_left * 2

        if fill_rectangle:
            # put filled text rectangle
            draw.rectangle([(x0, y0), (x1, y1)],
                           fill=fill_rectangle_color)

        # shadow effect
        if show_shadow:
            if shadow_color is None:
                shadow_color = self.default_shadow_color
            draw.multiline_text((x0 + padding_left + 1, y0 - padding_top + 1),
                                font=self.font, text=text, fill=shadow_color)

        # put text above rectangle
        if txt_color is None:
            txt_color = self.default_txt_color
        draw.multiline_text((x0 + padding_left, y0 - padding_top),
                            font=self.font, text=text, fill=txt_color)

        return draw
