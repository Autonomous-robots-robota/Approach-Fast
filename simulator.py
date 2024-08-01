import matplotlib.pyplot as plt
import numpy as np

from scenario import Scenario
from Config import Config
import error


class Simulator:
    def __init__(self, number=None):
        if number is None:
            self.config = Config()
        else:
            self.config = Config(number)
        self.scenario = Scenario(self.config)
        self.param = self.config.dx
        self.my_errors = error.Errors(self.config)

    def main(self):
        print()
        error_xs = []
        error_ys = []
        error_zs = []

        real_xs = []
        real_ys = []
        real_zs = []

        fixed_xs = []
        fixed_ys = []
        fixed_zs = []

        for x in self.scenario.x_points:
            y = self.scenario.case.a * x ** 2 + self.scenario.case.b * x + self.scenario.case.c
            z = self.scenario.case.m * x + self.scenario.case.n
            real_xs.append(x)
            real_ys.append(y)
            real_zs.append(z)

            error_x = self.my_errors.get_value_with_error(x)
            error_y = self.my_errors.get_value_with_error(y)
            error_z = self.my_errors.get_value_with_error(z)
            error_xs.append(error_x)
            error_ys.append(error_y)
            error_zs.append(error_z)

            fix_x, fix_y = self.scenario.find_spot_on_parabulah(self.scenario.case.a,
                                                                self.scenario.case.b,
                                                                self.scenario.case.c,
                                                                (error_x, error_y), (0, 0, 0),
                                                                self.config.intercept_point)
            fixed_xs.append(fix_x)
            fixed_ys.append(fix_y)

            fix_z = self.scenario.find_spot_on_linear2(self.scenario.case.m,
                                                       self.scenario.case.n,
                                                       fix_x)
            fixed_zs.append(fix_z)

        plt.figure(figsize=(12, 7))

        plt.subplot(1, 2, 1)
        plt.scatter(real_xs, real_ys, color='r', marker='.', label="real_parabulah")
        plt.scatter(error_xs, error_ys, color='b', marker='.', label="points with added error")
        plt.scatter(fixed_xs, fixed_ys, color='y', marker='.', label="where the points should be")
        plt.axis('scaled')
        plt.title("x-y path")
        plt.xlabel("x axis")
        plt.ylabel("y axis")
        plt.legend()

        plt.subplot(1, 2, 2)

        plt.scatter(real_xs, real_zs, color='r', marker='.', label="real_linear")
        plt.scatter(error_xs, error_zs, color='b', marker='.', label="points with added error")
        plt.scatter(fixed_xs, fixed_zs, color='y', marker='.', label="where the points should be")
        plt.axis('scaled')
        plt.title("x-z path")
        plt.xlabel("x axis")
        plt.ylabel("z axis")
        plt.legend()

        plt.show()


if __name__ == "__main__":
    simulator = Simulator()
    simulator.main()
