import random
import utills


class Config:
    def __init__(self):
        # FileNameList = ["config1", "config2", "config3", "config4", "config5"]
        # RanfomConfigFile = random.choice(FileNameList)
        self.df = utills.load_csv2('config1.csv')  # is a df
        #self.get_row_number = random.randint(0, self.df.shape[0])
        self.get_row_number = 0
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

        # self.configData = {
        #     'p1': (10, 10, 10),
        #     'p2': (15, 15, 15),
        #     'dist': (12, 12, 12),
        #     'pre_dist': 3,
        #     'mu': 0,
        #     'sigma': 1,  # std
        #     'bias': 0,
        #     'dx': 1 / 10,  # sec
        #     'case_name': 'test'
        # }

    def get_point(self, mystring) -> tuple:
        mystring = mystring.split(',')
        mystrin_x = float(mystring[0].split('(')[1])
        mystrin_y = float(mystring[1])
        mystrin_z = float(mystring[2].split(')')[0])


        return (mystrin_x, mystrin_y, mystrin_z)

#
# def main():
#     c = Config()
#     # print(c.configData)
#
#
# if __name__ == '__main__':
#     main()
