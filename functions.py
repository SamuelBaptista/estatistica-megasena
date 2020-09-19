import requests
import zipfile
import io
import os

import pandas as pd

from config import DOWNLOAD_PATH, FILENAME


def get_working_dir_path():

    return os.getcwd()



def download_raffle_file(url, path, filename):

    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    files = z.namelist()

    for f in files:
        if f.endswith('.htm'):   
            z.extract(f, path)
            os.replace(f, filename)


def transform_html_to_csv(path, filename):

    table = pd.read_html(os.path.join(path, filename),
                         thousands=".",
                         decimal=",")

    dataframe = pd.DataFrame(table[0])

    dataframe.to_csv(os.path.join(path, os.path.splitext(filename)[0] + '.csv'), index=False)


def pre_process_dataframe(filename, **kwargs):

    csv_file = os.path.splitext(filename)[0] + '.csv'

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

if __name__ == "__main__":

    save_path = get_working_dir_path()

    download_raffle_file(url=DOWNLOAD_PATH,
                         path=save_path,
                         filename=FILENAME)


    transform_html_to_csv(path=save_path,
                          filename=FILENAME)

    pre_process_dataframe(filename=FILENAME, drop=['Cidade', 'UF'])            