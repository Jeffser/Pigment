# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import PigmentWindow


class PigmentApplication(Adw.Application):
    __gtype_name__ = 'PigmentApplication'

    def __init__(self, version):
        super().__init__(application_id='com.jeffser.Pigment',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/com/jeffser/Pigment')
        self.version = version
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = PigmentWindow(application=self)
        win.present()

    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name='Pigment',
                                application_icon='com.jeffser.Pigment',
                                developer_name='Jeffry Samuel Eduarte Rojas',
                                version=self.version,
                                developers=['Jeffry Samuel Eduarte Rojas https://github.com/Jeffser'],
                                copyright='© 2025 Jeffry Samuel Eduarte Rojas\nBased on Color Thief')
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    app = PigmentApplication(version)
    return app.run(sys.argv)
