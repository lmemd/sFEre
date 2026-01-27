import numpy as np
import os
from FE_mesh.utilities import working_directory, merge_txt_files
from sieve_analysis_tools import velocity_stochasticity as vs

def output_inp_file_entities(nodes_s, elements_s, sphere_dic, pid, mid, filename):
    """
    Outputs an ABAQUS .inp file with nodes, elements, and optional initial velocity.

    Args:
        nodes_s (array): Nx4 array [node_id, x, y, z].
        elements_s (array): Mx9 array [elem_id, node1, node2, ..., node8].
        sphere_dic: dictionary of containing the nodes of each sphere for a bach.
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
               comments="")

    section(pid,mid)

    creat_abq_set(sphere_dic)

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
    is needed for ABAQUS keyword file format.

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


def creat_abq_set(sphere_dic):
    """
    Create an Abaqus node set file a dictionary cointaining the nodes of each element.

    xxxx This function extracts the first column (assumed to contain node IDs) 
    For each sphere in the input dictionary there exists a column of node IDs.
    xxxx from the input array, reshapes it into rows of 10 elements, and writes 
    The function takes it, reshapes it into rows of 10 elements, and writes
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

    with open("node_set.txt", "w") as f: 

        for sphere_id in sphere_dic:
            node_ids = sphere_dic[sphere_id][:,0]
            

            n = node_ids.size
            pad_size = (10 - n % 10) % 10
            padded = np.pad(node_ids, (0, pad_size), mode='constant', constant_values = np.nan)

            node_ids_reshaped = padded.reshape(-1,10)

        
            f.write("*NSET, NSET={}_velocity_nodes\n".format(sphere_id))       
            for row in node_ids_reshaped:
                valid_numbers = [str(int(x)) for x in row if not np.isnan(x)]
                if valid_numbers:
                    f.write(", ".join(valid_numbers) + "\n")



def initial_velocity(NSET, velocity, angle):
    """
    This function creates initial velocity entity
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

def apply_initial_velocity(filename, velocity_stochasticity_option, *velocity_args, angle, dyna_id = 1):
    """Applies (or not) initial velocity to sphere entities in an LS-DYNA file.

    Args:
        filename (str): Name of the output LS-DYNA file.
        velocity_stochasticity_option (str): The type of stochasticity to apply to the initial velocity. Valid options are "Normal distribution", "Mixed random", "Constant"
        stochasticity_args (tuple): The arguments to be passed to the stochasticity function.
        angle (float): The impact angle to apply.
        pid (int): The process ID for the LS-DYNA file.

    Raises:
        TypeError: If user_initial_velocity is not False, float, or int.

    Notes:
        - This function modifies the LS-DYNA file at `filename` to apply the specified initial velocity and angle to any sphere entities.
        - If `user_initial_velocity` is False, no velocity is applied.
        - If `user_initial_velocity` is a float or int, it will be used directly as the initial velocity.
        - If `velocity_stochasticity_option` is "Normal distribution", the `vs.normally_distributed_velocity()` function will be used to apply a normally-distributed stochastic velocity.
        - If `velocity_stochasticity_option` is "Mixed random", the `vs.mixed_random_velocities()` function will be used to apply mixed random velocities.
        - If `velocity_stochasticity_option` is "Constant" will be applied a constant velocity, defined by the user input.
    """
    change_path = os.getcwd()
    os.chdir(change_path)
        
    #feature for application of stochastic velocity to the stream added
    if velocity_stochasticity_option == "Normal distribution":
        user_initial_velocity = vs.normally_distributed_velocity(*velocity_args)
        print("applied velocity: ", user_initial_velocity)
    
    elif velocity_stochasticity_option == "Mixed random":
        user_initial_velocity = vs.mixed_random_velocities(*velocity_args)
        print("applied velocity: ", user_initial_velocity)
    
    elif velocity_stochasticity_option == "Constant":
        user_initial_velocity = velocity_args[0]
        print("applied velocity: ", user_initial_velocity)
    
    else:
        pass
        #print("Arguments for initial velocity stochasticity not found, constant velocity applied: ", user_initial_velocity)


    if os.path.exists(f"{filename}.inp"):
        initial_velocity(dyna_id, user_initial_velocity, angle)
        with open("initial_velocity.txt", "r+") as f:
            text = f.read()
        f.close()
        with open(f"{filename}.inp", "a+") as fout:
            fout.write(text)
        fout.close()
        
        os.remove("initial_velocity.txt")
    else:
        print("Initial velocity can only be applied for LS-DYNA file forms.")
  
    return user_initial_velocity


