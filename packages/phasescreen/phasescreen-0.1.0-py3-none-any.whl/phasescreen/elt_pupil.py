from __future__ import annotations
from anisocado.pupil_utils import generateEeltPupilMask
from dataclasses import dataclass
from phasescreen.base import Coordinate, Flip, PhaseImageMaker, PolarScreen, cart2pol, noflip, reorient 
import numpy as np 
# generateEeltPupilMask( 500, 1.0, 250, 250, 40/400, 0.00, 0)


@dataclass
class EltScreenMaker:
    diameter: float = 40.0
    angle: float =0.0
    center: Coordinate = Coordinate(0, 0)
    spider_width: float = 1.0
    gap: float = 0.0
    phase_angle: float = 0.0 
    phase_flip: Flip = noflip 

    def make_screen(self, shape, scale:float|None = None )->PolarScreen:
        ny, nx = shape 
        size =  int(max( ny, nx ) )
        
        if scale is None:
            scale = size / self.diameter 
        x0, y0 = self.center 
        p_x, p_y = x0*scale+size/2.0, y0*scale+size/2.0  
         
        p_radius = self.diameter * scale / 2.0
        
        elt_scale = 40.0/self.diameter
    
        # inverse p_y and p_x (not the same convention ) 
        mask = generateEeltPupilMask( size, self.spider_width*elt_scale , p_y, p_x, elt_scale/scale, self.gap*elt_scale, self.angle*180/np.pi )

        if nx==ny:
            pass
        elif ny>nx:
            dx = (nx-size)//2 
            dy = 0
            mask = mask[:,dx:dx+nx] 
        else:
            dx = 0
            dy = (nx-ny)//2
            mask = mask[dy:dy+ny,:] 


        vx = (np.arange(nx)-p_x-dx )/ p_radius   
        vy = (np.arange(ny)-p_y-dy )/ p_radius

        x, y = np.meshgrid(vx, vy) 
        r, theta = cart2pol( x, y) 
        theta = reorient(theta,  self.phase_flip, self.phase_angle) 
        return PolarScreen( mask, r[mask], theta[mask])


if __name__ == "__main__":
    from phasescreen.phasescreen import  PhaseImageMaker
    screen = EltScreenMaker( center=( 0.5, 0.0), angle=np.pi/8.0, phase_angle = np.pi/4 ).make_screen( (500,800), 400/40 )

    
 
    p = PhaseImageMaker(screen) 
    from matplotlib.pylab import plt 
    plt.imshow( p.make_phase( [0, 0.0, 1.0, 0.0] ) )
    plt.show()


        



        
        
