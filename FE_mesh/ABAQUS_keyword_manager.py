import numpy as np
import os
from FE_mesh.utilities import working_directory, merge_txt_files
from sieve_analysis_tools import velocity_stochasticity as vs

def output_inp_file_entities(nodes_s, elements_s, pid, mid, filename):
    """
    Outputs an ABAQUS .inp file with nodes, elements, and optional initial velocity.

    Args:
        nodes_s (array): Nx4 array [node_id, x, y, z].
        elements_s (array): Mx9 array [elem_id, node1, node2, ..., node8].
        pid (int): Part ID (can be used for material/section assignment).
        mid (int): Material ID
        filename (str): Output filename (without .inp extension).
    """
    
    change_path = os.getcwd()
    os.chdir(change_path)

    # Save nodes using np.savetxt
    np.savetxt('nodes.txt', nodes_s, 
               header="*NODE", 
               fmt='%d, %.6f, %.6f, %.6f', 
               comments='')
    
    elem_fmt = ', '.join(['%d'] * elements_s.shape[1])
    # Save elements using np.savetxt
    np.savetxt('elements.txt', elements_s,
               header="*Element, type=C3D8R, ELSET=P" + str(pid) + ';EALL',
               fmt=elem_fmt,
               comments='')

    section(pid,mid)

    creat_abq_set(nodes_s)

    # Create .inp file by merging
    filenames = ['nodes.txt', 'elements.txt', 'section.txt', 'material.txt', 'node_set.txt']
    merge_txt_files(filenames, '%s.inp' %filename)

    for fname in filenames:
        if os.path.exists(fname):
            os.remove(fname)

    #changing path in order to produce multiple batches
    os.chdir(change_path)


def section(PID, MID = 1000000):
    """This function defines a section, which 
    is needed for LS - DYNA keyword file format.

    Args:
        PID (int): Property's identification number.
        MID (int, optional): Material's identification number (default is 1000000).
    """
    with open('section.txt', 'w') as outfile1, open('material.txt', 'w') as outfile2:
       
        outfile1.write("*SOLID SECTION, ELSET=P" + str(PID) + ";EALL, MATERIAL=M"  + str(MID) + ';Default steel' +  '\n')

        outfile2.write("*MATERIAL,"  + 'NAME=M' + str(MID)  +  ';Default steel' +  '\n')
        outfile2.write('*DENSITY' + '\n' + '7.85E-6' + '\n')
        outfile2.write('*ELASTIC, TYPE=ISOTROPIC' + '\n' + '210, 0.3' + '\n')

        outfile1.close()
        outfile2.close()


def creat_abq_set(nodes_s):
    """
    Create an Abaqus node set file from a list of nodes.

    This function extracts the first column (assumed to contain node IDs) 
    from the input array, reshapes it into rows of 10 elements, and writes 
    the node IDs to a text file ('node_set.txt') in Abaqus NSET format.

    If the number of node IDs is not a multiple of 10, the array is padded 
    with NaNs for reshaping. These NaNs are then skipped when writing to the file, 
    so only valid integers are included in the output.

    Parameters
    ----------
    nodes_s : np.ndarray
        A NumPy array of shape (N, ≥1) where the first column contains node IDs.

    Output
    ------
    A file named 'node_set.txt' is created in the current working directory,
    formatted according to Abaqus NSET specifications.

    Example output:
        *NSET, NSET=velocity_nodes
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10
        11, 12, 13
    """

    change_path = os.getcwd()
    os.chdir(change_path)
    
    node_ids = nodes_s[:,0]
    

    n = node_ids.size
    pad_size = (10 - n % 10) % 10
    padded = np.pad(node_ids, (0, pad_size), mode='constant', constant_values = np.nan)

    node_ids_reshaped = padded.reshape(-1,10)

    with open("node_set.txt", "w") as f:
        f.write("*NSET, NSET=velocity_nodes\n")
        for row in node_ids_reshaped:
            valid_numbers = [str(int(x)) for x in row if not np.isnan(x)]
            if valid_numbers:
                f.write(", ".join(valid_numbers) + "\n")



def initial_velocity(NSET, velocity, angle):
    """This function creates initial velocity entity
    and assigns it to elements, nodes etc.

    Args:
        PID (int) : Described before.
        velocity (float): Initial velocity of spheres.
        angle (float): Impact angle.

    Returns:
        boolean: A boolean variable in case initial velocity entity 
        isn't necessary. 
    """
    with open('initial_velocity.txt', 'w') as outfile:
        if velocity and angle:
            velocity = float(velocity)

            impact_angle = float(angle)

            impact_angle_rads = impact_angle*np.pi/180

            vx = velocity*np.sin(np.pi/2 - impact_angle_rads)
            vy = velocity*np.cos(np.pi/2 - impact_angle_rads)

            outfile.write("*INITIAL CONDITIONS, TYPE=VELOCITY" + "\n")
            outfile.write(NSET + ",1," + "%0.3f,    "%-vx + "\n")
            outfile.write(NSET + ",2," + "%0.3f,    "%-vy + "\n")
            
            variable = True
        else:
            variable = False
            pass
        outfile.close()

    return variable



