# -*- coding: utf-8 -*-
"""
@author: dominic
"""

def plot_plane(plane, color='b', ax=None): #Add in existing_subplot -> takes an existing figure
    if ax==None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    y_surf=np.arange(-5, 5, 0.1)                # generate a mesh
    z_surf=np.arange(-5, 5, 0.1)
    y_surf, z_surf = np.meshgrid(y_surf, z_surf)
    x_surf = np.array((-plane[1]/float(plane[0]))*y_surf+(-plane[2]/float(plane[0]))*z_surf+(-plane[3]/float(plane[0])))
    ax.plot_surface(x_surf, y_surf, z_surf, color=color) 
#    fig.show()

def plot_configuration_3D(pts, color='r', ax=None): #Add in fig_ref -> takes an existing figure
    if ax==None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    pts = np.array(pts)
#    print pts[0]
    ax.scatter(pts[:,0],pts[:,1],pts[:,2], c=color)
#    legend()
#    fig.show()

