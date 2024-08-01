import numpy as np
from shapely.geometry import Polygon
import Config
import pandas as pd
import matplotlib.pyplot as plt
import utills



class Case:
    def __init__(self, name, drone_pos, hit_point, intercept_point, pre_dist):
        self.name = name
        self.a, self.b, self.c = self.get_parabola(drone_pos, hit_point, intercept_point, pre_dist)
        # self.dronePath_array, self.dronePath_poly = self.get_parabola((0, 0, 0), hit_point, intercept_point, pre_dist)

    def get_parabola(self, drone_pos, hit_point, intercept_point, pre_dist):
        # Calculate vx and vy using the correct points
        # print(type(hit_point[0]), hit_point[0])
        # print(type(pre_dist), pre_dist)
        # print(type(intercept_point[0]), intercept_point[0])
        vx = hit_point[0] - pre_dist - intercept_point[0]
        vy = hit_point[1] - pre_dist - intercept_point[1]

        # Creating matrix A and vector b for solving the parabola coefficients
        A = np.array([
            [drone_pos[0] ** 2, drone_pos[0], 1],
            [intercept_point[0] ** 2, intercept_point[0], 1],
            [2 * intercept_point[0], 1, 0]
        ])
        b = np.array([drone_pos[1], intercept_point[1], vy / vx])

        # Solve for coefficients a, b, c
        coefficients = np.linalg.solve(A, b)
        a, b, c = coefficients
        utills.plot_parbulah(a,b,c, int(drone_pos[0]),int(intercept_point[0]),drone_pos,intercept_point)
        # Print coefficients for debugging
        print(f"Coefficients = a: {a}, b: {b}, c: {c}")

        # Create and return the polygon
        # poly = Polygon([(drone_pos[0], drone_pos[1]), (intercept_point[0], intercept_point[1])])
        # Calculate 100 points along the polygon's boundary
        # boundary = poly.boundary
        # length = boundary.length
        # points = [boundary.interpolate(i / 100, normalized=True) for i in range(100)]

        # Convert to an array of tuples
        # points_array = [(point.x, point.y) for point in points]
        # return points_array, poly
        return a, b, c




