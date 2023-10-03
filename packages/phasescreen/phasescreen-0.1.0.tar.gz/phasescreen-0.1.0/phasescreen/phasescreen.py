

from functools import wraps
from phasescreen.base import (
    PhaseImageMaker,
    PolarScreen, 
    CartezianScreen, 
)
from phasescreen.disk_pupil import DiskScreenMaker 
from phasescreen.rectangular_pupil import RectangleScreenMaker 
from phasescreen.elt_pupil import EltScreenMaker

from zernpol import zernpol_func as _zernpol_func, zernpol, ZIS

@wraps(_zernpol_func)
def zernpol_func(*args, **kwargs):
    kwargs.setdefault("masked", False)
    return _zernpol_func( *args, **kwargs)


