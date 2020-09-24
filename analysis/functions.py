import requests
import zipfile
import io
import os

import pandas as pd


def get_data_dir():

    data_dir = os.path.join(os.getcwd(), 'data')

    return data_dir


def download_raffle_file(url, path, filename):

    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    files = z.namelist()

    for f in files:
        if f.endswith('.htm'):   
            z.extract(f, path)
            os.replace('data/' + f, 'data/' + filename)


def transform_html_to_csv(path, filename):

    table = pd.read_html(os.path.join(path, filename),
                         thousands=".",
                         decimal=",")

    dataframe = pd.DataFrame(table[0])

    dataframe.to_csv(os.path.join(path, os.path.splitext(filename)[0] + '.csv'), index=False)


def pre_process_dataframe(filename, **kwargs):

    csv_file = 'data/' + os.path.splitext(filename)[0] + '.csv'

    dataframe = pd.read_csv(csv_file,
                            index_col='Concurso',
                            parse_dates=['Data Sorteio'],
                            na_values='000')

    if 'drop' in kwargs.keys():

        drop_columns = kwargs['drop']

        dataframe.drop(drop_columns,
                       axis=1,
                       inplace=True)


    dataframe.drop_duplicates(inplace=True)
    dataframe.fillna(0, inplace=True)
    
    dataframe = dataframe.convert_dtypes()

    return dataframe


def print_frequency_report(frequency_dataframe):

    freq_num = frequency_dataframe.sort_values()
    freq_num2 = freq_num.reset_index()

    menos = []
    mais = []

    bold = '\033[1m'
    clear = '\033[m'         

    print(f'{bold}OS NÚMEROS QUE MAIS APARECERAM FORAM:{clear}\n')

    for i in range(59, 53, -1):
        print(f'{bold}{freq_num2["Numero"][i]}{clear} que apareceu em {bold}{freq_num2["Concurso"][i]}{clear} sorteios')
        mais.append(freq_num2["Numero"][i])

    print()
    print(f'{bold}OS NÚMEROS QUE MENOS APARECERAM FORAM:{clear}\n')

    for i in range(6):
        print(f'{bold}{freq_num2["Numero"][i]}{clear} que apareceu em {bold}{freq_num2["Concurso"][i]}{clear} sorteios')
        menos.append(freq_num2["Numero"][i])

    # Formatando os jogos com números mais e menos frequentes para futura avaliação

    mais.sort()
    menos.sort()

    print()                                                                                                        
    print(f'Jogo com números mais frequentes: {mais}')
    print(f'Jogo com números menos frequentes: {menos}')          