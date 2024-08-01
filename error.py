import numpy as np
from Config import Config

class Errors():
    def __init__(self, config):
        self.mu = config.mu
        self.sigma = config.sigma
        self.bias = config.bias
        self.max_shift = 5

    def get_value_with_error(self, val):
        value = np.random.normal(self.mu+self.bias, self.sigma)
        return val + value * self.max_shift



#
# def main():
#     errors_instance = Errors(Config)
#     for i in range(10):
#         print(errors_instance.get_value_with_error(val=1))
#
#
# if __name__ == '__main__':
#     main()
