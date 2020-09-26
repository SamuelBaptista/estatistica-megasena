from collections import namedtuple
from random import sample


class Raffler:

    def __init__(self, numbers_range, numbers_amount):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount

        self.raffle_numbers = None

        self.run()
        
    def run(self):
        nr = self.numbers_range+1
        n = self.numbers_amount

        self.raffle_numbers = sample(range(1, nr), n)

        return self.raffle_numbers