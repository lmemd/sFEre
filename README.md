<img src=https://user-images.githubusercontent.com/49105794/160626739-4a59b7f9-8d7b-43f0-ae3e-71a015e293ab.png />

## Authors

- [_**Gakias Christos**_](https://github.com/clgakias)
    - Dipl. Mechanical Engineer and PhD Candidate, Laboratory of Machine Elements and Machine Design, Aristotle University of Thessaloniki
    - https://lmemd.meng.auth.gr
    - email: clgakias@auth.gr
    - LinkedIn: https://www.linkedin.com/in/christos-gakias-367455195
- [_**Lamprou Apostolos**_](https://github.com/aalamprou)
    - MSc student, Laboratory of Machine Elements and Machine Design, Aristotle University of Thessaloniki
    - email: lamprou.tolis@gmail.com
    - LinkedIn: www.linkedin.com/in/aalamprou
 

## Project description

This developed package, refers to engineers who simply want to simulate and mesh a sphere, or a batch of spheres,\
with a random or predefined position in space. It is totally suitable for _**shot peening simulation**_ or other simulation
problems that require allocated spheres in a specific space domain. Thus, it includes tools for handling such a complex problem,
and can be widely used from anyone.

Main aspects, are:
- **_Excellent mesh quality_**, using Hexaedral finite elements 
- **_Timestep handling_**, for crash analyses
- **_Low cpu run time_**, both in producing the spheres and FE simulation time
- **_Random or prescribed positions_** of the generated spheres

>Especially, the new implementation of the **_spherified cube_** mesh method proposed, drops down cpu time dramatically,\
reducing the elements needed to mesh the sphere and minimizing geometric errors (distance from real sphere's surface etc).\
Also, by using this package, the need of commercial products, in order to simply mesh a sphere or a number of spheres, is absent.

## **Modules included in this package**

- ### [***sphere_generator***](https://github.com/aalamprou/Thesis-Codes/blob/main/sphere_generator)
  Generic sphere generator module, including: 
    - Geometric characteristics (e.g., diameter)
    - Random diameter of the sphere(s) that follows the Gaussian distribution
    - Random or prescribed allocation of spheres in prefined, rectangular space
  
  It also gives the user the option to generate a single sphere, in any desired point in a 3D space, using the **_sphere_** sub-module,\
  as it is shown in the examples below.

  Furthermore, the generator implements two different sphere configurations. Either **_2-Dimensional_** spheres (disks) in the X-Y plane,\
  or **_3-Dimensional_** spheres, inside the corresponding predefined space domains.

- ### [***FE_mesh***](https://github.com/aalamprou/Thesis-Codes/blob/main/FE_mesh)
  
  **_WARNING:_** This specific module for FE discretization works only for the **_3-Dimensional spheres_** 
   
  FE mesh module, including:
    - 2 dominant ways of mesh (_with their alternatives_) 
        - _**Spherified cube**_ (default mesh method)
        - _**Normalized cube**_ (alternative method, similar to the mesh method followed by LS-PrePost commercial FE package)
    - Single or multiple spheres creation
    - User-defined file output form (file format of commercial FE software)
        -  LS-DYNA
        -  or simple .txt format
        >Implementation of other FE software file formats are in progress.
    
    - FE metrics for mesh quality checks

## **Examples Section**

- ### **_Spherified cube_**

A short example of creating and FE meshing a single sphere, with 1 mm diameter, using the spherified cube method and nonlinear spacing.\
The sphere will be then extracted, in a file using *_LS-Dyna_* format.

<p float="left">
  <img src=https://user-images.githubusercontent.com/49105794/158652216-95bd30d4-3bf8-4826-b028-f7487510b272.png width="450" />
  <img src=https://user-images.githubusercontent.com/49105794/158652241-7c799cb7-9794-41ee-93ea-014041ddcfa7.png width="450" />
    
  ```python
  from sphere_generator.sphere import sphere_3D
  from sphere_generator import shot_stream
  from FE_mesh.configure_shots_mesh import mesh_interface


  def main():

      radius = 0.5 # average radius of created sphere

      # Define sphere's position in space 
      x, y, z = 0, 0, 0

      # Define FE length for spheres
      element_length = 0.04

      # Define sphere's filename
      filename = "single_sphere_spherified"

      # Define FE mesh and spacing method
      sphere = shot_stream.single_sphere([x, y, z], radius) #create sphere entity
      mesh_interface(mesh_method = "spherified_cube", spacing_method = "nonlinear", sph, element_length, filename, output_option = "general") # process and output of meshed generated spheres


  if __name__ == "__main__":
      main()
```
</p>

- ### **_Normalized cube_**

A short example of creating and FE meshing a single sphere, with 1 mm diameter, using the normalized cube method and linear spacing.\
The sphere will be then extracted, in a file using *_LS-Dyna_* format.

<p float="left">
  <img src=https://user-images.githubusercontent.com/49105794/158652313-126be193-15ff-4ca8-8aab-741dea94430b.png width="450" />
  <img src=https://user-images.githubusercontent.com/49105794/158652352-e7c5b30b-7467-43c3-b6e3-93e384b12e43.png width="450" />
  
  ```python
  from sphere_generator.sphere import sphere_3D
  from sphere_generator import shot_stream
  from FE_mesh.configure_shots_mesh import mesh_interface


  def main():

      radius = 0.5 # average radius of created sphere

      # Define sphere's position in space 
      x, y, z = 0, 0, 0

      # Define FE length for spheres
      element_length = 0.04

      # Define sphere's filename
      filename = "single_sphere_normalized"

      # Define FE mesh and spacing method
      sphere = shot_stream.single_sphere([x, y, z], radius) #create sphere entity
      mesh_interface(mesh_method = "normalized_cube", spacing_method = "linear", sph, element_length, filename, output_option = "LSDYNA") # process and output of meshed generated spheres


  if __name__ == "__main__":
      main()
```
</p>

- ### **_Random placed shots_**

The following example focuses on **_shot peening simulations_**. It uses the capabilities of the developed functions to their maximum.\
At first, spheres characteristics are defined, including their average radius and standard deviation. Then the dimensions of the space domain,\
including the desired angle of inclination. The created spheres can be plotted as well as their impact spots on the vertical plane (useful feature for **_coverage predictions_**).

Specifically, the following part of code, will generate one batch with 40 3D spheres, inside a vertical domain with dimensions 2 x 2 x 2 mm,\
with a mean radius of 0.5 mm, and a standard deviation of 0.3 mm. Then, an LS-Dyna .k file will be exported. 

<p float="left">
  <img src=https://user-images.githubusercontent.com/49105794/160381295-af279842-4371-47ad-8ac4-f9d842f4e912.png width="454" />
  <img src=https://user-images.githubusercontent.com/49105794/160381559-bc8b328b-5a63-4418-8f39-53ea463f5e7e.png width="450" />
  
  ```python
from FE_mesh.configure_shots_mesh import mesh_interface
from FE_mesh.LSDYNA_keyword_manager import apply_initial_velocity
from sphere_generator.shot_stream_generator import shot_stream
from sphere_generator.utilities import *


def main():
    #**************************************INPUT SECTION******************************************
    filename = "demo_batch_of_spheres" # name of sphere file
    mean_radius = 0.5 # average radius of created sphere
    radius_std = 0.2 # standard deviation of radius for the created sphere
    spheres_number = 10 # total number of sphere created
    spheres_batches = 1 # change this variable if you want to create more than one batch of shots

    # Define FE length for spheres
    element_length = 0.04

    # Define the domain characteristics (the space that contains the created spheres)
    box_width = 2 # width of the domain containing the spheres (alongside X axis)
    box_length = 2 # length of the domain containing the spheres (alongside Z axis)
    box_height = 5 # height of the domain containing the spheres (alongside Y axis)
    box_angle = 90 # change this value if you want an inlcined box (defined by the angle between the box and the XZ plane)

    # Define if your problem is in 2 dimensional or 3 dimensional space (2D or 3D)
    # If the problem is 2D, only length and height of the box are taken into account

    #****************FE sphere mesh is not implemented if problem is 2D****************

    problem_dimensions = problem_dimensions_setter("3D") # Input 2D or 3D according to your problem dimensions
    box = box_getter(problem_dimensions,box_width,box_height,box_length) # create the box 

    #***********************************END OF INPUT SECTION**************************************

    spheres_list = [] # initialize empty spheres list
    for set_number in range(spheres_batches):

        # Generate stream of random distributed shots in space
        stream = shot_stream(spheres_number, problem_dimensions, box, box_angle, mean_radius, radius_std)
        spheres = stream.generate() # Create the stream
        
        # Change the filename according to current index of set number
        filename = f"{filename}_{set_number + 1}"
        
        # Define FE mesh and spacing method
        # process and output of meshed generated spheres
        mesh_interface("spherified_cube", "nonlinear", spheres, element_length, filename, "LSDYNA")

        # Call this function if you want to apply initial velocity to the shot stream, in LSDYNA keyword format.
        # Currently, an absolute initial velocity of 70 m/s will be applied.
        apply_initial_velocity(filename, 70, box_angle)

        spheres_list.extend(spheres)

        # 3D plot of generated spheres        
        stream.plot_spheres(spheres_list)
        stream.plot_coverage(spheres_list)

    # Print the X,Y coordinates and the radii of created spheres
    list_to_print = ['%.4f'%s.x + '    ' +  '%.4f'%s.y + '   ' +  '%.4f'%s.z + '    ' +  '%.4f'%s.r for s in spheres]
    list_to_print.insert(0,'X coord    Y coord    Z coord    Radius')
    print(*list_to_print, sep='\n')

if __name__ == "__main__":
    main()
```

The procedure for generating 2-Dimensional spheres is the same, except of the mesh generation. Check **_batch_of_spheres_2D_** file.
Also, for generation of spheres with prescribed position in space check **_structured_batch_of_spheres_3D_**

</p>

## **Few words about the mesh methods applied in this package**

- ***Normalized cube method:***\
This method provides a smooth sphere mesh. At first, a cube is formed, and then, it is projected at desired sphere's surface.\
Finally, the space between sphere's surface and cube is layered (multiple elements), and gives the sphere's mesh.

- ***Spherified cube method:***\
In the same manner as the normalized method, an inside cube is formed. Instead of projecting the cube to sphere's surface,
we now use a [**_mathematical model_**][1], which transforms and then wraps cube's surface to a sphere shaped surface,
squeezzing cube's vertices in order to form a sphere. There, lies the **_advantage_** of this method, and this,
is why it is the dominant meshing way in this package. It gives a very **_uniform_** mesh, especially away from the "corners".
Also, it uses lesser elements for nearly same-sized spheres, contrary to the normalized method.

[1]: https://mathproofs.blogspot.com/2005/07/mapping-cube-to-sphere.html

## **Installation**

In **_requirements.txt_** file, are located the necessary python libraries. In order to install them, simply run in terminal:
```
pip install -r requirements.txt
```

## **Authors contributions**
- _**Apostolos Lamprou**_, proposed the idea of **_spherified cube_**, after his findings (and the results he excluded from simulations)
that this mesh was more _uniform_, had _better element aspect ratios_, and was _less time consuming_ than the **_normalized cube_** mesh
method. He carried out the codes for all of the proposed meshes, while the whole project was supervised by **_Christos Gakias_**.

- _**Christos Gakias**_, conceived the idea of a **_uniform_** and **_flexible_** sphere mesh, within the framework of his research in _shot
peening simulations_. His findings that, _contact stiffness_ and _aspect ratio_ optimization (aspect ratio of an ideally shaped element is 1),
lead in a better contact response and realistic peening results (induced stresses etc.), resulted in the proposal of this idea. He also carried
out the codes for _random spheres allocation in predefined space_.

Both carried out various simulations to confirm their findings, and both contributed, after consecutive conversations, in the development of this package.

## **Next steps and future releases**
- ***Implementation of more statistical distributions***\
Except of the Gaussian distribution, that the diameter of the spheres may follow, other distributions such as Weibull or empirical distributions,
will be implemented in the future. 

- ***Implementation of keywords of other commercial FE solvers***\
Another goal, are new output options for other FE solvers, such as ABAQUS, or NASTRAN, besides LS-Dyna, currently, the only option for keyword output.

- ***Implementation of FE mesh on 2-Dimensional spheres***

- ***Implementation of a FE meshed hexhahedral box***\
Besides the FE discretization of spheres, the implementation of FE meshed boxes, is also important. This feature, will expand the capabilities of this
package and help anyone who wants to create a shot peening model fast.
