import Config
import error
import case
import numpy as np


class Scenario:
    def __init__(self, config):
        self.config = config
        self.error = error.Errors(config)

        self.case = case.Case(self.config.missle_type, (0, 0, 0), self.config.hit_point, self.config.intercept_point,
                              self.config.pre_dist)
        # self.dronePath = self.case.dronePath_array
        self.x_points = np.linspace(0, self.config.intercept_point[0], 100)
        self.speed_param = 30  # will be in the config csv
        self.speed = 0

    def update_speed(self, time_from_start):
        # calculate the speed of the drone, m/s
        # the speed linearly goes up to speed_param and gets to that speed at 1 sec
        # and then stays steady
        if time_from_start < 1:
            self.speed = time_from_start * self.speed_param
        else:
            self.speed = self.speed_param

    def calc_dist(self, last_dist, time_from_start_last, dx):
        # calc the distance the drone has moved
        # take the last distance + the time difference * the average speed
        old_speed = self.speed
        self.update_speed(time_from_start_last + dx)
        return last_dist + dx * ((old_speed + self.speed) / 2)

    def curve(self, p0, p1, p2, pcurr, P = None):
        # this function calcs the ratio from curr to p1 and curr to p2,
        # if its smaller then P then continue aiming for p1,
        # if its bigger then P then update p0 = p1, p1 = p2, p2 = new_p
        if P is None:
            P = self.distance(p0[0], p0[1], p1[0], p1[0])/self.distance(p0[0], p0[1], p2[0], p2[0])
        curr_ratio = self.distance(pcurr[0], pcurr[1], p1[0], p1[0])/self.distance(pcurr[0], pcurr[1], p2[0], p2[0])
        if curr_ratio > P:
            print("update points")
        else:
            return curr_ratio

    def update(self, old_point):
        """
        find the new point with error and pid on xy and th
        """
        point_with_error = (self.error.get_value_with_error(old_point[0]),
                            self.error.get_value_with_error(old_point[1]))
        # self.error.get_value_with_error(old_point[2]))
        # pid_z = self.Pid(point_with_error[2])
        pid_x = self.Pid(point_with_error[0])
        pid_y = self.Pid(point_with_error[1])
        # return pid_x, pid_y #todo: add z
        return old_point

    def Pid(self, x):
        # todo: add pid
        return x

    def find_spot_on_parabulah(self, a, b, c, drone_pos_curr, drone_start_pos, intercept_pos):
        # this function uses binary search to find the closest spot on the parabulah
        if drone_start_pos[0] <= intercept_pos[0]:
            x1 = drone_start_pos[0]
            x2 = intercept_pos[0]
        else:
            x1 = intercept_pos[0]
            x2 = drone_start_pos[0]
        y1 = a * x1 ** 2 + b * x1 + c
        y2 = a * x2 ** 2 + b * x2 + c
        count = 0
        while self.distance(x1, y1, x2, y2) > 1:
            if self.distance(drone_pos_curr[0], drone_pos_curr[1], x1, y1) < self.distance(drone_pos_curr[0],
                                                                                           drone_pos_curr[1], x2, y2):
                # closer to x1
                x2 = (x1 + x2) / 2
                y2 = a * x2 ** 2 + b * x2 + c
            else:
                # closer to x2
                x1 = (x1 + x2) / 2
                y1 = a * x1 ** 2 + b * x1 + c
            count += 1

        return (x1 + x2) / 2, (y1 + y2) / 2

    def distance(self, x1, y1, x2, y2):
        # distace between 2 points
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def find_spot_on_linear(self, m, n, drone_pos_curr, drone_start_pos, intercept_pos):
        # find the closest spot on a linear line using binary search
        # most likely use the other search - "find_spot+on_linear2"
        if drone_start_pos[0] <= intercept_pos[0]:
            x1 = drone_start_pos[0]
            x2 = intercept_pos[0]
        else:
            x1 = intercept_pos[0]
            x2 = drone_start_pos[0]
        z1 = m * x1 + n
        z2 = m * x2 + n
        count = 0
        while self.distance(x1, z1, x2, z2) > 1:
            if self.distance(drone_pos_curr[0], drone_pos_curr[1], x1, z1) < self.distance(drone_pos_curr[0],
                                                                                           drone_pos_curr[1], x2, z2):
                # closer to x1
                x2 = (x1 + x2) / 2
                z2 = m * x2 + n
            else:
                # closer to x2
                x1 = (x1 + x2) / 2
                z1 = m * x1 + n
            count += 1

        return (x1 + x2) / 2, (z1 + z2) / 2

    def find_spot_on_linear2(self, m, n, curr_x):
        # this function gets the correct x from the fixed parbulah,
        # with the correct x it gets the y
        return m * curr_x + n
