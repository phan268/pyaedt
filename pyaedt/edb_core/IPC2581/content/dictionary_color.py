import xml.etree.cElementTree as ET

from pyaedt.edb_core.IPC2581.content.entry_color import EntryColor


class DictionaryColor(object):
    def __init__(self):
        self._dict_colors = {}

    @property
    def dict_colors(self):
        return self._dict_colors

    @dict_colors.setter
    def dict_colors(self, value):
        if isinstance(value, list):
            self._dict_colors = value

    def add_color(self, value):
        if isinstance(value, EntryColor):
            self._dict_colors.append(value)

    def write_xml(self, content=None):
        if content:
            dict_color = ET.SubElement(content, "DictionaryColor")
            for color_name in self._dict_colors.keys():
                entry_color = ET.SubElement(dict_color, "EntryColor")
                entry_color.set("id", color_name)
                self._dict_colors[color_name].write_xml(entry_color)
