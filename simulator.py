import matplotlib.pyplot as plt
import numpy as np

from scenario import Scenario
from Config import Config
import error


class Simulator:
    def __init__(self):
        self.config = Config()
        self.scenario = Scenario(self.config)
        self.param = self.config.dx
        self.my_errors = error.Errors(self.config)

        # # Setup the plot
        # self.fig, self.ax = plt.subplots()
        # self.ax.set_xlim(-10, 10)
        # self.ax.set_ylim(-10, 10)
        # self.scatter = self.ax.scatter([], [])

    def main(self):
        print()
        error_xs = []
        error_ys = []
        real_xs = []
        real_ys = []
        fixed_xs = []
        fixed_ys = []

        for x in self.scenario.x_points:
            y = self.scenario.case.a * x ** 2 + self.scenario.case.b * x + self.scenario.case.c
            real_xs.append(x)
            real_ys.append(y)
            error_x = self.my_errors.get_value_with_error(x)
            error_y = self.my_errors.get_value_with_error(y)
            error_xs.append(error_x)
            error_ys.append(error_y)
            fix_x, fix_y = self.scenario.find_spot_on_parabulah(self.scenario.case.a,
                                                                self.scenario.case.b,
                                                                self.scenario.case.c,
                                                                (error_x, error_y), (0, 0, 0),
                                                                self.config.intercept_point)
            fixed_xs.append(fix_x)
            fixed_ys.append(fix_y)

        plt.scatter(real_xs, real_ys, color='r', marker='.')
        plt.scatter(error_xs, error_ys, color='b', marker='.')
        plt.scatter(fixed_xs, fixed_ys, color='y', marker='.')
        plt.show()
        print()

    #     for i in range(len(self.scenario.dronePath)):
    #         new_point = self.scenario.update(self.scenario.dronePath[i])
    #         self.scenario.dronePath[i] = new_point
    #
    #     self.draw()
    #
    # def draw(self):
    #     self.scatter.set_offsets(self.scenario.dronePath)
    #     self.scatter.set_offsets(self.scenario.dronePath)
    #     plt.draw()
    #     plt.show()
    #     print()


if __name__ == "__main__":
    simulator = Simulator()
    # plt.ion()  # Turn on interactive mode for live plotting
    simulator.main()
