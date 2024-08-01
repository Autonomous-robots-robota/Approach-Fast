import Config
import error
import case
import numpy as np


class Scenario:
    def __init__(self, config):
        self.config = config
        self.error = error.Errors(config)

        self.case = case.Case(self.config.missle_type, (0, 0, 0), self.config.hit_point, self.config.intercept_point, self.config.pre_dist)
        # self.dronePath = self.case.dronePath_array
        self.x_points = np.linspace(0,self.config.intercept_point[0],100)



    def update(self, old_point):
        """
        find the new point with error and pid on xy and th
        """
        point_with_error = (self.error.get_value_with_error(old_point[0]),
                            self.error.get_value_with_error(old_point[1]))
                            #self.error.get_value_with_error(old_point[2]))
        #pid_z = self.Pid(point_with_error[2])
        pid_x = self.Pid(point_with_error[0])
        pid_y = self.Pid(point_with_error[1])
        # return pid_x, pid_y #todo: add z
        return old_point



    def Pid(self, x):
        #todo: add pid
        return x


    def find_spot_on_parabulah(self,a,b,c,drone_pos, start_pos, end_pos):
        if start_pos[0] <= end_pos[0]:
            x1 = start_pos[0]
            x2 = end_pos[0]
        else:
            x1 = end_pos[0]
            x2 = start_pos[0]
        y1 = a * x1 ** 2 + b * x1 + c
        y2 = a * x2 ** 2 + b * x2 + c
        count=0
        while self.distance(x1, y1, x2, y2) > 1:
            if self.distance(drone_pos[0], drone_pos[1], x1, y1 ) < self.distance(drone_pos[0], drone_pos[1], x2, y2):
                # closer to x1
                x2 = (x1+x2)/2
                y2 = a * x2 ** 2 + b * x2 + c
            else:
                #closer to x2
                x1 = (x1 + x2) / 2
                y1 = a * x1 ** 2 + b * x1 + c
            count+=1

        return (x1+x2)/2, (y1+y2)/2


    def distance(self, x1, y1, x2, y2):
        return ((x1-x2)**2+(y1-y2)**2)**0.5





#
# def main():
#     s = Scenario()
#
#
# if __name__ == '__main__':
#     main()