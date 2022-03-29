import os
import matplotlib.pyplot as plt


def working_directory(path):   
    if not os.path.exists(path):
         os.mkdir(path)   
    os.chdir(path)


def merge_txt_files(filenames_list, final_output_filename, delete_temp = False, working_path = os.getcwd()):
    """This function merges txt files including initial velocity, 
    property and material.

    Args:
        filenames_list (list): List which contains the above mentioned txts.
        final_output_filename (str): Final output name of keyword file.
        delete_temp (bool, optional): Default's to False.
        working_path (str, optional): Wroking path.. Default's to os.getcwd().
    """
    with open(final_output_filename, 'w') as outfile:
        for f in filenames_list:
            with open(f) as infile:
                for line in infile:
                    outfile.write(line)
        outfile.close()
    if delete_temp:
        for f in filenames_list:
            os.remove(f)


def plot_grid(grid):
    ax = plt.axes(projection="3d")
    ax.plot3D(grid[:, 1], grid[:, 2], grid[:, 3], marker = ".", markersize = '1', c="k")
    plt.show()