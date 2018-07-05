"""
clickabit datasets manager
"""
import json
import random
import os


ABS_PATH = os.path.dirname(__file__)

def __load_data_saurabhmathur96(dataset):
    cb_path = os.path.join(ABS_PATH, 'data@saurabhmathur96', 'clickbait.txt')
    with open(cb_path, 'r') as file:
        rawdata = file.read().split('\n')
        dataset.extend([(e, True) for e in rawdata])

    norm_path = os.path.join(ABS_PATH, 'data@saurabhmathur96', 'genuine.txt')
    with open(norm_path, 'r') as file:
        rawdata = file.read().split('\n')
        dataset.extend([(e, False) for e in rawdata])

    return dataset


def __load_data_peterldowns(dataset):
    path = 'data@peterldowns'
    file_names = ['buzzfeed.json', 'clickhole.json', 'dose.json', 'nytimes.json']
    for file_name in file_names:
        full_path = os.path.join(ABS_PATH, path, file_name)
        with open(full_path, 'r') as file:
            raw_data = json.load(file)
            dataset.extend([(d['article_title'], bool(d['clickbait'])) for d in raw_data])
    return dataset


def __load_data(train_len, test_len):
    dataset = []
    __load_data_saurabhmathur96(dataset)
    __load_data_peterldowns(dataset)
    random.shuffle(dataset)
    if train_len is None:
        train_len = int(0.9 * len(dataset))
    if test_len is None:
        test_len = len(dataset) - train_len
    train_set = dataset[0: min(train_len, len(dataset))]
    test_set = dataset[(-min(test_len, len(dataset))-1): -1]
    return train_set, test_set


def load_data(train_len=None, test_len=None):
    """
    Load clickbait dataset
    now there are 17917 titles in total
    Args:
    train_len: the length of train set(load 90% of dataset by default)
    test_len: the length of test set(load remains by default)
    Returns:
    (train_set_x, train_set_y, test_set_x, test_set_y) each one is a list
    """
    raw_data_train, raw_data_test = __load_data(train_len, test_len)
    return [i[0] for i in raw_data_train], [i[1] for i in raw_data_train],\
            [i[0] for i in raw_data_test], [i[1] for i in raw_data_test]


# for test only
def __test():
    train_set_x, train_set_y, test_set_x, test_set_y = load_data(10, 10)
    print('Train set:')
    for i, title in enumerate(train_set_x):
        print(str(train_set_y[i]) + '\t' + title)
    print('\nTest set:')
    for i, title in enumerate(test_set_x):
        print(str(test_set_y[i]) + '\t' + title)

if __name__ == '__main__':
    __test()
