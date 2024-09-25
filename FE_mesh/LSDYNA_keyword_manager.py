import numpy as np
import os
from FE_mesh.utilities import working_directory, merge_txt_files
from sieve_analysis_tools import velocity_stochasticity as vs

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


def output_keyword_file(nodes_s, elements_s, pid, filename, velocity = [], angle = []):
    """Function which outputs the final keyword file
    including sphere entity.

    Args:
        nodes_s (array): Nodes matrix.
        elements_s (array): Elements matrix.
        pid (int): Described before.
        filename (string): Final output name.
        output_path (string): The final output directory
        velocity (float): Initial velocity of spheres.
        angle (float): Impact angle.
    """
    change_path = os.getcwd()
    os.chdir(change_path)
    os.chdir(change_path)

    # creating txt files (NEEDS TO BE FIXED)
    np.savetxt('nodes.txt', nodes_s, header="*KEYWORD\n*NODES", fmt="%i,%f,%f,%f", comments="")
    np.savetxt('elements.txt', elements_s, header="*ELEMENT_SOLID", fmt="%8i%8i%8i%8i%8i%8i%8i%8i%8i%8i", comments="")

    section(pid)
    velocity = initial_velocity(pid, velocity, angle)

    filenames = ['nodes.txt', 'elements.txt', 'section.txt', 'material.txt', 'initial_velocity.txt']
    if velocity:
        merge_txt_files(filenames,'%s.k' %filename)
    else:
        merge_txt_files(filenames[0:-1], '%s.k' %filename)
        """with open('%s.k' %filename, "a+") as f:
            f.write("*END")
        f.close()""" # under investigation (if *END is needed at the end of the .k file)

    os.remove('nodes.txt')
    os.remove('elements.txt')
    os.remove('section.txt')
    os.remove('material.txt')
    os.remove('initial_velocity.txt')



def output_include_file(nodes_s, elements_s, pid, filename, velocity = [], angle = []):
    """Same function as output_keyword_file, 
    but with the absence of property and material.

    Args:
        nodes_s (array): Nodes matrix.
        elements_s (array): Elements matrix.
        pid (int): Described before.
        filename (string): Final output name.
        velocity (float): Initial velocity of spheres.
        angle (float): Impact angle.
    """
    change_path = os.getcwd()
    os.chdir(change_path)
    os.chdir(change_path)

    # creating txt files (NEEDS TO BE FIXED)
    np.savetxt('nodes.txt', nodes_s, header="*KEYWORD\n*NODES", fmt="%i,%f,%f,%f", comments="")
    np.savetxt('elements.txt', elements_s, header="*ELEMENT_SOLID", fmt="%8i%8i%8i%8i%8i%8i%8i%8i%8i%8i", comments="")

    initial_velocity(pid, velocity, angle)
    filenames = ['nodes.txt', 'elements.txt', 'initial_velocity.txt']
    merge_txt_files(filenames, '%s.k' %filename)

    os.remove('nodes.txt')
    os.remove('elements.txt')
    os.remove('initial_velocity.txt')

    #changing path in order to produce multiple batches
    os.chdir(change_path)


def output_general_file(nodes_s, elements_s, filename, ending = ".txt"):
    """Same function as output_keyword_file, 
    but outputs only nodes and elements matrices.

    Args:
        nodes_s (array): Nodes matrix.
        elements_s (array): Elements matrix.
        filename (string): Final output name.
        ending (string): Default's '.txt'. Filename's ending.
    """
    change_path = os.getcwd()
    os.chdir(change_path)
    os.chdir(change_path)

    # creating txt files (NEEDS TO BE FIXED)
    np.savetxt('nodes.txt', nodes_s, header="*KEYWORD\n*NODES", fmt="%i,%f,%f,%f", comments="")
    np.savetxt('elements.txt', elements_s, header="*ELEMENT_SOLID", fmt="%8i%8i%8i%8i%8i%8i%8i%8i%8i%8i", footer="*END", comments="")

    filenames = ['nodes.txt', 'elements.txt']
    merge_txt_files(filenames, '%s%s' %(filename, ending))

    os.remove('nodes.txt')
    os.remove('elements.txt')

    #changing path in order to produce multiple batches
    os.chdir(change_path)

    
def apply_initial_velocity(filename, user_initial_velocity, velocity_stochasticity_option, *stochasticity_args,angle, pid = 1):
    """Applies (or not) initial velocity to sphere entities in an LS-DYNA file.

    Args:
        filename (str): Name of the output LS-DYNA file.
        user_initial_velocity (float or int or False): The initial velocity to be applied. If False, no velocity is applied.
        velocity_stochasticity_option (str): The type of stochasticity to apply to the initial velocity. Valid options are "Normal distribution", "Mixed random", and "Uniform".
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
        - If `velocity_stochasticity_option` is "Uniform", `numpy.random.uniform()` will be used to apply a uniform stochastic velocity.
    """
    change_path = os.getcwd()
    os.chdir(change_path)
    
    if isinstance(user_initial_velocity, (float, int)) and not user_initial_velocity == True or not user_initial_velocity:
        
        #feature for application of stochastic velocity to the stream added
        if velocity_stochasticity_option == "Normal distribution":
            if user_initial_velocity != stochasticity_args[0]:
                print('WARNING: Requested velocity of ' + str(user_initial_velocity) + ' m/s do not match with the input average velocity of ' + str(stochasticity_args[0]) + ' m/s. \n' + str(stochasticity_args[0]) + ' m/s will be used instead as nominal-average velocity.')
            user_initial_velocity = vs.normally_distributed_velocity(*stochasticity_args)[0]
            print("applied velocity: ", user_initial_velocity)
        
        elif velocity_stochasticity_option == "Mixed random":
            user_initial_velocity = vs.mixed_random_velocities(*stochasticity_args)
            print("applied velocity: ", user_initial_velocity)
        
        elif velocity_stochasticity_option == "Uniform":
            user_initial_velocity = np.random.uniform(*stochasticity_args)
            print("applied velocity: ", user_initial_velocity)
        
        else:
            print("Arguments for initial velocity stochasticity not found, constant velocity applied: ", user_initial_velocity)
  
        if os.path.exists(f"{filename}.k"):
            initial_velocity(pid, user_initial_velocity, angle)
            with open("initial_velocity.txt", "r+") as f:
                text = f.read()
            f.close()
            with open(f"{filename}.k", "a+") as fout:
                fout.write(text)
            fout.close()
            """with open(f"{filename}.k", "r+") as fout:
                text = fout.read()
                if "*END" in text:
                    text = text.replace("*END", lines)
            fout.close()
            with open(f"{filename}.k", "w+") as fout:
                fout.write(text)
            fout.close()""" # under investigation (if *END is needed at the end of the .k file)
            os.remove("initial_velocity.txt")
        else:
            print("Initial velocity can only be applied for LS-DYNA file forms.")
        return user_initial_velocity
    else:
        raise TypeError("initial_velocity should be set as False or int/float!")

