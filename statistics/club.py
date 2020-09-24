import random

from tqdm import tqdm

from threading import Thread
from threading import Lock


class GamblersClub:

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

        self.lock.acquire()
                     
        for raffle_card in tqdm(gamble, total=self.trials):
            
            hits = self.check_hits(raffle_card, raffle_numbers)            
            self.hits.append(hits)

        self.hits_list.append(self.hits.copy())
        self.hits.clear()

        self.lock.release()     


    def play(self, raffle_numbers):

        for i in range(self.samples):
            self.gamble_list.append(self.gamble())
            
            self.thread_list.append(Thread(target=self.check_gambles,
                                           args=(self.gamble_list[i],
                                                 raffle_numbers)))              

        for thread in self.thread_list:
            thread.start()

        for thread in self.thread_list:
            thread.join()