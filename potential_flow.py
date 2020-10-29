### Potential Flow
# Script based on JoshTheEngineer's Panel_Methods repo (@jte0419)
# Objective:            help me study for this goddamn midterm
# Secondary objective:  provide visualization for potential flows in modular fashion
#                       (modularity takes advantage of superimposition since potential flow is linear)

### Imports
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Suppress warnings - I don't want to know what I did wrong
warnings.filterwarnings("ignore")

### Constants
pi = np.pi

### Grid definition
plot_limits = [-10, 10, -10, 10]            # (-x, x, -y, y)
res         = 10                        # Root of number of points in each unit square
numX        = res*(plot_limits[1] - plot_limits[0]) + 1
numY        = res*(plot_limits[3] - plot_limits[2]) + 1
X           = np.linspace(plot_limits[0],   # X-grid spacing
                          plot_limits[1],
                          numX)
Y           = np.linspace(plot_limits[2],   # Y-grid spacing
                          plot_limits[3],
                          numY)
XX, YY        = np.meshgrid(X, Y)
U_x = np.zeros([numX, numY])
U_y = np.zeros([numX, numY])

### Uniform flow (2D Cartesian)
# U     = flow velocity
# alpha = flow angle from the Cartesian x-axis
def uniform_flow(U, alpha): 
    ## Calculate flow at each grid point
    for i in range(numX):
        for j in range(numY):
            x = XX[i, j]
            y = YY[i, j]
            U_x[i, j] += U*np.cos(alpha*pi/180)
            U_y[i, j] += U*np.sin(alpha*pi/180)
 
### Source/sink flow (2D Cartesian)
# m     = source/sink strength
# x_0   = source/sink x-coordinate
# y_0   = source/sink y-coordinate
def source_sink_flow(m, x_0, y_0):        
    origin  = [x_0, y_0]
    ## Calculate flow at each grid point
    for i in range(numX):
        for j in range(numY):
            x = XX[i, j]
            y = YY[i, j]
            U_x[i, j] += (m/(2*pi))*((x-origin[0])/((x-origin[0])**2 + (y-origin[1])**2))
            U_y[i, j] += (m/(2*pi))*((y-origin[1])/((x-origin[0])**2 + (y-origin[1])**2))
            
### Doublet flow (2D Cartesian)
# mu    = source/sink strength
# alpha = doublet angle
# x_0   = source/sink x-coordinate
# y_0   = source/sink y-coordinate
def doublet_flow(mu, alpha, x_0, y_0):        
    origin  = [x_0, y_0]
    ## Calculate flow at each grid point
    for i in range(numX):
        for j in range(numY):
            x = XX[i, j]
            y = YY[i, j]
            U_x[i, j] += (mu/(2*pi))*((x-origin[0])**2*np.cos(alpha) - (y-origin[1])**2*np.cos(alpha) + 2*(x-origin[0])*(y-origin[1])*np.sin(alpha))/ \
                (((x-origin[0])**2 + (y-origin[1])**2)**2)
            U_y[i, j] += (mu/(2*pi))*((y-origin[1])**2*np.sin(alpha) - (x-origin[0])**2*np.sin(alpha) + 2*(x-origin[0])*(y-origin[1])*np.cos(alpha))/ \
                (((x-origin[0])**2 + (y-origin[1])**2)**2)
      
### SET UP FLOW FIELD ###
uniform_flow(0.1, 0)
# source_sink_flow(-5, 1/res, 0)
doublet_flow(-5, 0, 0, 0)
        
## Streamline setup
numSL       = 30
xSL         = plot_limits[0] * np.ones(numSL)                       # Start on left side of plot
ySL         = np.linspace(plot_limits[2], plot_limits[3], numSL)    # Space evenly on left side of plot
xySL        = np.vstack((xSL.T, ySL.T)).T

### Plotting
fig = plt.figure(figsize=[12,12])
plt.cla()   

# Vector plot
# plt.quiver(X, Y, U_x, U_y) 
# Streamlines
plt.streamplot(X, Y, U_x, U_y, density=numSL*.7, color='black', arrowstyle='-', start_points=xySL)
# Colormap
# plt.contourf(X, Y, np.sqrt(U_x**2 + U_y**2), levels=np.linspace(0, 5, 100), cmap='RdBu_r')
# plt.colorbar(fraction=0.046, pad=0.04);

plt.gca().set_aspect('equal') 
plt.show()