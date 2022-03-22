from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

if __name__=='__main__':

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    file_path = r'C:\Users\WHI93526\OneDrive - Mott MacDonald\Documents\thing_files\BT_smooth.stl'

    # Load the STL files and add the vectors to the plot
    your_mesh = mesh.Mesh.from_file(file_path)
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

    # Auto scale to the mesh size
    scale = your_mesh.points.flatten()
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()