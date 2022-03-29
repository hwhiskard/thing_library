import math
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

class ThingViewer():
    """
    """
    def __init__(self, file_path):
        # Load the STL file
        self.mesh = mesh.Mesh.from_file(file_path)

    def rotate_mesh(self, x, y, z):

        self.mesh.rotate([0.5, 0, 0], math.radians(x))
        self.mesh.rotate([0, 0.5, 0], math.radians(y))
        self.mesh.rotate([0, 0, 0.5], math.radians(z))

    def translate_centre_of_mass(self):
        pass
    
    def visualise_stl(self):
        """
        """

        # Create a new plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)
        

        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.mesh.vectors))

        # Auto scale to the mesh size
        scale = self.mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()

    def save(self):
        self.mesh.save(file_path)
    

if __name__=='__main__':

    file_path = r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files\BT_smooth.stl'

    dog = ThingViewer(file_path)
    mesh = dog.mesh
    dog.rotate_mesh(0, 0, 90)
    dog.visualise_stl()
    dog.save()