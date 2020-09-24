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

        print(f'A quantidade de acertos foi de {confidence_interval[down]}', end= ' ')
        print(f'até {confidence_interval[up]} considerando {confidence*100}% de confiança')


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


    def save_hits(self):
        save(f'data/{self.trials:_}_trials_{len(self.hits_list):_}_samples.npy', self.hits_list)


    def load_hits(self, path):
        self.hits_list = load(path)
        self.trials = len(self.hits_list[0])


            