import os

CLUSTERED_RESULT_PATH = '../../../data/clustered_results'
RAW_DATASET_PATH = '../../../data/datasets'
RATINGS_FILE_NAME = 'ratings.csv'
RESULT_FILE_NAME = 'HierarchicalClustering.pkl'


def clustered_result_path(dataset_name):
    return os.path.join(CLUSTERED_RESULT_PATH, dataset_name, RESULT_FILE_NAME)


def raw_dataset_path(dataset_name):
    return os.path.join(RAW_DATASET_PATH, dataset_name, RATINGS_FILE_NAME)