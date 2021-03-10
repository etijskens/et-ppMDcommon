# -*- coding: utf-8 -*-
"""
Package et_ppmdcommon
=======================================

Common components for the Parallel Programming project assignment
"""
__version__ = "0.1.0"

import numpy as np
import math

# some constants
R0 = pow(2.,1/6) # equilibrium distance of (coefficientless) Lennard-Jones potential : V(r) = 1/r**12 - 1*r**6

def cc2ucc(W):
    """Transform Cartesian coordinates into hexagonal unit cell coordinates.

    Primitive hexagonal unit cell:

       (1/2,H)-(3/2,H)
          /       /
        /       /
    (0,0)----(0,1)

    :param np.array W: cartesian coordinates
    :returns: np.array of unit cell coordinates

    W' = T W
    """
    return np.matmul(T, W)

def cc2uc_ij(W):
    """Return indices of the unit cell containing the point W.

    :param np.array W: Cartesian coordinates of point
    :returns: tuple (i,j) of unit cell indices.
    """
    Wprime = cc2ucc(W)
    return math.floor(Wprime[0]),math.floor(Wprime[1])

class Box:
    def __init__(self, xll, yll, xur, yur):
        """
        :param float xll: x-coordinate of lower left corner
        :param float yll: y-coordinate of lower left corner
        :param float xur: x-coordinate of upper right corner
        :param float yur: y-coordinate of upper right corner
        """
        self.xll = float(xll)
        self.yll = float(yll)
        self.xur = float(xur)
        self.yur = float(yur)

    def inside(self,x,y):
        if self.xll <= x and x < self.xur and self.yll <= y and y < self.yur:  # outside above
            return True
        else:
            return False


    def outside(self,x,y):
        """test location of point (x,y)

        :param float x: x-coordinate
        :param float y: y-coordinate
        :return: 0 if inside -1 if to the left, -2 if to the right, -3 if below, -4 if above
        """
        if x < self.xll:     # outside to the left
            return -1
        elif x >= self.xur:  # outside to the right
            return -2
        elif y < self.yll:   # outside below
            return -3
        elif y >= self.yur:  # outside above
            return -4
        else:
            return 0            # inside

def generateAtoms(xll, yll, wx, wy, r=R0, noise=None):
    """generate atom positions on hexagonal closest packing

    Only positions inside the rectangle with lower left corner (x0,y0)
    and width wx and height wy are generated.

    :param float xll: x-coordinate of lower left corner of the rectangle in which to generate atoms
    :param float yll: y-coordinate of lower left corner of the rectangle in which to generate atoms
    :param float wx: width of the rectangle
    :param float wy: height of the rectanle
    :param float r: edge length of hexagonal cell = interatomic distance
    :param float noise: add a bit of noise to the atom positions. expressed as a fraction of the interatomic distance
    :returns: two numpy arrays with resp. the x- and y-coordinates of the atoms
    """
    # unit cell rectangular centered
    ucx = r
    ucy = r*np.sqrt(3)

    xur = xll + wx
    yur = yll + wy

    i0 = math.floor(xll/ucx)
    i1 = math.ceil (xur/ucx)
    j0 = math.floor(yll/ucy)
    j1 = math.ceil (yur/ucy)

    dxc = 0.5*r
    dyc = 0.5*np.sqrt(3.0)*r

    box = Box(xll, yll, xll+wx, yll+wy)
    nmax = 2*(i1-i0)*(j1-j0)
    x = np.empty((nmax,),dtype=float)
    y = np.empty((nmax,),dtype=float)
    n = -1
    for j in range(j0,j1):
        yj = ucy*j
        yc = yj + dyc
        for i in range(i0,i1):
            xi = ucx*i

            if box.inside(xi,yj):
                n += 1
                x[n] = xi
                y[n] = yj

            xc = xi + dxc
            if box.inside(xc,yc):
                n += 1
                x[n] = xc
                y[n] = yc
    x = x[:n+1]
    y = y[:n+1]
    if noise:
        addNoise(noise, x, y)

    return x, y


def addNoise(x,y,noise):
    n = len(x)
    theta = np.random.random(n)*(2*np.pi) # random angle in [0,2*pi[
    d     = np.random.random(n)*noise     # random amplitude in [0,noise[
    x    += np.cos(theta)*d
    y    += np.sin(theta)*d

# eof
