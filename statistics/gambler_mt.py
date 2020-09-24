import random

from numpy import max

from threading import Thread
from threading import Lock


class GamblerMT:

    def __init__(self, numbers_range, numbers_amount, numbers_played, trials, samples):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount
        self.numbers_played = numbers_played
        
        self.trials = trials
        self.samples = samples

        self.lock = Lock()

        self.hits = []
        self.hits_list = []

        self.gamble_list = []
        self.thread_list = []
                
        self.cheers = False

    def gamble(self):

        nr = self.numbers_range+1
        np = self.numbers_played
        tr = self.trials

        return (random.sample(range(1, nr), np) for _ in range(tr))


    @staticmethod
    def check_hits(raffle_card, raffle_numbers):
        hits = sum(numbers in raffle_card for numbers in raffle_numbers)
        return hits
    

    def check_gambles(self, gamble, raffle_numbers):
                     
        for raffle_card in gamble:
            
            hits = self.check_hits(raffle_card, raffle_numbers)            
            self.hits.append(hits)

        self.hits_list.append(self.hits.copy())     
            

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

            print(f"WOW! Even with {bold}{self.trials:,}{clear} trials,", end=' ')
            print(f"we didn't hit all the {bold}{self.numbers_amount}{clear} numbers!")
            print(f'Our best game just hit {bold}{max(self.hits)}{clear} numbers!')


    def play(self, raffle_numbers):

        for i in range(self.samples):
            self.gamble_list.append(self.gamble())
            self.thread_list.append(Thread(target=self.check_gambles, args=(self.gamble_list[i], raffle_numbers)))              

        for thread in self.thread_list:
            thread.start()

        for thread in self.thread_list:
            thread.join()
               
        print()       
        self.celebrate()
        self.yell()  
        print()
        print('-=' * 30, end='\n\n')                
            
        self.hits.clear()
        self.cheers = False