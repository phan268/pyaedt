import xml.etree.cElementTree as ET

from pyaedt.edb_core.IPC2581.ecad.cad_data.padstack_def.drill import Drill
from pyaedt.edb_core.IPC2581.ecad.cad_data.padstack_def.padstack_def import PadstackDef
from pyaedt.edb_core.IPC2581.ecad.cad_data.padstack_def.padstack_instance import PadstackInstance
from pyaedt.edb_core.IPC2581.ecad.cad_data.primitives.path import Path
from pyaedt.edb_core.IPC2581.ecad.cad_data.primitives.polygon import Polygon


class Feature(object):
    def __init__(self):
        self.feature_type = self.FeatureType().Polygon
        self.net = ""
        self.x = 0.0
        self.y = 0.0
        self.polygon = Polygon()
        self._cutouts = []
        self.path = Path()
        self.pad = PadstackDef()
        self.padstack_instance = PadstackInstance()
        self.drill = Drill()

    @property
    def cutouts(self):
        return self._cutouts

    @cutouts.setter
    def cutouts(self, value):
        if isinstance(value, list):
            if len([poly for poly in value if isinstance(poly, Polygon)]) == len(value):
                self._cutouts = value

    def add_cutout(self, cutout=None):
        if isinstance(cutout, Polygon):
            self._cutouts.append(cutout)

    def write_xml(self, layer_feature):
        if layer_feature:
            net = ET.SubElement("Set")
            net.set("net", self.net)
            feature = ET.SubElement(net, "Features")
            location = ET.SubElement(feature, "Location")
            location.set("x", self.x)
            location.set("y", self.y)
            if self.feature_type == self.FeatureType.Polygon:
                contour = ET.SubElement(feature, "Contour")
                polygon = ET.SubElement(contour, "Polygon")
                polygon_begin = ET.SubElement(polygon, "PolyBegin")
                polygon_begin.set("x", self.polygon.poly_steps[0].x)
                polygon_begin.set("y", self.polygon.poly_steps[0].y)
                for poly_step in self.polygon.poly_steps[1:]:
                    if poly_step.poly_type == 1:
                        poly = ET.SubElement(polygon, "PolyStepSegment")
                        poly.set("x", poly_step.x)
                        poly.set("y", poly_step.y)
                    elif poly_step.poly_type == 2:
                        poly = ET.SubElement(polygon, "PolyStepCurve")
                        poly.set("x", poly_step.x)
                        poly.set("y", poly_step.y)
                        poly.set("centerX", poly_step.center_X)
                        poly.set("centerY", poly_step.center_y)
                        poly.set("clockwise", poly_step.clock_wise)

    class FeatureType:
        (Polygon, Paths, Padstack, Via, Drill) = range(1, 5)
