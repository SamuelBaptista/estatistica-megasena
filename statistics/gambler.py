from random import sample
from tqdm import tqdm
from numpy import max
from time import sleep


class Gambler:

    def __init__(self, numbers_range, numbers_amount, numbers_played, trials, raffle_numbers):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount
        self.numbers_played = numbers_played
       
        self.trials = trials
        self.raffle_numbers = raffle_numbers

        self.hits = None
        self.numbers = None               
        self.cheers = False

    def gamble(self):
        nr = self.numbers_range+1
        np = self.numbers_played
        
        self.numbers = [sample(range(1, nr), np) for _ in range(self.trials)]
        
        return self.numbers

    def check_hits(self):
        self.hits = [sum(numbers in self.numbers[i] for numbers in self.raffle_numbers) for i in range(self.trials)]

        return self.hits  
            

    def celebrate(self):        
        if self.numbers_amount in self.hits:
            self.cheers = True


    def yell(self):
        bold = '\033[1m'
        clear = '\033[m' 
        
        if self.cheers:

            print('YAY! We won!')
            print(f'We hit all the {bold}{self.numbers_amount}{clear} numbers!')

        else:

            print(f"That´s SAD! We tried {bold}{self.trials:,}{clear} time(s), but,", end=' ')
            print(f"we didn't hit all the {bold}{self.numbers_amount}{clear} numbers!")
            print(f'Our best game just hit {bold}{max(self.hits)}{clear} number(s)!')


    def play(self):
        self.gamble()
        self.check_hits()
        self.celebrate()

        print()       
        self.yell()  
                   
        self.cheers = False