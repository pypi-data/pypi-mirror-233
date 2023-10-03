from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from typing import Callable, NamedTuple
import numpy as np 
import zernpol 


class Coordinate(NamedTuple):
    x: float 
    y: float 

class Size(NamedTuple):
    width: float 
    height: float 

class Flip(NamedTuple):
    x: int 
    y: int 

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(r, theta):
    return (r*np.cos(theta), 
            r*np.sin(theta)
        )

_flip_func_loockup = {
(1,  1) : lambda t: t, 
(-1, 1) : lambda t: -t + np.pi,
(-1,-1) : lambda t: t  + np.pi,
(1, -1) : lambda t: -t,
}   

_flip_func_loockup[None] = _flip_func_loockup[(1,1)]
_flip_func_loockup[''] = _flip_func_loockup[(1,1)]
_flip_func_loockup['x'] = _flip_func_loockup[(-1,1)]
_flip_func_loockup['xy'] = _flip_func_loockup[(-1,-1)]
_flip_func_loockup['yx'] = _flip_func_loockup[(-1,-1)]
_flip_func_loockup['y'] = _flip_func_loockup[(1,-1)]
noflip = (1,1)


def reorient(theta, flip, offset_angle):
    try:
        f = _flip_func_loockup[flip]
    except KeyError:
        raise ValueError(f"flip argument not understood got: {flip!r}")
    if offset_angle: # avoid to add 0.0 to a big theta array 
        return f(theta) + offset_angle
    else:
        return f(theta)


class _BaseScreen:
    def construct(self, phases:np.ndarray , dtype=None, fill: np.ScalarType = np.nan, ma: bool = False):
        phases = np.asarray( phases) 
        if dtype is None:
            dtype = phases.dtype
        screen = np.ndarray( phases.shape[:-1]+self.mask.shape, dtype=dtype)
        screen[...] = fill
        screen[..., self.mask] = phases 
        if ma:
            return np.ma.masked_array( screen , ~self.mask)
        return screen
    
    def deconstruct(self, images:np.ndarray)->np.ndarray:
        return np.asarray(images)[..., self.mask]


@dataclass
class PolarScreen(_BaseScreen):
    mask: np.ndarray
    r: np.ndarray
    theta: np.ndarray 
    
    def to_polar(self)->PolarScreen:
        return PolarScreen( self.mask, self.r, self.theta )
    
    def to_cartezian(self)->CartezianScreen:
        x, y = pol2cart(self.r, self.theta)
        return CartezianScreen( self.mask, x, y)


@dataclass
class CartezianScreen(_BaseScreen):
    mask: np.ndarray
    x: np.ndarray
    y: np.ndarray 
    
    def to_polar(self)->PolarScreen:
        r, theta = cart2pol( self.x, self.y)
        return PolarScreen( self.mask, r, theta )
    
    def to_cartezian(self)->CartezianScreen:
        return CartezianScreen( self.mask, self.x, self.y)

    
def make_polar_screen( mask: np.ndarray, phase_angle: float = 0.0, phase_flip: str | None = None )->PolarScreen:
    """ Make a polar screen from a pupill mask 

    Guess the center with the barycenter of the mask 
    The radius is the maximum distance between center and illuminated pixels. 
    
    Args:
        mask: image array of boolean. True are illuminated pixels  
        phase_angle: Offset angle of the projected phase
        phase_flip: Flip "", "x" or "xy" flip of the phase 
            
    Returns:
        screen (PolarScreen): normalized screen built from mask 

    """
    ny, nx = mask.shape 

    xc, yc = mask_barycenter(mask)
    x, y = np.meshgrid( np.arange(nx) - xc,  np.arange(ny)-yc )
    r, theta = cart2pol( x, y)
    r = r[mask]
    theta = theta[mask]
    theta = reorient(theta, phase_flip, phase_angle ) 
    r /= np.max(r) 
    return PolarScreen( mask, r, theta)

def mask_barycenter(mask)->Coordinate:
    ny, nx = mask.shape 
    x, y = np.meshgrid( np.arange(nx). np.arange(ny))
    xc = np.mean( x[mask] )
    yc = np.mean( y[mask] )
    return Coordinate(xc, yc)


def rms_norm(phase:np.ndarray):
    values /= np.std(phase)

def pv_norm(phase:np.ndarray):
    values /=  (np.max(values)-np.min(phase))

def no_norm(_):
    pass

def phase(
        func,  
        screen: PolarScreen|CartezianScreen, 
        coef: tuple|list[tuple], 
        amplitude: list[float] | None = None,  
        norm: Callable = no_norm
    ):
    coordinates = _get_coordinates(screen)
    if _is_scalar(coef):
        phase =  _scalar_phase( func, coordinates, amplitude) 
    else:
        phase = _vect_phase( func, coordinates, amplitude) 
    norm( phase) 
    return phase     


def _is_scalar( coef ):
    return isinstance( coef, tuple)

def _get_coordinates(screen: PolarScreen | CartezianScreen ):
    if isinstance(screen, PolarScreen):
        coordinates = (screen.r, screen.theta)
    elif isinstance(screen, CartezianScreen):
        coordinates = ( screen.x, screen.y ) 
    else:
        raise ValueError(f"Expecting a PolarScreen or CartezianScreen as second argument got a {type(screen)}")
    return coordinates

def _scalar_phase( 
        func: Callable, 
        coef: tuple|list[tuple], 
        coordinates: tuple[np.ndarray, np.ndarray], 
        amplitude: list[float] | None = None,  
    ):
    amplitude = 1.0 if amplitude is None else amplitude 
    return  func( coef, *coordinates)* amplitude

def _vect_phase(
       func: Callable, 
       coordinates: tuple[np.ndarray, np.ndarray], 
       coef: list[tuple], 
       amplitude: list[float] | None = None
    ):
    x1, _ = coordinates 
    values = np.zeros( x1.shape, float)
    if amplitudes is None:
        amplitudes = [1.0]*len(coef)
    for c,a in zip( coef, amplitude):
        values +=  func( c, *coordinates) * a
    return values 
    

def phase_image(
        func,  
        screen: PolarScreen|CartezianScreen , 
        coef: tuple|list[tuple], 
        amplitude: list[float] | None = None,
        fill=np.nan, 
        dtype=float, 
        ma: bool = False, 
        norm: Callable = no_norm
    ):
    values = phase( func, screen, coef, amplitude, norm=norm)
    return screen.construct( values, dtype=dtype, fill=fill, ma=ma)


    
@dataclass 
class PhaseImageMaker:
    """ This object make phase screen images

    Args:
        screen: A ScreenPolar or ScreenCartezian as returned by e.g. :func:`DiskScreenMaker.make_screen` 
        func: A function of signature  ``f( coef, r, theta)``  (or ``f(coef, x, y) if screen is in cartezian coordinates)
            This is the function describing the polynomial base system.  By default it is the zernike function.
        polynoms: A list of polynoms representig the polynomial base system decomposition.
            By default this is 40 Zernike polynoms sorted by the Noll system

    Exemple:
    
        from phasescreen import DiskScreenMaker, PhaseImageMaker, zernpol, zernpol_func  
        from matplotlib.pylab import plt
        import numpy as np

        screen = DiskScreenMaker( diameter = 1.0, obscuration_diameter=0.2, center=(0.3,0) ).make_screen( (800,800), 400.0)
        phase_maker = PhaseImageMaker( screen, func=zernpol_func, polynoms = zernpol(["tip","tilt","defocus"]) )
        plt.imshow( phase_maker.make_phase( [ 1.0, 0.2, 0.5] ) )
        plt.show()


    """
    screen: PolarScreen| CartezianScreen
    func: Callable = partial( zernpol.zernpol_func, masked=False)
    polynoms: tuple|list[tuple] = field( default_factory= lambda : zernpol.zernpol( range(1,41), "Noll" ) )

    def make_phase(self, amplitudes:list|dict ):
        if isinstance(amplitudes,dict):
            iterator = amplitudes.items()
        else:
            iterator = zip(self.polynoms, amplitudes)
        coordinates = _get_coordinates( self.screen )
        x1, _ = coordinates 
        phase = np.zeros( x1.shape, float )
        for pol,a  in iterator:
            phase += _scalar_phase( self.func, pol,  coordinates, a )
        return self.screen.construct(phase) 
     


