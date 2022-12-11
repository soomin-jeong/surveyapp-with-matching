import pandas as pd

import os
import string
import random
import csv

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

RAW_DATASET_PATH = f'{CURRENT_PATH}/../../data/datasets'
CLUSTERED_RESULT_PATH = f'{CURRENT_PATH}/../../data/clustered_results'
STRATEGY_RESULT_PATH = f'{CURRENT_PATH}/../../data/strategy_rep_items'

RATINGS_FILE_NAME = 'ratings.csv'
CLUSTERED_RESULT_FILE_NAME = 'HierarchicalClustering.pkl'
STRATEGY_RESULT_FILE_NAME = 'StrategyRep.pkl'




def generate_random_tokens(token_len):
    """Gemerate a random string of given length

    Args:
        token_len (int): desired length of random token string

    Returns:
        _type_(str): a token string of desired length
    """
    # all lowercase characters and numbers in ascii
    all_chars = string.ascii_lowercase + string.digits
    res = ''
    for i in range(token_len):
        c = random.choice(all_chars)
        res = res + random.choice(all_chars)
    return res


def list_subdirectoreis(dir_path):
    directories = []
    for file in os.listdir(dir_path):
        d=os.path.join(dir_path, file)
        if os.path.isdir(d) and file != "__init__.py":
            directories.append(file)
    return directories


def list_directory_files(dir_path):
    files = []
    for file in os.listdir(dir_path):
        f=os.path.join(dir_path, file)
        filenames = file.split('.')
        if os.path.isfile(f) and file != '__init__.py':
            if filenames[0] != "":
                files.append(file.split('.')[0])
    return files


def generate_random_reclists(dataset_file_path, save_file_path, reclist_length):
    df = pd.read_csv(dataset_file_path,dtype='str')
    all_items = df['movieId'].unique().tolist()
    

    all_users = df['userId'].unique()


    with open(save_file_path, 'w') as f:
        write = csv.writer(f)
        index = ['userId']+ [f'item_{i+1}' for i in range(reclist_length)]
        write.writerow(index)
        for u in all_users:
            res = [u] + (random.choices(all_items, k=reclist_length))
            write.writerow(res)


def raw_dataset_path(dataset_name):
    return os.path.join(RAW_DATASET_PATH, dataset_name, RATINGS_FILE_NAME)


def clustered_result_path(dataset_name):
    return os.path.join(CLUSTERED_RESULT_PATH, dataset_name, CLUSTERED_RESULT_FILE_NAME)


def strategy_result_path(strategy_name, dataset_name):
    return os.path.join(STRATEGY_RESULT_PATH, strategy_name, dataset_name, STRATEGY_RESULT_FILE_NAME)


def convert_current_ratings_str_into_list(current_ratings_str: str) -> [int]:
    ## convert the chosen items as string into list
    if current_ratings_str == "[]" or current_ratings_str is None:
        return []
    else:
        return [int(each) for each in current_ratings_str[1:-1].split(',')]


class abstract_attribute(object):
    def __get__(self, obj, type):
        raise NotImplementedError("This attribute was not set in a subclass")