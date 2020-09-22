from pandas import Series
from collections import Counter

from numpy import mean
from numpy import int64

class Reporter:

    def __init__(self, gambler_hits, numbers_played):

        self.hits_list = gambler_hits
        self.numbers_played = numbers_played
        
        self.trials = len(self.hits_list[0])
        
        self.hits_amount = []
        

    def count_gambler_hits(self):        
        for hits in self.hits_list:           
            self.hits_amount.append(Counter(hits))


    def get_number_info(self, number):

        self.hits_amount.clear()
        self.count_gambler_hits()
        
        number_list = []
        
        for counter in self.hits_amount:
            number_list.append(counter[number])

        return number_list
        

    def number_bootstrap_report(self, number, confidence):

        up = 1-((1-confidence)/2)
        down = 0+((1-confidence)/2)

        bootstrap = []        
        series = Series(self.get_number_info(number))

        for _ in range(10000):
            bootstrap.append(int(series.sample(frac=1, replace=True).mean()))

        confidence_interval = Series(bootstrap).quantile([down, up]).astype(int64)
        print(confidence_interval.to_string())


    def number_hit_report(self, number):
        
        bootstrap = []
        series = Series(self.get_number_info(number))

        for _ in range(10000):
            bootstrap.append(series.sample(frac=1, replace=True).mean())

        mean_hits = int(mean(bootstrap))

        if mean_hits == 0:
            chance = 0
        else:              
            chance = self.trials // mean_hits
            
        bold = '\033[1m'
        clear = '\033[m'
        urder = '\033[4m'
        
        print(f'The mean score was approximately', end=' ')
        print(f'{bold}{mean_hits}{clear} each', end=' ')
        print(f'{bold}{self.trials:,.0f}{clear} trials:')
        print()

        if chance == 0:
            print('We didnt hit the pot in any raffle! Or almost that...')
        else:
            print(f'{urder}{bold}1{clear} hit each {urder}{bold}{chance:,.0f}{clear} games played!')
            
        print()
        print(f'We have played with {bold}{self.numbers_played}{clear} numbers.')

            