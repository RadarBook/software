"""
Project: RadarBook
File: display_facet_model.py
Created by: Lee A. Harrison
On: 10/20/2018
Created with: PyCharm
"""
from scipy import zeros, array, cross
from numpy import min, max
from pathlib import Path

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib.patches import FancyArrowPatch


def read_facet_model(file_name):
    """
    Read the facet model from the given file.
    :param file_name: The name of the facet file.
    :return: The model name, vertices and faces.
    """
    # Open the file
    base_path = Path(__file__).parent
    with open((base_path / file_name), 'r') as file:

        # Read the name of the model
        model_name = file.readline()

        # Read the number of vertices
        number_of_vertices = int(file.readline())

        # Read the vertices
        vertices = zeros([number_of_vertices, 3])

        for i in range(number_of_vertices):
            line = file.readline()
            line_list = line.split( )

            # Parse the values
            vertices[i] = [float(line_list[0]), float(line_list[1]), float(line_list[2])]

        # Read the number of faces
        number_of_faces = int(file.readline())

        # Read the faces
        faces = zeros([number_of_faces, 3], dtype=int)

        for i in range(number_of_faces):
            line = file.readline()
            line_list = line.split( )

            # Parse the values
            faces[i] = [float(line_list[0]), float(line_list[1]), float(line_list[2])]

        return model_name, vertices, faces


def display_facet(model_name, vertices, faces, plot_type, display_normals=False, scale=0.2):
    """
    Display a facet model.
    :param model_name: The name of the model.
    :param vertices: The vertices of the model.
    :param faces: The faces of the model.
    :param plot_type: The type of plot to create (facet/wireframe).
    :param display_normals: Normals on or off.
    :param scale: Scale factor for the model.
    :return:
    """
    # Separate the coordinates of the vertices
    x = vertices[:, 0]
    y = vertices[:, 1]
    z = vertices[:, 2]

    # Display the model
    ax = Axes3D(plt.figure())
    if plot_type == 'Facet':
        ax.plot_trisurf(x, y, z, triangles=faces, color=(1, 1, 1, 1), edgecolor='gray')
    elif plot_type == 'Wireframe':
        ax.plot_trisurf(x, y, z, triangles=faces, color='none', edgecolor='black')
    ax.grid(True)
    set_equal(ax)

    ax.set_title(model_name, size='14')
    ax.set_xlabel('X', size='12')
    ax.set_ylabel('Y', size='12')
    ax.set_zlabel('Z', size='12')

    # Set the tick label size
    ax.tick_params(labelsize=12)

    if display_normals:

        # Vector from origin to vertices
        r = zeros([vertices.shape[0], 3])

        for i in range(vertices.shape[0]):
            r[i] = [vertices[i][0], vertices[i][1], vertices[i][2]]

        for i in range(faces.shape[0]):
            a = r[faces[i][1]] - r[faces[i][0]]
            b = r[faces[i][2]] - r[faces[i][1]]

            # Outward normal
            normal = cross(a, b) + 0.

            # Scale the size of the arrow to be displayed
            normal *= scale

            # Put the arrow at the center of the facet
            mean_r = (r[faces[i][0]] + r[faces[i][1]] + r[faces[i][2]]) / 3.0

            # Get the arrow for the normal
            arrow = Arrow3D([mean_r[0], mean_r[0] + normal[0]], [mean_r[1], mean_r[1] + normal[1]],
                         [mean_r[2], mean_r[2] + normal[2]], mutation_scale=10, lw=1, arrowstyle="-|>", color="r")
            ax.add_artist(arrow)

    plt.show()


def set_equal(ax):
    """
    Make the axes equal for displaying facet models.
    :param ax: Reference to the axes in the figure.
    :return:
    """
    scaling = array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    ax.auto_scale_xyz(*[[min(scaling), max(scaling)]]*3)


class Arrow3D(FancyArrowPatch):
    """
    Arrow object for displaying normals.
    """
    def __init__(self, x, y, z, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._v = x, y, z

    def draw(self, renderer):
        xp, yp, zp = self._v
        x, y, z = proj3d.proj_transform(xp, yp, zp, renderer.M)
        self.set_positions((x[0], y[0]), (x[1], y[1]))
        FancyArrowPatch.draw(self, renderer)
