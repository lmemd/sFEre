import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
import sys 
sys.path.append('../sFEre')

from FE_mesh.sphere_creation import sphere_entity

class sphere_dims:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r


class distance(sphere_dims):
    def __init__(self, center_x, center_y, center_z, radius, points, elements, element_length):
        super().__init__(center_x, center_y, center_z, radius)
        self.points = points[:, 1:]
        self.elements = elements[:, 2:]
        self.number = np.shape(self.elements)[0]
        self.length = element_length

    
    def point_distance(self, id1, id2):
        xx = np.array([[(self.points[id1, 0] - self.points[id2, 0])**2]])
        yy = np.array([[(self.points[id1, 1] - self.points[id2, 1])**2]])
        zz = np.array([[(self.points[id1, 2] - self.points[id2, 2])**2]])
        dist = np.hstack((xx.T, yy.T, zz.T))

        return np.sqrt(abs(np.sum(dist, axis=1)))


    def distance_from_surface(self, points):
        x_dist = np.array([[(points[:, 0] - self.x)**2]])
        y_dist = np.array([[(points[:, 1] - self.y)**2]])
        z_dist = np.array([[(points[:, 2] - self.z)**2]])
        dist_all = np.hstack((x_dist.T, y_dist.T, z_dist.T))

        return np.sqrt(abs(np.sum(dist_all, axis=1) - self.r**2))
        

    def surface_points(self):
        surface_points_id = np.where(self.distance_from_surface(self.points) < self.length/1000)[0]

        return self.points[surface_points_id, :]


class error_types(distance):
    def __init__(self, center_x, center_y, center_z, radius, points, elements, element_length):
        super().__init__(center_x, center_y, center_z, radius, points, elements, element_length)


    def error(self):
        return self.distance_from_surface(self.surface_points())


    def average_error(self):
        return np.sum(self.error())/self.number

    
    def maximum_error(self):
        return np.max(self.error())

    
    def minimum_error(self):
        return np.min(self.error())


    def mean_square_error(self):
        return np.sum(self.error()**2)/self.number


    def maximum_square_error(self):
        return np.max(self.error()**2)


class mesh_accuracy(distance):
    def __init__(self, center_x, center_y, center_z, radius, points, elements, element_length):
        super().__init__(center_x, center_y, center_z, radius, points, elements, element_length)
        self.id1 = self.elements[:, 0] - 1
        self.id2 = self.elements[:, 1] - 1
        self.id3 = self.elements[:, 2] - 1
        self.id4 = self.elements[:, 3] - 1
        self.id5 = self.elements[:, 4] - 1
        self.id6 = self.elements[:, 5] - 1
        self.id7 = self.elements[:, 6] - 1
        self.id8 = self.elements[:, 7] - 1


    def aspect_ratio(self):
        length1 = self.point_distance(self.id1, self.id2)
        length2 = self.point_distance(self.id2, self.id3)
        length3 = self.point_distance(self.id3, self.id4)
        length4 = self.point_distance(self.id4, self.id1)
        length5 = self.point_distance(self.id5, self.id6)
        length6 = self.point_distance(self.id6, self.id7)
        length7 = self.point_distance(self.id7, self.id8)
        length8 = self.point_distance(self.id8, self.id5)
        length9 = self.point_distance(self.id1, self.id5)
        length10 = self.point_distance(self.id2, self.id6)
        length11 = self.point_distance(self.id3, self.id7)
        length12 = self.point_distance(self.id4, self.id8)
        all_sides = np.hstack((length1, length2, length3, length4, length5, length6, length7, length8, length9, length10, length11, length12))
        min_side_length = np.min(all_sides, axis=1)
        max_side_length = np.max(all_sides, axis=1)
        aspect = max_side_length/min_side_length
        max_aspect_id = np.argmax(aspect, axis=0) + 1
        min_aspect_id = np.argmin(aspect, axis=0) + 1

        min_aspect_ratio = np.min(aspect)
        max_aspect_ratio = np.max(aspect)
        print('\x1b[1;37;45m' + "Minimum aspect ratio (for solid element %i): %0.4f" %(min_aspect_id, min_aspect_ratio) + '\x1b[0m')
        print('\x1b[1;37;45m' + "Maximum aspect ratio (for solid element %i): %0.4f" %(max_aspect_id, max_aspect_ratio) + '\x1b[0m')

        return min_aspect_ratio, max_aspect_ratio


    def volume(self, element):
        id1 = self.elements[element, 0] - 1
        id2 = self.elements[element, 1] - 1
        id4 = self.elements[element, 2] - 1
        id3 = self.elements[element, 3] - 1
        id5 = self.elements[element, 4] - 1
        id6 = self.elements[element, 5] - 1
        id8 = self.elements[element, 6] - 1
        id7 = self.elements[element, 7] - 1
        coords1 = self.points[id1, :].reshape(3, 1)
        coords2 = self.points[id2, :].reshape(3, 1)
        coords3 = self.points[id3, :].reshape(3, 1)
        coords4 = self.points[id4, :].reshape(3, 1)
        coords5 = self.points[id5, :].reshape(3, 1)
        coords6 = self.points[id6, :].reshape(3, 1)
        coords7 = self.points[id7, :].reshape(3, 1)
        coords8 = self.points[id8, :].reshape(3, 1)
        coords_c = (coords1 + coords2 + coords3 + coords4
        + coords5 + coords6 + coords7 + coords8)/8
        matrix1 = np.hstack((coords1 - coords_c, coords2 - coords_c, coords3 - coords_c))
        matrix2 = np.hstack((coords2 - coords_c, coords3 - coords_c, coords4 - coords_c))
        matrix3 = np.hstack((coords1 - coords_c, coords2 - coords_c, coords5 - coords_c))
        matrix4 = np.hstack((coords2 - coords_c, coords5 - coords_c, coords6 - coords_c))
        matrix5 = np.hstack((coords2 - coords_c, coords4 - coords_c, coords6 - coords_c))
        matrix6 = np.hstack((coords4 - coords_c, coords6 - coords_c, coords8 - coords_c))
        matrix7 = np.hstack((coords4 - coords_c, coords8 - coords_c, coords3 - coords_c))
        matrix8 = np.hstack((coords7 - coords_c, coords8 - coords_c, coords3 - coords_c))
        matrix9 = np.hstack((coords1 - coords_c, coords7 - coords_c, coords3 - coords_c))
        matrix10 = np.hstack((coords1 - coords_c, coords7 - coords_c, coords5 - coords_c))
        matrix11 = np.hstack((coords6 - coords_c, coords7 - coords_c, coords8 - coords_c))
        matrix12 = np.hstack((coords5 - coords_c, coords6 - coords_c, coords7 - coords_c))
        vol = (abs(np.linalg.det(matrix1)) + abs(np.linalg.det(matrix2)) +abs(np.linalg.det(matrix3)) +
        abs(np.linalg.det(matrix4)) + abs(np.linalg.det(matrix5)) + abs(np.linalg.det(matrix6)) +
        abs(np.linalg.det(matrix7)) + abs(np.linalg.det(matrix8)) + abs(np.linalg.det(matrix9)) +
        abs(np.linalg.det(matrix10)) + abs(np.linalg.det(matrix11)) + abs(np.linalg.det(matrix12)))/6

        return vol


    def jacobian(self):
            x = self.points[:, 0]
            y = self.points[:, 1]
            z = self.points[:, 2]

            i = sym.Symbol("i")
            j = sym.Symbol("j")
            k = sym.Symbol("k")

            N1 = (1 + i)*(1 - j)*(1 - k)
            N2 = (1 + i)*(1 + j)*(1 - k)
            N3 = (1 - i)*(1 + j)*(1 - k)
            N4 = (1 - i)*(1 - j)*(1 - k)
            N5 = (1 + i)*(1 - j)*(1 + k)
            N6 = (1 + i)*(1 + j)*(1 + k)
            N7 = (1 - i)*(1 + j)*(1 + k)
            N8 = (1 - i)*(1 - j)*(1 + k)

            shape_functions = np.array([N1, N2, N3, N4, N5, N6, N7, N8])
            jacobian_ratio = []
            for ii in range(np.shape(self.elements)[0]):
                xx = 0
                yy = 0
                zz = 0
                for jj in range(np.shape(self.elements)[1]):
                    xx += shape_functions[jj]*x[self.elements[ii, jj] - 1]
                    yy += shape_functions[jj]*y[self.elements[ii, jj] - 1]
                    zz += shape_functions[jj]*z[self.elements[ii, jj] - 1]
            
                gauss_points = [(-np.sqrt(5/3), -np.sqrt(5/3), -np.sqrt(5/3)), 
                (-np.sqrt(5/3), +np.sqrt(5/3), +np.sqrt(5/3)),
                (-np.sqrt(5/3), +np.sqrt(5/3), -np.sqrt(5/3)),
                (-np.sqrt(5/3), -np.sqrt(5/3), +np.sqrt(5/3)),
                (+np.sqrt(5/3), +np.sqrt(5/3), +np.sqrt(5/3)),
                (+np.sqrt(5/3), -np.sqrt(5/3), -np.sqrt(5/3)),
                (+np.sqrt(5/3), -np.sqrt(5/3), +np.sqrt(5/3)),
                (+np.sqrt(5/3), +np.sqrt(5/3), -np.sqrt(5/3))]

                deriv1 = sym.lambdify([i, j, k], sym.diff(xx, i), "numpy")
                deriv2 = sym.lambdify([i, j, k], sym.diff(yy, i), "numpy")
                deriv3 = sym.lambdify([i, j, k], sym.diff(zz, i), "numpy")
                deriv4 = sym.lambdify([i, j, k], sym.diff(xx, j), "numpy")
                deriv5 = sym.lambdify([i, j, k], sym.diff(yy, j), "numpy")
                deriv6 = sym.lambdify([i, j, k], sym.diff(zz, j), "numpy")
                deriv7 = sym.lambdify([i, j, k], sym.diff(xx, k), "numpy")
                deriv8 = sym.lambdify([i, j, k], sym.diff(yy, k), "numpy")
                deriv9 = sym.lambdify([i, j, k], sym.diff(zz, k), "numpy")

                jacobian_values = np.zeros((1, 8))
                count = 0
                for point in gauss_points:
                    jacobian_matrix = np.array([[deriv1(point[0], point[1], point[2]), deriv2(point[0], point[1], point[2]), deriv3(point[0], point[1], point[2])],
                    [deriv4(point[0], point[1], point[2]), deriv5(point[0], point[1], point[2]), deriv6(point[0], point[1], point[2])],
                    [deriv7(point[0], point[1], point[2]), deriv8(point[0], point[1], point[2]), deriv9(point[0], point[1], point[2])]])

                    jacobian_values[0, count] = np.linalg.det(jacobian_matrix)
                    count += 1
                jacobian_ratio.append(np.min(jacobian_values)/np.max(jacobian_values))
            print(jacobian_ratio)

            
def plot_3d(nodes):
    ax = plt.axes(projection="3d")
    ax.plot3D(nodes[:, 0], nodes[:, 1], nodes[:, 2], "b.", markersize=0.5)
    plt.show()


def main():
    sphere = sphere_dims(0, 0, 0, 1)
    element_length = 0.5#np.linspace(1, 0.025, num=100)
    pid = 1000000

    #outer_nodes = error.surface_points()
    #plot_3d(outer_nodes)

    #error.aspect_ratio()
    """e = []
    a = []
    for el in element_length:
        sphere_ent = sphere_entity(sphere.r, el, sphere.x, sphere.y, sphere.z, pid)
        error = error_types(sphere.x, sphere.y, sphere.z, sphere.r, sphere_ent[0], sphere_ent[1], el)
        mesh = mesh_accuracy(sphere.x, sphere.y, sphere.z, sphere.r, sphere_ent[0], sphere_ent[1], el)
        e.append(error.maximum_error()*1E9)
        a.append(mesh.aspect_ratio()[1])
    
    np.savetxt("C:/Users/lampr/Desktop/length.txt", element_length, fmt="%f")
    np.savetxt("C:/Users/lampr/Desktop/error.txt", np.array(e), fmt="%f")
    np.savetxt("C:/Users/lampr/Desktop/aspect.txt", np.array(a), fmt="%f")"""
    sphere_ent = sphere_entity(sphere.r, element_length, sphere.x, sphere.y, sphere.z, pid)
    mesh = mesh_accuracy(sphere.x, sphere.y, sphere.z, sphere.r, sphere_ent[0], sphere_ent[1], element_length)
    mesh.jacobian()
    """a = 0
    for i in range(np.shape(sphere_ent[1])[0]):
        a += mesh.volume(int(i))
        #print(mesh.volume(int(i)))
    print(a)"""


if __name__ == "__main__":
    main()

