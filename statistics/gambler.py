import random

from tqdm import tqdm
from numpy import max
from time import sleep


class Gambler:

    def __init__(self, numbers_range, numbers_amount, numbers_played, trials, samples):

        self.numbers_range = numbers_range
        self.numbers_amount = numbers_amount
        self.numbers_played = numbers_played
        
        self.trials = trials
        self.samples = samples

        self.hits = []
        self.hits_list = []
                
        self.cheers = False

    def gamble(self):
        return (random.sample(range(1, self.numbers_range+1),
                              self.numbers_played) for _ in range(self.trials))
         

    def gamble_samples(self):   
        return (self.gamble() for _ in range(self.samples))


    @staticmethod
    def check_hits(raffle_card, raffle_numbers):
        hits = sum(numbers in raffle_card for numbers in raffle_numbers)
        return hits
    

    def check_gambles(self, gamble, raffle_numbers):              
        for raffle_card in tqdm(gamble, total=self.trials):
            
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

        gamble_samples = self.gamble_samples()      

        for i, gamble in enumerate(gamble_samples):
            sleep(0.5)          
            self.check_gambles(gamble, raffle_numbers)

            if i == 0:
                
                print()       
                self.celebrate()
                self.yell()  
                print()
                print('-=' * 30, end='\n\n')

                if self.samples > 1:
                
                    print("Now, i'll play all the remaining games... Just wait! Thanks.", end='\n\n')
                
            
            self.hits.clear()
            self.cheers = False