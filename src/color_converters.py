# color_converters.py

import colorsys

class Color:
    def __init__(self, rgb: tuple):
        self.raw_rgb = rgb

        # RGB
        self.rgb = f"rgb({', '.join(str(c) for c in self.raw_rgb)})"

        # HEX
        self.hex = "#{:02x}{:02x}{:02x}".format(*self.raw_rgb)

        # HSL
        h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in self.raw_rgb])
        hsl_numbers = (round(h * 360, 2), round(s * 100, 2), round(l * 100, 2))
        self.hsl = f"hsl({', '.join(str(c) + ('%' if i > 0 else '') for i, c in enumerate(hsl_numbers))})"

        # HSV
        h, s, v = colorsys.rgb_to_hsv(*[c / 255.0 for c in self.raw_rgb])
        hsv_numbers = (round(h * 360, 2), round(s * 100, 2), round(v * 100, 2))
        self.hsv = f"hsv({', '.join(str(c) + ('%' if i > 0 else '') for i, c in enumerate(hsv_numbers))})"

        self.menu_options = (
            self.rgb,
            self.hex,
            self.hsl,
            self.hsv
        )
