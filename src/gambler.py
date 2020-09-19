import random
import os

from numpy import mean  
from time import time
from tqdm import tqdm

from threading import Thread
from threading import Lock



class Gambler(Thread):

    def __init__(self, numbers_range, numbers_amount, trials, samples):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount
        self.trials = trials
        self.samples = samples

        self.lock = Lock()

        self.cpu_count = os.cpu_count()

        super().__init__()

    def run(self):
        pass


    def _generate_cards(self):
        pass


    def _do_raffle(self):
        pass


    def _check_numbers(self):
        pass


    def _create_report(self):
        pass