import io
import random
import zipfile
import requests
import numpy as np
from utils import *
from consts import *
from rapidfuzz import process
from Levenshtein import distance
from joblib import Parallel, delayed
from weighted_levenshtein import dam_lev
from sklearn.model_selection import train_test_split


def dl_distance(*args, **kwargs):
    del kwargs["score_cutoff"]
    return 10000 - dam_lev(*args, **kwargs)


def scorer():
    insert_costs = np.ones(128, dtype=np.float64) * 2.0
    delete_costs = np.ones(128, dtype=np.float64) * 2.0
    transpose_costs = np.ones((128, 128), dtype=np.float64) * 2.5
    substitute_costs = np.ones((128, 128), dtype=np.float64) * 3.0

    return {
        "scorer": dl_distance,
        "scorer_kwargs": {
            "insert_costs": insert_costs,
            "delete_costs": delete_costs,
            "transpose_costs": transpose_costs,
            "substitute_costs": substitute_costs,
        },
        "scorer": distance,
        "scorer_kwargs": {"weights": (2, 2, 3)},
    }


def get_match(query, candidates):
    return process.extract(query, candidates, limit=1, **scorer())[0]


def get_dataset(path="data/tcc_ceds_music.csv"):
    try:
        train = load_csv("data/train.csv")
        test = load_csv("data/test.csv")
        return train, test
    except FileNotFoundError:
        print("Dataset not found. Creating dataset...")
        return _create_dataset(path)


def _create_dataset(path):
    random.seed(42)
    try:
        songs = load_csv(path)
    except FileNotFoundError:
        print("Dataset not found. Downloading dataset...")
        _download_dataset()

    songs = load_csv(path)
    titles = [{TITLE_KEY: process_title(song[TITLE_KEY])} for song in songs]
    titles = [title for title in titles if title[TITLE_KEY]]

    train, test = train_test_split(titles, test_size=0.2, random_state=42)
    candidates = [song[TITLE_KEY] for song in train]

    def process(song):
        match = get_match(song[TITLE_KEY], candidates)
        song[GT_KEY] = match[0]
        song[DIST_KEY] = match[1]
        return song

    test = Parallel(n_jobs=11)(delayed(process)(song) for song in test)

    save_csv("data/train.csv", train, fieldnames=[TITLE_KEY])
    save_csv("data/test.csv", test, fieldnames=list(test[0].keys()))

    return train, test


def _download_dataset():
    url = "https://www.kaggle.com/api/v1/datasets/download/saurabhshahane/music-dataset-1950-to-2019"
    response = requests.get(url, allow_redirects=True)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
        zip_file.extractall("data")
