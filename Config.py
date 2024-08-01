import random
import utills


class Config:
    def __init__(self, number=None):
        self.df = utills.load_csv2('config1.csv')  # is a df
        # self.get_row_number = random.randint(0, self.df.shape[0])
        if number is None:
            self.get_row_number = 0
        else:
            self.get_row_number = number
        self.row = self.df.loc[self.get_row_number]
        print(self.row)

        self.hit_point = self.get_point(self.row['hit_point'])
        self.intercept_point = self.get_point(self.row['intercept_point'])
        self.pre_intercept_point = self.get_point(self.row['pre_intercept_point'])
        self.pre_dist = float(self.row['pre_dist'])
        self.mu = float(self.row['mu'])
        self.sigma = float(self.row['sigma'])  # std
        self.bias = float(self.row['bias'])
        self.dx = float(self.row['d/x'])  # sec
        self.missle_type = self.row['missle type']

    def get_point(self, mystring) -> tuple:
        mystring = mystring.split(',')
        mystrin_x = float(mystring[0].split('(')[1])
        mystrin_y = float(mystring[1])
        mystrin_z = float(mystring[2].split(')')[0])

        return mystrin_x, mystrin_y, mystrin_z
