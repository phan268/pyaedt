from pyaedt import emit_core
import sys

# Use a class to apply properties to the EmitConstants module
class This(sys.__class__):  # sys.__class__ is <class 'module'>

    @property
    def UnitType(self):
        return emit_core.emit_api_python().UnitType
    #UnitType = emit_core.emit_api_python().UnitType
    """UnitType enum."""

    @property
    def ResultType(self):
        return emit_core.emit_api_python().ResultType
    """ResultType enum."""

    @property
    def TxRxMode(self):
        return emit_core.emit_api_python().TxRxMode
    """TxRxMode enum."""

    @property
    def InterfererType(self):
        return emit_core.emit_api_python().InterfererType
    """InterfererType enum."""

sys.modules[__name__].__class__ = This  # change module class into This

EMIT_UNIT_TYPES = ["Power", "Frequency", "Length", "Time", "Voltage", "Data Rate", "Resistance"]
"""Valid unit types."""

EMIT_VALID_UNITS = {
    "Power": ["mW", "W", "kW", "dBm", "dBW"],
    "Frequency": ["Hz", "kHz", "MHz", "GHz", "THz"],
    "Length": ["pm", "nm", "um", "mm", "cm", "dm", "meter", "km", "mil", "in", "ft", "yd", "mile"],
    "Time": ["ps", "ns", "us", "ms", "s"],
    "Voltage": ["mV", "V"],
    "Data Rate": ["bps", "kbps", "Mbps", "Gbps"],
    "Resistance": ["uOhm", "mOhm", "Ohm", "kOhm", "megOhm", "GOhm"],
}
"""Valid units for each unit type."""


def emit_unit_type_string_to_enum(unit_string):
    EMIT_UNIT_TYPE_STRING_TO_ENUM = {
        "Power": emit_core.EmitConstants.UnitType.POWER,
        "Frequency": emit_core.EmitConstants.UnitType.FREQUENCY,
        "Length": emit_core.EmitConstants.UnitType.LENGTH,
        "Time": emit_core.EmitConstants.UnitType.TIME,
        "Voltage": emit_core.EmitConstants.UnitType.VOLTAGE,
        "Data Rate": emit_core.EmitConstants.UnitType.DATA_RATE,
        "Resistance": emit_core.EmitConstants.UnitType.RESISTANCE,
    }
    return EMIT_UNIT_TYPE_STRING_TO_ENUM[unit_string]
