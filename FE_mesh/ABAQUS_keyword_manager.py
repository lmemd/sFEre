import numpy as np
import os
from FE_mesh.utilities import working_directory, merge_txt_files
from sieve_analysis_tools import velocity_stochasticity as vs
'''
def section(PID, MID = 1000000, ELFORM = 1):
    """This function defines a section, which 
    is needed for LS - DYNA keyword file format.

    Args:
        PID (int): Property's identification number.
        MID (int, optional): Material's identification number (default is 1000000).
        ELFORM (int, optional): Element's integration scheme (reduced[default] or full).
    """
    with open('section.txt', 'w') as outfile1, open('material.txt', 'w') as outfile2:
        outfile1.write("*PART" +  '\n' + 'SECTION_SOLID' + '\n')
        outfile1.write('  %d' %PID + ',    '+ '%d' %MID + ',    ' + '%d' %MID + ',    ' + '0,    0,    0,    0,    0,    0,    %d'%ELFORM + '\n')

        outfile1.write("*SECTION_SOLID_TITLE" +  '\n' + 'SECTION_SOLID' + '\n')
        outfile1.write('  %d' %PID + ',    '+ '%d' %MID + '\n')

        outfile2.write("*MAT_ELASTIC_TITLE" +  '\n' + 'Default MAT1 MAT_ELASTIC' + '\n')
        outfile2.write('  %d'% MID + ',    '+ '7.85E-6,    '+ '210.,    ' + '0.3,    ' + '0.,    0.,    0.' '\n')

        outfile1.close()
        outfile2.close()

def initial_velocity(PID, velocity, angle):
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

            outfile.write("*INITIAL_VELOCITY_GENERATION" + "\n")
            outfile.write("%i,    " %PID + "2,    " + "0,    " + "%0.3f,    "%-vx
            + "%0.1f,    " %-vy + "0,    " + "0,    " + "0,    " + "\n")
            outfile.write("0,    " + "0,    " + "0,     " + "0,    " + "0,    " + "0,    " + "0,    " + "0,    " + "\n")
            outfile.write("*END")

            variable = True
        else:
            variable = False
            pass
        outfile.close()

    return variable
'''

def output_inp_file_entities(nodes_s, elements_s, pid, filename):
    """
    Outputs an ABAQUS .inp file with nodes, elements, and optional initial velocity.

    Args:
        nodes_s (array): Nx4 array [node_id, x, y, z].
        elements_s (array): Mx9 array [elem_id, node1, node2, ..., node8].
        pid (int): Part ID (can be used for material/section assignment).
        filename (str): Output filename (without .inp extension).
        velocity (list): Optional [vx, vy, vz] initial velocity.
        angle (list): Optional angle (not used here).
    """
    
    change_path = os.getcwd()
    os.chdir(change_path)
    os.chdir(change_path)

    #The initial format of element matrix is in LS-Dyna format, which is composed by 10 columns, the second one refers to the PID.
    #For proper ABAQUS output, this column must be excluded.
    #elements_all_filtered = np.delete(elements_s, 1, axis=1)
    elements_all_filtered = elements_s

    # Save nodes using np.savetxt
    np.savetxt('nodes.txt', nodes_s, 
               header="*Node", 
               fmt='%d, %.6f, %.6f, %.6f', 
               comments='')
    
    elem_fmt = ', '.join(['%d'] * elements_all_filtered.shape[1])
    # Save elements using np.savetxt
    np.savetxt('elements.txt', elements_all_filtered,
               header="*Element, type=C3D8R, elset=P" + str(pid) + ';EALL',
               fmt=elem_fmt,
               comments='')

    # Create .inp file by merging
    filenames = ['nodes.txt', 'elements.txt']
    merge_txt_files(filenames, '%s.inp' %filename)

    os.remove('nodes.txt')
    os.remove('elements.txt')
    #os.remove('initial_velocity.txt')

    #changing path in order to produce multiple batches
    os.chdir(change_path)

