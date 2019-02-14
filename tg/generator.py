import re
import os
from pandas import DataFrame
from .tools import clear_text
from tweepy.error import TweepError
from .tools import prepare_batchs
from . import rows_number
from . import tweepy
from . import read_csv
from . import step
from . import ids
from . import api
from . import save_path
from . import print_errors

def generate():
    print('|--------------------------------------------------------------')
    print('|              PREPARING CLEARED TWEET TEXT                   |')
    print('|--------------------------------------------------------------')

    # Define buffer to store cleared twitter text
    prepared_texts = []
    prepared_labels = []

    for i in range (0, rows_number, step):
        batch = ids[i:i+step]
        print('| - Read size: {} from {} to {} .'.format(len(batch), i, i+step), end='')

        try:
            signal_batch = api.statuses_lookup(batch)
        except TweepError as e:
            errors = ['Bad authentication data']
            print_errors(errors)

        print('signal received . . . ', end='')
        text_batch, label_batch = prepare_batchs(signal_batch)
        print('text extracted . . . ', end='')
        cleared_batch = clear_text(text_batch)
        print('cleared | Proceed {} %'.format(round(((i+step) / rows_number )*100)))
        prepared_texts = prepared_texts + cleared_batch
        prepared_labels = prepared_labels + label_batch

    # Grab all data tougether and save them into new csv file
    packed_data = DataFrame({'text': prepared_texts, 'label': prepared_labels})

    save_dir = re.sub(r'([^\/]+)$','',save_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    packed_data.to_csv(save_path, index=False)

    print('|-------------------------------------------------------------|')
    print('|                       CREATED                               |')
    print('|-------------------------------------------------------------|')
