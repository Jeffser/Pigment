# widgets.py

from gi.repository import Gtk, Adw, Gio

import colorsys


def raw_rgb_to_hex(raw_rgb: tuple, uppercase: bool):
    hex_result = "#{:02x}{:02x}{:02x}".format(*raw_rgb)
    if uppercase:
        hex_result = hex_result.upper()
    return hex_result


def raw_rgb_to_rgb(raw_rgb: tuple, uppercase: bool):
    rgb_result = f"rgb({', '.join(str(c) for c in raw_rgb)})"
    if uppercase:
        rgb_result = rgb_result.upper()
    return rgb_result


def raw_rgb_to_hsl(raw_rgb: tuple, uppercase: bool):
    h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in raw_rgb])
    hsl_numbers = (round(h * 360, 2), round(s * 100, 2), round(l * 100, 2))
    hsl_result = f"hsl({', '.join(str(c) + ('%' if i > 0 else '') for i, c in enumerate(hsl_numbers))})"
    if uppercase:
        hsl_result = hsl_result.upper()
    return hsl_result


def raw_rgb_to_hsv(raw_rgb: tuple, uppercase: bool):
    h, s, v = colorsys.rgb_to_hsv(*[c / 255.0 for c in raw_rgb])
    hsv_numbers = (round(h * 360, 2), round(s * 100, 2), round(v * 100, 2))
    hsv_result = f"hsv({', '.join(str(c) + ('%' if i > 0 else '') for i, c in enumerate(hsv_numbers))})"
    if uppercase:
        hsv_result = hsv_result.upper()
    return hsv_result


class ColorBox(Gtk.DrawingArea):
    __gtype_name__ = 'PigmentColorBox'

    def __init__(self, rgb: tuple):
        super().__init__()
        self.rgb = rgb
        self.set_content_width(32)
        self.set_content_height(32)
        self.set_overflow(1)

        self.set_draw_func(self.draw_color)

    def draw_color(self, area, cr, width, height):
        cr.set_source_rgb(*[c / 255.0 for c in self.rgb])
        cr.rectangle(0, 0, width, height)
        cr.fill()


class ColorButtonContent(Gtk.Box):
    __gtype_name__ = 'PigmentButtonContent'

    def __init__(self, color):
        super().__init__(
            spacing=10,
            margin_end=10
        )
        self.append(ColorBox(rgb=color.raw_rgb))

        self.append(
            Gtk.Label(
                label=color.default_value
            )
        )


class ColorPopover(Gtk.Popover):
    __gtype_name__ = 'PigmentPopover'

    def __init__(self, color):
        container = Gtk.Box(
            orientation=1
        )

        super().__init__(
            has_arrow=True,
            autohide=True,
            child=container
        )

        for c in color.menu_options:
            button = Gtk.Button(
                child=Adw.ButtonContent(
                    label=c,
                    icon_name='edit-copy-symbolic',
                    hexpand=True,
                    halign=1
                ),
                css_classes=['flat', 'monospace', 'small'],
                tooltip_text=_('Copy Color')
            )
            button.connect('clicked', lambda button, text=c: self.copy(text))
            container.append(button)

    def copy(self, text):
        self.popdown()
        self.get_root().copy_requested(text)


class Color:
    def __init__(self, rgb: tuple, uppercase: bool, default_index: int):
        self.raw_rgb = rgb

        self.menu_options = [
            raw_rgb_to_hex(self.raw_rgb, uppercase),
            raw_rgb_to_rgb(self.raw_rgb, uppercase),
            raw_rgb_to_hsl(self.raw_rgb, uppercase),
            raw_rgb_to_hsv(self.raw_rgb, uppercase)
        ]

        self.default_value = self.menu_options[default_index]

        self.button = Adw.SplitButton(
            overflow=1,
            css_classes=['monospace'],
            tooltip_text=_('Copy Color'),
            child=ColorButtonContent(
                color=self
            ),
            name=self.default_value
        )

        self.button.set_popover(ColorPopover(self))
        self.button.connect('clicked', lambda button, text=self.default_value: button.get_root().copy_requested(text))
        self.button.get_child().get_parent().add_css_class('p0')

@Gtk.Template(resource_path='/com/jeffser/Pigment/preferences.ui')
class PreferencesDialog(Adw.PreferencesDialog):
    __gtype_name__ = 'PigmentPreferencesDialog'

    autogenerate_switch = Gtk.Template.Child()
    uppercase_switch = Gtk.Template.Child()
    skip_duplicated_colors_switch = Gtk.Template.Child()
    default_format_switch = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        self.settings = Gio.Settings(schema_id='com.jeffser.Pigment')

        self.settings.bind(
            'autogenerate',
            self.autogenerate_switch,
            'active',
            Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            'format-uppercase',
            self.uppercase_switch,
            'active',
            Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            'skip-duplicated-colors',
            self.skip_duplicated_colors_switch,
            'active',
            Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            'default-format',
            self.default_format_switch,
            'selected',
            Gio.SettingsBindFlags.DEFAULT
        )

