from pandas import Series
from collections import Counter

from numpy import save
from numpy import load
from numpy import mean
from numpy import int64

import matplotlib.pyplot as plt

class Reporter:

    def __init__(self, numbers_played, gambler_hits=None):

        self.hits_list = gambler_hits
        self.numbers_played = numbers_played

        if not self.hits_list == None:
            self.trials = len(self.hits_list[0])

        else:
            self.trials = None
        
        self.hits_amount = []

        self.bold = '\033[1m'
        self.clear = '\033[m'
        self.urder = '\033[4m'
        self.red = '\033[31m'
        

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

    @staticmethod
    def show_probabilities_table():
        prob_table = plt.imread("data/probabilities_table.png")
        plt.figure(figsize=(10,10))
        plt.axis('off')
        plt.tight_layout()        
        plt.imshow(prob_table)

        
    def confidence_report(self, number, confidence):

        if confidence > 1:
            confidence /= 100

        up = 1-((1-confidence)/2)
        down = 0+((1-confidence)/2)

        bootstrap = []        
        series = Series(self.get_number_info(number))

        for _ in range(10000):
            bootstrap.append(int(series.sample(frac=1, replace=True).mean()))

        confidence_interval = Series(bootstrap).quantile([down, up]).astype(int64)

        print('A média da quantidade de acertos foi de', end=' ')
        print(f'{self.red}{self.bold}{confidence_interval[down]}{self.clear}', end= ' ')
        print(f'até {self.red}{self.bold}{confidence_interval[up]}{self.clear}', end=' ')
        print(f'considerando {self.bold}{confidence*100:.0f}%{self.clear} de confiança')


    def hit_report(self, number):
        
        bootstrap = []
        series = Series(self.get_number_info(number))

        for _ in range(10000):
            bootstrap.append(series.sample(frac=1, replace=True).mean())

        mean_hits = int(mean(bootstrap))

        if mean_hits == 0:
            chance = 0
        else:              
            chance = self.trials // mean_hits
            
        
        print(f'The mean score was approximately', end=' ')
        print(f'{self.bold}{mean_hits}{self.clear} each', end=' ')
        print(f'{self.bold}{self.trials:,.0f}{self.clear} trials:')
        print()

        if chance == 0:
            print('We didnt hit the pot in any raffle! Or almost that...')
        else:
            print(f'{self.urder}{self.bold}1{self.clear}', end=' ')
            print(f'hit each {self.urder}{self.bold}{chance:,.0f}{self.clear} games played!')
            
        print()
        print(f'We have played with {self.bold}{self.numbers_played}{self.clear} numbers.')


    def save_hits(self):
        save(f'data/{self.trials:_}_trials_{len(self.hits_list):_}_samples.npy', self.hits_list)


    def load_hits(self, path):
        self.hits_list = load(path)
        self.trials = len(self.hits_list[0])


            