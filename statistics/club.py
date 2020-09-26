import random
import multiprocessing as mp


class GamblersClub:

    def __init__(self, numbers_range, numbers_amount, numbers_played, trials, players, raffle_numbers):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount
        self.numbers_played = numbers_played
        
        self.trials = trials
        self.players = players

        self.raffle_numbers = raffle_numbers

        self.gamblers = mp.cpu_count()

        self.hits = None
        self.hits_list = None


    def gamble(self, _):
        nr = self.numbers_range+1
        np = self.numbers_played
        
        gamble = random.sample(range(1, nr), np)

        return sum(numbers in gamble for numbers in self.raffle_numbers)


    def check_hits(self):        
        pool = mp.Pool(processes=self.gamblers) 
               
        self.hits = pool.map(self.gamble, range(self.trials))        
        pool.close()
        
        return self.hits


    def play(self):
        self.hits_list = [self.check_hits() for _ in range(self.players)]
                    
        