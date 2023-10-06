#!/usr/bin/python3
"""Simple library for working with physical quantities"""
import json as _json
from datetime import datetime as _datetime
import decimal as _decimal
from dateutil import parser as _parser
import pytz as _pytz
import simplejson as _simplejson

def _get_planckunit_constants():
    # pylint: disable=invalid-name, non-ascii-name
    r = {}
    # planck constant
    h = _decimal.Decimal('6.6260703412e-34')
    # pi
    π = _decimal.Decimal('3.1415926535897932384626433832795')
    # Reduced planck constant
    ℏ = h/(_decimal.Decimal(2) * π)
    # gravitational constant
    G = _decimal.Decimal('6.67448478e-11')
    # speed of light
    c = _decimal.Decimal('299792568')
    # Boltzmann constant
    k = _decimal.Decimal('1.3806485279e-23')
    # Planck length
    r["length"] = (ℏ * G / (c  * c * c)).sqrt()
    # Planck mass
    r["mass"] = (ℏ * c / G).sqrt()
    # Planck time
    r["time"] = (ℏ * G / (c * c * c * c * c)).sqrt()
    # Planck current
    r["current"] = (c * c * c * c * c * c /(k * G)).sqrt()
    # Planck temperature
    r["temperature"] = (ℏ * c * c * c * c * c / (G * k * k)).sqrt()
    # Planck substance (doesn't exist, we just use 1 so everything can be normalized)
    r["substance"] = _decimal.Decimal(1)
    # Planck intensity (doesn't exist, we just use 1 so everything can be normalized)
    r["intensity"] = _decimal.Decimal(1)
    return r

_PLANCK_UNIT_CONSTANTS = _get_planckunit_constants()

_PLANCK_UNITS = {
  "one":       {},
  "plancklength":     {"dimensions": {"length": 1}},
  "planckmass":        {"dimensions": {"mass": 1}},
  "plancktime":    {"dimensions": {"time": 1}},
  "planckcurrent":    {"dimensions": {"current": 1}},
  "plancktemperature":    {"dimensions": {"temperature": 1}},
  "plancksubstance":      {"dimensions": {"substance": 1}},
  "planckintensity":   {"dimensions": {"intensity": 1}},
  "planckfrequency":     {"dimensions": {"time": -1}},
  "planckforce":    {"dimensions": {"length": 1, "mass": 1, "time": -2}},
  "planckpressure":    {"dimensions": {"length": -1, "mass": 1, "time": -2}},
  "planckenergy":     {"dimensions": {"length": 2, "mass": 1, "time": -2}},
  "planckpower":      {"dimensions": {"length": 2, "mass": 1, "time": -3}},
  "planckcharge":   {"dimensions": {"current": 1, "time": 1}},
  "planckpotential":      {"dimensions": {"length": 2, "mass": 1, "time": -3, "current": -1}},
  "planckresistance":       {"dimensions": {"length": 2, "mass": 1, "time": -3, "current": -2}},
  "planckconductance":   {"dimensions": {"length": -2, "mass": -1, "time": 3, "current": 2}},
  "planckcapacitance":     {"dimensions": {"length": -2, "mass": -1, "time": 4, "current": 2}},
  "planckfluxdensity":     {"dimensions": {"mass": 1, "time": -2, "current": -1}},
  "planckflux":     {"dimensions": {"length": 2, "mass": 1, "time": -2, "current": -1}},
  "planckinductance":     {"dimensions": {"length": 2, "mass": 1, "time": -2, "current": -2}},
  "planckilluminance":       {"dimensions": {"intensity": 1, "length": -2}},
  "planckabsorbedradiation":      {"dimensions": {"length": 2, "time": -2}},
  "planckarea":        {"dimensions": {"length": 2}},
  "planckvolume":        {"dimensions": {"length": 3}},
  "planckvelocity":       {"dimensions": {"length": 1, "time": -1}},
  "planckacceleration":   {"dimensions": {"length": 1, "time": -2}},
  "planckwavenumber":     {"dimensions": {"length": -1}},
  "planckdensity":        {"dimensions": {"mass": 1, "length": -3}},
  "plancksurfacedensity": {"dimensions": {"mass": 1, "length": -2}},
  "planckspecificvolume": {"dimensions": {"mass": -1, "length": 3}},
  "planckcurrentdensity": {"dimensions": {"current": 1, "length": -2}},
  "planckmagneticfieldstrength": {"dimensions": {"current": 1, "length": -1}},
  "planckconcentration":  {"dimensions": {"substance": 1, "length": -3}},
  "planckmassconcentration": {"dimensions": {"mass": 1, "length": -3}},
  "planckluminance": {"dimensions": {"intensity": 1, "length": -2}}
}

_ISO_UNITS = {
  "one":       {},
  "metre":     {"dimensions": {"length": 1}},
  "kg":        {"dimensions": {"mass": 1}},
  "second":    {"dimensions": {"time": 1}},
  "ampere":    {"dimensions": {"current": 1}},
  "kelvin":    {"dimensions": {"temperature": 1}},
  "mole":      {"dimensions": {"substance": 1}},
  "candela":   {"dimensions": {"intensity": 1}},
  "hertz":     {"dimensions": {"time": -1}},
  "newton":    {"dimensions": {"length": 1, "mass": 1, "time": -2}},
  "pascal":    {"dimensions": {"length": -1, "mass": 1, "time": -2}},
  "joule":     {"dimensions": {"length": 2, "mass": 1, "time": -2}},
  "watt":      {"dimensions": {"length": 2, "mass": 1, "time": -3}},
  "coulomb":   {"dimensions": {"current": 1, "time": 1}},
  "volt":      {"dimensions": {"length": 2, "mass": 1, "time": -3, "current": -1}},
  "ohm":       {"dimensions": {"length": 2, "mass": 1, "time": -3, "current": -2}},
  "siemens":   {"dimensions": {"length": -2, "mass": -1, "time": 3, "current": 2}},
  "farad":     {"dimensions": {"length": -2, "mass": -1, "time": 4, "current": 2}},
  "tesla":     {"dimensions": {"mass": 1, "time": -2, "current": -1}},
  "weber":     {"dimensions": {"length": 2, "mass": 1, "time": -2, "current": -1}},
  "henry":     {"dimensions": {"length": 2, "mass": 1, "time": -2, "current": -2}},
  "lux":       {"dimensions": {"intensity": 1, "length": -2}},
  "grey":      {"dimensions": {"length": 2, "time": -2}},
  "m2":        {"dimensions": {"length": 2}},
  "m3":        {"dimensions": {"length": 3}},
}

_NONAME_UNITS = {
  "velocity":       {"dimensions": {"length": 1, "time": -1}},
  "acceleration":   {"dimensions": {"length": 1, "time": -2}},
  "wavenumber":     {"dimensions": {"length": -1}},
  "density":        {"dimensions": {"mass": 1, "length": -3}},
  "surfacedensity": {"dimensions": {"mass": 1, "length": -2}},
  "specificvolume": {"dimensions": {"mass": -1, "length": 3}},
  "currentdensity": {"dimensions": {"current": 1, "length": -2}},
  "magneticfieldstrength": {"dimensions": {"current": 1, "length": -1}},
  "concentration":  {"dimensions": {"substance": 1, "length": -3}},
  "massconcentration": {"dimensions": {"mass": 1, "length": -3}},
  "luminance": {"dimensions": {"intensity": 1, "length": -2}},
}

_TRANSPOSED_UNITS = {
  "degrees":   {"scale": 0.017453292},
  "coordinate": {"scale": 0.017453292},
  "foot":      {"dimensions": {"length": 1}, "scale": 0.3048},
  "inch":      {"dimensions": {"length": 1}, "scale": 0.0254},
  "mile":      {"dimensions": {"length": 1}, "scale": 1609.344},
  "yard":      {"dimensions": {"length": 1}, "scale": 0.9144},
  "au":        {"dimensions": {"length": 1}, "scale": 149597870700},
  "lightyear": {"dimensions": {"length": 1}, "scale": 9460730472580000},
  "parsec":    {"dimensions": {"length": 1}, "scale": 30856775812799588},
  "gram":      {"dimensions": {"mass": 1}, "scale": 0.001},
  "pound":     {"dimensions": {"mass": 1}, "scale": 0.45359},
  "ounce":     {"dimensions": {"mass": 1}, "scale": 0.02835},
  "stone":     {"dimensions": {"mass": 1}, "scale": 6.3502934},
  "minute":    {"dimensions": {"time": 1}, "scale": 60},
  "hour":      {"dimensions": {"time": 1}, "scale": 3600},
  "day":       {"dimensions": {"time": 1}, "scale": 86400},
  "year":      {"dimensions": {"time": 1}, "scale": 31557600},
  "celsius":   {"dimensions": {"temperature": 1}, "offset": 273.15},
  "fahrenheit":{"dimensions": {"temperature": 1}, "offset": 255.3722, "scale": 0.5555555556},
  "are":       {"dimensions": {"length": 2}, "scale": 100},
  "hectare":   {"dimensions": {"length": 2}, "scale": 10000},
  "acre":      {"dimensions": {"length": 2}, "scale": 4046.86},
  "barn":      {"dimensions": {"length": 2}, "scale": 0.0000000000000000000000000001},
  "litre":     {"dimensions": {"length": 3}, "scale": 0.001},
  "barrel":    {"dimensions": {"length": 3}, "scale": 0.158987294928},
  "gallon":    {"dimensions": {"length": 3}, "scale": 0.003785411784},
  "pint":      {"dimensions": {"length": 3}, "scale": 0.000473176473},
  "radianpersecond": {"dimensions": {}, "scale": 3.14159265358979323846},
  "plancklength": {"dimensions": {"length": 1}, "scale": 1.6162e-35},
  "planckmass": {"dimensions": {"mass": 1}, "scale": 2.1765e-8},
  "plancktime": {"dimensions": {"time": 1}, "scale": 5.391247e-44},
  "plancktemperature": {"dimensions": {"temperature": 1}, "scale": 1.41678416e32},
  "planckarea": {"dimensions": {"length": 2}, "scale": 2.6121e-70},
  "planckvolume":      {"dimensions": {"length": 3}, "scale": 4.2217e-105},
  "planckmomentum": {"dimensions": {"length": 1, "mass": 1, "time": -1}, "scale": 6.5249},
  "planckenergy": {"dimensions": {"length": 2, "mass": 1, "time": -2}, "scale": 1.9561e9},
  "planckforce": {"dimensions": {"length": 1, "mass": 1, "time": -2}, "scale": 1.2103e44},
  "planckdensity": {"dimensions": {"length": -3, "mass": 1}, "scale": 5.1550e96},
  "planckacceleration": {"dimensions": {"length": 1, "time": -2}, "scale": 5.5608e51},
  "planckcurrent": {"dimensions": {"current": 1}, "scale": 3.479e25},
  "planckfrequency": {"dimensions": {"time": -1}, "scale": 2.952e42},
  "planckpressure":    {"dimensions": {"length": -1, "mass": 1, "time": -2}, "scale": 4.63309e113},
  "planckpower":      {"dimensions": {"length": 2, "mass": 1, "time": -3}, "scale": 3.628e52},
  "planckcharge":   {"dimensions": {"current": 1, "time": 1}, "scale": 1.8755e-18},
  "planckvoltage":      {
      "dimensions": {"length": 2, "mass": 1, "time": -3, "current": -1},
      "scale": 1.043e27},
  "planckimpedance": {
      "dimensions": {"length": 2, "mass": 1, "time": -3, "current": -2},
      "scale": 29.9792458}
}

_UNIT_ALIAS = {
    "one": [
        "number",
        "radians",
        "one-radian",
        "dimentionless",
        "steradian",
        "watt-db",
        "one-db",
        "one-undef",
        "one-percentage",
        "one-ppb"
    ],
    "metre": ["meter", "meters","metres", "length", "m"],
    "foot": ["feet","ft"],
    "candela": ["intencity", "lumen", "illuminance"],
    "au": ["astronomicalunit"],
    "gram": ["g"],
    "kg": ["weight"],
    "pound": ["lbs", "lb", "pounds"],
    "ounce": ["oz"],
    "second": ["time", "seconds", "sec"],
    "minute": ["minutes","min"],
    "hour": ["hr"],
    "day": ["dy"],
    "year": ["yr"],
    "ampere": ["current", "amp"],
    "kelvin": ["temperature"],
    "hertz": ["frequency","becquerel", "hz"],
    "newton": ["force"],
    "pascal": ["stress", "pressure", "pa"],
    "joule": ["energy", "work", "heat"],
    "watt": ["power"],
    "coulomb": ["charge"],
    "volt": ["potential"],
    "ohm": ["resistance"],
    "farad": ["capacitance"],
    "tesla": ["fluxdensity"],
    "weber": ["flux"],
    "henry": ["inductance"],
    "lux": ["illuminance"],
    "grey": ["absorbedradiation", "sievert"],
    "m2": ["squaremetre", "area"],
    "m3": ["cubicmetre", "volume"],
    "litre": ["liter"],
    "stone": ["stones","st"]
}

_ISO_PREFIX = {
  "quetta": 1000000000000000000000000000000,
  "ronna": 1000000000000000000000000000,
  "yotta": 1000000000000000000000000,
  "zetta": 1000000000000000000000,
  "exa":   1000000000000000000,
  "peta":  1000000000000000,
  "tera":  1000000000000,
  "giga":  1000000000,
  "mega":  1000000,
  "kilo":  1000,
  "hecto": 100,
  "deca":  10,
  "deci":  0.1,
  "centi": 0.01,
  "milli": 0.001,
  "micro": 0.000001,
  "nano":  0.000000001,
  "pico":  0.000000000001,
  "femto": 0.000000000000001,
  "atto":  0.000000000000000001,
  "zepto": 0.000000000000000000001,
  "yocto": 0.000000000000000000000001,
  "ronto": 0.000000000000000000000000001,
  "quecto":0.000000000000000000000000000001
}

_LOG_UNIT = {
  "dB": {"unit": "pascal", "scale": 0.00002, "base": 10, "rexponent": 10},
  "dBV": {"unit": "volt", "scale": 1, "base": 10, "rexponent": 20},
  "dBA": {"unit": "ampere", "scale": 1, "base": 10, "rexponent": 20},
  "dBW": {"unit": "watt", "scale": 1, "base": 10, "rexponent": 10},
  "dBm": {"unit": "watt", "scale": 0.001, "base": 10, "rexponent": 10},
  "pitch": {"unit": "hertz", "scale": 440.0, "base": 2, "rexponent": 12}
}

_NOTES = {
    "C": -9,
    "D": -7,
    "E": -5,
    "F": -4,
    "G" : -2,
    "A": 0,
    "B": 2
}

def _note_to_pitch(note):
    parts = list(note)
    if len(note) > 3 or len(note) < 1:
        raise RuntimeError("Invalid note: " + note)
    pitch = 0
    if len(note) == 3:
        if parts[1].lower() == "b":
            pitch = -1
        elif parts[1] == "#":
            pitch = 1
        else:
            raise RuntimeError("Invalid note: " + note)
    if parts[0].upper() in _NOTES:
        pitch += _NOTES[parts[0].upper()]
    else:
        raise RuntimeError("Invalid note: " + note)
    if parts[-1] in list("012345678"):
        pitch += (int(parts[-1]) - 4) * 12
    else:
        raise RuntimeError("Invalid note: " + note)
    return pitch

def _scale_for_dimensions(dimensions):
    scale = _decimal.Decimal(1.0)
    dimnames = ["length", "mass", "time", "current", "temperature", "substance", "intensity"]
    for ndx in range(0,7):
        if dimensions[ndx] != 0:
            dimscale = _PLANCK_UNIT_CONSTANTS[dimnames[ndx]]
            dimcount = abs(dimensions[ndx])
            positive = dimensions[ndx] > 0
            for _ in range(0, int(dimcount)):
                if positive:
                    scale *= dimscale
                else:
                    scale /= dimscale
    return scale

def _name_to_unit(name):
    # pylint: disable = too-many-statements, too-many-branches, too-many-locals
    offset = _decimal.Decimal(0.0)
    scale = _decimal.Decimal(1.0)
    rescale = _decimal.Decimal(1.0)
    unit_name = name
    full_prefix = ""
    fullname = name
    scale_from_planck_units = False
    for prefix,mscale in _ISO_PREFIX.items():
        if name.startswith(prefix):
            name = name[len(prefix):]
            rescale *= _decimal.Decimal(mscale)
            full_prefix += prefix
    if name.startswith("planck"):
        name = name[len("planck"):]
        scale_from_planck_units = True
    if "planck" + name in _PLANCK_UNITS:
        unit = _PLANCK_UNITS["planck" + name].copy()
        unit_name = fullname
    elif name in _ISO_UNITS:
        unit = _ISO_UNITS[name].copy()
        unit_name = fullname
    elif name in _TRANSPOSED_UNITS:
        if scale_from_planck_units:
            raise RuntimeError("The 'planck' prefix is incompatible with transposed unit " + name)
        unit = _TRANSPOSED_UNITS[name].copy()
        unit_name = fullname
    elif name in _LOG_UNIT:
        logunit = _LOG_UNIT[name]
        unit = _ISO_UNITS[logunit["unit"]].copy()
        unit["logscale"] = {}
        unit["logscale"]["scale"] = _decimal.Decimal(logunit["scale"])
        unit["logscale"]["base"] = _decimal.Decimal(logunit["base"])
        unit["logscale"]["exponent"] = _decimal.Decimal(1) / _decimal.Decimal(logunit["rexponent"])
        unit_name = logunit["unit"]
    else:
        unit = None
        for key, value in _UNIT_ALIAS.items():
            if name in value:
                if key in _ISO_UNITS:
                    unit = _ISO_UNITS[key].copy()
                    unit_name = full_prefix + key
                elif key in _TRANSPOSED_UNITS:
                    unit = _TRANSPOSED_UNITS[name].copy()
                    unit_name = full_prefix + key
                else:
                    raise RuntimeError("Invalid unit name for physical quantity")
    if unit is None:
        if fullname in _NONAME_UNITS:
            unit = _NONAME_UNITS[fullname]
            unit_name = None
        else:
            raise RuntimeError("Invalid unit name for physical quantity")
    if "scale" in unit:
        scale = _decimal.Decimal(unit["scale"]) * rescale
    else:
        scale = rescale
    if "offset" in unit:
        offset = unit["offset"]
        if isinstance(offset, (float, int)):
            offset = _decimal.Decimal(offset)
    dimensions = []
    dims = {}
    if "dimensions" in unit:
        dims = unit["dimensions"]
    for dimension in ["length",
                      "mass",
                      "time",
                      "current",
                      "temperature",
                      "substance",
                      "intensity"]:
        if dimension in dims:
            dimensions.append(dims[dimension])
        else:
            dimensions.append(0)
    if scale_from_planck_units:
        scale *= _scale_for_dimensions(dimensions)
    unit["dim_array"] = dimensions
    unit["unit_name"] = unit_name
    unit["offset"] = offset
    unit["scale"] = scale
    return unit

def _find_si_name(dimarr):
    for key, val in _ISO_UNITS.items():
        dimension_array = []
        dimensions = val.get("dimensions",{})
        for dimension in ["length",
                          "mass",
                          "time",
                          "current",
                          "temperature",
                          "substance",
                          "intensity"]:
            if dimension in dimensions:
                dimension_array.append(dimensions[dimension])
            else:
                dimension_array.append(0)
        if dimarr == dimension_array:
            return key
    return None

def _find_planck_unit_name(dimarr):
    for key, val in _PLANCK_UNITS.items():
        dimension_array = []
        dimensions = val.get("dimensions",{})
        for dimension in ["length",
                          "mass",
                          "time",
                          "current",
                          "temperature",
                          "substance",
                          "intensity"]:
            if dimension in dimensions:
                dimension_array.append(dimensions[dimension])
            else:
                dimension_array.append(0)
        if dimarr == dimension_array:
            return key
    return None

class PhysicalQuantity:  # pylint: disable=too-many-instance-attributes
    """Single class for representing any type of physical unit"""
    def __init__(
            self,
            value=0.0,
            name="one",
            dimensions=None,
            scale=1.0,
            offset=0.0):
        """Constructor"""
        # pylint: disable=too-many-arguments
        if name == "time" and isinstance(value, str):
            self.value_hr = _decimal.Decimal(_parser.parse(value).timestamp())
        elif not isinstance(value, (int, float, _decimal.Decimal)):
            raise RuntimeError("value should be a number")
        else:
            self.value_hr = _decimal.Decimal(value)
        if name is None and dimensions is not None:
            self.dimensions = dimensions
            self.unit_name = None
            self.scale_hr = _decimal.Decimal(scale)
            self.offset_hr = _decimal.Decimal(offset)
            self.value = float(self.value_hr)
            self.scale = float(self.scale_hr)
            self.offset = float(self.offset_hr)
            return
        unit = _name_to_unit(name)
        self.unit_name = unit["unit_name"]
        self.scale_hr = unit["scale"]
        self.offset_hr = unit["offset"]
        self.dimensions = unit["dim_array"]
        if "logscale" in unit:
            scale = unit["logscale"]["scale"]
            base = unit["logscale"]["base"]
            exponent = unit["logscale"]["exponent"]
            self.value_hr = scale * base ** (self.value_hr * exponent)
        self.value = float(self.value_hr)
        self.scale = float(self.scale_hr)
        self.offset = float(self.offset_hr)

    def normalized(self, planck_units=False, allow_ambiguous=False):
        """Normalize to ISO units"""
        normalized = self.value_hr * self.scale_hr + self.offset_hr
        if planck_units:
            normalized /= _scale_for_dimensions(self.dimensions)
            planck_unit_name = _find_planck_unit_name(self.dimensions)
            if planck_unit_name is None:
                if not allow_ambiguous:
                    raise RuntimeError(
                        "Can't normalize to planckunits without loss of unambiguous representation")
                return PhysicalQuantity(normalized, None, self.dimensions)
            return PhysicalQuantity(normalized, planck_unit_name)
        si_name = _find_si_name(self.dimensions)
        if si_name is None:
            return PhysicalQuantity(normalized, None, self.dimensions)
        return PhysicalQuantity(normalized, si_name)

    def __mul__(self, other):
        """Multiplication"""
        if not isinstance(other, (PhysicalQuantity, int, float, _decimal.Decimal)):
            raise RuntimeError("Can only multiply with PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        result_dimensions = [x + y for (x, y) in zip(selfn.dimensions, othern.dimensions)]
        result_value = selfn.value_hr * othern.value_hr
        si_name = _find_si_name(result_dimensions)
        if si_name is None:
            return PhysicalQuantity(result_value, None, result_dimensions)
        return PhysicalQuantity(result_value, si_name)

    def __rmul__(self, other):
        """Something multiplied by self"""
        if not isinstance(other, (int, float, _decimal.Decimal)):
            raise RuntimeError("Non numeric used in subtraction")
        return self * other

    def __truediv__(self, other):
        """Division"""
        if not isinstance(other, (PhysicalQuantity, int, float, _decimal.Decimal)):
            raise RuntimeError("Can only divide by PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        result_dimensions = [x - y for (x, y) in zip(selfn.dimensions, othern.dimensions)]
        result_value = selfn.value_hr / othern.value_hr
        si_name = _find_si_name(result_dimensions)
        if si_name is None:
            return PhysicalQuantity(result_value, None, result_dimensions)
        return PhysicalQuantity(result_value, si_name)

    def __rtruediv__(self, other):
        """Something divided by self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in division")
        return PhysicalQuantity(other) / self

    def __add__(self, other):
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only add a PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        if selfn.dimensions != othern.dimensions:
            raise RuntimeError("Can't add up physical quantities with non-matching units")
        if selfn.unit_name is None:
            return PhysicalQuantity(selfn.value_hr + othern.value_hr, None, selfn.dimensions)
        return PhysicalQuantity(selfn.value_hr + othern.value_hr, selfn.unit_name)

    def __radd__(self, other):
        """Something plus self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in addition")
        return self + other

    def __sub__(self, other):
        """Subtract"""
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only subtract a PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        if selfn.dimensions != othern.dimensions:
            raise RuntimeError("Can't add up physical quantities with non-matching units")
        if selfn.unit_name is None:
            return PhysicalQuantity(selfn.value_hr - othern.value_hr, None, selfn.dimensions)
        return PhysicalQuantity(selfn.value_hr - othern.value_hr, selfn.unit_name)

    def __rsub__(self, other):
        """Something minus self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in subtraction")
        return PhysicalQuantity(other) - self

    def __pow__(self, other):
        """To the power"""
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only exponentialize with PhysicalQuantity, int or float")
        selfn = self.normalized()
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        if othern.dimensions != [0,0,0,0,0,0,0]:
            raise RuntimeError("Can only raise to a dimensionless power")
        result_dimensions = [x * othern.value_hr for x in selfn.dimensions]
        result_value = selfn.value_hr ** othern.value_hr
        si_name = _find_si_name(result_dimensions)
        if si_name is None:
            return PhysicalQuantity(result_value, None, result_dimensions)
        return PhysicalQuantity(result_value, si_name)

    def __rpow__(self, other):
        """Something to the power of self"""
        if not isinstance(other, (int, float)):
            raise RuntimeError("Non numeric used in exponentiation")
        return PhysicalQuantity(other) ** self

    def __eq__(self, other):
        """Equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value_hr == othern.value_hr and selfn.dimensions == othern.dimensions

    def __ne__(self, other):
        """Not Equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value_hr != othern.value_hr or selfn.dimensions != othern.dimensions

    def __lt__(self, other):
        """Less than"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value_hr < othern.value_hr and selfn.dimensions == othern.dimensions

    def __gt__(self, other):
        """Greater than"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value_hr > othern.value_hr and selfn.dimensions == othern.dimensions

    def __le__(self, other):
        """Less or equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value_hr <= othern.value_hr and selfn.dimensions == othern.dimensions

    def __ge__(self, other):
        """Greater or equal"""
        selfn = self.normalized()
        if not isinstance(other, (PhysicalQuantity, int, float)):
            raise RuntimeError("Can only compare with PhysicalQuantity, int or float")
        if isinstance(other, PhysicalQuantity):
            othern = other.normalized()
        else:
            othern = PhysicalQuantity(other)
        return selfn.value_hr >= othern.value_hr and selfn.dimensions == othern.dimensions

    def as_absolute(self, name):
        """Cast to a value of a named unit,respecting offsets as to get an absolute value"""
        unit = _name_to_unit(name)
        if self.dimensions != unit["dim_array"]:
            raise RuntimeError("Unit mismatch for absolute cast")
        nself = self.normalized()
        return PhysicalQuantity((nself.value_hr - unit["offset"]) / unit["scale"], name)

    def as_relative(self, name):
        """Cast to a value of a named unit, discarding offsets as to get a relative value"""
        unit = _name_to_unit(name)
        if self.dimensions != unit["dim_array"]:
            raise RuntimeError("Unit mismatch for absolute cast")
        nself = self.normalized()
        return PhysicalQuantity(nself.value_hr / unit["scale"], name)

    def as_iso8601(self):
        """Get as iso8601 datetime string"""
        if not self.same_dimensions("time"):
            raise RuntimeError(
                "Only physical quanties with time dimensions can be fetched as iso8601"
            )
        tzone = _pytz.timezone('UTC')
        return _datetime.fromtimestamp(self.normalized().value, tzone).isoformat()

    def same_dimensions(self, name):
        """Check if a PhysicalQuantity has the same dimensions as a named unit"""
        unit = _name_to_unit(name)
        return self.dimensions == unit["dim_array"]

    def as_dict(self, use_iso8601=False, decimal=False):  # pylint: disable=too-many-branches
        """Serializable dict of PhysicalQuantity"""
        result = {}
        if decimal:
            result["value"] = self.value_hr
        else:
            result["value"] = self.value
        if self.unit_name is None:
            result["unit"] = {}
            result["unit"]["dimensions"] = {}
            for idx, name in enumerate(["length",
                                        "mass",
                                        "time",
                                        "current",
                                        "temperature",
                                        "substance",
                                        "intensity"]):
                if self.dimensions[idx] != 0:
                    result["unit"]["dimensions"][name]= self.dimensions[idx]
            if self.scale != 1.0:
                if decimal:
                    result["unit"]["scale"] = self.scale_hr
                else:
                    result["unit"]["scale"] = self.scale
            if self.offset != 0.0:
                if decimal:
                    result["unit"]["offset"] = self.offset_hr
                else:
                    result["unit"]["offset"] = self.offset
        else:
            result["unit"] = self.unit_name
            if use_iso8601 and result["unit"] in ["second", "time", "seconds", "sec"]:
                result["unit"] = "time"
                result["value"] = self.as_iso8601()
        return result

    def __str__(self):
        as_dict = self.as_dict()
        rval = str(as_dict["value"]) + " "
        if isinstance(as_dict["unit"], str):
            rval += as_dict["unit"]
            return rval
        has_positive = False
        has_negative = False
        negative = "/"
        for pair in [["length","m"],
                     ["mass","Kg"],
                     ["time", "s"],
                     ["current","A"],
                     ["temperature","K"],
                     ["substance","Mol"],
                     ["intensity", "Cd"]]:
            if pair[0] in as_dict["unit"]["dimensions"]:
                if as_dict["unit"]["dimensions"][pair[0]] > 0:
                    rval += pair[1]
                    has_positive = True
                else:
                    negative += pair[1]
                    has_negative = True
        if not has_positive:
            rval += "1"
        if has_negative:
            rval += negative
        if "scale" in as_dict["unit"] or "offset" in as_dict["unit"]:
            rval += " ("
            if "scale" in as_dict["unit"]:
                rval += " scale=" + as_dict["unit"]["scale"]
            if "offset" in as_dict["unit"]:
                rval += " offset=" + as_dict["unit"]["offset"]
            rval += " )"
        return rval

    def __repr__(self):
        as_dict = self.as_dict()
        rval = "physicalquantity.PhysicalQuantity(" + str(as_dict["value"]) + ","
        if isinstance(as_dict["unit"], str):
            rval += as_dict["unit"]
        else:
            rval += "None"
        rval += "," + self.dimensions.__repr__()
        rval += "," + str(self.scale)
        rval += "," + str(self.offset)
        rval += ")"
        return rval

    def json(self, use_iso8601=False, decimal=False):
        """JSON serialzation of PhysicalQuantity"""
        if decimal:
            _simplejson.dumps(self.as_dict(use_iso8601, decimal=True), indent=4, sort_keys=True)
        return _json.dumps(self.as_dict(use_iso8601), indent=4, sort_keys=True)

def from_dict(quantity_dict):
    """Re-create a PhysicalQuantity from a serializable dict"""
    if "value" not in quantity_dict:
        raise RuntimeError("No value key in dict")
    if "unit" not in quantity_dict:
        raise RuntimeError("No unit key in dict")
    if isinstance(quantity_dict["unit"],str):
        return PhysicalQuantity(quantity_dict["value"], quantity_dict["unit"])
    unit_dict = quantity_dict["unit"]
    offset = _decimal.Decimal(0.0)
    if "offset" in unit_dict:
        offset = _decimal.Decimal(unit_dict["offset"])
    scale = _decimal.Decimal(1.0)
    if "scale" in unit_dict:
        offset = _decimal.Decimal(unit_dict["scale"])
    dimension_array = []
    if "dimensions" in unit_dict:
        dimensions = unit_dict["dimensions"]
    else:
        raise RuntimeError("No dimensions in in dict")
    for dimension in ["length",
                      "mass",
                      "time",
                      "current",
                      "temperature",
                      "substance",
                      "intensity"]:
        if dimension in dimensions:
            dimension_array.append(dimensions[dimension])
        else:
            dimension_array.append(0)
    return PhysicalQuantity(quantity_dict["value"], None, dimension_array, scale, offset)

def from_json(data, decimal=False):
    """Re-create a PhysicalQuantity from a json string"""
    if decimal:
        as_dict = _simplejson.loads(data, use_decimal=True)
    else:
        as_dict = _json.loads(data)
    return from_dict(as_dict)

def from_note(note):
    """Conventince function for creating a PhysicalQuantity from a music note"""
    return PhysicalQuantity(_note_to_pitch(note), "pitch")
