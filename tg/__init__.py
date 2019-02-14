from pandas import read_csv
import tweepy
import json


def print_errors(errors: list):
    """Prints pretty errors

    Args:
        errors (list): A list of error strings
    Return
        None
    """
    if len(errors) > 0:
        for error in errors:
            print('\n')
            print('### Errors')
            print(f'\t- {error}', end='\n\n\n')
            exit()

with open('config.json', 'r') as f:
    config = json.load(f)
    consumer_key = config['twitter_api']['consumer_key']
    consumer_secret = config['twitter_api']['consumer_secret']
    access_token = config['twitter_api']['access_token']
    access_token_secret = config['twitter_api']['access_token_secret']
    path = config['dataset_path']
    save_path = config['generated_dataset_path']
    rows_number = config['rows_to_read']
    step = config['clearing_batch_step']

    errors = []
    if not consumer_key:
        errors.append('Consumer key was not set')
    if not consumer_secret:
        errors.append('Consumer secrete was not set')
    if not access_token:
        errors.append('Access token was not set')
    if not access_token_secret:
        errors.append('Access token secrete was not set')
    if not path:
        errors.append('Dataset file path was not set')
    if not save_path:
        errors.append('Prepared dataset file path was not set')
    if not rows_number:
        errors.append('Rows number was not set')
    if not step:
        errors.append('Step size was not set')
    if not 10 <= rows_number <= 100000:
        errors.append('Rows number is not between 100000 and 100000')
    if not 10 <= step <= 100:
        errors.append('Step must be between 10 and 100')

    print_errors(errors)

# Authenticate to the twitter using thweety
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create tweepy API isinstance
api = tweepy.API(auth, wait_on_rate_limit=True)

try:
    # Read csv file with tweets dataset
    df = read_csv(path, nrows=rows_number)
except:
    errors = ['Dataset file was not found']
    print_errors(errors)

# Receive as array the thweets ids list
ids = df.TweetID.array
