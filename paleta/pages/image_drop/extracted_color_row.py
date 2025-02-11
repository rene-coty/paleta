from gi.repository import Gtk, Gdk, GObject

from paleta.util import rgb_to_hex

import re

@Gtk.Template(resource_path='/io/github/nate_xyz/Paleta/extracted_color_row.ui')
class ExtractedColorRow(Gtk.ListBoxRow):
    __gtype_name__ = 'ExtractedColorRow'

    row_box = Gtk.Template.Child(name="row_box")
    hex_name_label = Gtk.Template.Child(name="hex_name_label")
    rgb_name_label = Gtk.Template.Child(name="rgb_name_label")
    copy_icon = Gtk.Template.Child(name="copy_icon")

    def __init__(self, color) -> None:
        super().__init__()
        self.load_color(color)
        
        ctrl = Gtk.EventControllerMotion()
        ctrl.connect("enter", lambda _controller, _x, _y: self.copy_icon.show())
        ctrl.connect("leave", lambda _controller: self.copy_icon.hide())
        self.add_controller(ctrl)
        
    def load_color(self, color):
        rgba = Gdk.RGBA()
        success = rgba.parse(color.rgb_name)
        if success:
            color_button = Gtk.ColorButton.new_with_rgba(rgba)
            color_button.connect('color-set', self.set_from_button)
            color_button.props.show_editor = True
            self.row_box.prepend(color_button)
        
        self.hex_name_label.set_label(color.hex_name)
        self.rgb_name_label.set_label(color.rgb_name)

        self.hex_name = color.hex_name

    def set_from_button(self, button):
        new_color = button.get_rgba()
        rgb_name = new_color.to_string()
        self.rgb_name_label.set_label(rgb_name)
        rgb = [int(i) for i in re.search('\(([^)]+)', rgb_name).group(1).split(',')]
        self.hex_name = rgb_to_hex(*rgb)
        self.hex_name_label.set_label("#{}".format(self.hex_name))


class ExtractedColor(GObject.GObject):
    __gtype_name__ = "ExtractedColor"

    def __init__(self, rgb_tuble) -> None:
        super().__init__()
        self.add_rgb(rgb_tuble)
    
    def add_rgb(self, rgb_tuble):
        self.rgb = rgb_tuble
        self.rgb_name = "rgb{}".format(rgb_tuble)
        self.hex_name = "#{}".format(rgb_to_hex(*rgb_tuble))

