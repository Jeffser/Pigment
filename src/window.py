# window.py
#
# Copyright 2025 Jeffry Samuel Eduarte Rojas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, Gio, Gdk, GLib

import os, threading
from colorthief import ColorThief

from .widgets import Color


@Gtk.Template(resource_path='/com/jeffser/Pigment/window.ui')
class PigmentWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'PigmentWindow'

    main_stack = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    picture_overlay = Gtk.Template.Child()
    palette_stack = Gtk.Template.Child()
    palette_container = Gtk.Template.Child()

    preference_quality = Gtk.Template.Child()
    preference_number = Gtk.Template.Child()

    preferences_dialog = Gtk.Template.Child()
    autogenerate_switch = Gtk.Template.Child()
    uppercase_switch = Gtk.Template.Child()
    default_format_switch = Gtk.Template.Child()

    image_mimetypes = (
        'image/png',
        'image/jpeg',
        'image/gif',
        'image/webp',
        'image/bmp',
        'image/tiff'
    )

    def get_image_filter(self) -> Gtk.FileFilter:
        file_filter = Gtk.FileFilter()
        file_filter.set_name(_("Image files"))
        for mime in self.image_mimetypes:
            file_filter.add_mime_type(mime)
        return file_filter

    def copy_requested(self, text:str):
        Gdk.Display().get_default().get_clipboard().set(text)
        self.toast_overlay.add_toast(
            Adw.Toast(
                title=_('Palette copied to clipboard.') if '\n' in text else _('Color copied to clipboard.'),
                timeout=1
            )
        )

    def copy_all_requested(self):
        colors = []
        for widget in list(self.palette_container.get_child()):
            colors.append(widget.get_name())
        self.copy_requested('\n'.join(colors))

    def on_generate(self, palette:list):
        wbox = Adw.WrapBox(
            child_spacing=10,
            line_spacing=10,
            justify=1,
            justify_last_line=1
        )
        for c in palette:
            color = Color(
                rgb=c,
                uppercase=self.settings.get_value('format-uppercase').unpack(),
                default_index=self.settings.get_value('default-format').unpack()
            )
            GLib.idle_add(wbox.append, color.button)
        GLib.idle_add(self.palette_container.set_child, wbox)

    def generate_requested(self):
        GLib.idle_add(self.get_application().lookup_action('upload').set_enabled, False)
        GLib.idle_add(self.get_application().lookup_action('generate').set_enabled, False)
        GLib.idle_add(self.get_application().lookup_action('copy_all').set_enabled, False)
        GLib.idle_add(self.palette_stack.set_visible_child_name, 'loading')
        GLib.idle_add(self.palette_container.set_child, None)
        picture = self.picture_overlay.get_child().get_file()
        if picture and picture.get_path():
            quality = int(self.preference_quality.get_value())
            number = int(self.preference_number.get_value())
            ct_picture = ColorThief(picture.get_path())
            if ct_picture:
                palette = ct_picture.get_palette(
                    color_count=1+number,
                    quality=11-quality
                )
                if palette and len(palette) > 0:
                    self.on_generate(palette[:number])
        GLib.idle_add(self.get_application().lookup_action('upload').set_enabled, True)
        GLib.idle_add(self.get_application().lookup_action('generate').set_enabled, True)
        GLib.idle_add(self.get_application().lookup_action('copy_all').set_enabled, True)
        GLib.idle_add(self.palette_stack.set_visible_child_name, 'content')

    def on_upload(self, file:Gio.File):
        if file.get_path():
            mimetype = file.query_info('standard::content-type', Gio.FileQueryInfoFlags.NONE, None).get_content_type()
            if mimetype in self.image_mimetypes:
                self.picture_overlay.get_child().set_file(file)
                self.main_stack.set_visible_child_name('content')
                if bool(self.settings.get_value('autogenerate').unpack()):
                    threading.Thread(target=self.generate_requested).start()
                else:
                    self.palette_stack.set_visible_child_name('no-content')
                    self.palette_container.set_child(None)

    def upload_requested(self):
        def open_finish_wrapper(dialog, result):
            try:
                self.on_upload(dialog.open_finish(result))
            except GLib.GError as e:
                pass

        filter_list = Gio.ListStore.new(Gtk.FileFilter)
        filter_list.append(self.get_image_filter())

        Gtk.FileDialog(
            filters=filter_list
        ).open(
            self,
            None,
            lambda dialog, result: open_finish_wrapper(dialog, result) if result else None
        )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_application().create_action('upload', lambda *_: self.upload_requested(), ['<primary>U'])
        self.get_application().create_action('generate', lambda *_: threading.Thread(target=self.generate_requested).start(), ['<primary>R'])
        self.get_application().create_action('preferences', lambda *_: self.preferences_dialog.present(self), ['<primary>comma'])
        self.get_application().create_action('copy_all', lambda *_: self.copy_all_requested())
        self.get_application().lookup_action('copy_all').set_enabled(False)

        for widget in (self.picture_overlay.get_parent(), self.main_stack.get_child_by_name('welcome')):
            drop_target = Gtk.DropTarget.new(
                type=Gio.File,
                actions=Gdk.DragAction.COPY
            )
            drop_target.connect("drop", lambda target, file, x, y: self.on_upload(file))
            widget.add_controller(drop_target)


        self.settings = Gio.Settings(schema_id='com.jeffser.Pigment')
        for setting in ('default-width', 'default-height', 'maximized'):
            self.settings.bind(
                setting,
                self,
                setting,
                Gio.SettingsBindFlags.DEFAULT
            )

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
            'default-format',
            self.default_format_switch,
            'selected',
            Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            'color-quality',
            self.preference_quality,
            'value',
            Gio.SettingsBindFlags.DEFAULT
        )

        self.settings.bind(
            'color-number',
            self.preference_number,
            'value',
            Gio.SettingsBindFlags.DEFAULT
        )

