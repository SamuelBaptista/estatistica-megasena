import random


class Raffler:

    def __init__(self, numbers_range, numbers_amount):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount


    def run(self):

       return random.sample(range(1, self.numbers_range+1),
                            self.numbers_amount)