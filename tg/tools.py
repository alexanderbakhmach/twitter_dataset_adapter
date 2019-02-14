import re
from . import json
from . import tweepy
from . import df


labels_digits = {
    'Negative': 0,
    'Positive': 1,
    'Neutral': 2
}

def clear_text(texts: list):
    """Crear russian twitter text
    Remove all special characters and ascii characters
    Remove all unicodes which are not russian lowercase letters
    Remove all whitespaces at the begining of the line
    Remove all multi whitespaces and leave only one between words

    Args:
        texts (list): The batch of texts to clean
    Return:
        list - The batch of cleared texts
    """
    cleared_texts = []  # Define cleared text buffer
    regex_chars = r'[^\u0430-\u044F ]'  # Regex to filter all non russian chars
    regex_whitespaces_begining = r'^\s*'  # Regex to remove all whitespaces at the begining
    regex_multiple_whitespaces = r' +'  # Regex to remove multiple whitespaces
    regex_whitespaces_ending = r'[ \t]+$'  # Regex to remove all trailing whitespaces

    for text in texts:
        lower_case_text = text.lower()
        cleared_text = re.sub(regex_chars, '', lower_case_text)
        cleared_text = re.sub(regex_whitespaces_begining, '', cleared_text)
        cleared_text = re.sub(regex_multiple_whitespaces, ' ', cleared_text)
        cleared_text = re.sub(regex_whitespaces_ending, '', cleared_text)
        cleared_texts.append(cleared_text)
    return cleared_texts


def prepare_batchs(signals: list):
    """Receive text from tweepy signal object
    According to the docs of the tweepy
    http://docs.tweepy.org/en/v3.5.0/api.html#API.statuses_lookup
    lookup method returns signal object which have the twitter text
    in the text attribute so we turn our signal batch into tweeter texts batch
    Args:
        signals (list): tweepy signal objects list
    Return:
        list - the batch of tweeter texts
    """
    texts = []  # Define epty batch to store received text
    labels = []
    for signal in signals:
        texts.append(signal.text)
        label = df[df.TweetID==signal.id].iloc[0].HandLabel
        labels.append(labels_digits[label])
    return texts, labels
