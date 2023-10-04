# General Info

# Installation 
```bash
>>> pip install OskarFieldModule
```

# Importing
```python
>>> import Field
```


Functions for calculating and plotting electromagnetic fields and potentials in 3d.

# Functions

## Efield, Epot
Field and potential from line charge parallel to x, y or z axis. Can be placed anywhere in 3D


## EfieldCircle, EpotCircle 
Field and potential from circle charge in origin

## BfieldLine
Field from line current parallel to x, y or z axis. Can be placed anywhere in 3D

## BfieldCircle
Field from circular current in origin

## PlotVector
Plots vector field. Customize colorscheme, density, and figsize

## PlotContour
Plots vector field. Customize colorscheme, levels, norm and figsize

## PlotCircle
Plots circle just using radius
    
# See example code below:

## Single Point Charge
```Python 
>>> L = 2
>>> N = 10
>>> Q = [1.0]
>>> r_Q = np.array([[0.0, 0.0, 0.0]])
>>> plane = 'xy'

>>> rx, ry, Ex, Ey = CalculateEfield(L, N, Q, r_Q, plane)
>>> PlotVector(rx, ry, Ex, Ey, 'quiver', show = True)

>>> N = 100
>>> rx, ry, V = CalculateEpot(L, N, Q, r_Q, plane)
>>> PlotContour(rx, ry, V, show=True)


## Double Point Charge Example     

>>> L = 2
>>> N = 100
>>> Q = [2.0, -2.0]
>>> r_Q = [-1, 1]
>>> r_Q = np.array([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
>>> plane = 'xy'

>>> rx, ry, Ex, Ey = CalculateEfield(L, N, Q, r_Q, plane)
>>> PlotVector(rx, ry, Ex, Ey, 'stream', show = True, broken_streamlines = False)

## Double Line Charge Example       

>>> L = 2
>>> N = 50
>>> line_charges = [-1, 1]
>>> line_lengths = [1, 1]
>>> line_center_coords = [[0, 0, -1], [0, 0, 1]]
>>> axis = ['x', 'x']
>>> plane = 'xz'

>>> rx, rz, Ex, Ez = CalculateEfieldLine(L, N, line_charges, line_lengths, line_center_coords, axis, plane)
>>> rx, rz, V = CalculateEpotLine(L, N, line_charges, line_lengths, line_center_coords, axis, plane)

>>> PlotVector(rx, rz, Ex, Ez, 'stream', broken_streamlines = False, show = True)
>>> PlotContour(rx, rz, V, show = True, norm = 'linear') 


## Circular Charge Example

>>> L = 5
>>> N = 100
>>> circle_charge = [5]
>>> radius = [2]
>>> plane = 'yz'
>>> plane_circles = ['yz']
>>> ry, rz, Ey, Ez = CalculateEfieldCircle(L, N, circle_charge, radius, plane, plane_circles)
>>> PlotVector(ry, rz, Ey, Ez, 'stream', show = False, equal = True)

>>> t = np.linspace(0, 2*np.pi, 100)
>>> plt.plot(radius[0]*np.cos(t), radius[0]*np.sin(t))
>>> plt.show()

>>> N = 500
>>> ry, rz, V = CalculateEpotCircle(L, N, circle_charge, radius, plane, plane_circles)
>>> PlotContour(ry, rz, V, show = False, equal = True)

>>> t = np.linspace(0, 2*np.pi, 100)
>>> plt.plot(radius[0]*np.cos(t), radius[0]*np.sin(t))
>>> plt.show()


## Line Current Example

>>> L = 5
>>> N = 24
>>> line_currents = [5]
>>> line_lengths = [1]
>>> line_center_coords = [[0.0, 0.0, 0.0]]
>>> axis = ['x']
>>> plane = 'yz'

>>> rx, rz, Bx, Bz = CalculateBfieldLine(L, N, line_currents, line_lengths, line_center_coords, axis, plane)

>>> PlotVector(rx, rz, Bx, Bz, 'quiver', title = 'Magnetic Field from Lin e Current', show = True)

## Circular Current Example

>>> L = 8
>>> N = 40
>>> circle_currents = [5]
>>> radii = [5]
>>> plane = 'xz'
>>> circle_planes = ['xy']
>>> rx, rz, Bx, Bz = CalculateBfieldCircle(L, N, circle_currents, radii, plane, circle_planes)

>>> PlotVector(rx, rz, Bx, Bz, 'stream', broken_streamlines=False, show = True, cmap = 'inferno', density = .5)   
```

[Github-flavored Markdown](https://github.com/Oskar-Idland/Oskar-Field-Module)