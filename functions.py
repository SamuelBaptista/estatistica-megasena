import requests
import zipfile
import io
import os

import pandas as pd

from config import SAVE_PATH, DOWNLOAD_PATH, FILENAME


def download_raffle_file(url, path, filename):

    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    files = z.namelist()

    for f in files:
        if f.endswith('.htm'):   
            z.extract(f, path)
            os.replace(f, filename)


def transform_html_to_csv(path, filename):
    table = pd.read_html(os.path.join(path, filename))
    df = pd.DataFrame(table[0])

    df.to_csv(os.path.join(path, os.path.splitext(filename)[0] + '.csv'), index=False)



if __name__ == "__main__":

    download_raffle_file(url=DOWNLOAD_PATH, path=SAVE_PATH, filename=FILENAME)
    transform_html_to_csv(path=SAVE_PATH, filename=FILENAME)